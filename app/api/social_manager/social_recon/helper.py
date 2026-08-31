import re
from urllib.parse import unquote


class helper:
    @staticmethod
    def platform_key(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", (value or "").casefold()).strip("_")

    @staticmethod
    def _identity(value: str) -> str:
        identity = unquote(value or "").strip().strip("/").lstrip("@~").casefold()
        for prefix in ("user/", "u/"):
            if identity.startswith(prefix):
                identity = identity[len(prefix):]
                break
        return identity.strip().strip("/")

    @classmethod
    def _matches_requested_identity(cls, item: dict, requested_username: str) -> bool:
        metadata = (item or {}).get("metadata") or {}
        requested = cls._identity(requested_username)
        candidate = cls._identity(
            metadata.get("username") or metadata.get("social_handle") or ""
        )
        return bool(requested and candidate and candidate == requested)

    @staticmethod
    def _result_key(item: dict) -> tuple[str, str] | None:
        metadata = (item or {}).get("metadata") or {}
        platform = (
            metadata.get("platform_key") or metadata.get("platform") or ""
        ).strip().lower()
        identity = (
            metadata.get("username") or metadata.get("social_handle") or ""
        ).strip().lower()
        target = (metadata.get("target_type") or "profile").strip().lower()
        return (f"{platform}:{target}", identity) if platform and identity else None

    @classmethod
    def _dedup_results(cls, results: list) -> list:
        seen = set()
        seen_urls = set()
        out = []
        for item in results or []:
            key = cls._result_key(item)
            if not key or key in seen:
                continue
            url = (
                str((item.get("metadata") or {}).get("url") or "")
                .strip()
                .rstrip("/")
                .lower()
            )
            if url and url in seen_urls:
                continue
            seen.add(key)
            if url:
                seen_urls.add(url)
            out.append(item)
        return out

    FLAT_FIELDS = ("platform", "username", "url", "target_type", "entity_type", "status", "timestamp", "description", "avatar")

    @classmethod
    def _flatten(cls, item: dict) -> dict:
        metadata = (item or {}).get("metadata") or {}
        ids = (((item or {}).get("data") or {}).get("platform_profile") or {}).get("ids") or {}
        merged = {**ids, **metadata}
        return {key: merged[key] for key in cls.FLAT_FIELDS if merged.get(key) not in (None, "", [], {})}

    @classmethod
    def _flatten_results(cls, results: list) -> list:
        return [cls._flatten(item) for item in results or []]
