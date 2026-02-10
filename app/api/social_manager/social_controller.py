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
from api.social_manager.scrapers._twitter import TwitterScraper
from api.social_manager.models import social_model

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

    def _get_scraper(self, platform, username, max_followers, max_following, scope=SCRAPE_SCOPE.FOLLOWERS_FOLLOWING):
        scraper = None
        if platform == SOCIAL_PLATFORMS.INSTAGRAM:
            scraper = InstagramScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.FACEBOOK:
            scraper = FacebookScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.BEHANCE:
            scraper = BehanceScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.VIMEO:
            scraper = VimeoScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.TWITTER:
            scraper = TwitterScraper(username, max_followers, max_following)

        if scraper and hasattr(scraper, 'set_scope'):
            scraper.set_scope(scope)

        return scraper

    def _block_media(self, route):
        if route.request.resource_type in BLOCKED_RESOURCES:
            route.abort()
        else:
            route.continue_()

    def _update_progress(self, scrape_key: str, progress: int, step: str):
        if scrape_key:
            self._scrape_states[scrape_key] = {
                "status": "pending",
                "progress": progress,
                "step": step
            }

    def _run_scraper(self, scraper, page, scrape_key: str = None):

        if getattr(scraper, "requires_login", False):
            self._update_progress(scrape_key, 10, "loading session")

            session = SessionManager(scraper.__class__.__name__)

            if not session.load(page):
                return {
                    "error": "login_required",
                    "platform": scraper.name
                }

            self._update_progress(scrape_key, 20, "navigating to profile")
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

        else:
            self._update_progress(scrape_key, 20, "navigating to profile")
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

        self._update_progress(scrape_key, 50, "parsing page data")
        data = scraper.parse_page(page)
        self._update_progress(scrape_key, 90, "finalizing")

        return data

    def _run_posts_scraper(self, scraper, page, max_posts: int, scrape_key: str = None):

        if getattr(scraper, "requires_login", False):
            self._update_progress(scrape_key, 10, "loading session")

            session = SessionManager(scraper.__class__.__name__)

            if not session.load(page):
                return {
                    "error": "login_required",
                    "platform": scraper.name
                }

            self._update_progress(scrape_key, 20, "navigating to profile")
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

        else:
            self._update_progress(scrape_key, 20, "navigating to profile")
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

        self._update_progress(scrape_key, 50, "scraping posts")
        posts_data = scraper.scrape_posts(page, max_posts)
        self._update_progress(scrape_key, 90, "finalizing")

        return posts_data

    def _scrape_user(self, platform, username, max_followers, max_following, scope=SCRAPE_SCOPE.FOLLOWERS_FOLLOWING, scrape_key: str = None):

        scraper = self._get_scraper(platform, username, max_followers, max_following, scope)

        if not scraper:
            return {
                "error": f"Unsupported platform: {platform}"
            }

        self._update_progress(scrape_key, 5, "launching browser")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=BROWSER_ARGS)
            page = browser.new_page()
            page.route("**/*", self._block_media)

            try:
                return self._run_scraper(scraper, page, scrape_key)
            finally:
                browser.close()

    def scrape_profile(self, scrape_key: str, platform: str, username: str):
        self._update_progress(scrape_key, 0, "initializing")
        result = self._scrape_user(platform, username, 0, 0, SCRAPE_SCOPE.PROFILE_ONLY, scrape_key)
        self._scrape_states[scrape_key] = {"status": "done", "data": result}
        return result

    def scrape_followers(self, scrape_key: str, platform: str, username: str, max_followers: int):
        self._update_progress(scrape_key, 0, "initializing")
        result = self._scrape_user(platform, username, max_followers, 0, SCRAPE_SCOPE.FOLLOWERS_ONLY, scrape_key)
        self._scrape_states[scrape_key] = {"status": "done", "data": result}
        return result

    def scrape_following(self, scrape_key: str, platform: str, username: str, max_following: int):
        self._update_progress(scrape_key, 0, "initializing")
        result = self._scrape_user(platform, username, 0, max_following, SCRAPE_SCOPE.FOLLOWING_ONLY, scrape_key)
        self._scrape_states[scrape_key] = {"status": "done", "data": result}
        return result

    def scrape_posts(self, scrape_key: str, platform: str, username: str, max_posts: int):
        self._update_progress(scrape_key, 0, "initializing")

        scraper = self._get_scraper(platform, username, 0, 0, None)

        if not scraper:
            result = {"error": f"Unsupported platform: {platform}"}
            self._scrape_states[scrape_key] = {"status": "done", "data": result}
            return result

        self._update_progress(scrape_key, 5, "launching browser")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=BROWSER_ARGS)
            page = browser.new_page()
            page.route("**/*", self._block_media)

            try:
                posts_data = self._run_posts_scraper(scraper, page, max_posts, scrape_key)

                result = {
                    "username": username,
                    "platform": platform,
                    "posts": posts_data,
                    "total_count": len(posts_data) if isinstance(posts_data, list) else 0
                }

                self._scrape_states[scrape_key] = {"status": "done", "data": result}
                return result

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
                base_progress = int((completed / total_tasks) * 100)
                self._update_progress(scrape_key, base_progress, f"{platform}:{username}")

                result = self._scrape_user(
                    platform,
                    username,
                    max_followers,
                    max_following,
                    SCRAPE_SCOPE.FOLLOWERS_FOLLOWING,
                    scrape_key=None
                )

                results.append(result)

                if result and "error" not in result:
                    card = social_model(
                        m_platform=result.get("platform", platform),
                        m_username=result.get("username", username),
                        m_followers=result.get("followers", []),
                        m_following=result.get("following", []),
                        m_mutual_usernames=result.get("mutual", [])
                    )
                    cross_platform_mapper.add_card(card)

                completed += 1

        analysis = cross_platform_mapper.get_full_analysis(70)

        return {
            "results": results,
            "analysis": analysis
        }

    def invoke_trigger(self, command, data):

        if command != SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE:
            return None

        scrape_key = data["scrape_key"]
        self._update_progress(scrape_key, 0, "starting")

        result = self._scrape_multiple(scrape_key, data["targets"])

        self._scrape_states[scrape_key] = {"status": "done", "data": result}

        return result

    def get_scrape_status(self, scrape_key):
        return self._scrape_states.get(scrape_key, {"status": "new"})

    def clear_scrape_status(self, scrape_key):
        self._scrape_states.pop(scrape_key, None)