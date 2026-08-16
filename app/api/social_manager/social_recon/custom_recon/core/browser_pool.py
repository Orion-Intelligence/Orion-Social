import asyncio
import threading

from api.social_manager.social_recon.constants.custom_recon_constants import BrowserPoolConstants, HttpClientConstants


class browser_pool:
    _instance = None
    _guard = threading.Lock()

    def __new__(cls):
        with cls._guard:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._loop: asyncio.AbstractEventLoop | None = None
        self._ready = threading.Event()
        self._playwright = None
        self._browsers: list = []
        self._contexts: list = []
        self._slots: list[asyncio.Semaphore] = []
        self._cursor = 0

    def _ensure(self) -> None:
        if self._loop is not None:
            return
        with self._guard:
            if self._loop is not None:
                return
            self._loop = asyncio.new_event_loop()
            threading.Thread(target=self._loop.run_forever, name="browser-pool", daemon=True).start()
            asyncio.run_coroutine_threadsafe(self._start(), self._loop).result(BrowserPoolConstants.RESULT_TIMEOUT)

    async def _launch(self):
        error: Exception | None = None
        for executable in BrowserPoolConstants.EXECUTABLES:
            try:
                options = {"headless": BrowserPoolConstants.HEADLESS, "args": list(BrowserPoolConstants.ARGS)}
                if executable:
                    options["executable_path"] = executable
                return await self._playwright.chromium.launch(**options)
            except Exception as exc:
                error = exc
        raise RuntimeError(f"no chromium could be launched: {error}")

    async def _start(self) -> None:
        from playwright.async_api import async_playwright

        self._playwright = await async_playwright().start()
        for _ in range(BrowserPoolConstants.INSTANCES):
            browser = await self._launch()
            context = await browser.new_context(user_agent=BrowserPoolConstants.USER_AGENT, locale="en-US")
            await context.add_init_script(BrowserPoolConstants.INIT_SCRIPT)
            self._browsers.append(browser)
            self._contexts.append(context)
            self._slots.append(asyncio.Semaphore(BrowserPoolConstants.TABS_PER_INSTANCE))

    async def _revive(self, index: int) -> None:
        if self._browsers[index].is_connected():
            return
        browser = await self._launch()
        context = await browser.new_context(user_agent=BrowserPoolConstants.USER_AGENT, locale="en-US")
        await context.add_init_script(BrowserPoolConstants.INIT_SCRIPT)
        self._browsers[index], self._contexts[index] = browser, context

    def _pick(self) -> int:
        index = self._cursor % len(self._slots)
        self._cursor += 1
        return index

    async def _fetch(self, url: str, max_bytes: int) -> tuple[int, str, str]:
        index = self._pick()
        async with self._slots[index]:
            await self._revive(index)
            page = await self._contexts[index].new_page()
            try:
                response = await page.goto(url, wait_until="domcontentloaded", timeout=BrowserPoolConstants.NAV_TIMEOUT_MS)
                try:
                    await page.wait_for_load_state("networkidle", timeout=BrowserPoolConstants.IDLE_TIMEOUT_MS)
                except Exception:
                    pass
                await page.wait_for_timeout(BrowserPoolConstants.SETTLE_MS)
                status = response.status if response else 0
                content_type = (response.headers.get("content-type", "") if response else "").casefold()
                try:
                    body = await page.content() if "html" in content_type or not response else await response.text()
                except Exception:
                    await page.wait_for_timeout(BrowserPoolConstants.SETTLE_MS)
                    body = await page.content()
                return status, (body or "")[:max_bytes], page.url
            finally:
                await page.close()

    def fetch(self, url: str, max_bytes: int = HttpClientConstants.MAX_BYTES) -> tuple[int, str, str]:
        try:
            self._ensure()
            future = asyncio.run_coroutine_threadsafe(self._fetch(url, max_bytes), self._loop)
            return future.result(BrowserPoolConstants.RESULT_TIMEOUT)
        except Exception:
            return 0, "", url
