import re
from urllib.parse import unquote, urlparse


class normalizer:
    HOST_PREFIXES = ("www.", "m.", "mobile.")
    HOST_ALIASES = {"x.com": "twitter.com"}

    @classmethod
    def host(cls, hostname: str | None) -> str:
        host = (hostname or "").casefold().rstrip(".")
        for prefix in cls.HOST_PREFIXES:
            if host.startswith(prefix):
                host = host[len(prefix):]
                break
        return cls.HOST_ALIASES.get(host, host)

    @classmethod
    def url(cls, url: str) -> tuple[str, str, str, str] | None:
        value = (url or "").strip().split("#", 1)[0]
        if not value:
            return None
        if not re.match(r"^https?://", value, flags=re.IGNORECASE):
            value = f"https://{value}"
        parsed = urlparse(value)
        if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
            return None
        return value, cls.host(parsed.hostname), unquote(parsed.path or "").strip("/"), unquote(parsed.query or "")
