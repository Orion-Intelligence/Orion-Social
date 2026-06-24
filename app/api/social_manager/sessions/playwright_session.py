import os
from typing import Optional, List, Set
from playwright.sync_api import sync_playwright

SESSION_DIR = os.path.dirname(os.path.abspath(__file__))

SESSION_FILE_MAP = {
    "InstagramScraper": "instagramscraper_session.json.gz",
    "FacebookScraper": "FacebookScraper_session.json.gz",
}

BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--disable-software-rasterizer",
    "--disable-blink-features=AutomationControlled",
]

BLOCKED_RESOURCES = {"image", "media", "font"}


class playwright_session:
    def __init__(self, browser_args: Optional[List[str]] = None, blocked_resources: Optional[Set[str]] = None, headless: bool = True, proxy: Optional[dict] = None):
        self.browser_args = browser_args or BROWSER_ARGS
        self.blocked_resources = blocked_resources or BLOCKED_RESOURCES
        self.headless = headless
        self.proxy = proxy
        self._playwright = None
        self._browser = None
        self._context = None
        self.page = None

    @staticmethod
    def session_file_for(scraper) -> str:
        handler_class = str(scraper.__class__.__name__).lower()
        path = os.path.join(
            SESSION_DIR,
            SESSION_FILE_MAP.get(scraper.__class__.__name__, f"{handler_class}_session.json.gz"),
        )
        print(f":::::::::::: session_file_for -> {path.lower()} ::::::::::::", flush=True)
        return path.lower()

    def __enter__(self):
        self._playwright = sync_playwright().start()

        if self.proxy:
            self._browser = self._playwright.chromium.launch(headless=self.headless, args=self.browser_args, proxy=self.proxy)
        else:
            self._browser = self._playwright.chromium.launch(headless=self.headless, args=self.browser_args)

        self._context = self._browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 900},
            locale="en-US",
        )
        self._context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)
        self.page = self._context.new_page()

        self.page.route("**/*", self._block_media)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
        finally:
            if self._playwright:
                self._playwright.stop()

    def _block_media(self, route):
        r = route.request

        if any(r.url.startswith(s) for s in ("data:image", "data:video", "data:audio")):
            route.abort()
            return

        if r.resource_type in self.blocked_resources:
            route.abort()
            return

        route.continue_()
