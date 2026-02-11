import time
from typing import Dict, Any, List

from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.helper_methods.social_recon import social_recon
from api.social_manager.sessions.playwright_session import playwright_session
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS, SOCIAL_PLATFORMS
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper
from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.instagram import InstagramScraper
from api.social_manager.scrapers.facebook import FacebookScraper
from api.social_manager.scrapers.behance_scraper import BehanceScraper
from api.social_manager.scrapers.vimeo import VimeoScraper
from api.social_manager.models import social_model


class social_controller:

    def __init__(self):
        self._recon = social_recon()
        self._progress = progress_controller.get_instance()
        self.job_id = None

    def init_job(self, job_id: str):
        self.job_id = job_id
        self._progress.init(job_id)
        self._progress.update(job_id, 0, "starting")

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

    def _run_scraper(self, scraper, page) -> Dict[str, Any]:
        if getattr(scraper, "requires_login", False):
            session = SessionManager(playwright_session.session_file_for(scraper))
            if not session.load(page):
                return {"status": "login_required", "platform": scraper.name}
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded")
        else:
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
        return {"status": "success", "platform": scraper.name, "data": scraper.parse_page(page)}

    def _scrape_user(self, platform, username, max_followers, max_following) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, max_followers, max_following)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with playwright_session() as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_scraper(scraper, s.page)
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
            self.init_job(data.get("job_id"))
            try:
                result = {"status": "success", "platform": "recon", "data": self._recon.parse(data.get("username"), data.get("mode", "default"), job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE:
            self.init_job(data.get("job_id"))
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
            self.init_job(data.get("job_id"))
            try:
                result = self._scrape_user(data.get("platform"), data.get("username"), data.get("max_followers", 0), data.get("max_following", 0))
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
