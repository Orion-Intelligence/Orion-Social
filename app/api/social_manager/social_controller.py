import os
import time
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright

from api.progress_controller import progress_controller
from api.social_manager.helper_methods.social_recon import social_recon
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS, SOCIAL_PLATFORMS
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper
from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.instagram import InstagramScraper
from api.social_manager.scrapers.facebook import FacebookScraper
from api.social_manager.scrapers.behance_scraper import BehanceScraper
from api.social_manager.scrapers.vimeo import VimeoScraper

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
        self._recon = social_recon()
        self._progress = progress_controller.get_instance()

    def _get_scraper(self, platform: str, username: str, max_followers: int, max_following: int):
        if platform == SOCIAL_PLATFORMS.INSTAGRAM:
            return InstagramScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.FACEBOOK:
            return FacebookScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.BEHANCE:
            return BehanceScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.VIMEO:
            return VimeoScraper(username, max_followers, max_following)
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
                       job_id: str = None) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, max_followers, max_following)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}

        if job_id:
            self._progress.update(job_id, 10, f"initializing:{platform}:{username}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=BROWSER_ARGS)
            page = browser.new_page()
            page.route("**/*", self._block_media)

            try:
                if job_id:
                    self._progress.update(job_id, 30, f"loading:{platform}:{username}")

                result = self._run_scraper(scraper, page)

                if job_id:
                    self._progress.update(job_id, 80, f"parsing:{platform}:{username}")
            finally:
                browser.close()

        return result

    def _scrape_multiple(self, job_id: str, targets: List[Dict], compare_results: bool, threshold: int) -> Dict[str, Any]:
        cross_platform_mapper.clear_cards()

        total_tasks = sum(len(t.get("usernames", [])) for t in targets) or 1
        completed = 0
        all_results = []

        for target in targets:
            platform = target.get("platform", "")
            usernames = target.get("usernames", [])
            max_followers = target.get("max_followers")
            max_following = target.get("max_following")

            for username in usernames:
                if job_id:
                    self._progress.update(job_id, int((completed / total_tasks) * 100), f"scraping:{platform}:{username}")

                time.sleep(1)

                result = self._scrape_single(platform, username, max_followers, max_following, job_id)
                all_results.append(result)
                completed += 1

                if job_id:
                    self._progress.update(job_id, int((completed / total_tasks) * 100), f"completed:{platform}:{username}")

        response = {"status": "success", "scrape_results": all_results, "total_scraped": len(all_results)}

        if compare_results:
            if job_id:
                self._progress.update(job_id, 95, "analyzing")
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

        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_USER:
            job_id = (data or {}).get("job_id") or (data or {}).get("scrape_key")
            if job_id:
                self._progress.init(job_id)
                self._progress.update(job_id, 0, "starting")
            try:
                username = (data or {}).get("username")
                mode = (data or {}).get("mode", "default")
                result = {"status": "success", "platform": "recon", "data": self._recon.parse(username, mode, job_id=job_id)}
                if job_id:
                    self._progress.done(job_id, result)
                return result
            except Exception as exc:
                if job_id:
                    self._progress.error(job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_INSTAGRAM:
            job_id = (data or {}).get("job_id") or (data or {}).get("scrape_key")
            if job_id:
                self._progress.init(job_id)
                self._progress.update(job_id, 0, "starting")
            try:
                result = self._scrape_single(
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    (data or {}).get("username"),
                    (data or {}).get("max_followers"),
                    (data or {}).get("max_following"),
                    job_id
                )
                if job_id:
                    self._progress.done(job_id, result)
                return result
            except Exception as exc:
                if job_id:
                    self._progress.error(job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_FACEBOOK:
            job_id = (data or {}).get("job_id") or (data or {}).get("scrape_key")
            if job_id:
                self._progress.init(job_id)
                self._progress.update(job_id, 0, "starting")
            try:
                result = self._scrape_single(
                    SOCIAL_PLATFORMS.FACEBOOK,
                    (data or {}).get("username"),
                    (data or {}).get("max_followers"),
                    (data or {}).get("max_following"),
                    job_id
                )
                if job_id:
                    self._progress.done(job_id, result)
                return result
            except Exception as exc:
                if job_id:
                    self._progress.error(job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_BEHANCE:
            job_id = (data or {}).get("job_id") or (data or {}).get("scrape_key")
            if job_id:
                self._progress.init(job_id)
                self._progress.update(job_id, 0, "starting")
            try:
                result = self._scrape_single(
                    SOCIAL_PLATFORMS.BEHANCE,
                    (data or {}).get("username"),
                    (data or {}).get("max_followers"),
                    (data or {}).get("max_following"),
                    job_id
                )
                if job_id:
                    self._progress.done(job_id, result)
                return result
            except Exception as exc:
                if job_id:
                    self._progress.error(job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_VIMEO:
            job_id = (data or {}).get("job_id") or (data or {}).get("scrape_key")
            if job_id:
                self._progress.init(job_id)
                self._progress.update(job_id, 0, "starting")
            try:
                result = self._scrape_single(
                    SOCIAL_PLATFORMS.VIMEO,
                    (data or {}).get("username"),
                    (data or {}).get("max_followers"),
                    (data or {}).get("max_following"),
                    job_id
                )
                if job_id:
                    self._progress.done(job_id, result)
                return result
            except Exception as exc:
                if job_id:
                    self._progress.error(job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE:
            job_id = (data or {}).get("job_id") or (data or {}).get("scrape_key") or "default"
            targets = (data or {}).get("targets", [])
            compare_results = (data or {}).get("compare_results", False)
            threshold = (data or {}).get("similarity_threshold", 70)

            if job_id:
                self._progress.init(job_id)
                self._progress.update(job_id, 0, "starting")

            try:
                result = self._scrape_multiple(job_id, targets, compare_results, threshold)
                if job_id:
                    self._progress.done(job_id, result)
                return result
            except Exception as exc:
                if job_id:
                    self._progress.error(job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_GET_MAPPING_DATA:
            return self._get_mapping_data(
                (data or {}).get("include_analysis", True),
                (data or {}).get("similarity_threshold", 70)
            )

        if command == SOCIAL_REQUEST_COMMANDS.S_COMPARE_FOLLOWING:
            return self._compare_following((data or {}).get("similarity_threshold", 70))

        if command == SOCIAL_REQUEST_COMMANDS.S_ANALYZE_INFLUENCE:
            return self._analyze_influence((data or {}).get("similarity_threshold", 70))

        if command == SOCIAL_REQUEST_COMMANDS.S_CLEAR_DATA:
            return self._clear_data()

        return None

    def get_scrape_status(self, job_id: str) -> Dict[str, Any]:
        return self._progress.get(job_id)

    def clear_scrape_status(self, job_id: str) -> None:
        self._progress.error(job_id, "cleared")
