import importlib
import json
import os
import random
import sys
import hashlib
import asyncio
import threading

from playwright.async_api import async_playwright
from typing import Optional, List
from api.model.rule_model import FetchProxy
from api.runtime_parse_manager.runtime_parse_enum import RUNTIME_PARSE_REQUEST_QUERIES, RUNTIME_PARSE_REQUEST_COMMANDS
from crawler.crawler_instance.proxies.tor_controller.tor_controller import tor_controller
from crawler.crawler_instance.proxies.tor_controller.tor_enums import TOR_COMMANDS
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.redis_manager.redis_enums import REDIS_COMMANDS


class runtime_parse_controller:

    def __init__(self):
        self.driver = None
        self.playwright = None
        self.browser = None
        self._redis = redis_controller()
        self._loop = asyncio.new_event_loop()
        threading.Thread(target=self._loop.run_forever, daemon=True).start()
        self._active_jobs = 0
        self._jobs_lock = threading.Lock()
        try:
            rc = redis_controller()
            for k in rc.invoke_trigger(REDIS_COMMANDS.S_GET_KEYS):
                key = k.decode() if isinstance(k, (bytes, bytearray)) else k
                if isinstance(key, str) and key.startswith("runtime:parse:"):
                    rc.invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [key, "", 1])
        except Exception as ex:
            pass

    @staticmethod
    async def _get_block_resources(route):
        request_url = route.request.url.lower()
        if any(request_url.startswith(scheme) for scheme in ["data:image", "data:video", "data:audio"]) or \
                route.request.resource_type in ["image", "media", "font", "stylesheet"]:
            return await route.abort()
        else:
            return await route.continue_()

    async def _initialize_webdriver(self, use_proxy: FetchProxy = FetchProxy.TOR) -> Optional[object]:
        tor_proxy = None
        if use_proxy == FetchProxy.TOR:
            tor_proxy, _ = tor_controller.get_instance().invoke_trigger(TOR_COMMANDS.S_PROXY, [])
        proxy_url = next(iter(tor_proxy.values()))
        ip_port = proxy_url.split('//')[1]
        ip, port = ip_port.split(':')
        proxy_host = tor_proxy.get('host', ip)
        proxy_port = tor_proxy.get('port', port)
        proxies = {"server": f"socks5://{proxy_host}:{proxy_port}"}
        if self.playwright is None:
            self.playwright = await async_playwright().start()
        if self.browser is None:
            self.browser = await self.playwright.chromium.launch(headless=True, proxy=proxies)
        context = await self.browser.new_context()
        context.set_default_timeout(600000)
        context.set_default_navigation_timeout(600000)
        await context.route("**/*", self._get_block_resources)
        return context

    @staticmethod
    def _suffix_for_command(command: int) -> str:
        if command == RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_USERNAME:
            return "email_username"
        if command == RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_SOCIAL:
            return "social_username"
        return "generic"

    @staticmethod
    def _parsers_for_command(command: int) -> List[str]:
        if command == RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_USERNAME:
            return RUNTIME_PARSE_REQUEST_QUERIES.S_USERNAME
        if command == RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_SOCIAL:
            return RUNTIME_PARSE_REQUEST_QUERIES.S_SOCIAL_USER
        if command == RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_APP:
            return RUNTIME_PARSE_REQUEST_QUERIES.S_APP
        if command == RUNTIME_PARSE_REQUEST_COMMANDS.S_PARSE_SOFTWARE:
            return RUNTIME_PARSE_REQUEST_QUERIES.S_SOFTWARE
        return []

    @staticmethod
    def _key(command: int, query) -> str:
        base = json.dumps(query or {}, sort_keys=True, separators=(",", ":"))
        digest = hashlib.md5(f"{command}:{base}".encode("utf-8")).hexdigest()
        return f"runtime:parse:{digest}"

    def _state_get(self, key: str):
        raw = self._redis.invoke_trigger(REDIS_COMMANDS.S_GET_STRING, [key, None, 3600])
        return json.loads(raw) if raw else None

    def _state_set(self, key: str, state: dict, ttl: int):
        self._redis.invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [key, json.dumps(state), ttl])

    def get_status(self, command: int, query: dict) -> dict:
        key = self._key(command, query)
        state = self._state_get(key)
        if not state:
            return {"status": "none"}
        return state

    def run_parse_job_sync(self, command: int, query: dict):
        key = self._key(command, query)
        with self._jobs_lock:
            if self._active_jobs >= 60:
                self._state_set(key, {"status": "error", "code": "QUEUE_FULL", "message": "queue full try again later"}, 30)
                return {"status": "error", "code": "QUEUE_FULL", "message": "queue full try again later"}
            self._active_jobs += 1
        try:
            fut = asyncio.run_coroutine_threadsafe(self._run_parse_with_progress(command, query), self._loop)
            return fut.result()
        finally:
            with self._jobs_lock:
                self._active_jobs -= 1

    async def _run_parse_with_progress(self, command: int, query: dict):
        key = self._key(command, query)
        parsers = self._parsers_for_command(command)
        total = max(1, len(parsers))
        progress = 1
        self._state_set(key, {"status": "pending", "progress": progress, "step": "running"}, 3600)
        result = []
        try:
            driver = await self._initialize_webdriver()
            progress = max(progress, 3)
            self._state_set(key, {"status": "pending", "progress": progress, "step": "running"}, 3600)
            for idx, parser in enumerate(parsers, start=1):
                try:
                    parse_script = self.on_init_leak_parser(parser)
                    target = min(70, int(idx * 70 / total))
                    if not parse_script:
                        progress = max(progress + 1, target)
                        self._state_set(key, {"status": "pending", "progress": progress, "step": f"{parser}:init_failed"}, 3600)
                        continue
                    q = dict(query or {})
                    q["url"] = parse_script.base_url
                    task = asyncio.create_task(parse_script.parse_leak_data(q, driver))
                    while not task.done():
                        await asyncio.sleep(0.6)
                        bump = random.randint(1, 3)
                        progress = min(70, progress + bump)
                        self._state_set(key, {"status": "pending", "progress": int(progress), "step": "running"}, 3600)
                    resp = await task
                    if hasattr(resp, "cards_data") and len(resp.cards_data) > 0:
                        result.extend(resp.model_dump().get("cards_data", []))
                    progress = max(progress, target)
                    self._state_set(key, {"status": "pending", "progress": int(progress), "step": f"{parser}:done"}, 3600)
                except Exception as ex:
                    log.g().i(ex)
                    self._state_set(key, {"status": "done", "progress": 100, "step": f"{parser}:failed"}, 3600)
            self._state_set(key, {"status": "done", "progress": 100, "result": result}, 3600)
            if driver:
                await driver.close()
            return {"status": "done", "result": result}
        except Exception as ex:
            log.g().i(ex)
            self._state_set(key, {"status": "done", "progress": 100, "step": "failed"}, 3600)
            return {"status": "done", "step": "failed"}

    def clear_status(self, command: int, query: dict):
        key = self._key(command, query)
        self._redis.invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [key, "", 1])

    @staticmethod
    def on_init_leak_parser(file_name):
        class_name = "_" + file_name
        try:
            module_path = f"raw.parsers.api_collector.{class_name}"
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)
            module = importlib.import_module(module_path)
            class_ = getattr(module, class_name)
            return class_()
        except Exception as ex:
            log.g().i(ex)
            return None

    async def invoke_trigger(self, command, data=None):
        return json.dumps(self.get_status(command, data))
