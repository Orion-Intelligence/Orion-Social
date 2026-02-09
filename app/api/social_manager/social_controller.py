import time
from typing import Dict, Any
from playwright.sync_api import sync_playwright

from api.social_manager.social_enums import (
    SOCIAL_PLATFORMS,
    SOCIAL_REQUEST_COMMANDS,
    SCRAPE_SCOPE
)
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper
from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.instagram import InstagramScraper
from api.social_manager.scrapers.facebook import FacebookScraper
from api.social_manager.scrapers.behance_scraper import BehanceScraper
from api.social_manager.scrapers.vimeo import VimeoScraper

BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--disable-software-rasterizer"
]

BLOCKED_RESOURCES = {"image", "media", "font"}


class social_controller:

    def __init__(self):
        self._scrape_states: Dict[str, Dict[str, Any]] = {}

    def _get_scraper(self, platform, username, max_followers, max_following, scope=SCRAPE_SCOPE.ALL_DATA):
        scraper = None
        if platform == SOCIAL_PLATFORMS.INSTAGRAM:
            scraper = InstagramScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.FACEBOOK:
            scraper = FacebookScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.BEHANCE:
            scraper = BehanceScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.VIMEO:
            scraper = VimeoScraper(username, max_followers, max_following)

        if scraper and hasattr(scraper, 'set_scope'):
            scraper.set_scope(scope)

        return scraper

    def _block_media(self, route):
        if route.request.resource_type in BLOCKED_RESOURCES:
            route.abort()
        else:
            route.continue_()

    def _run_scraper(self, scraper, page):

        if getattr(scraper, "requires_login", False):

            session = SessionManager(scraper.__class__.__name__)

            if not session.load(page):
                return {
                    "status": "login_required",
                    "platform": scraper.name
                }

            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

        else:
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

        return {
            "status": "success",
            "platform": scraper.name,
            "data": scraper.parse_page(page)
        }

    def _scrape_user(self, platform, username, max_followers, max_following, scope=SCRAPE_SCOPE.ALL_DATA):

        scraper = self._get_scraper(platform, username, max_followers, max_following, scope)

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
                return self._run_scraper(scraper, page)
            finally:
                browser.close()

    def scrape_profile(self, scrape_key: str, platform: str, username: str):
        self._scrape_states[scrape_key] = {
            "status": "pending",
            "progress": 0,
            "step": f"scraping profile: {username}"
        }
        result = self._scrape_user(platform, username, 0, 0, SCRAPE_SCOPE.PROFILE_ONLY)
        self._scrape_states[scrape_key] = {
            "status": "done",
            "result": result
        }
        return result

    def scrape_followers(self, scrape_key: str, platform: str, username: str, max_followers: int):
        self._scrape_states[scrape_key] = {
            "status": "pending",
            "progress": 0,
            "step": f"scraping followers: {username}"
        }
        result = self._scrape_user(platform, username, max_followers, 0, SCRAPE_SCOPE.FOLLOWERS_ONLY)
        self._scrape_states[scrape_key] = {
            "status": "done",
            "result": result
        }
        return result

    def scrape_following(self, scrape_key: str, platform: str, username: str, max_following: int):
        self._scrape_states[scrape_key] = {
            "status": "pending",
            "progress": 0,
            "step": f"scraping following: {username}"
        }
        result = self._scrape_user(platform, username, 0, max_following, SCRAPE_SCOPE.FOLLOWING_ONLY)
        self._scrape_states[scrape_key] = {
            "status": "done",
            "result": result
        }
        return result

    def _scrape_multiple(self, scrape_key, targets):

        cross_platform_mapper.clear_cards()

        total_tasks = sum(len(t["usernames"]) for t in targets)
        completed = 0
        results = []

        for target in targets:
            platform = target["platform"]
            max_followers = target["max_followers"]
            max_following = target["max_following"]

            for username in target["usernames"]:
                self._scrape_states[scrape_key] = {
                    "status": "pending",
                    "progress": int((completed / total_tasks) * 100),
                    "step": f"{platform}:{username}"
                }

                time.sleep(1)

                result = self._scrape_user(
                    platform,
                    username,
                    max_followers,
                    max_following
                )

                results.append(result)
                completed += 1

        analysis = cross_platform_mapper.get_full_analysis(70)

        return {
            "status": "success",
            "scrape_results": results,
            "analysis": analysis,
            "total_scraped": len(results)
        }

    def invoke_trigger(self, command, data):

        if command != SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE:
            return None

        scrape_key = data["scrape_key"]

        self._scrape_states[scrape_key] = {
            "status": "pending",
            "progress": 0,
            "step": "starting"
        }

        result = self._scrape_multiple(scrape_key, data["targets"])

        self._scrape_states[scrape_key] = {
            "status": "done",
            "result": result
        }

        return result

    def get_scrape_status(self, scrape_key):
        return self._scrape_states.get(scrape_key, {"status": "new"})

    def clear_scrape_status(self, scrape_key):
        self._scrape_states.pop(scrape_key, None)
