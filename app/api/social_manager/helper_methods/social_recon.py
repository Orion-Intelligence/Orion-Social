import json
import os
import re
import shlex
import shutil
import subprocess
import time
import uuid
from urllib.parse import urlparse

from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.helper_methods.custom_recon import custom_recon
from api.social_manager.scrapers.live_search.live_search_handler import live_search_handler
from api.social_manager.social_enums import SITE_DATA


class social_recon:
    _instance = None
    TARGETED_MAIGRET_SITES = [
        "Instagram",
        "Facebook",
        "YouTube",
        "Twitter",
        "Behance",
    ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self._progress = progress_controller.get_instance()
        self._custom_recon = custom_recon()

    def _clean_maigret(self, data: dict) -> dict:
        out = {}
        for site_name, v in (data or {}).items():
            status = (v or {}).get("status") or {}
            ids = status.get("ids") or {}
            tags = status.get("tags") or (v or {}).get("tags") or []
            item = {
                "url": status.get("url") or (v or {}).get("url_user"),
                "status": status.get("status"),
            }
            if ids:
                item["ids"] = ids
            if tags:
                item["tags"] = tags
            if (v or {}).get("http_status") is not None:
                item["http_status"] = (v or {}).get("http_status")
            out[site_name] = item
        return out

    def _dedup_results(self, results: list) -> list:
        seen = {}
        out = []

        for r in results or []:
            meta = (r or {}).get("metadata") or {}

            plat = (meta.get("platform") or "").strip().lower()
            uname = (meta.get("username") or "").strip().lower()
            handle = (meta.get("social_handle") or "").strip().lower()

            ident_raw = uname or handle
            if not plat or not ident_raw:
                continue

            ident = ident_raw.strip()

            i = 0
            n = len(ident)
            while i < n and not ident[i].isalnum():
                i += 1
            ident = ident[i:]

            j = len(ident) - 1
            while j >= 0 and not ident[j].isalnum():
                j -= 1
            ident = ident[: j + 1]

            if not ident:
                continue

            if plat == "reddit":
                proof = ((r or {}).get("data") or {}).get("profile_existence_proof") or {}
                proof_url = " ".join(
                    str(value or "").lower()
                    for value in (
                        meta.get("url"),
                        proof.get("checked_url"),
                        proof.get("final_url"),
                    )
                )
                bare_ident = ident.split("/", 1)[-1] if ident.startswith(("u/", "r/", "user/")) else ident
                account_type = str(proof.get("account_type") or "").lower()
                if account_type == "subreddit" or "/r/" in proof_url:
                    ident = f"r/{bare_ident}"
                elif account_type == "user" or "/user/" in proof_url or "/u/" in proof_url:
                    ident = f"user/{bare_ident}"

            per_plat = seen.get(plat)
            if per_plat is None:
                per_plat = set()
                seen[plat] = per_plat

            if ident in per_plat:
                continue

            should_skip = False
            if plat != "reddit":
                for s in per_plat:
                    if s in ident or ident in s:
                        should_skip = True
                        break
            if should_skip:
                continue

            per_plat.add(ident)
            out.append(r)

        return out

    def run_maigret_on_platform(self, username: str, platform: str, job_id: str | None = None):
        if job_id:
            self._progress.update(job_id, 82, f"maigret:init:{platform}:{username}")

        report_dir = f"reports_{username}"
        os.makedirs(report_dir, exist_ok=True)
        report_file = os.path.join(report_dir, f"report_{username}_simple.json")

        if job_id:
            self._progress.update(job_id, 84, f"maigret:run:{platform}:{username}")

        result = subprocess.run(
            ["maigret", username, "--site", platform, "--json", "simple", "--folderoutput", report_dir],
            capture_output=True,
            text=True,
        )

        if job_id:
            self._progress.update(job_id, 86, f"maigret:exit:{platform}:{username}:{result.returncode}")

        cleaned = None
        if result.returncode == 0 and os.path.exists(report_file):
            if job_id:
                self._progress.update(job_id, 87, f"maigret:read:{platform}:{username}")
            with open(report_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if job_id:
                self._progress.update(job_id, 88, f"maigret:clean:{platform}:{username}")
            cleaned = self._clean_maigret(data)
            os.remove(report_file)

        if not cleaned:
            container_cleaned = self._run_maigret_in_container(username, platform)
            if container_cleaned:
                cleaned = container_cleaned

        if os.path.exists(report_dir) and not os.listdir(report_dir):
            os.rmdir(report_dir)

        if job_id:
            self._progress.update(job_id, 89, f"maigret:done:{platform}:{username}")

        return cleaned

    def _run_maigret_in_container(self, username: str, platform: str) -> dict | None:
        if os.path.exists("/.dockerenv"):
            return None

        docker_bin = shutil.which("docker")
        if not docker_bin:
            return None

        report_dir = f"/tmp/maigret_{uuid.uuid4().hex}"
        report_file = f"{report_dir}/report_{username}_simple.json"
        maigret_cmd = [
            "maigret",
            username,
            "--site",
            platform,
            "--json",
            "simple",
            "--folderoutput",
            report_dir,
        ]
        shell_cmd = (
            f"mkdir -p {shlex.quote(report_dir)} && "
            f"{' '.join(shlex.quote(part) for part in maigret_cmd)} >/dev/null 2>&1; "
            f"cat {shlex.quote(report_file)} 2>/dev/null || true"
        )
        result = subprocess.run(
            [docker_bin, "exec", "trusted-social-api", "sh", "-lc", shell_cmd],
            capture_output=True,
            text=True,
        )
        payload = (result.stdout or "").strip()
        if not payload:
            return None
        try:
            return self._clean_maigret(json.loads(payload))
        except Exception:
            return None

    def run_sherlock(self, username: str, job_id: str | None = None):
        if job_id:
            self._progress.update(job_id, 5, f"sherlock:init:{username}")

        cmd = [
            "sherlock",
            "--timeout",
            "10",
            username,
            "--print-found",
            "--no-color",
        ]

        if job_id:
            self._progress.update(job_id, 6, f"sherlock:run:{username}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if job_id:
            self._progress.update(job_id, 7, f"sherlock:exit:{username}:{result.returncode}")

        txt_file = f"{username}.txt"
        if os.path.exists(txt_file):
            os.remove(txt_file)

        profiles = []
        lines = result.stdout.splitlines()
        total_lines = len(lines) or 1
        for i, line in enumerate(lines, start=1):
            s = line.strip()
            if job_id and (i == 1 or i == total_lines or i % 25 == 0):
                self._progress.update(job_id, 7 + int((i / total_lines) * 2), f"sherlock:parse:{username}:{i}/{total_lines}")
            if s.startswith("[+]"):
                match = re.search(r"https?://\S+", s)
                if match:
                    url = match.group(0).rstrip("/")
                    parsed = urlparse(url)
                    host = (parsed.netloc or "").split(":")[0]
                    host_no_www = host[4:] if host.startswith("www.") else host
                    parts = host_no_www.split(".")
                    platform_key = parts[-2] if len(parts) >= 2 else (parts[0] if parts else "")
                    platform = platform_key.capitalize() if platform_key else ""
                    path = (parsed.path or "").strip("/")
                    user = path.split("/")[-1] if path else username
                    profiles.append({"platform": platform, "username": user, "url": url})

        if job_id:
            self._progress.update(job_id, 9, f"sherlock:done:{username}:found={len(profiles)}")

        return profiles

    def run_holehe(self, email: str, job_id: str | None = None):
        if not shutil.which("holehe"):
            if job_id:
                self._progress.update(job_id, 6, f"holehe:missing:{email}")
            return None

        if job_id:
            self._progress.update(job_id, 7, f"holehe:run:{email}")

        result = subprocess.run(["holehe", email], capture_output=True, text=True)

        if job_id:
            self._progress.update(job_id, 9, f"holehe:exit:{email}:{result.returncode}")

        found = []
        lines = result.stdout.splitlines()
        total_lines = len(lines) or 1
        for i, line in enumerate(lines, start=1):
            s = line.strip()
            if job_id and (i == 1 or i == total_lines or i % 25 == 0):
                self._progress.update(job_id, 9 + int((i / total_lines) * 4), f"holehe:parse:{email}:{i}/{total_lines}")
            m = re.match(r"^\[\+\]\s*([^:]+):\s*(.+)$", s)
            if m:
                found.append({"service": m.group(1).strip(), "result": m.group(2).strip()})
            elif "found" in s.lower() or s.startswith("[+]"):
                found.append({"line": s})

        if job_id:
            self._progress.update(job_id, 14, f"holehe:done:{email}:found={len(found)}")

        return {"returncode": result.returncode, "found": found}

    def parse_username(self, username: str, mode: str = "default", job_id: str | None = None):
        if job_id:
            self._progress.update(job_id, 1, "init:username")

        if job_id:
            self._progress.update(job_id, 5, "sherlock")

        found_profiles = self.run_sherlock(username, job_id=job_id)

        base_uname = username.strip().lower() + ""

        if job_id:
            self._progress.update(job_id, 10, f"sherlock_done:{len(found_profiles) or 0}")

        total = len(found_profiles) or 1
        seen = set()
        results = []
        done = 0

        scanned_maigret = set()

        for p in found_profiles:
            done += 1
            uname = (p.get("username") or "").lower()
            plat = p.get("platform")
            plat_lower = (plat or "").lower()
            key = (uname, plat_lower)

            if plat_lower == "artstation":
                if job_id:
                    self._progress.update(job_id, 10 + int((done / total) * 70), f"skip:artstation:{uname}")
                continue

            if key in seen:
                if job_id:
                    self._progress.update(job_id, 10 + int((done / total) * 70), f"skip_dup:{plat}:{uname}")
                continue
            seen.add(key)

            scanned_maigret.add(plat_lower)

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if str(uname).__contains__("discord"):
                pass
            results.append(
                {
                    "metadata": {
                        "platform": plat,
                        "username": uname,
                        "social_handle": uname,
                        "url": p.get("url"),
                        "timestamp": timestamp,
                        "status": "active",
                    },
                    "data": {},
                }
            )

            if job_id:
                self._progress.update(job_id, 10 + int((done / total) * 70), f"accepted:{plat}:{uname}")

        if job_id:
            self._progress.update(job_id, 80, "focused")

        focused_total = len(SITE_DATA.FOCUSED_SITES) or 1
        focused_done = 0
        for site in SITE_DATA.FOCUSED_SITES:
            focused_done += 1
            site_lower = site.lower()
            if site_lower not in scanned_maigret and site not in self.TARGETED_MAIGRET_SITES:
                continue

            if job_id:
                self._progress.update(job_id, 80 + int((focused_done / focused_total) * 10), f"maigret_focused:{site}:{base_uname}")

            raw = self.run_maigret_on_platform(base_uname, site, job_id=job_id)

            k = next((kk for kk in (raw or {}).keys() if kk.lower() == site_lower), None)
            if k:
                data = raw[k]
            elif len(raw or {}) == 1:
                data = next(iter((raw or {}).values()))
            else:
                data = raw

            if not data:
                if job_id:
                    self._progress.update(job_id, 80 + int((focused_done / focused_total) * 10), f"focused_not_verified:{site}:{base_uname}")
                continue

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            results.append(
                {
                    "metadata": {
                        "platform": site,
                        "username": base_uname,
                        "social_handle": base_uname,
                        "url": None,
                        "timestamp": timestamp,
                        "status": "active",
                    },
                    "data": data,
                }
            )

            if job_id:
                self._progress.update(job_id, 80 + int((focused_done / focused_total) * 10), f"focused_verified:{site}:{base_uname}")

        if job_id:
            self._progress.update(job_id, 90, "ddg_validate")

        try:
            ddg = live_search_handler()
            keep = []
            for r in results:
                meta = r.get("metadata") or {}
                plat = (meta.get("platform") or "").strip()
                if not plat:
                    continue
                if plat in SITE_DATA.TOP_10_SITES:
                    if ddg.check_username_exists(base_uname, plat):
                        keep.append(r)
                else:
                    keep.append(r)
            results = keep
        except Exception:
            pass

        if job_id:
            self._progress.update(job_id, 90, "checking online presence")

        if len(results) < 100:
            try:
                ddg = live_search_handler()
                if job_id:
                    self._progress.update(job_id, 91, f"ddg:run:{base_uname}")
                ddg_payload = ddg.collect_social_handles(base_uname) or {}
                ddg_results = ddg_payload.get("results") or []
                if job_id:
                    self._progress.update(job_id, 93, f"ddg:parse:{len(ddg_results)}")

                existing_keys: set[tuple[str, str]] = set()
                for r in results:
                    meta = r.get("metadata") or {}
                    uname = (meta.get("username") or "").lower()
                    handle = (meta.get("social_handle") or "").lower()
                    plat = (meta.get("platform") or "").lower()
                    ident = uname or handle
                    if plat and ident:
                        existing_keys.add((plat, ident))

                ddg_total = len(ddg_results) or 1
                for i, item in enumerate(ddg_results, start=1):
                    if job_id and (i == 1 or i == ddg_total or i % 10 == 0):
                        self._progress.update(job_id, 93, f"ddg:merge:{i}/{ddg_total}")
                    meta = item.get("metadata") or {}
                    meta["status"] = "suggested"
                    item["metadata"] = meta

                    plat = (meta.get("platform") or "").lower()
                    uname = (meta.get("username") or "").lower()
                    handle = (meta.get("social_handle") or meta.get("username") or "").lower()
                    ident = uname or handle
                    if not plat or not ident:
                        continue
                    k = (plat, ident)
                    if k in existing_keys:
                        continue
                    existing_keys.add(k)
                    results.append(item)

                if job_id:
                    self._progress.update(job_id, 94, f"ddg:done:{len(results)}")
            except Exception:
                if job_id:
                    self._progress.update(job_id, 94, "ddg:error")
                pass

        if job_id:
            self._progress.update(job_id, 95, "custom_recon")

        try:
            custom_results = self._custom_recon.parse_username(base_uname, existing_results=results)
            if custom_results:
                existing_keys: set[tuple[str, str]] = set()
                for r in results:
                    meta = r.get("metadata") or {}
                    uname = (meta.get("username") or "").lower()
                    handle = (meta.get("social_handle") or "").lower()
                    plat = (meta.get("platform") or "").lower()
                    ident = uname or handle
                    if plat and ident:
                        existing_keys.add((plat, ident))

                custom_total = len(custom_results) or 1
                for i, item in enumerate(custom_results, start=1):
                    if job_id and (i == 1 or i == custom_total or i % 10 == 0):
                        self._progress.update(job_id, 95, f"custom:merge:{i}/{custom_total}")
                    meta = item.get("metadata") or {}
                    plat = (meta.get("platform") or "").lower()
                    uname = (meta.get("username") or "").lower()
                    handle = (meta.get("social_handle") or meta.get("username") or "").lower()
                    ident = uname or handle
                    if not plat or not ident:
                        continue
                    k = (plat, ident)
                    if k in existing_keys:
                        continue
                    existing_keys.add(k)
                    results.append(item)
        except Exception:
            if job_id:
                self._progress.update(job_id, 95, "custom:error")

        if job_id:
            self._progress.update(job_id, 96, "finalizing")

        return self._dedup_results(results)

    def parse_email(self, email: str, mode: str = "default", job_id: str | None = None):
        email = (email or "").strip().lower()

        if job_id:
            self._progress.update(job_id, 2, "init:email")

        if job_id:
            self._progress.update(job_id, 5, "email:holehe")

        holehe_data = self.run_holehe(email, job_id=job_id)

        if job_id:
            self._progress.update(job_id, 15, "email:pivot")

        pivot_username = None
        if holehe_data:
            items = holehe_data.get("found") or []
            total = len(items) or 1
            for i, item in enumerate(items, start=1):
                if job_id and (i == 1 or i == total or i % 10 == 0):
                    self._progress.update(job_id, 15, f"email:pivot_scan:{i}/{total}")
                if item:
                    url = item.get("result") or ""
                    m = re.search(r"gravatar\.com/([^/?#\s]+)", url)
                    if m:
                        pivot_username = m.group(1).strip().lower()
                        break
                    srv = item.get("service") or ""
                    m = re.search(r"FullName\s+([^\s/]+)", srv)
                    if m:
                        pivot_username = m.group(1).strip().lower()
                        break

        if not pivot_username and "@" in email:
            pivot_username = email.split("@", 1)[0].strip().lower() or None

        if job_id:
            self._progress.update(job_id, 20, f"email:pivot_username:{pivot_username or 'none'}")

        pivot_results = None
        if pivot_username:
            try:
                if job_id:
                    self._progress.update(job_id, 25, "email:pivot_recon")
                pivot_results = self.parse_username(pivot_username, mode=mode, job_id=None)
            except Exception:
                pivot_results = None

        if pivot_results:
            if job_id:
                self._progress.update(job_id, 85, "email:normalize")
            for r in pivot_results:
                d = r["data"]
                if d and len(d) == 1:
                    r["data"] = next(iter(d.values()))
            pivot_results = self._dedup_results(pivot_results)

        if job_id:
            self._progress.update(job_id, 95, "finalizing")

        return pivot_results

    def parse(self, value: str, mode: str = "default", job_id: str | None = None):
        v = (value or "").strip()
        if not v:
            if job_id:
                self._progress.update(job_id, 100, "empty")
            return []

        if job_id:
            self._progress.update(job_id, 1, "init")

        try:
            custom_direct = self._custom_recon.parse_direct(v)
            if custom_direct:
                if job_id:
                    self._progress.update(job_id, 95, "custom:direct")
                return self._dedup_results(custom_direct)
            if re.match(r"^https?://", v, flags=re.IGNORECASE) or re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$", v):
                if job_id:
                    self._progress.update(job_id, 100, "custom:direct:not_supported")
                return []
        except Exception:
            if job_id:
                self._progress.update(job_id, 3, "custom:direct:error")

        is_email = "@" in v and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v) is not None
        if is_email:
            if job_id:
                self._progress.update(job_id, 3, "detect:email")
            return self.parse_email(v, mode=mode, job_id=job_id)

        digits = re.sub(r"\D+", "", v)
        is_phone = re.match(r"^\+?[\d\s().\-]{7,}$", v) is not None and len(digits) >= 7
        if is_phone:
            if job_id:
                self._progress.update(job_id, 100, "skip:phone")
            return []

        if job_id:
            self._progress.update(job_id, 3, "detect:username")
        return self.parse_username(v, mode=mode, job_id=job_id)

    def parse_image(self, file_bytes: bytes, filename: str | None = None, job_id: str | None = None):
        if not file_bytes:
            if job_id:
                self._progress.update(job_id, 100, "empty:image")
            return []

        if job_id:
            self._progress.update(job_id, 2, "init:image")

        try:
            tmp_dir = "tmp_uploads"
            os.makedirs(tmp_dir, exist_ok=True)

            ext = os.path.splitext(filename or "")[1] or ".jpg"
            tmp_path = os.path.join(tmp_dir, f"{uuid.uuid4().hex}{ext}")

            with open(tmp_path, "wb") as f:
                f.write(file_bytes)

            if job_id:
                self._progress.update(job_id, 10, "image:search")

            ddg = live_search_handler()
            payload = ddg.extract_accounts_from_image(tmp_path)
            if isinstance(payload, tuple) and len(payload) == 2:
                results, _titles = payload
            elif isinstance(payload, dict):
                results = payload.get("results") or []
            else:
                results = payload or []
            if not results:
                results = []

            if job_id:
                self._progress.update(job_id, 40, f"image:found:{len(results)}")

            existing_keys: set[tuple[str, str]] = set()
            merged = []

            total = len(results) or 1
            for i, item in enumerate(results, start=1):
                if job_id and (i == 1 or i == total or i % 10 == 0):
                    self._progress.update(job_id, 40 + int((i / total) * 40), f"image:merge:{i}/{total}")

                meta = item.get("metadata") or {}
                plat = (meta.get("platform") or "").strip().lower()
                uname = (meta.get("username") or "").strip().lower()
                handle = (meta.get("social_handle") or "").strip().lower()
                status = "active" if plat in {s.lower() for s in SITE_DATA.ALL_SITES} else "informational"
                ident = uname or handle
                if status == "informational" and not ident:
                    ident = ((item.get("data") or {}).get("matched_page") or meta.get("url") or "").strip().lower()
                if not plat or not ident:
                    continue

                k = (plat, ident)
                meta["status"] = status
                if status == "informational":
                    meta["username"] = ""
                    meta["social_handle"] = ""
                else:
                    if k in existing_keys:
                        continue
                    existing_keys.add(k)
                item["metadata"] = meta
                merged.append(item)

            if job_id:
                self._progress.update(job_id, 90, "image:dedup")

            active_items = [r for r in merged if ((r.get("metadata") or {}).get("status") == "active")]
            informational_items = [r for r in merged if ((r.get("metadata") or {}).get("status") == "informational")]
            merged = self._dedup_results(active_items) + informational_items

            try:
                os.remove(tmp_path)
            except Exception:
                pass

            if job_id:
                self._progress.update(job_id, 95, "finalizing")

            return merged

        except Exception:
            if job_id:
                self._progress.update(job_id, 95, "image:error")
            return []

if __name__ == "__main__":

    recon = social_recon()
    data = "calmmelancholy"
    results = recon.parse(data, mode="default", job_id=None)
    print(json.dumps(results, indent=2, ensure_ascii=False))
