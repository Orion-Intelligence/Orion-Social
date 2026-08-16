import os
import re
import tempfile
import uuid

from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.scrapers.live_search_handler import live_search_handler
from api.social_manager.social_recon.custom_recon.custom_recon import custom_recon
from api.social_manager.social_recon.extractors.email_extractor import email_extractor
from api.social_manager.social_recon.extractors.username_extractor import username_extractor
from api.social_manager.social_recon.helper import helper
from api.social_manager.social_enums import SITE_DATA


class social_recon:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self._progress = progress_controller.get_instance()

    def _step(self, job_id: str | None, percent: int, label: str) -> None:
        if job_id:
            self._progress.update(job_id, percent, label)

    def _platform_progress(self, job_id: str | None, source: str, start: int, end: int):
        if not job_id:
            return None

        def report(done: int, total: int, platform: str, state: str) -> None:
            span = max(end - start, 1)
            percent = start + int((done / max(total, 1)) * span)
            self._step(job_id, min(percent, end), f"{source}:{platform}:{state}")

        return report

    def parse_username(self, username: str, job_id: str | None = None) -> list[dict]:
        base_uname = helper._identity(username)
        if not base_uname or "/" in base_uname:
            self._step(job_id, 100, "invalid:username")
            return []

        self._step(job_id, 5, f"custom:run:{base_uname}")
        results = custom_recon.extract(
            base_uname,
            progress=self._platform_progress(job_id, "custom", 5, 25),
        )

        self._step(job_id, 25, f"maigret:run:{base_uname}")
        results.extend(
            username_extractor.extract(
                base_uname,
                progress=self._platform_progress(job_id, "maigret", 25, 95),
            )
        )

        self._step(job_id, 96, "finalizing")
        exact = [
            item
            for item in results
            if helper._matches_requested_identity(item, base_uname)
        ]
        return helper._dedup_results(exact)

    def parse_email(self, email: str, job_id: str | None = None) -> list[dict]:
        email = (email or "").strip().lower()
        self._step(job_id, 7, f"holehe:run:{email}")
        holehe_data = email_extractor.extract(email)
        if holehe_data is not None:
            self._step(job_id, 14, f"holehe:done:{len(holehe_data.get('found') or [])}")

        pivot_username = None
        for item in (holehe_data or {}).get("found") or []:
            match = re.search(r"gravatar\.com/([^/?#\s]+)", item.get("result") or "")
            if match:
                pivot_username = match.group(1).strip().lower()
                break

        if not pivot_username and "@" in email:
            pivot_username = email.split("@", 1)[0].strip().lower() or None

        self._step(job_id, 20, f"email:pivot:{pivot_username or 'none'}")
        if not pivot_username:
            return []
        try:
            return self.parse_username(pivot_username, job_id=job_id) or []
        except Exception:
            return []

    def parse_image(self, file_bytes: bytes, filename: str | None = None, job_id: str | None = None) -> list[dict]:
        if not file_bytes:
            self._step(job_id, 100, "empty:image")
            return []

        self._step(job_id, 2, "init:image")
        tmp_path = None
        try:
            extension = os.path.splitext(filename or "")[1] or ".jpg"
            if not re.match(r"^\.[A-Za-z0-9]{1,8}$", extension):
                extension = ".jpg"
            tmp_path = os.path.join(tempfile.gettempdir(), f"orion_recon_{uuid.uuid4().hex}{extension}")
            with open(tmp_path, "wb") as handle:
                handle.write(file_bytes)

            self._step(job_id, 10, "image:search")
            found = live_search_handler().extract_accounts_from_image(tmp_path) or []

            known_sites = {site.lower() for site in SITE_DATA.ALL_SITES}
            active, informational = [], []
            for item in found or []:
                metadata = item.get("metadata") or {}
                platform = (metadata.get("platform") or "").strip().lower()
                identity = (metadata.get("username") or metadata.get("social_handle") or "").strip().lower()
                if not platform:
                    continue
                if platform in known_sites and identity:
                    metadata["status"] = "active"
                    item["metadata"] = metadata
                    active.append(item)
                else:
                    metadata["status"] = "informational"
                    metadata["username"] = ""
                    metadata["social_handle"] = ""
                    item["metadata"] = metadata
                    informational.append(item)

            self._step(job_id, 95, "finalizing")
            return helper._dedup_results(active) + informational
        except Exception:
            self._step(job_id, 95, "image:error")
            return []
        finally:
            if tmp_path:
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

    def parse_url(self, url: str, job_id: str | None = None) -> list[dict]:
        self._step(job_id, 5, "custom:url:run")
        results = custom_recon.extract_url(url)
        if results is None:
            self._step(job_id, 10, "maigret:url:run")
            results = username_extractor.extract_url(
                url,
                progress=self._platform_progress(job_id, "maigret", 10, 95),
            )
        self._step(job_id, 96, "finalizing")
        return helper._dedup_results(results)

    def parse(self, value: str, _mode: str = "default", job_id: str | None = None) -> list[dict]:
        value = (value or "").strip()
        if not value:
            self._step(job_id, 100, "empty")
            return []

        self._step(job_id, 1, "init")

        if re.match(r"^https?://", value, flags=re.IGNORECASE) or re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$", value):
            return self.parse_url(value, job_id=job_id)

        if "@" in value and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
            return self.parse_email(value, job_id=job_id)

        digits = re.sub(r"\D+", "", value)
        if re.match(r"^\+?[\d\s().\-]{7,}$", value) and len(digits) >= 7:
            self._step(job_id, 100, "skip:phone")
            return []

        return self.parse_username(value, job_id=job_id)
