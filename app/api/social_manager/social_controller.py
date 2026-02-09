import time
from typing import Dict, Any
from playwright.sync_api import sync_playwright

from api.social_manager.social_enums import (
    SOCIAL_PLATFORMS,
    SOCIAL_REQUEST_COMMANDS
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

    def _get_scraper(self, platform, username, max_followers, max_following):
        if platform == SOCIAL_PLATFORMS.INSTAGRAM:
            return InstagramScraper(username, max_followers, max_following)
        if platform == SOCIAL_PLATFORMS.FACEBOOK:
            return FacebookScraper(username, max_followers, max_following)
        if platform == SOCIAL_PLATFORMS.BEHANCE:
            return BehanceScraper(username, max_followers, max_following)
        if platform == SOCIAL_PLATFORMS.VIMEO:
            return VimeoScraper(username, max_followers, max_following)
        return None

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

    def _scrape_user(self, platform, username, max_followers, max_following):

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
                return self._run_scraper(scraper, page)
            finally:
                browser.close()

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
