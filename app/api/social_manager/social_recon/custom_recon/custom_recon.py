import re
import time
from collections.abc import Callable, Iterable
from types import ModuleType
from typing import Any, cast
from urllib.parse import urlparse

import api.social_manager.social_recon.custom_recon.core.http_client as http_client
import api.social_manager.social_recon.custom_recon.core.parse as parse
import api.social_manager.social_recon.custom_recon.core.registry as registry
from api.social_manager.social_recon.constants.custom_recon_constants import CrawlConstants, HttpClientConstants, VerdictConstants
from api.social_manager.social_recon.custom_recon.core.verdict import ProfileCheck
from api.social_manager.social_recon.helper import helper
from api.social_manager.social_recon.normalizer import normalizer


ProgressCallback = Callable[[int, int, str, str], None]
Transport = Callable[[str], tuple[int, str, str]]
ProbeUrlBuilder = Callable[[str], str]
Evaluator = Callable[[int, str, str], tuple[str, dict[str, Any]]]


class custom_recon:
    _cache: dict[tuple[str, str], ProfileCheck] = {}

    @staticmethod
    def _clean(username: str) -> str:
        return (username or "").strip().strip("/").lstrip("@~")

    @staticmethod
    def _crawl_type(module: ModuleType) -> str:
        return getattr(module.constants, "CRAWL_TYPE", CrawlConstants.NORMAL)

    @classmethod
    def _fetch(cls, module: ModuleType, url: str, max_bytes: int = HttpClientConstants.MAX_BYTES) -> tuple[int, str, str]:
        crawl_type = cls._crawl_type(module)
        if crawl_type == CrawlConstants.PLAYWRIGHT:
            return http_client.browser_fetch(url, max_bytes)
        if crawl_type == CrawlConstants.ONLINE:
            return http_client.online_fetch(url, max_bytes)
        return http_client.fetch(url, max_bytes)

    @staticmethod
    def _profile_url(module: ModuleType, username: str) -> str:
        return getattr(module.constants, "PROFILE_URL", "").format(username=username)

    @classmethod
    def check(cls, platform: str, username: str, refresh: bool = False) -> ProfileCheck:
        module = registry.resolve(platform)
        username = cls._clean(username)
        if module is None:
            return ProfileCheck(platform, username, VerdictConstants.UNKNOWN, reason="unknown platform")
        if not username:
            return ProfileCheck(module.constants.NAME, username, VerdictConstants.ABSENT, reason="empty username")

        key = (module.constants.NAME, username.casefold())
        if not refresh and key in cls._cache:
            return cls._cache[key]

        url = cls._profile_url(module, username)

        if cls._crawl_type(module) == CrawlConstants.UNVERIFIED:
            return ProfileCheck(module.constants.NAME, username, VerdictConstants.UNKNOWN, url, reason="unverified: routing only, existence delegated to maigret")

        if not registry.supported(module):
            return cls._store(key, ProfileCheck(module.constants.NAME, username, VerdictConstants.UNSUPPORTED, url, reason=getattr(module.constants, "REASON", "")))

        if not re.match(module.constants.GRAMMAR, username):
            return cls._store(key, ProfileCheck(module.constants.NAME, username, VerdictConstants.ABSENT, url, reason="handle violates platform grammar"))

        transport_member = getattr(module, "fetch", None)
        if transport_member is not None and not callable(transport_member):
            return cls._store(key, ProfileCheck(module.constants.NAME, username, VerdictConstants.UNKNOWN, url, reason="fetch is not callable"))
        transport = cast(Transport | None, transport_member)
        try:
            if transport is not None:
                status, body, final_url = transport(username)
            else:
                probe_url_member = getattr(module, "probe_url", None)
                if not callable(probe_url_member):
                    return cls._store(key, ProfileCheck(module.constants.NAME, username, VerdictConstants.UNKNOWN, url, reason="probe_url is not callable"))
                probe_url = cast(ProbeUrlBuilder, probe_url_member)
                status, body, final_url = cls._fetch(module, probe_url(username), getattr(module.constants, "MAX_BYTES", HttpClientConstants.MAX_BYTES))
        except Exception as exc:
            return cls._store(key, ProfileCheck(module.constants.NAME, username, VerdictConstants.UNKNOWN, url, reason=f"request failed: {type(exc).__name__}"))
        if status == 0:
            return cls._store(key, ProfileCheck(module.constants.NAME, username, VerdictConstants.UNKNOWN, url, reason="request failed"))

        evaluate_member = getattr(module, "evaluate", None)
        if not callable(evaluate_member):
            return cls._store(key, ProfileCheck(module.constants.NAME, username, VerdictConstants.UNKNOWN, url, reason="evaluate is not callable", status_code=status, final_url=final_url))
        evaluate = cast(Evaluator, evaluate_member)
        try:
            verdict, info = evaluate(status, body, final_url)
        except Exception:
            verdict, info = VerdictConstants.UNKNOWN, {}
        target_type = info.pop("target_type", "profile") if isinstance(info, dict) else "profile"

        return cls._store(
            key,
            ProfileCheck(
                module.constants.NAME,
                username,
                verdict,
                url,
                info=info,
                reason="" if verdict == VerdictConstants.EXISTS else f"http {status}",
                status_code=status,
                final_url=final_url,
                target_type=target_type,
            ),
        )

    @classmethod
    def _route(cls, url: str) -> tuple[ModuleType, str, str, str] | None:
        parts = normalizer.url(url)
        if parts is None:
            return None
        value, host, path, query = parts
        for module in registry.platforms.values():
            subdomain, sub_target = getattr(module, "SUBDOMAIN", ("", ""))
            if subdomain and host.endswith(f".{subdomain}") and not path:
                return module, cls._clean(host[: -len(subdomain) - 1]), sub_target, value
            hosts = (normalizer.host(urlparse(module.constants.PROFILE_URL).hostname), *getattr(module, "HOSTS", ()))
            if host not in hosts:
                continue
            for pattern, target in getattr(module, "ROUTES", ()):
                match = re.fullmatch(pattern, path, flags=re.IGNORECASE) or (query and re.fullmatch(pattern, f"{path}?{query}", flags=re.IGNORECASE))
                identity = cls._clean(match.group("id") if match else "")
                if identity:
                    return module, identity, target, value
            return None
        return None

    @classmethod
    def check_url(cls, url: str) -> ProfileCheck | None:
        route = cls._route(url)
        if route is None:
            return None
        module, identity, target, value = route
        if target == "profile" or cls._crawl_type(module) == CrawlConstants.UNVERIFIED:
            return cls.check(module.constants.NAME, identity)
        status, body, final_url = cls._fetch(module, value)
        resource_member = getattr(module, "evaluate_resource", None)
        info: dict[str, Any] = {}
        if callable(resource_member):
            try:
                verdict, info = resource_member(status, body, final_url)
            except Exception:
                verdict, info = VerdictConstants.UNKNOWN, {}
        else:
            verdict = VerdictConstants.EXISTS if status == 200 else VerdictConstants.ABSENT if status in (404, 410) else VerdictConstants.UNKNOWN
            info = parse.social_info(body) if verdict == VerdictConstants.EXISTS else {}
        if not isinstance(info, dict):
            info = {}
        info = {key: value for key, value in info.items() if value}
        return ProfileCheck(module.constants.NAME, identity, verdict, value, info=info, reason="" if status == 200 else f"http {status}", status_code=status, final_url=final_url, target_type=target)

    @classmethod
    def _store(cls, key: tuple[str, str], result: ProfileCheck) -> ProfileCheck:
        cls._cache[key] = result
        return result

    @classmethod
    def check_all(cls, username: str, platforms: Iterable[str] | None = None, refresh: bool = False, progress: ProgressCallback | None = None) -> list[ProfileCheck]:
        targets = tuple(platforms or registry.names())
        total = len(targets)
        results = []
        for index, name in enumerate(targets, start=1):
            result = cls.check(name, username, refresh)
            results.append(result)
            if progress:
                progress(index, total, result.platform, result.verdict)
        return results

    @classmethod
    def _format_result(cls, check: ProfileCheck) -> dict[str, Any]:
        return {
            "metadata": {
                "platform": check.platform,
                "platform_key": helper.platform_key(check.platform),
                "username": check.username,
                "social_handle": check.username,
                "url": check.url,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "status": "active",
                "target_type": check.target_type,
                "entity_type": "user" if check.target_type == "profile" else "resource",
            },
            "data": {
                "profile_existence_proof": {
                    "type": "custom_recon_verified",
                    "status_code": check.status_code,
                    "checked_url": check.url,
                    "final_url": check.final_url or check.url,
                    "target_type": check.target_type,
                    "resolver_source": "custom_recon",
                },
                "platform_profile": {
                    "source": "custom_recon",
                    "ids": check.info,
                    "tags": [],
                },
            },
        }

    @classmethod
    def extract(cls, username: str, platforms: Iterable[str] | None = None, refresh: bool = False, progress: ProgressCallback | None = None) -> list[dict[str, Any]]:
        username = cls._clean(username)
        if not username:
            return []
        return [
            cls._format_result(check)
            for check in cls.check_all(username, platforms, refresh, progress)
            if check.verdict == VerdictConstants.EXISTS
        ]

    @classmethod
    def extract_url(cls, url: str) -> list[dict[str, Any]] | None:
        route = cls._route(url)
        if route is None or cls._crawl_type(route[0]) == CrawlConstants.UNVERIFIED:
            return None
        check = cls.check_url(url)
        if check is None:
            return None
        return [cls._format_result(check)] if check.verdict == VerdictConstants.EXISTS else []
