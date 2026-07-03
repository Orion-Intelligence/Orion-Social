import os
import secrets
import string
import traceback
from enum import Enum
from threading import Lock, Timer
from typing import Any

import cloudscraper
from playwright.sync_api import Route, sync_playwright

from crawler.crawler_instance.local_interface_model.extractor.model.leak_data_model import leak_data_model
from crawler.crawler_instance.local_shared_model.rule_model import FetchConfig, FetchProxy, ThreatType
from crawler.crawler_services.redis_manager.redis_enums import CUSTOM_SCRIPT_REDIS_KEYS, REDIS_COMMANDS, REDIS_KEYS
from crawler.session_manager import BrowserSessionManager


class RequestParser:
    def __init__(self, proxy: dict, model, reset_cache: bool = False) -> None:
        self.proxy = proxy
        self.model = model
        self.model.init_callback(self.callback)

        self.browser = None
        self.context = None
        self.timeout_flag = False
        self.timeout_timer = None
        self._close_lock = Lock()
        self.session_manager = BrowserSessionManager(self.model)

        if reset_cache:
            self.reset_cache()

    @staticmethod
    def reset_cache() -> None:
        r = lambda: ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(23))
        for obj in (REDIS_KEYS, CUSTOM_SCRIPT_REDIS_KEYS):
            if hasattr(obj, '__members__'):
                globals()[obj.__name__] = Enum(obj.__name__, {n: m.value + r() for n, m in obj.__members__.items()})
            else:
                for k, v in list(vars(obj).items()):
                    if k.isupper() and isinstance(v, str):
                        setattr(obj, k, v + r())

    def callback(self) -> None:
        print("currently parsing index : " + str(len(self.model.card_data)))

    @staticmethod
    def _should_block_resource(route: Route) -> bool:
        request_url = route.request.url.lower()
        return (
            any(request_url.startswith(scheme) for scheme in ["data:image", "data:video", "data:audio"]) or
            route.request.resource_type in ["image", "media", "font", "stylesheet"]
        )

    def _handle_route(self, route: Route) -> None:
        if self._should_block_resource(route):
            route.abort()
        else:
            route.continue_()

    def _terminate(self) -> None:
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

    def _safe_close(self, page=None) -> None:
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

    def _proxy_config(self) -> dict[str, str] | None:
        if self.model.rule_config.m_fetch_proxy == FetchProxy.NONE:
            return None
        if self.model.rule_config.m_fetch_proxy == FetchProxy.TOR:
            if isinstance(self.proxy, dict) and self.proxy.get("server"):
                return {"server": self.proxy["server"].replace("socks5h://", "socks5://", 1)}
            tor_url = os.getenv("TOR_PROXY_URL") or "socks5://127.0.0.1:9150"
            return {"server": tor_url.replace("socks5h://", "socks5://", 1)}
        return None

    def _requests_proxy_config(self) -> dict[str, str] | None:
        proxy = self._proxy_config()
        if not proxy:
            return None
        return {"server": proxy["server"].replace("socks5://", "socks5h://", 1)}

    def _launch_session_browser(self, playwright) -> Any:
        args = ["--ignore-certificate-errors"]
        proxy = self._proxy_config()
        self.session_manager.prepare()
        kwargs = {
            "headless": os.getenv("ORION_PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"} or not os.getenv("DISPLAY"),
            "args": args,
            "ignore_https_errors": True,
        }
        if proxy:
            kwargs["proxy"] = proxy
        context = playwright.chromium.launch_persistent_context(
            str(self.session_manager.profile_path()), **kwargs
        )
        self.session_manager.restore_context(context)
        return context

    def _create_scraper_session(self) -> Any:
        scraper_session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        proxy = self._requests_proxy_config()
        if proxy:
            scraper_session.proxies = {
                "http": proxy["server"],
                "https": proxy["server"]
            }
        scraper_session.headers.update({
            "Referer": "https://www.google.com/",
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1",
            "Connection": "keep-alive",
        })
        seed_timeout = min(120, max(15, int(getattr(self.model.rule_config, "m_timeout", 120) or 120)))
        resp = scraper_session.get(self.model.seed_url, timeout=seed_timeout)
        scraper_session._seed_response = resp
        return scraper_session

    def _set_crawl_state(self) -> str:
        is_crawled_key = CUSTOM_SCRIPT_REDIS_KEYS.URL_PARSED.value + self.model.__class__.__name__
        is_crawled = bool(self.model.invoke_db(REDIS_COMMANDS.S_GET_BOOL, is_crawled_key, False))
        self.model._is_crawled = is_crawled
        return is_crawled_key

    def parse(self, session: bool = False) -> tuple[leak_data_model, None]:
        threat_type = getattr(self.model.rule_config, "m_threat_type", None)
        rule_type = getattr(self.model.rule_config, "m_rule_type", None)
        social_threat_types = {
            ThreatType.SOCIAL,
            ThreatType.BLOGGER,
            ThreatType.BLUESKY,
            ThreatType.DEVTO,
            ThreatType.TWITTER,
            ThreatType.REDDIT,
            ThreatType.TIKTOK,
            ThreatType.HABR,
            ThreatType.HACKERNOON,
            ThreatType.HASHNODE,
            ThreatType.PASTEBIN,
            ThreatType.MASTODON,
            ThreatType.MEDIUM,
            ThreatType.MICROBLOG,
            ThreatType.MISSKEY,
            ThreatType.NOSTR,
            ThreatType.PLEROMA,
            ThreatType.PRIMAL,
            ThreatType.QUORA,
            ThreatType.STACKOVERFLOW,
            ThreatType.SUBSTACK,
            ThreatType.THREADS,
            ThreatType.YOUTUBE,
            ThreatType.FACEBOOK,
            ThreatType.INSTAGRAM,
            ThreatType.LINKEDIN,
            ThreatType.DISCORD,
            ThreatType.WHATSAPP,
        }
        if threat_type in social_threat_types and hasattr(rule_type, "value"):
            content_type = [rule_type.value]
        elif hasattr(threat_type, "value"):
            content_type = [threat_type.value]
        elif hasattr(rule_type, "value"):
            content_type = [rule_type.value]
        else:
            content_type = ["leak"]
        default_data_model = leak_data_model(
            cards_data=[],
            contact_link=self.model.contact_page(),
            base_url=self.model.base_url,
            content_type=content_type
        )

        page = None
        parse_result = None
        if self.model.rule_config.m_fetch_config == FetchConfig.REQUESTS and not session:
            try:
                page = self._create_scraper_session()
                is_crawled_key = self._set_crawl_state()
                parse_result = self.model.parse_leak_data(page)
                self.model.invoke_db(REDIS_COMMANDS.S_SET_BOOL, is_crawled_key, True)
                self.model._set_latest_data_point()
            except KeyboardInterrupt:
                return default_data_model, None
            except Exception:
                print("TRACEBACK:", traceback.format_exc())
            finally:
                self._safe_close(page=page)
            default_data_model.cards_data = self.model.card_data
            return default_data_model, None

        try:
            with sync_playwright() as playwright:
                if session:
                    reset_persistent = os.getenv("ORION_RESET_SESSION", "").lower() in {"1", "true", "yes"}
                    if reset_persistent:
                        self.session_manager.reset()
                self.context = self._launch_session_browser(playwright)
                self.context.set_default_timeout(600000)
                self.context.set_default_navigation_timeout(600000)
                self.timeout_timer = Timer(self.model.rule_config.m_timeout, self._terminate)
                self.timeout_timer.start()

                try:
                    if self.model.rule_config.m_fetch_config == FetchConfig.API and not session:
                        if self.model.rule_config.m_fetch_proxy == FetchProxy.TOR:
                            page = self.context.new_page()
                    elif self.model.rule_config.m_fetch_config == FetchConfig.PLAYRIGHT or session:
                        pages = getattr(self.context, "pages", [])
                        page = pages[0] if pages else self.context.new_page()
                        rule = self.model.rule_config
                        resource_block = bool(getattr(rule, "m_resoource_block", False) or getattr(rule, "m_resource_block", False))
                        if resource_block:
                            page.route("**/*", self._handle_route)
                        page.goto(self.model.seed_url, wait_until="domcontentloaded", timeout=120000)
                        if session:
                            input("Session mode active. Log in, then press Enter here to save the session.")
                    else:
                        page = self._create_scraper_session()

                    is_crawled_key = self._set_crawl_state()

                    if not session:
                        parse_result = self.model.parse_leak_data(page)

                    self.model.invoke_db(REDIS_COMMANDS.S_SET_BOOL, is_crawled_key, True)
                    self.model._set_latest_data_point()

                except KeyboardInterrupt:
                    return default_data_model, None
                except Exception:
                    print("TRACEBACK:", traceback.format_exc())
                finally:
                    try:
                        if self.timeout_timer:
                            self.timeout_timer.cancel()
                    except Exception:
                        pass
                    try:
                        if session or parse_result is True:
                            self.session_manager.save(self.context)
                    except Exception:
                        print("TRACEBACK:", traceback.format_exc())
        except Exception:
            print("TRACEBACK:", traceback.format_exc())
        finally:
            self._safe_close(page=page)
            if session:
                self.session_manager.archive()

        default_data_model.cards_data = self.model.card_data
        return default_data_model, None
