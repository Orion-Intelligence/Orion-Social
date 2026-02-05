import asyncio
import os
import time
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright

from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS, SOCIAL_PLATFORMS
from api.social_manager.cross_platform_mapping import cross_platform_mapper
from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.instagram import InstagramScraper
from api.social_manager.scrapers.facebook import FacebookScraper
from api.social_manager.scrapers.behance_scraper import BehanceScraper
from api.social_manager.scrapers.vimeo import VimeoScraper
from api.social_manager.scrapers._tiktok import tiktok
from api.social_manager.scrapers._twitter import twitter

SESSION_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_FILE_MAP = {
    "InstagramScraper": "instagram_session.json.gz",
    "FacebookScraper": "FacebookScraper_session.json.gz",
}

BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-software-rasterizer'
]

BLOCKED_RESOURCES = ['image', 'media', 'font']


class social_controller:

    def __init__(self):
        self._browser = None
        self._playwright = None
        self._scrape_states: Dict[str, Dict[str, Any]] = {}

    def _get_scraper(self, platform: str, username: str, max_followers: int, max_following: int):
        if platform == SOCIAL_PLATFORMS.INSTAGRAM:
            return InstagramScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.FACEBOOK:
            return FacebookScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.BEHANCE:
            return BehanceScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.VIMEO:
            return VimeoScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.TIKTOK:
            return tiktok(username)
        elif platform == SOCIAL_PLATFORMS.TWITTER:
            return twitter(username)
        return None

    def _block_media(self, route):
        if route.request.resource_type in BLOCKED_RESOURCES:
            route.abort()
        else:
            route.continue_()

    def _run_scraper(self, scraper, page) -> Dict[str, Any]:
        if getattr(scraper, "requires_login", False):
            session_filename = SESSION_FILE_MAP.get(
                scraper.__class__.__name__,
                f"{scraper.__class__.__name__}_session.json.gz"
            )
            session_file = os.path.join(SESSION_DIR, session_filename)

            session = SessionManager(session_file)
            loaded = session.load(page)

            if not loaded:
                return {
                    "status": "login_required",
                    "platform": scraper.name,
                    "message": "Manual login required. Please authenticate and retry."
                }

            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
        else:
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

        result = scraper.parse_page(page)
        return {
            "status": "success",
            "platform": scraper.name,
            "data": result
        }

    def _scrape_single(self, platform: str, username: str, max_followers: int, max_following: int,
                       scrape_key: str = None) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, max_followers, max_following)
        if not scraper:
            return {
                "status": "error",
                "message": f"Unsupported platform: {platform}"
            }

        if scrape_key:
            self._scrape_states[scrape_key] = {
                "status": "pending",
                "progress": 10,
                "step": f"initializing scraper for {platform}:{username}"
            }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=BROWSER_ARGS)
            page = browser.new_page()
            page.route("**/*", self._block_media)

            try:
                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "pending",
                        "progress": 30,
                        "step": f"loading page for {platform}:{username}"
                    }

                result = self._run_scraper(scraper, page)

                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "pending",
                        "progress": 80,
                        "step": f"parsing data for {platform}:{username}"
                    }
            finally:
                browser.close()

        return result

    def _scrape_single_task(self, task: Dict) -> Dict[str, Any]:
        platform = task["platform"]
        username = task["username"]
        max_followers = task.get("max_followers")
        max_following = task.get("max_following")

        scraper = self._get_scraper(platform, username, max_followers, max_following)
        if not scraper:
            return {
                "status": "error",
                "message": f"Unsupported platform: {platform}"
            }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=BROWSER_ARGS)
            page = browser.new_page()
            page.route("**/*", self._block_media)

            try:
                result = self._run_scraper(scraper, page)
            finally:
                browser.close()

        return result

    def _scrape_multiple(self, scrape_key: str, targets: List[Dict], compare_results: bool, threshold: int) -> Dict[
        str, Any]:
        cross_platform_mapper.clear_cards()

        total_tasks = sum(len(t.get("usernames", [])) for t in targets)
        completed = 0

        all_results = []

        for target in targets:
            platform = target.get("platform", "")
            usernames = target.get("usernames", [])
            max_followers = target.get("max_followers")
            max_following = target.get("max_following")
            
            for username in usernames:
                self._scrape_states[scrape_key] = {
                    "status": "pending",
                    "progress": int((completed / max(total_tasks, 1)) * 100),
                    "step": f"scraping {platform}:{username}"
                }

                time.sleep(1)

                result = self._scrape_single(
                    platform,
                    username,
                    max_followers,
                    max_following
                )

                all_results.append(result)
                completed += 1

                self._scrape_states[scrape_key] = {
                    "status": "pending",
                    "progress": int((completed / max(total_tasks, 1)) * 100),
                    "step": f"completed {platform}:{username}"
                }

        response = {
            "status": "success",
            "scrape_results": all_results,
            "total_scraped": len(all_results)
        }

        if compare_results:
            self._scrape_states[scrape_key] = {
                "status": "pending",
                "progress": 95,
                "step": "analyzing cross-platform data"
            }
            response["analysis"] = cross_platform_mapper.get_full_analysis(threshold)

        return response

    def _get_mapping_data(self, include_analysis: bool, threshold: int) -> Dict[str, Any]:
        if include_analysis:
            return cross_platform_mapper.get_full_analysis(threshold)
        return cross_platform_mapper.get_summary()

    def _compare_following(self, threshold: int) -> Dict[str, Any]:
        return cross_platform_mapper.compare_following_across_platforms(threshold)

    def _analyze_influence(self, threshold: int) -> Dict[str, Any]:
        return cross_platform_mapper.analyze_cross_platform_influence(threshold)

    def _clear_data(self) -> Dict[str, Any]:
        cross_platform_mapper.clear_cards()
        return {"status": "success", "message": "All social data cleared"}

    def invoke_trigger(self, command: int, data: Any = None) -> Any:
        if command == SOCIAL_REQUEST_COMMANDS.S_INIT:
            return {"status": "initialized"}

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_INSTAGRAM:
            scrape_key = data.get("scrape_key")

            if scrape_key:
                self._scrape_states[scrape_key] = {
                    "status": "pending",
                    "progress": 0,
                    "step": "starting"
                }

            try:
                result = self._scrape_single(
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    data.get("username"),
                    data.get("max_followers"),
                    data.get("max_following"),
                    scrape_key
                )

                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "done",
                        "result": result
                    }

                return result

            except Exception as exc:
                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "done",
                        "result": {"status": "error", "message": str(exc)}
                    }
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_FACEBOOK:
            scrape_key = data.get("scrape_key")

            if scrape_key:
                self._scrape_states[scrape_key] = {
                    "status": "pending",
                    "progress": 0,
                    "step": "starting"
                }

            try:
                result = self._scrape_single(
                    SOCIAL_PLATFORMS.FACEBOOK,
                    data.get("username"),
                    data.get("max_followers"),
                    data.get("max_following"),
                    scrape_key
                )

                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "done",
                        "result": result
                    }

                return result

            except Exception as exc:
                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "done",
                        "result": {"status": "error", "message": str(exc)}
                    }
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_BEHANCE:
            scrape_key = data.get("scrape_key")

            if scrape_key:
                self._scrape_states[scrape_key] = {
                    "status": "pending",
                    "progress": 0,
                    "step": "starting"
                }

            try:
                result = self._scrape_single(
                    SOCIAL_PLATFORMS.BEHANCE,
                    data.get("username"),
                    data.get("max_followers"),
                    data.get("max_following"),
                    scrape_key
                )

                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "done",
                        "result": result
                    }

                return result

            except Exception as exc:
                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "done",
                        "result": {"status": "error", "message": str(exc)}
                    }
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_VIMEO:
            scrape_key = data.get("scrape_key")

            if scrape_key:
                self._scrape_states[scrape_key] = {
                    "status": "pending",
                    "progress": 0,
                    "step": "starting"
                }

            try:
                result = self._scrape_single(
                    SOCIAL_PLATFORMS.VIMEO,
                    data.get("username"),
                    data.get("max_followers"),
                    data.get("max_following"),
                    scrape_key
                )

                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "done",
                        "result": result
                    }

                return result

            except Exception as exc:
                if scrape_key:
                    self._scrape_states[scrape_key] = {
                        "status": "done",
                        "result": {"status": "error", "message": str(exc)}
                    }
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE:
            scrape_key = data.get("scrape_key", "default")
            targets = data.get("targets", [])
            compare_results = data.get("compare_results", False)
            threshold = data.get("similarity_threshold", 70)

            self._scrape_states[scrape_key] = {
                "status": "pending",
                "progress": 0,
                "step": "starting"
            }

            try:
                result = self._scrape_multiple(scrape_key, targets, compare_results, threshold)

                self._scrape_states[scrape_key] = {
                    "status": "done",
                    "result": result
                }

                return result

            except Exception as exc:
                error_result = {
                    "status": "error",
                    "message": str(exc)
                }

                self._scrape_states[scrape_key] = {
                    "status": "done",
                    "result": error_result
                }

                return error_result

        if command == SOCIAL_REQUEST_COMMANDS.S_GET_MAPPING_DATA:
            return self._get_mapping_data(
                data.get("include_analysis", True),
                data.get("similarity_threshold", 70)
            )

        if command == SOCIAL_REQUEST_COMMANDS.S_COMPARE_FOLLOWING:
            return self._compare_following(data.get("similarity_threshold", 70))

        if command == SOCIAL_REQUEST_COMMANDS.S_ANALYZE_INFLUENCE:
            return self._analyze_influence(data.get("similarity_threshold", 70))

        if command == SOCIAL_REQUEST_COMMANDS.S_CLEAR_DATA:
            return self._clear_data()

        return None

    def get_scrape_status(self, scrape_key: str) -> Dict[str, Any]:
        state = self._scrape_states.get(scrape_key)

        if not state:
            return {"status": "new"}

        return state

    def clear_scrape_status(self, scrape_key: str) -> None:
        if scrape_key in self._scrape_states:
            del self._scrape_states[scrape_key]