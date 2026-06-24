import traceback
import secrets
import string
from enum import Enum
from threading import Timer, Lock

import cloudscraper
from playwright.sync_api import sync_playwright, Route

from crawler.crawler_instance.local_interface_model.leak.model.leak_data_model import leak_data_model
from crawler.crawler_instance.local_shared_model.rule_model import FetchProxy, FetchConfig
from crawler.crawler_services.redis_manager.redis_enums import REDIS_COMMANDS, CUSTOM_SCRIPT_REDIS_KEYS, REDIS_KEYS
from crawler.crawler_services.shared.helper_method import helper_method


class RequestParser:
    def __init__(self, proxy: dict, model, reset_cache: bool = False):
        self.proxy = proxy
        self.model = model
        self.model.init_callback(self.callback)

        self.browser = None
        self.context = None
        self.timeout_flag = False
        self.timeout_timer = None
        self._close_lock = Lock()

        if reset_cache:
            self.reset_cache()

    @staticmethod
    def reset_cache():
        r = lambda: ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(23))
        for obj in (REDIS_KEYS, CUSTOM_SCRIPT_REDIS_KEYS):
            if hasattr(obj, '__members__'):
                globals()[obj.__name__] = Enum(obj.__name__, {n: m.value + r() for n, m in obj.__members__.items()})
            else:
                for k, v in list(vars(obj).items()):
                    if k.isupper() and isinstance(v, str):
                        setattr(obj, k, v + r())

    def callback(self):
        print("currently parsing index : " + str(len(self.model.card_data)))

    @staticmethod
    def _should_block_resource(route: Route) -> bool:
        request_url = route.request.url.lower()
        return (
            any(request_url.startswith(scheme) for scheme in ["data:image", "data:video", "data:audio"]) or
            route.request.resource_type in ["image", "media", "font", "stylesheet"]
        )

    def _handle_route(self, route: Route):
        if self._should_block_resource(route):
            route.abort()
        else:
            route.continue_()

    def _terminate(self):
        with self._close_lock:
            if self.timeout_flag:
                return
            self.timeout_flag = True
            try:
                print("Timeout reached. Closing browser context and terminating tasks.")
                if self.context:
                    try:
                        self.context.close()
                    except Exception:
                        pass
                if self.browser:
                    try:
                        self.browser.close()
                    except Exception:
                        pass
            except Exception:
                pass

    def _safe_close(self, page=None):
        with self._close_lock:
            try:
                if page:
                    try:
                        page.close()
                    except Exception:
                        pass
                if self.context:
                    try:
                        self.context.close()
                    except Exception:
                        pass
                    finally:
                        self.context = None
                if self.browser:
                    try:
                        self.browser.close()
                    except Exception:
                        pass
                    finally:
                        self.browser = None
            except Exception:
                pass

    def parse(self):
        default_data_model = leak_data_model(
            cards_data=[],
            contact_link=self.model.contact_page(),
            base_url=self.model.base_url,
            content_type=["leak"]
        )

        page = None
        try:
            with sync_playwright() as playwright:
                self.browser = self._launch_browser(playwright)
                if helper_method.get_network_type(self.model.base_url).__eq__("onion"):
                    self.context = self.browser.new_context(ignore_https_errors=True)
                else:
                    self.context = self.browser.new_context()
                self.context.set_default_timeout(600000)
                self.context.set_default_navigation_timeout(600000)
                self.timeout_timer = Timer(self.model.rule_config.m_timeout, self._terminate)
                self.timeout_timer.start()

                try:
                    if self.model.rule_config.m_fetch_config == FetchConfig.PLAYRIGHT:
                        page = self.context.new_page()
                        rule = self.model.rule_config
                        resource_block = bool(getattr(rule, "m_resoource_block", False) or getattr(rule, "m_resource_block", False))
                        if resource_block:
                            page.route("**/*", self._handle_route)
                        page.goto(self.model.seed_url, wait_until="load", timeout=11111111)
                    else:
                        session = cloudscraper.create_scraper(
                            browser={
                                'browser': 'chrome',
                                'platform': 'windows',
                                'mobile': False
                            }
                        )
                        if self.model.rule_config.m_fetch_proxy is not FetchProxy.NONE and isinstance(self.proxy, dict) and "server" in self.proxy:
                            session.proxies = {
                                "http": self.proxy["server"],
                                "https": self.proxy["server"]
                            }
                        session.headers.update({
                            "Referer": "https://www.google.com/",
                            "Accept-Language": "en-US,en;q=0.9",
                            "DNT": "1",
                            "Connection": "keep-alive",
                        })
                        resp = session.get(self.model.seed_url, timeout=360)
                        resp.raise_for_status()
                        session._seed_response = resp
                        page = session

                    is_crawled_key = CUSTOM_SCRIPT_REDIS_KEYS.URL_PARSED.value + self.__class__.__name__
                    is_crawled = bool(self.model.invoke_db(REDIS_COMMANDS.S_GET_BOOL, is_crawled_key, False))
                    self.model._is_crawled = is_crawled

                    self.model.parse_leak_data(page)

                    self.model.invoke_db(REDIS_COMMANDS.S_SET_BOOL, is_crawled_key, True)

                except Exception:
                    print("TRACEBACK:", traceback.format_exc())
                finally:
                    try:
                        if self.timeout_timer:
                            self.timeout_timer.cancel()
                    except Exception:
                        pass
        except Exception:
            print("TRACEBACK:", traceback.format_exc())
        finally:
            self._safe_close(page=page)

        default_data_model.cards_data = self.model.card_data
        return default_data_model, None

    def _launch_browser(self, playwright):
        args = ["--ignore-certificate-errors"]
        browser = (
            playwright.chromium.launch(headless=False, args=args)
            if self.model.rule_config.m_fetch_proxy is FetchProxy.NONE
            else playwright.chromium.launch(proxy=self.proxy, headless=False, args=args)
        )
        self.context = browser.new_context(ignore_https_errors=True)
        return browser
