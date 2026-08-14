import re


class HttpClientConstants:
    TIMEOUT = 12
    MAX_BYTES = 600_000
    IMPERSONATE = "chrome"


class ParseConstants:
    META = re.compile(r"<meta[^>]+>", re.IGNORECASE)
    KEY = re.compile(r"(?:property|name)\s*=\s*[\"\']([^\"\']+)[\"\']", re.IGNORECASE)
    VALUE = re.compile(r"content\s*=\s*[\"\'](.*?)[\"\']", re.IGNORECASE | re.DOTALL)
    TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
    GENERIC_IMAGE = (
        "default_open_graph",
        "default_avatar",
        "defaultavatar",
        "default_profile",
        "placeholder",
        "missing.png",
        "/static/img/default",
    )


class RegistryConstants:
    ALIASES = {
        "twitter": "x",
        "x.com": "x",
        "fb": "facebook",
        "ig": "instagram",
        "yt": "youtube",
        "bsky": "bluesky",
    }


class VerdictConstants:
    EXISTS = "exists"
    ABSENT = "absent"
    UNKNOWN = "unknown"
    UNSUPPORTED = "unsupported"
