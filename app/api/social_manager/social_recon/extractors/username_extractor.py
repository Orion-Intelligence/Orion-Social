import asyncio
import os
import re
import sys
import time
from urllib.parse import unquote

from typing import Callable

from api.social_manager.social_recon.constants.extractor_constants import UsernameExtractorConstants
from api.social_manager.social_recon.helper import helper
from api.social_manager.social_recon.normalizer import normalizer

import maigret
from maigret.result import MaigretCheckStatus
from maigret.sites import MaigretDatabase


ProgressCallback = Callable[[int, int, str, str], None]


class _silent_logger:
    def __getattr__(self, _name):
        return lambda *args, **kwargs: None


class _progress_notify:
    def __init__(self, total: int, callback: ProgressCallback | None):
        self.total = total
        self.callback = callback
        self._seen: set[str] = set()

    @staticmethod
    def _state(result) -> str:
        status = getattr(result, "status", None)
        value = getattr(status, "value", status)
        return str(value or "unknown").casefold().rsplit(".", 1)[-1]

    def start(self, _message=None, _id_type="username") -> None:
        return

    def update(self, result, _is_similar=False) -> None:
        if not self.callback:
            return
        platform = str(getattr(result, "site_name", None) or "unknown").strip()
        self._seen.add(platform.casefold())
        self.callback(len(self._seen), self.total, platform, self._state(result))

    def finish(self, _message=None) -> None:
        return

    def warning(self, _message, _symbol="-", _advice=None) -> None:
        return

    def enrich(self, _message, _symbol="*", _verbose_only=False) -> None:
        return


class username_extractor:
    _database: MaigretDatabase | None = None

    @classmethod
    def _url_targets(cls, url: str) -> list[tuple[str, str]]:
        parts = normalizer.url(url)
        if parts is None:
            return []
        _value, actual_host, actual_path, actual_query = parts

        marker = "orionusername"
        actual_base = f"{actual_host}/{actual_path}"

        sites = cls._load_database().ranked_sites_dict(
            top=sys.maxsize,
            disabled=False,
            id_type="username",
        )
        targets: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for site_name, site in sites.items():
            template = str(getattr(site, "url", "") or "")
            template = template.replace("{urlMain}", str(getattr(site, "url_main", "") or ""))
            template = template.replace("{urlSubpath}", str(getattr(site, "url_subpath", "") or ""))
            if "{username}" not in template:
                continue

            template_parts = normalizer.url(template.replace("{username}", marker))
            if template_parts is None or template_parts[1] != actual_host:
                continue
            _template_value, template_host, template_path, template_query = template_parts
            template_key = f"{template_host}/{template_path}"
            actual_key = actual_base
            if template_query:
                template_key = f"{template_key}?{template_query}"
                actual_key = f"{actual_key}?{actual_query}"

            escaped_marker = re.escape(marker)
            username_pattern = r"(?P<username>[^/?#&]+?)"
            exact_pattern = re.escape(template_key).replace(escaped_marker, username_pattern)
            match = re.fullmatch(exact_pattern, actual_key, flags=re.IGNORECASE)

            if not match and marker in template_path:
                prefix, suffix = template_key.split(marker, 1)
                if suffix.startswith("/") and "?" not in actual_key:
                    short_pattern = re.escape(prefix).replace(escaped_marker, username_pattern) + username_pattern
                    match = re.fullmatch(short_pattern, actual_key, flags=re.IGNORECASE)

            if not match:
                continue
            username = unquote(match.group("username")).strip().lstrip("@")
            key = (str(site_name), username.casefold())
            if not username or key in seen:
                continue
            seen.add(key)
            targets.append((str(site_name), username))
        return targets

    @classmethod
    def _load_database(cls) -> MaigretDatabase:
        if cls._database is None:
            database_path = os.path.join(
                os.path.dirname(maigret.__file__),
                "resources",
                "data.json",
            )
            cls._database = MaigretDatabase().load_from_path(database_path)
        return cls._database

    @classmethod
    async def _search(cls, username: str, progress: ProgressCallback | None = None, site_names: set[str] | None = None) -> dict:
        sites = cls._load_database().ranked_sites_dict(
            top=sys.maxsize,
            disabled=False,
            id_type="username",
        )
        if site_names is not None:
            sites = {name: site for name, site in sites.items() if name in site_names}
        if not sites:
            return {}
        return await maigret.search(
            username,
            site_dict=sites,
            query_notify=_progress_notify(len(sites), progress),
            logger=_silent_logger(),
            timeout=UsernameExtractorConstants.SITE_TIMEOUT,
            is_parsing_enabled=True,
            max_connections=UsernameExtractorConstants.MAX_CONNECTIONS,
            no_progressbar=True,
            retries=1,
        )

    @classmethod
    def _format_result(cls, site_name: str, result: dict) -> dict | None:
        status = result.get("status")
        if getattr(status, "status", None) != MaigretCheckStatus.CLAIMED:
            return None

        http_status = result.get("http_status")
        if isinstance(http_status, int) and not 200 <= http_status < 300:
            return None
        if result.get("is_similar"):
            return None

        platform = str(getattr(status, "site_name", None) or site_name).strip()
        username = str(getattr(status, "username", None) or result.get("username") or "").strip()
        url = str(getattr(status, "site_url_user", None) or result.get("url_user") or "").strip()
        if not platform or not username or not url:
            return None
        if UsernameExtractorConstants.SEARCH_ENDPOINT.search(url):
            return None
        if username.casefold() not in unquote(url).casefold():
            return None

        ids = getattr(status, "ids_data", None) or {}
        tags = list(getattr(status, "tags", None) or getattr(result.get("site"), "tags", None) or [])
        platform_profile = {
            "source": "maigret",
            "ids": ids,
            "tags": tags,
        }
        if getattr(status, "query_time", None) is not None:
            platform_profile["query_time"] = status.query_time

        return {
            "metadata": {
                "platform": platform,
                "platform_key": helper.platform_key(site_name or platform),
                "username": username,
                "social_handle": username,
                "url": url,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "status": "active",
                "target_type": "profile",
                "entity_type": "user",
            },
            "data": {
                "profile_existence_proof": {
                    "type": "maigret_claimed_account",
                    "status_code": result.get("http_status"),
                    "checked_url": url,
                    "final_url": url,
                    "target_type": "profile",
                    "resolver_source": "maigret",
                },
                "platform_profile": platform_profile,
            },
        }

    @classmethod
    def extract(cls, username: str, progress: ProgressCallback | None = None, site_names: set[str] | None = None) -> list[dict]:
        username = (username or "").strip()
        if not username:
            return []

        try:
            raw_results = asyncio.run(
                asyncio.wait_for(
                    cls._search(username, progress, site_names),
                    timeout=UsernameExtractorConstants.SEARCH_DEADLINE,
                )
            )
        except Exception:
            return []

        results = []
        for site_name, result in (raw_results or {}).items():
            if not isinstance(result, dict):
                continue
            item = cls._format_result(str(site_name), result)
            if item:
                results.append(item)
        return results

    @classmethod
    def extract_url(cls, url: str, progress: ProgressCallback | None = None) -> list[dict]:
        results = []
        for site_name, username in cls._url_targets(url):
            results.extend(cls.extract(username, progress=progress, site_names={site_name}))
        return helper._dedup_results(results)
