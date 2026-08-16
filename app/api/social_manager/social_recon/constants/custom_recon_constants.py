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


class CrawlConstants:
    NORMAL = "normal"
    PLAYWRIGHT = "playwright"
    ONLINE = "online"
    UNVERIFIED = "unverified"


class BrowserPoolConstants:
    INSTANCES = 5
    TABS_PER_INSTANCE = 15
    HEADLESS = True
    NAV_TIMEOUT_MS = 25_000
    IDLE_TIMEOUT_MS = 6_000
    SETTLE_MS = 1_500
    RESULT_TIMEOUT = 60
    EXECUTABLES = ("", "/usr/bin/chromium-browser", "/usr/bin/chromium", "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable")
    ARGS = ("--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    INIT_SCRIPT = "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"


class OnlineSearchConstants:
    QUERY = "site:{target}"
    MAX_RESULTS = 10
    BACKENDS = ("auto", "bing", "yahoo")
