import re
from abc import ABC
from datetime import datetime
from typing import List, Dict, Any, Tuple

from playwright.sync_api import Page

from crawler.crawler_instance.genbot_service.helpers.mastodon.mastodon_helper_methods import MastodonHelperMethods
from crawler.crawler_instance.local_interface_model.leak.leak_extractor_interface import leak_extractor_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, \
    RuleType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS

class _mastodon(leak_extractor_interface, ABC):
    _instance = None

    def __init__(self, username: str = "",callback=None):
        self.callback = callback
        self._card_data: List[social_model] = []
        self._entity_data: List[entity_model] = []
        self.soup = None
        self._scope = SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY
        self._username = (username or "").strip()
        self._initialized = None
        self.m_seed_url = f"https://mastodon.social/@{self._username}"
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._requested_posts_limit = None
        self._helper_methods = MastodonHelperMethods()

    def init_callback(self, callback=None):
        self.callback = callback

    def set_scope(self, scope: int):
        self._scope = scope

    @property
    def name(self) -> str:
        return "Mastodon"

    def parse_page(self, page) -> dict:
        self._card_data = []
        self._entity_data = []
        self.parse_leak_data(page)
        return {
            "username": self._username,
            "profile_url": self.seed_url,
            "platform": "mastodon",
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

    def scrape_videos(self, page, max_videos: int = 5):
        return []

    def scrape_shorts(self, page, max_shorts: int = 5):
        return []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(_mastodon, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @property
    def is_crawled(self) -> bool:
        return self._is_crawled

    @property
    def seed_url(self) -> str:
        return self.m_seed_url

    @property
    def developer_signature(self) -> str:
        return "Muhammad Hannan Zahid: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hOii"

    @property
    def base_url(self) -> str:
        return "https://mastodon.social"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(m_fetch_proxy=FetchProxy.NONE, m_fetch_config=FetchConfig.PLAYRIGHT,
                         m_threat_type=ThreatType.MASTODON, m_rule_type=RuleType.MASTODON, m_resoource_block=False)

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
        if self.callback:
            if self.callback():
                self._card_data.clear()
                self._entity_data.clear()

    def _parse_social_count(self, text: str) -> str:
        if not text:
            return "0"

        match = re.search(r"([\d\.,]+)\s*([KkMm]?)", text)
        if not match:
            return "0"

        num_str = match.group(1).replace(",", "")
        suffix = match.group(2).upper()

        try:
            val = float(num_str)
            if suffix == "K":
                val *= 1000
            elif suffix == "M":
                val *= 1000000
            return str(int(val))
        except Exception:
            return "0"

    def prepare_target_context(self, page: Page) -> Tuple[str, str]:
        target_url = self.m_seed_url
        default_username = target_url.rstrip("/").split("/")[-1].replace("@", "")

        page.goto(target_url, wait_until="networkidle")
        page.wait_for_selector('article, ._comp_account_header__nameWrapper', timeout=20000)
        page.wait_for_timeout(2000)

        return target_url, default_username

    def _extract_profile_metadata(self, page: Page, default_username: str) -> dict:
        real_name = ""
        try:
            name_loc = page.locator("div._comp_account_header__name h1").first
            if name_loc.count() > 0:
                real_name = name_loc.inner_text().strip()
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract display name: {e}")

        username = default_username
        try:
            handle_loc = page.locator("button._comp_account_header__handleHelpButton").first
            if handle_loc.count() > 0:
                raw_handle = handle_loc.inner_text().strip().split("\n")[0]
                if raw_handle:
                    username = raw_handle
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract username handle: {e}")

        bio_text = ""
        try:
            bio_loc = page.locator("div._comp_account_header__bio").first
            if bio_loc.count() > 0:
                bio_text = bio_loc.inner_text().strip()
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract bio: {e}")

        followers = "0"
        try:
            f_loc = page.locator("li._comp_number_fields__item:has-text('Followers')").first
            if f_loc.count() > 0:
                followers = f_loc.get_attribute("title") or "0"
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract followers: {e}")

        following = "0"
        try:
            f_loc = page.locator("li._comp_number_fields__item:has-text('Following')").first
            if f_loc.count() > 0:
                following = f_loc.get_attribute("title") or "0"
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract following: {e}")

        posts = "0"
        try:
            p_loc = page.locator("li._comp_number_fields__item:has-text('Posts')").first
            if p_loc.count() > 0:
                posts = p_loc.get_attribute("title") or "0"
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract total posts: {e}")

        join_date = ""
        try:
            join_loc = page.locator("li._comp_number_fields__item:has-text('Joined') time").first
            if join_loc.count() > 0:
                join_date_iso = join_loc.get_attribute("datetime")
                if join_date_iso:
                    join_date = datetime.fromisoformat(join_date_iso.replace("Z", "+00:00")).strftime("%Y-%m-%d")
            else:
                join_li = page.locator("li._comp_number_fields__item:has-text('Joined')").first
                if join_li.count() > 0:
                    join_date = join_li.get_attribute("title") or ""
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract join date: {e}")

        profile_photo = ""
        try:
            pfp_loc = page.locator("div._comp_account_header__avatarWrapper img").first
            if pfp_loc.count() > 0:
                profile_photo = pfp_loc.get_attribute("src") or ""
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract profile photo: {e}")

        cover_photo = ""
        try:
            cover_loc = page.locator("div._comp_account_header__header img").first
            if cover_loc.count() > 0:
                cover_photo = cover_loc.get_attribute("src") or ""
        except Exception as e:
            log.g().w(f"[Scraper] Failed to extract cover photo: {e}")

        followers = followers.replace(",", "")
        following = following.replace(",", "")
        posts = posts.replace(",", "")

        return {
            "username": username,
            "real_name": real_name,
            "bio_text": bio_text,
            "followers": followers,
            "following": following,
            "posts": posts,
            "join_date": join_date,
            "profile_photo": profile_photo,
            "cover_photo": cover_photo
        }

    def surface_info(self, page: Page) -> Dict[str, Any]:
        target_url, target_username = self.prepare_target_context(page)
        meta = self._extract_profile_metadata(page, target_username)

        formatted_info = (
            f"Bio: {meta['bio_text']}\n"
            f"Joined: {meta['join_date']}"
        )

        return {
            "target_url": target_url,
            "username": meta['username'],
            "real_name": meta['real_name'],
            "formatted_info": formatted_info,
            "followers": meta['followers'],
            "following": meta['following'],
            "posts": meta['posts'],
            "profile_photo": meta['profile_photo'],
            "cover_photo": meta['cover_photo']
        }

    def heavy_content(self, page: Page, username: str) -> List[social_model]:
        desired_count = 10 if self.is_crawled else (self._requested_posts_limit or 5)
        comments_per_post = 50
        existing_ids = set()

        posts = self._helper_methods.scroll_and_collect(page, username, existing_ids, desired_count)
        parsed_post = []

        if len(posts) < 3:
            log.g().w("[Scraper] Response empty or too few posts found.")
            return []

        page.keyboard.press("Home")
        page.wait_for_timeout(2000)

        for post_id in posts:
            article = page.locator(f'article[data-id="{post_id}"]')

            attempts = 0
            while article.count() == 0 and attempts < 15:
                page.keyboard.press("PageDown")
                page.wait_for_timeout(300)
                attempts += 1

            if article.count() == 0:
                log.g().w(f"[Scraper] Could not find post {post_id} in DOM. Skipping.")
                continue

            article.scroll_into_view_if_needed()
            page.wait_for_timeout(500)

            post = self._helper_methods.extract_post_details(page, post_id, self.seed_url)

            try:
                title_loc = article.locator('.display-name__html')
                if title_loc.count() > 0:
                    title_text = title_loc.first.inner_text().strip()
                    post['card_title'] = title_text
            except Exception as e:
                log.g().w(f"Failed to extract title for {post_id}: {e}")

            try:
                reply_timeline = article.locator('button:has(svg.icon-reply) .icon-button__counter')
                if reply_timeline.count() > 0:
                    reply_text = reply_timeline.first.inner_text().strip()
                    post['replies'] = self._parse_social_count(reply_text)
                else:
                    post['replies'] = "0"
            except Exception as e:
                log.g().w(f"Failed to extract replies for {post_id}: {e}")

            try:
                boost_detail = article.locator('.detailed-status__reblogs')
                boost_timeline = article.locator('button:has(svg.icon-retweet) .icon-button__counter')

                if boost_detail.count() > 0:
                    boost_text = boost_detail.first.inner_text().strip()
                    post['boosts'] = self._parse_social_count(boost_text)
                elif boost_timeline.count() > 0:
                    boost_text = boost_timeline.first.inner_text().strip()
                    post['boosts'] = self._parse_social_count(boost_text)
                else:
                    post['boosts'] = "0"
            except Exception as e:
                log.g().w(f"Failed to extract boosts for {post_id}: {e}")

            try:
                fav_detail = article.locator('.detailed-status__favorites')
                fav_timeline = article.locator('button:has(svg.icon-star) .icon-button__counter')

                if fav_detail.count() > 0:
                    fav_text = fav_detail.first.inner_text().strip()
                    post['favourites'] = self._parse_social_count(fav_text)
                elif fav_timeline.count() > 0:
                    fav_text = fav_timeline.first.inner_text().strip()
                    post['favourites'] = self._parse_social_count(fav_text)
                else:
                    post['favourites'] = "0"
            except Exception as e:
                log.g().w(f"Failed to extract likes for {post_id}: {e}")

            post['comments_list'] = []
            post['commenters_list'] = []

            replies_count = int(post.get('replies', '0'))
            if replies_count > 0:
                try:
                    click_target = article.locator('a.status__relative-time').first
                    if click_target.count() > 0:
                        log.g().i(f"[Scraper] Post {post_id} has {replies_count} replies. Clicking to extract...")
                        click_target.click(force=True)

                        page.wait_for_selector('.detailed-status__wrapper', timeout=10000)
                        page.wait_for_timeout(1500)

                        reply_nodes = page.locator("div.status__wrapper-reply").all()
                        for node in reply_nodes:
                            if len(post['comments_list']) >= comments_per_post:
                                break
                            try:
                                c_user_loc = node.locator(".display-name__html").first
                                c_user = c_user_loc.inner_text().strip() if c_user_loc.count() > 0 else "Unknown"

                                c_text_loc = node.locator(".status__content__text").first
                                c_text = c_text_loc.inner_text().strip() if c_text_loc.count() > 0 else ""

                                if c_text:
                                    post['comments_list'].append(c_text)
                                    post['commenters_list'].append(c_user)
                            except Exception:
                                pass

                        log.g().i(f"[Scraper] Extracted {len(post['comments_list'])} comments. Returning to feed...")

                        page.go_back(wait_until="networkidle")

                        page.wait_for_selector('article', timeout=10000)
                        page.wait_for_timeout(1500)
                except Exception as e:
                    log.g().w(f"Failed to execute comment extraction for {post_id}: {e}")
                    if self.m_seed_url not in page.url:
                        page.go_back(wait_until="networkidle")
                        page.wait_for_selector('article', timeout=10000)

            parsed_post.append(post)

        cards: List[social_model] = []

        for post in parsed_post:
            date_str = post.get("date", "")
            parsed_date = None
            if date_str:
                try:
                    parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
                except Exception:
                    pass

            if not post.get("url", ""):
                continue

            msg_link = post.get("url", "")
            msg_sharable_link = self.base_url + msg_link

            card_data = social_model(
                m_platform="mastodon",
                m_message_sharable_link=msg_sharable_link,
                m_channel_url=self.seed_url,
                m_title=post.get("content", ""),
                m_sender_name=post.get("username", ""),
                m_weblink=post.get("weblinks", []),
                m_content=post.get("content", ""),
                m_content_type=["social_collector"],
                m_network="clearnet",
                m_message_date=parsed_date,
                m_message_id=post.get("id"),
                m_post_shares=post.get("boosts", "0"),
                m_post_likes=post.get("favourites", "0"),
                m_post_comments_count=post.get("replies", "0"),
                m_post_comments="\n\n".join(post.get("comments_list", [])),
                m_commenters=list(set(post.get("commenters_list", [])))
            )
            cards.append(card_data)

        return cards

    def parse_leak_data(self,page: Page):
        try:
            log.g().i(f"[Scraper] Initializing session on {self.m_seed_url}")
            # 1. Surface Data Extraction
            if self._scope == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY:

                surface = self.surface_info(page)
                username = surface["username"]
                target_url = surface["target_url"]

                surface_card = social_model(
                    m_platform="mastodon",
                    m_message_sharable_link=target_url,
                    m_title=username,
                    m_sender_name=surface["real_name"],
                    m_network="clearnet",
                    m_content_type=["user_profile"],
                    m_group_info=surface["formatted_info"],
                    m_followers=surface["followers"],
                    m_following=surface["following"],
                    m_total_posts=surface["posts"],
                    m_profile_pic=surface["profile_photo"],
                    m_cover_pic=surface["cover_photo"],
                    m_message_date=datetime.utcnow().date(),
                )

                self.append_leak_data(
                    surface_card,
                    entity_model(m_team="mastodon_scraper", m_scrap_file=self.__class__.__name__)
                )
                log.g().i(f"[Scraper] Surface metadata committed for {username}.")

                self._is_crawled = True
                log.g().i("[Scraper] Info Mode complete. Skipping heavy extraction.")
                return
            if self._scope == SOCIAL_REQUEST_COMMANDS.S_POSTS     :

                cards = self.heavy_content(page, username=self._username)
                for card in cards:
                    entity_data = entity_model(
                         m_team="mastodon_scraper",
                         m_scrap_file=self.__class__.__name__,
                         m_username=[self._username],
                     )
                    self.append_leak_data(card, entity_data)

                self._is_crawled = True
                log.g().i(f"[Scraper] Full execution completed for class {self.__class__.__name__}")

        except Exception as ex:
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
            raise