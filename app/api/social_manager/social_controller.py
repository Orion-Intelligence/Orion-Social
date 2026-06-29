from typing import Dict, Any, cast

from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.helper_methods.social_recon import social_recon
from api.social_manager.helper_methods.phone_recon import phone_recon
from api.social_manager.sessions.playwright_session import playwright_session
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS, SOCIAL_PLATFORMS
from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers._instagram import _instagram as InstagramScraper
from api.social_manager.scrapers._facebook import _facebook as FacebookScraper
from api.social_manager.scrapers._twitter import _twitter as TwitterScraper
from api.social_manager.scrapers._tiktok import _tiktok as TikTokScraper
from api.social_manager.scrapers._youtube import _youtube as YoutubeScraper
from api.social_manager.scrapers._linkedin import _linkedin as LinkedinScraper
from api.social_manager.scrapers._reddit import _reddit as RedditScraper
from api.social_manager.scrapers._mastodon import _mastodon as MastodonScraper
from api.social_manager.scrapers._pastebin import _pastebin as PastebinScraper
from api.social_manager.scrapers._public_web import _public_web as PublicWebScraper
from api.social_manager.scrapers.live_search_handler import live_search_handler
from crawler.crawler_instance.local_shared_model.rule_model import FetchProxy, SocialDataType


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
    def _clean_str(value: Any, default: str = "") -> str:
        if value is None:
            return default
        return str(value).strip()

    @staticmethod
    def _clean_lower(value: Any, default: str = "") -> str:
        return social_controller._clean_str(value, default).lower()

    @staticmethod
    def _int_value(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _bytes_value(value: Any) -> bytes:
        if isinstance(value, bytes):
            return value
        if isinstance(value, bytearray):
            return bytes(value)
        return b""

    @staticmethod
    def _list_str_value(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]

    @staticmethod
    def _scraper_name(scraper: Any) -> str:
        return getattr(scraper, "name", scraper.__class__.__name__.lstrip("_") or "scraper")

    @staticmethod
    def _social_data_type_for_command(command: int | None) -> SocialDataType:
        if command == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY:
            return SocialDataType.PROFILE
        if command == SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY:
            return SocialDataType.FOLLOWERS
        if command == SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY:
            return SocialDataType.FOLLOWING
        if command == SOCIAL_REQUEST_COMMANDS.S_POSTS:
            return SocialDataType.POSTS
        if command == SOCIAL_REQUEST_COMMANDS.S_VIDEOS:
            return SocialDataType.VIDEOS
        if command == SOCIAL_REQUEST_COMMANDS.S_SHORTS:
            return SocialDataType.SHORTS
        return SocialDataType.DEFAULT

    @staticmethod
    def _social_seed_url(platform: str, username: str) -> str:
        username = (username or "").strip()
        if username.startswith(("http://", "https://")):
            return username
        if platform == SOCIAL_PLATFORMS.INSTAGRAM:
            return f"https://www.instagram.com/{username.lstrip('@').strip('/')}/"
        if platform == SOCIAL_PLATFORMS.FACEBOOK:
            return f"https://www.facebook.com/{username.strip().strip('/')}"
        if platform == SOCIAL_PLATFORMS.TWITTER:
            return f"https://x.com/{username.lstrip('@')}"
        if platform == SOCIAL_PLATFORMS.TIKTOK:
            return f"https://www.tiktok.com/@{username.lstrip('@')}"
        if platform == SOCIAL_PLATFORMS.YOUTUBE:
            return f"https://www.youtube.com/@{username.lstrip('@')}"
        if platform == SOCIAL_PLATFORMS.LINKEDIN:
            handle = username.strip().strip("/")
            if handle.startswith(("company/", "in/", "school/")):
                return f"https://www.linkedin.com/{handle}/"
            return f"https://www.linkedin.com/in/{handle}/"
        if platform == SOCIAL_PLATFORMS.REDDIT:
            handle = username.strip().strip("/")
            reddit_path = handle
            if handle.startswith(("r/", "u/", "user/")):
                reddit_path = handle
            else:
                reddit_path = f"r/{handle}"
            return RedditScraper._to_reddit_tor_url(f"https://www.reddit.com/{reddit_path}/")
        if platform == SOCIAL_PLATFORMS.MASTODON:
            handle = username.lstrip("@")
            if "@" in handle:
                account, host = handle.split("@", 1)
                return f"https://{host}/@{account}"
            return f"https://mastodon.social/@{handle}"
        if platform == SOCIAL_PLATFORMS.PASTEBIN:
            return f"https://pastebin.com/u/{username.lstrip('@').strip('/')}"
        if PublicWebScraper.supports(platform):
            return PublicWebScraper.build_seed_url(platform, username)
        return username

    @staticmethod
    def _session_for_scraper(scraper: Any):
        import os
        proxy = None
        if hasattr(scraper, 'rule_config') and getattr(scraper.rule_config, 'm_fetch_proxy', None) == FetchProxy.TOR:
            tor_url = os.getenv("TOR_PROXY_URL") or "socks5://trusted-social_tor_instace_1:9552"
            tor_url = tor_url.replace("socks5h://", "socks5://")
            proxy = {"server": tor_url}
            
        data_type = getattr(scraper, "m_social_data_type", None)
        profile_data_types = {
            SocialDataType.PROFILE,
            SocialDataType.CHANNEL,
            SocialDataType.FOLLOWERS,
            SocialDataType.FOLLOWING,
        }
        if data_type in profile_data_types:
            return playwright_session(headless=True, blocked_resources=set(), proxy=proxy)

        if isinstance(scraper, (InstagramScraper, TwitterScraper, YoutubeScraper)):
            return playwright_session(headless=True, blocked_resources=set(), proxy=proxy)
        return playwright_session(headless=True, proxy=proxy)

    def _get_scraper(self, platform: str, username: str, max_followers: int, max_following: int) -> Any | None:
        platform = (platform or "").strip().lower()
        scraper_class = {
            SOCIAL_PLATFORMS.INSTAGRAM: InstagramScraper,
            SOCIAL_PLATFORMS.FACEBOOK: FacebookScraper,
            SOCIAL_PLATFORMS.TWITTER: TwitterScraper,
            SOCIAL_PLATFORMS.TIKTOK: TikTokScraper,
            SOCIAL_PLATFORMS.YOUTUBE: YoutubeScraper,
            SOCIAL_PLATFORMS.LINKEDIN: LinkedinScraper,
            SOCIAL_PLATFORMS.REDDIT: RedditScraper,
            SOCIAL_PLATFORMS.MASTODON: MastodonScraper,
            SOCIAL_PLATFORMS.PASTEBIN: PastebinScraper,
        }.get(platform)
        if not scraper_class and not PublicWebScraper.supports(platform):
            return None

        scraper = cast(Any, scraper_class)() if scraper_class else PublicWebScraper(platform=platform)
        if hasattr(scraper, "_card_data"):
            scraper._card_data = []
        if hasattr(scraper, "_entity_data"):
            scraper._entity_data = []
        scraper.m_social_data_type = self._social_data_type_for_command(self.command)
        if isinstance(scraper, PublicWebScraper):
            scraper.m_seed_url = PublicWebScraper.build_seed_url(platform, username, scraper.m_social_data_type)
        else:
            scraper.m_seed_url = self._social_seed_url(platform, username)
        scraper.m_followers_limit = max_followers
        scraper.m_following_limit = max_following
        scraper.m_max_followers = max_followers
        scraper.m_max_following = max_following
        return scraper

    @staticmethod
    def _parse_scraper(scraper: Any, page: Any) -> Any:
        result = scraper.parse_leak_data(page)
        if result is None or isinstance(result, bool):
            return getattr(scraper, "card_data", [])
        return result

    @staticmethod
    def _goto_seed(page: Any, url: str) -> None:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
        except Exception:
            pass

    def _run_scraper(self, scraper: Any, page: Any) -> Dict[str, Any]:
        if getattr(scraper, "requires_login", False):
            session = SessionManager(scraper.__class__.__name__)
            if not session.load(page):
                session = SessionManager(playwright_session.session_file_for(scraper))
                if not session.load(page):
                    return {"status": "login_required", "platform": self._scraper_name(scraper)}
            self._goto_seed(page, scraper.seed_url)
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded", timeout=25000)
        else:
            self._goto_seed(page, scraper.seed_url)
        return {"status": "success", "platform": self._scraper_name(scraper), "data": self._parse_scraper(scraper, page)}

    def _run_posts_scraper(self, scraper: Any, page: Any, max_posts: int) -> Dict[str, Any]:
        if getattr(scraper, "requires_login", False):
            session = SessionManager(scraper.__class__.__name__)
            if not session.load(page):
                session = SessionManager(playwright_session.session_file_for(scraper))
                if not session.load(page):
                    return {"status": "login_required", "platform": self._scraper_name(scraper)}
            self._goto_seed(page, scraper.seed_url)
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded", timeout=25000)
        else:
            self._goto_seed(page, scraper.seed_url)
        scraper.m_item_limit = max(1, min(self._int_value(max_posts, 10), 100))
        scraper.m_social_data_type = SocialDataType.POSTS
        return {"status": "active", "platform": self._scraper_name(scraper), "data": self._parse_scraper(scraper, page)}

    def _run_videos_scraper(self, scraper: Any, page: Any, max_videos: int) -> Dict[str, Any]:
        self._goto_seed(page, scraper.seed_url)
        scraper.m_item_limit = max(1, min(self._int_value(max_videos, 10), 100))
        scraper.m_social_data_type = SocialDataType.VIDEOS
        return {"status": "active", "platform": self._scraper_name(scraper), "data": self._parse_scraper(scraper, page)}

    def _run_shorts_scraper(self, scraper: Any, page: Any, max_shorts: int) -> Dict[str, Any]:
        self._goto_seed(page, scraper.seed_url)
        scraper.m_item_limit = max(1, min(self._int_value(max_shorts, 10), 100))
        scraper.m_social_data_type = SocialDataType.SHORTS
        return {"status": "active", "platform": self._scraper_name(scraper), "data": self._parse_scraper(scraper, page)}

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

    def _scrape_videos(self, platform, username, max_videos: int) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, 0, 0)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with self._session_for_scraper(scraper) as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_videos_scraper(scraper, s.page, max_videos)
            self._progress.update(self.job_id, 80, f"parsing:{platform}:{username}")
        return result

    def _scrape_shorts(self, platform, username, max_shorts: int) -> Dict[str, Any]:
        scraper = self._get_scraper(platform, username, 0, 0)
        if not scraper:
            return {"status": "error", "message": f"Unsupported platform: {platform}"}
        self._progress.update(self.job_id, 10, f"initializing:{platform}:{username}")
        with self._session_for_scraper(scraper) as s:
            self._progress.update(self.job_id, 30, f"loading:{platform}:{username}")
            result = self._run_shorts_scraper(scraper, s.page, max_shorts)
            self._progress.update(self.job_id, 80, f"parsing:{platform}:{username}")
        return result

    def invoke_trigger(self, command: int, data: Any = None) -> Any:
        data = data if isinstance(data, dict) else {}
        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_USER:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                mode = self._clean_str(data.get("mode"), "default")
                result = {"status": "success", "platform": "recon", "data": self._recon.parse(username, mode, job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_PHONE:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                phone = self._clean_str(data.get("phone"))
                if not phone:
                    result = {"status": "error", "message": "phone_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                mode = self._clean_str(data.get("mode"), "default")
                result = {"status": "success", "platform": "recon_phone", "data": self._phone_recon.parse_phone(phone, mode, job_id=self.job_id)}
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
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_lower(data.get("platform"))
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result

                followers_following_supported_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.LINKEDIN,
                    SOCIAL_PLATFORMS.REDDIT,
                    SOCIAL_PLATFORMS.MASTODON,
                    SOCIAL_PLATFORMS.PASTEBIN,
                    SOCIAL_PLATFORMS.TIKTOK,
                    SOCIAL_PLATFORMS.YOUTUBE,
                    SOCIAL_PLATFORMS.BEHANCE,
                    SOCIAL_PLATFORMS.VIMEO,
                ]

                if command in {SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY, SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY} and platform not in followers_following_supported_platforms:
                    result = {"status": "error", "message": f"{platform}_followers_following_not_supported", "data": None}
                    self._progress.done(self.job_id, result)
                    return result

                supported_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.TIKTOK,
                    SOCIAL_PLATFORMS.YOUTUBE,
                    SOCIAL_PLATFORMS.LINKEDIN,
                    SOCIAL_PLATFORMS.REDDIT,
                    SOCIAL_PLATFORMS.MASTODON,
                    SOCIAL_PLATFORMS.PASTEBIN,
                ]
                if command == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY and platform not in supported_platforms and not PublicWebScraper.supports(platform):
                    ddg_result = self._ddg.scrape_profile(username, platform)
                    result = {"status": "suggested", "data": ddg_result}
                    self._progress.done(self.job_id, result)
                    return result
                result = self._scrape_user(
                    platform,
                    username,
                    self._int_value(data.get("max_followers"), 0),
                    self._int_value(data.get("max_following"), 0),
                )
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_VIDEOS:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_lower(data.get("platform"))
                max_videos = self._int_value(data.get("max_videos"), 5)
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = self._scrape_videos(platform, username, max_videos)
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_SHORTS:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_lower(data.get("platform"))
                max_shorts = self._int_value(data.get("max_shorts"), 5)
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = self._scrape_shorts(platform, username, max_shorts)
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_IMAGE:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                file_bytes = self._bytes_value(data.get("file_bytes"))
                filename = self._clean_str(data.get("filename"))
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
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_lower(data.get("platform"))
                max_posts = self._int_value(data.get("max_posts"), 5)
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                native_platforms = [
                    SOCIAL_PLATFORMS.INSTAGRAM,
                    SOCIAL_PLATFORMS.TWITTER,
                    SOCIAL_PLATFORMS.FACEBOOK,
                    SOCIAL_PLATFORMS.YOUTUBE,
                    SOCIAL_PLATFORMS.LINKEDIN,
                    SOCIAL_PLATFORMS.REDDIT,
                    SOCIAL_PLATFORMS.TIKTOK,
                    SOCIAL_PLATFORMS.MASTODON,
                    SOCIAL_PLATFORMS.PASTEBIN,
                ]
                if platform in native_platforms or PublicWebScraper.supports(platform):
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
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                platform = self._clean_str(data.get("platform"))
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.collect_social_handles(username, platform or None)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES:
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_str(data.get("platform"))
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
            self.init_job(self._clean_str(data.get("job_id")), command)
            try:
                tokens = self._list_str_value(data.get("tokens"))
                username = self._clean_str(data.get("username")) or None
                platform = self._clean_str(data.get("platform")) or None
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
