import time
from typing import Dict, Any, List

from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.helper_methods.social_recon import social_recon
from api.social_manager.helper_methods.phone_recon import phone_recon
from api.social_manager.sessions.playwright_session import playwright_session
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS, SOCIAL_PLATFORMS
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper
from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.instagram import InstagramScraper
from api.social_manager.scrapers.facebook import FacebookScraper
from api.social_manager.scrapers.behance_scraper import BehanceScraper
from api.social_manager.scrapers.vimeo import VimeoScraper
from api.social_manager.scrapers.twitter import TwitterScraper
from api.social_manager.scrapers.tiktok import TikTokScraper
from api.social_manager.scrapers._youtube import YoutubeScraper
from api.social_manager.scrapers.live_search_handler import live_search_handler
from api.social_manager.models import social_model
from api.social_manager.scrapers._duckduckgo_dorker import DuckDuckGoDorker


class social_controller:

    def __init__(self):
        self._recon = social_recon()
        self._phone_recon = phone_recon()
        self._progress = progress_controller.get_instance()
        self.job_id = None
        self.command = None
        self._ddg = live_search_handler()

    def init_job(self, job_id: str, command):
        self.job_id = job_id
        self._progress.init(job_id)
        self.command = command
        self._progress.update(job_id, 0, "starting")

    @staticmethod
    def _session_for_scraper(scraper):
        if isinstance(scraper, YoutubeScraper):
            return playwright_session(headless=True, blocked_resources=set())
        return playwright_session(headless=True)

    def _get_scraper(self, platform, username, max_followers, max_following):
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
        elif platform == SOCIAL_PLATFORMS.TIKTOK:
            scraper = TikTokScraper(username, max_followers, max_following)
        elif platform == SOCIAL_PLATFORMS.YOUTUBE:
            scraper = YoutubeScraper(username, max_followers, max_following)

        if scraper and hasattr(scraper, 'set_scope'):
            scraper.set_scope(self.command)

        return scraper

    def _run_scraper(self, scraper, page) -> Dict[str, Any]:
        if getattr(scraper, "requires_login", False):
            session = SessionManager(scraper.__class__.__name__)
            if not session.load(page):
                session = SessionManager(playwright_session.session_file_for(scraper))
                if not session.load(page):
                    return {"status": "login_required", "platform": scraper.name}
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded")
        else:
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
        return {"status": "success", "platform": scraper.name, "data": scraper.parse_page(page)}

    def _run_posts_scraper(self, scraper, page, max_posts: int) -> Dict[str, Any]:
        if getattr(scraper, "requires_login", False):
            session = SessionManager(scraper.__class__.__name__)
            if not session.load(page):
                session = SessionManager(playwright_session.session_file_for(scraper))
                if not session.load(page):
                    return {"status": "login_required", "platform": scraper.name}
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded")
        else:
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
        if hasattr(scraper, "scrape_posts"):
            try:
                return {"status": "active", "platform": scraper.name, "data": scraper.scrape_posts(page, max_posts)}
            except Exception:
                return {"status": "active", "platform": scraper.name, "data": []}
        return {"status": "error", "message": "posts_not_supported", "platform": scraper.name}

    def _scrape_user(self, platform, username, max_followers, max_following) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, max_followers, max_following)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with self._session_for_scraper(scraper) as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_scraper(scraper, s.page)
            self._progress.update(self.job_id, 80, f"parsing:{platform}:{username}")
        return result

    def _scrape_posts(self, platform, username, max_posts: int) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, 0, 0)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with self._session_for_scraper(scraper) as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_posts_scraper(scraper, s.page, max_posts)
            self._progress.update(self.job_id, 80, f"parsing:{platform}:{username}")
        return result

    def _scrape_multiple(self, targets: List[Dict[str, Any]], compare_results: bool, threshold: int) -> Dict[str, Any]:
        cross_platform_mapper.clear_cards()
        total = sum(len(t.get("usernames", [])) for t in targets) or 1
        done = 0
        results = []
        for t in targets:
            for u in t.get("usernames", []):
                self._progress.update(self.job_id, int((done / total) * 100), f"scraping:{t.get('platform')}:{u}")
                time.sleep(1)
                r = self._scrape_user(t.get("platform"), u, t.get("max_followers", 0), t.get("max_following", 0))
                results.append(r)
                if r.get("status") == "success":
                    d = r.get("data") or {}
                    cross_platform_mapper.add_card(social_model(
                        m_platform=r.get("platform"),
                        m_username=d.get("username", u),
                        m_followers=d.get("followers", []),
                        m_following=d.get("following", []),
                        m_mutual_usernames=d.get("mutual", []),
                    ))
                done += 1
        response = {"status": "success", "scrape_results": results, "total_scraped": len(results)}
        if compare_results:
            self._progress.update(self.job_id, 95, "analyzing")
            response["analysis"] = cross_platform_mapper.get_full_analysis(threshold)
        return response

    def invoke_trigger(self, command: int, data: Any = None) -> Any:
        data = data or {}
        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_USER:
            self.init_job(data.get("job_id"), command)
            try:
                result = {"status": "success", "platform": "recon", "data": self._recon.parse(data.get("username"), data.get("mode", "default"), job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_PHONE:
            self.init_job(data.get("job_id"), command)
            try:
                phone = data.get("phone")
                if not phone:
                    result = {"status": "error", "message": "phone_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = {"status": "success", "platform": "recon_phone", "data": self._phone_recon.parse_phone(phone, data.get("mode", "default"), job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE:
            self.init_job(data.get("job_id"), command)
            try:
                result = self._scrape_multiple(data.get("targets", []), data.get("compare_results", False), data.get("similarity_threshold", 70))
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command in {
            SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY,
            SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY,
            SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY,
        }:
            self.init_job(data.get("job_id"), command)
            try:
                username = data.get("username")
                platform = data.get("platform")
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result

                followers_following_supported_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.BEHANCE,
                    SOCIAL_PLATFORMS.VIMEO,
                ]

                if command in {SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY, SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY} and platform not in followers_following_supported_platforms:
                    result = {"status": "success", "data": {}}
                    self._progress.done(self.job_id, result)
                    return result

                supported_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.TIKTOK,
                    SOCIAL_PLATFORMS.YOUTUBE,
                ]
                if command == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY and platform not in supported_platforms:
                    ddg_result = self._ddg.scrape_profile(username, platform)
                    result = {"status": "suggested", "data": ddg_result}
                    self._progress.done(self.job_id, result)
                    return result
                result = self._scrape_user(platform, username, data.get("max_followers", 0), data.get("max_following", 0))
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_IMAGE:
            self.init_job(data.get("job_id"), command)
            try:
                file_bytes = data.get("file_bytes")
                filename = data.get("filename")
                if not file_bytes:
                    result = {"status": "error", "message": "image_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = {"status": "success", "platform": "recon_image", "data": self._recon.parse_image(file_bytes, filename=filename, job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_POSTS:
            self.init_job(data.get("job_id"), command)
            try:
                username = data.get("username")
                platform = data.get("platform")
                max_posts = data.get("max_posts", 5)
                username = (username or "").strip()
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                native_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.YOUTUBE,
                ]
                if platform in native_platforms:
                    result = self._scrape_posts(platform, username, max_posts)
                    self._progress.done(self.job_id, result)
                    return result
                ddg_result = self._ddg.scrape_posts_search(username, platform, max_posts)
                result = {
                    "status": "suggested",
                    "platform": platform,
                    "data": ddg_result.get("posts", []),
                }
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_USERNAMES:
            self.init_job(data.get("job_id"), command)
            try:
                username = data.get("username")
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result


                dorker = DuckDuckGoDorker()
                dork_result = dorker.smart_search(query=username, platform=data.get("platform"))


                result = {"status": "success", "platform": "duckduckgo", "data": dork_result}

                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES:
            self.init_job(data.get("job_id"), command)
            try:
                username = data.get("username")
                platform = data.get("platform")
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.scrape_images(username, platform or "", limit=10)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_METADATA:   
            self.init_job(data.get("job_id"), command)
            try:
                tokens = data.get("tokens")
                username = data.get("username")
                platform = data.get("platform")
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.search_web(tokens, username, platform)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        return None

    def get_scrape_status(self, job_id: str) -> Dict[str, Any]:
        return self._progress.get(job_id)

    def clear_scrape_status(self, job_id: str) -> None:
        self._progress.error(job_id, "cleared")
