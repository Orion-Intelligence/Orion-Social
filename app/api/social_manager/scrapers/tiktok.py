import re
from abc import ABC
from typing import List
import asyncio
import threading
import random
from datetime import datetime, UTC

from TikTokApi import TikTokApi
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS
from crawler.crawler_instance.local_interface_model.leak.leak_extractor_interface import leak_extractor_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller


class TikTokScraper(leak_extractor_interface, ABC):
    _instance = None
    MS_TOKEN_WAIT_ATTEMPTS = 12

    def __init__(self, username: str = "", callback=None):
        if callable(username) and callback is None:
            callback = username
            username = ""
        self._username = (username or "").strip()
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self._initialized = None
        self._is_crawled = False
        self._scope = SOCIAL_REQUEST_COMMANDS.S_POSTS
        self.m_seed_url = f"https://www.tiktok.com/@{self._username}"
        self._redis_instance = redis_controller()
        self._profile_metadata = {}

        self.MIN_VIEWS = 100_000
        self.MIN_LIKES = 100_000
        self.MAX_VIDEOS = 30

        self._requested_posts_limit: int = 5
        self._requested_videos_limit: int = 5
        self._requested_shorts_limit: int = 5

        self.MS_TOKEN = ""

    def init_callback(self, callback=None):
        self.callback = callback

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TikTokScraper, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @property
    def name(self) -> str:
        return "TikTok"

    def set_scope(self, scope: int):
        self._scope = scope

    def parse_page(self, page) -> dict:
        self._card_data = []
        self._entity_data = []
        self.parse_leak_data(page)
        return {
            "username": self._username,
            "profile_url": self.seed_url,
            "platform": "tiktok",
            "cards": [card.model_dump(mode="json") for card in self._card_data],
            "entities": [entity.model_dump(mode="json") for entity in self._entity_data],
            "followers": [],
            "following": [],
            "mutual": [],
        }

    def scrape_posts(self, page, max_posts: int = 5):
        self._requested_posts_limit = max_posts
        data = self.parse_page(page)
        return data.get("cards", [])[:max_posts]

    def scrape_videos(self, page, max_videos: int):
        self._requested_videos_limit = max_videos
        self.set_scope(SOCIAL_REQUEST_COMMANDS.S_VIDEOS)
        data = self.parse_page(page)
        return data.get("cards", [])[:max_videos]

    def scrape_shorts(self, page, max_shorts: int):
        self._requested_shorts_limit = max_shorts
        self.set_scope(SOCIAL_REQUEST_COMMANDS.S_SHORTS)
        data = self.parse_page(page)
        return data.get("cards", [])[:max_shorts]

    @property
    def is_crawled(self) -> bool:
        return self._is_crawled

    @property
    def seed_url(self) -> str:
        return self.m_seed_url

    @property
    def developer_signature(self) -> str:
        return "Muhammad Huzaifa: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=OU1e"

    @property
    def base_url(self) -> str:
        return "https://www.tiktok.com/"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.TOR,
            m_fetch_config=FetchConfig.API,
            m_threat_type=ThreatType.TIKTOK,
            m_rule_type=RuleType.TIKTOK
        )

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def invoke_db(self, command: int, key: str, default_value, expiry: int = None):
        return self._redis_instance.invoke_trigger(command, [key + self.__class__.__name__, default_value, expiry])

    def contact_page(self) -> str:
        return self.seed_url

    def append_leak_data(self, leak: social_model, entity: entity_model):
        self._card_data.append(leak)
        self._entity_data.append(entity)
        if self.callback and self.callback():
            self._card_data.clear()
            self._entity_data.clear()

    @staticmethod
    def _extract_ms_token_from_cookies(cookies) -> str:
        candidates = []
        for cookie in cookies:
            if cookie.get("name") not in ("msToken", "ms_token"):
                continue
            value = cookie.get("value") or ""
            if not value:
                continue
            domain = cookie.get("domain") or ""
            priority = 1 if domain in ("www.tiktok.com", ".tiktok.com") else 0
            candidates.append((priority, len(value), value))
        if not candidates:
            return ""
        candidates.sort(reverse=True)
        return candidates[0][2]

    def _read_ms_token(self, page) -> str:
        local_token = page.evaluate("() => window.localStorage.getItem('msToken')") or ""
        if local_token:
            return local_token
        return self._extract_ms_token_from_cookies(page.context.cookies())


    def _fetch_ms_token_with_playwright(self, page=None) -> str:
        def _extract(pw_page) -> str:
            pw_page.goto(self.seed_url or self.base_url, wait_until="domcontentloaded", timeout=60000)
            ms_token = ""
            for _ in range(self.MS_TOKEN_WAIT_ATTEMPTS):
                pw_page.wait_for_timeout(random.randint(800, 1500))
                ms_token = self._read_ms_token(pw_page)
                if ms_token:
                    break
            return ms_token or ""

        try:
            if page is not None and hasattr(page, "goto"):
                return _extract(page)

            # page is a CloudScraper / non-Playwright session.
            # Run sync_playwright in a brand-new thread so it is isolated from
            # any active asyncio event loop in the calling thread.
            result: dict = {"token": "", "error": None}

            def _run_in_thread():
                try:
                    from playwright.sync_api import sync_playwright
                    with sync_playwright() as p:
                        browser = p.chromium.launch(
                            headless=True,
                            args=["--ignore-certificate-errors"]
                        )
                        ctx = browser.new_context(ignore_https_errors=True)
                        temp_page = ctx.new_page()
                        result["token"] = _extract(temp_page)
                        ctx.close()
                        browser.close()
                except Exception as exc:
                    result["error"] = exc

            t = threading.Thread(target=_run_in_thread, daemon=True)
            t.start()
            t.join()

            if result["error"]:
                raise result["error"]
            return result["token"]

        except Exception as ex:
            log.g().e(f"Failed to fetch MS token via Playwright: {ex}")
            return ""


    def parse_leak_data(self, page=None):
        try:
            self.MS_TOKEN = self._fetch_ms_token_with_playwright(page)

            def runner():
                asyncio.run(self._parse_leak_data_async())

            t = threading.Thread(target=runner, daemon=False)
            t.start()
            t.join()
        except Exception as ex:
            log.g().e(f"CRITICAL SCRIPT ERROR: {ex}")

    async def _parse_leak_data_async(self):
        if not self.seed_url:
            log.g().e("Seed URL is empty. Paste a TikTok profile URL into self.m_seed_url.")
            return

        if not self.MS_TOKEN:
            log.g().e("MS token not found via Playwright.")
            return

        m = re.search(r"tiktok\.com/@([^/?]+)", self.seed_url)
        if not m:
            log.g().e(f"Invalid TikTok profile URL: {self.seed_url}")
            return
        username = m.group(1)

        if self.is_crawled:
            count = 10
        elif self._scope == SOCIAL_REQUEST_COMMANDS.S_VIDEOS:
            count = self._requested_videos_limit
        elif self._scope == SOCIAL_REQUEST_COMMANDS.S_SHORTS:
            count = self._requested_shorts_limit
        else:
            count = self._requested_posts_limit
        fetched = 0

        async with TikTokApi() as api:
            await api.create_sessions(
                ms_tokens=[self.MS_TOKEN],
                num_sessions=1,
                sleep_after=random.randint(2, 5),
                context_options={"ignore_https_errors": True},
                override_browser_args=["--headless=new", "--ignore-certificate-errors"]
            )
            user = api.user(username=username)

            if self._scope == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY:
                user_info = await user.info()
                user_stats = user_info.get("userInfo", {}).get("stats", {})
                user_detail = user_info.get("userInfo", {}).get("user", {})

                total_followers = int(user_stats.get("followerCount", 0) or 0)
                total_following = int(user_stats.get("followingCount", 0) or 0)
                profile_pic = user_detail.get("avatarLarger", "") or user_detail.get("avatarMedium", "")
                bio = user_detail.get("signature", "") or ""

                is_viral = total_followers > 1_000_000

                card_data = social_model(
                    m_title=username,
                    m_message_id="",
                    m_message_sharable_link=self.seed_url,
                    m_post_likes="",
                    m_post_comments_count="",
                    m_content=bio,
                    m_followers=str(total_followers),
                    m_following=str(total_following),
                    m_profile_pic=profile_pic,
                    m_bio=bio,
                    m_post_comments=None,
                    m_commenters=[],
                    m_platform="tiktok",
                    m_network="clearnet",
                    m_post_tags=[],
                    m_message_date=datetime.now(UTC).date(),
                    m_viral=is_viral
                )

                entity_data = entity_model(
                    m_scrap_file=self.__class__.__name__,
                    m_name=username,
                )

                self.append_leak_data(card_data, entity_data)

            if self._scope == SOCIAL_REQUEST_COMMANDS.S_POSTS:
                async for video in user.videos(count=count):
                    if fetched >= count:
                        break
                    fetched += 1

                    stats = video.stats
                    desc = video.as_dict.get("desc", "") or ""

                    views = int(stats.get("playCount", 0) or 0)
                    likes = int(stats.get("diggCount", 0) or 0)
                    comments = int(stats.get("commentCount", 0) or 0)

                    status = views >= self.MIN_VIEWS or likes >= self.MIN_LIKES

                    hashtags = [tag.lower().strip("#") for tag in re.findall(r"#\w+", desc)]
                    content = desc

                    share_url = video.as_dict.get("shareInfo", {}).get("shareUrl")
                    author = getattr(video.author, "username", None)
                    fallback_url = f"https://www.tiktok.com/@{author}/video/{video.id}" if author else ""
                    video_url = share_url or fallback_url
                    video_id = str(video.id)

                    post_comments_list = []
                    commenters_list = []
                    try:
                        comment_count = 0
                        async for comment in video.comments(count=5):
                            if comment_count >= 5:
                                break

                            comment_text = getattr(comment, "text", "")
                            commenter_username = getattr(comment.author, "username", "unknown")

                            post_comments_list.append(comment_text)
                            commenters_list.append(commenter_username)
                            comment_count += 1
                    except Exception as ex:
                        log.g().e(f"Error fetching comments for video {video_id}: {ex}")

                    post_comments_str = " | ".join(post_comments_list) if post_comments_list else None

                    card_data = social_model(
                        m_title=username,
                        m_message_id=video_id,
                        m_message_sharable_link=video_url,
                        m_post_likes=str(likes),
                        m_post_comments_count=str(comments),
                        m_content=content,
                        m_followers="",
                        m_following="",
                        m_profile_pic="",
                        m_bio="",
                        m_post_comments=post_comments_str,
                        m_commenters=commenters_list,
                        m_platform="tiktok",
                        m_network="clearnet",
                        m_post_tags=hashtags,
                        m_message_date=datetime.now(UTC).date(),
                        m_viral=status
                    )

                    entity_data = entity_model(
                        m_scrap_file=self.__class__.__name__,
                        m_name=author or "unknown",
                    )

                    self.append_leak_data(card_data, entity_data)
                    await asyncio.sleep(random.uniform(0.3, 1.2))

