from datetime import datetime
from abc import ABC
from typing import List, Dict, Any, Optional
import random
import re

from playwright.sync_api import Page

from crawler.crawler_instance.genbot_service.helpers.twitter.tweet_helper_methods import TweetHelperMethods
from crawler.crawler_instance.local_interface_model.leak.leak_extractor_interface import leak_extractor_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.shared.helper_method import helper_method
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class _twitter(leak_extractor_interface, ABC):
    _instance = None

    def __init__(self, username: str = "", callback=None):
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self._scope = SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY
        self._username = (username or "").strip()
        self.m_seed_url = f"https://x.com/{self._username}"
        self.soup = None
        self._initialized = None
        # self.m_seed_url = "https://x.com/Arkbird_SOLG/"
        self._requested_posts_limit = None
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._helper_methods = TweetHelperMethods()

    def init_callback(self, callback=None):
        self.callback = callback

    def set_scope(self, scope: int):
        self._scope = scope

    @property
    def name(self) -> str:
        return "Twitter"

    def parse_page(self, page) -> dict:
        self._card_data = []
        self._entity_data = []
        self.parse_leak_data(page)
        return {
            "username": self._username,
            "profile_url": self.seed_url,
            "platform": "twitter",
            "cards": [card.model_dump(mode="json") for card in self._card_data],
            "entities": [entity.model_dump(mode="json") for entity in self._entity_data],
            "followers": [],
            "following": [],
            "mutual": [],
        }

    def scrape_posts(self, page, max_posts: int = 5):
        self._requested_posts_limit = max_posts
        self.set_scope(SOCIAL_REQUEST_COMMANDS.S_POSTS)
        data = self.parse_page(page)
        return data.get("cards", [])[:max_posts]

    def scrape_videos(self, page, max_videos: int = 5):
        return []

    def scrape_shorts(self, page, max_shorts: int = 5):
        return []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(_twitter, cls).__new__(cls)
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
        return "https://www.x.com"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(m_fetch_proxy=FetchProxy.NONE, m_fetch_config=FetchConfig.PLAYRIGHT, m_threat_type=ThreatType.TWITTER, m_rule_type=RuleType.TWITTER, m_resoource_block=False)

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def invoke_db(self, command: int, key: str, default_value, expiry: int = None):
        return self._redis_instance.invoke_trigger(command, [key + self.__class__.__name__, default_value, expiry])

    def contact_page(self) -> str:
        return "https://x.com/contact"

    def append_leak_data(self, leak: social_model, entity: entity_model):
        self._card_data.append(leak)
        self._entity_data.append(entity)
        if self.callback:
            if self.callback():
                self._card_data.clear()
                self._entity_data.clear()

    @staticmethod
    def safe_find(page, selector, attr=None):
        try:
            element = page.query_selector(selector)
            if element:
                return element.get_attribute(attr) if attr else element.inner_text().strip()
        except Exception:
            return None

    @staticmethod
    def _parse_iso(s):
        if not s:
            return None
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return helper_method.parse_date(s)

    def surface_info(self, page: Page, username: str) -> Optional[Dict[str, Any]]:
        try:
            page.wait_for_selector('a:has-text("Followers")', timeout=15000)
            page.wait_for_timeout(2000)
        except Exception:
            log.g().w("[Scraper] Profile elements not found within timeout. Continuing with limited data.")

        real_name = username
        try:
            rn_loc = page.locator('div[class*="text-headline1"], div[class*="text-headline2"]').first
            if rn_loc.count() > 0:
                real_name = rn_loc.inner_text().strip()
        except Exception as e:
            log.g().w(f"Failed to extract real name: {e}")

        total_posts = "0"
        try:
            posts_loc = page.locator('text=/[0-9.,KM]+\\s*posts/i').first
            if posts_loc.count() > 0:
                match = re.search(r'([0-9.,KM]+)\s*posts', posts_loc.inner_text(), re.IGNORECASE)
                if match:
                    total_posts = match.group(1).replace(',', '')
        except Exception:
            pass

        background_photo = "None"
        try:
            bg_loc = page.locator('a[href$="/header_photo"] img').first
            if bg_loc.count() > 0:
                background_photo = bg_loc.get_attribute("src") or "None"
        except Exception:
            pass

        profile_photo = "None"
        try:
            pfp_loc = page.locator('a[href$="/photo"] img').first
            if pfp_loc.count() > 0:
                profile_photo = pfp_loc.get_attribute("src") or "None"
        except Exception:
            pass

        bio = ""
        try:
            bio_loc = page.locator('div[dir="auto"][class*="text-body"]').first
            if bio_loc.count() > 0:
                bio = bio_loc.inner_text().strip()
        except Exception:
            pass

        join_date = ""
        try:
            jd_texts = page.locator('div:has-text("Joined ")').all_inner_texts()
            for text in jd_texts:
                if "Joined" in text:
                    match = re.search(r'Joined\s+([A-Za-z]+\s+\d{4})', text)
                    if match:
                        join_date = match.group(1).strip()
                        break
        except Exception:
            pass

        following = "0"
        try:
            fwing_loc = page.locator('a:has-text("Following")').first
            if fwing_loc.count() > 0:
                text = fwing_loc.inner_text()
                match = re.search(r'([0-9.,KM]+)\s*Following', text, re.IGNORECASE)
                if match:
                    following = match.group(1).replace(',', '')
        except Exception as e:
            log.g().w(f"Failed to extract following: {e}")

        followers = "0"
        try:
            fwers_loc = page.locator('a:has-text("Followers")').first
            if fwers_loc.count() > 0:
                text = fwers_loc.inner_text()
                match = re.search(r'([0-9.,KM]+)\s*Followers', text, re.IGNORECASE)
                if match:
                    followers = match.group(1).replace(',', '')
        except Exception as e:
            log.g().w(f"Failed to extract followers: {e}")

        formatted_info = f"Bio: {bio}".strip()

        return {
            "username": username,
            "target_url": self.seed_url,
            "real_name": real_name,
            "total_posts": total_posts,
            "background_photo": background_photo,
            "profile_photo": profile_photo,
            "formatted_info": formatted_info,
            "following": following,
            "followers": followers,
            "join_date": join_date
        }

    def heavy_content(self, page: Page, username: str, desired_count: int) -> List[social_model]:
        collected_cards = {}
        stagnant_count = 0

        log.g().i(f"[Scraper] Starting Virtual DOM traversal for {desired_count} tweets...")

        while len(collected_cards) < desired_count:
            try:
                page.wait_for_selector('article[data-tweet-id]', timeout=15000)
            except Exception:
                log.g().w("[Scraper] No tweets found on the timeline. The page might be login-walled.")
                break

            articles = page.locator('article[data-tweet-id]').all()
            new_additions = 0

            for article in articles:
                if len(collected_cards) >= desired_count:
                    break

                try:
                    tweet_id = article.get_attribute("data-tweet-id")

                    if not tweet_id or tweet_id in collected_cards:
                        continue

                    tweet_url = f"https://x.com/{username}/status/{tweet_id}"

                    parsed_date = None
                    time_el = article.locator('time').first
                    if time_el.count() > 0:
                        date_str = time_el.get_attribute('datetime')
                        if date_str:
                            dt_obj = self._parse_iso(date_str)
                            if dt_obj:
                                try:
                                    parsed_date = dt_obj.date()
                                except AttributeError:
                                    parsed_date = dt_obj

                    if not parsed_date:
                        date_el = article.locator(f'a[href$="/status/{tweet_id}"]').first
                        if date_el.count() > 0:
                            date_str = date_el.inner_text().strip()
                            if date_str:
                                dt_obj = helper_method.parse_date(date_str)
                                if dt_obj:
                                    try:
                                        parsed_date = dt_obj.date()
                                    except AttributeError:
                                        parsed_date = dt_obj

                    content_parts = []
                    for block in article.locator('div[dir="auto"]').all():
                        text = block.inner_text().strip()
                        if text and text not in content_parts:
                            content_parts.append(text)
                    content = "\n".join(content_parts)

                    def get_metric(icon_attr):
                        try:
                            icon = article.locator(f'svg[data-icon="{icon_attr}"]').first
                            if icon.count() > 0:
                                group = icon.locator('xpath=ancestor::span[contains(@class, "group")]').first
                                if group.count() > 0:
                                    for el in group.locator('[aria-label]').all():
                                        val = el.get_attribute('aria-label')
                                        if val and val.replace(',', '').isdigit():
                                            return val.replace(',', '')
                        except Exception:
                            pass
                        return "0"

                    replies = get_metric("icon-reply-stroke")
                    retweets = get_metric("icon-retweet-stroke")
                    likes = get_metric("icon-heart-stroke")
                    views = get_metric("icon-bar-chart")

                    weblinks = []
                    for a in article.locator('a[href^="http"]').all():
                        hr = a.get_attribute("href")
                        if hr and hr not in weblinks and "twimg.com" not in hr and "x.com" not in hr:
                            weblinks.append(hr)

                    card_data = social_model(
                        m_title=content,
                        m_channel_url=self.seed_url,
                        m_sender_name=f"@{username}",
                        m_message_sharable_link=tweet_url,
                        m_weblink=weblinks,
                        m_content=content,
                        m_content_type=["social_collector"],
                        m_network="clearnet",
                        m_message_date=parsed_date,
                        m_message_id=tweet_id,
                        m_platform="twitter",
                        m_likes=likes,
                        m_comment_count=replies,
                        m_retweets=retweets,
                        m_views=views,
                    )

                    collected_cards[tweet_id] = card_data
                    new_additions += 1

                    page.wait_for_timeout(random.randint(150, 650))

                except Exception as e:
                    log.g().w(f"[Scraper] Error parsing individual tweet ID {tweet_id}: {e}")

            if new_additions == 0:
                stagnant_count += 1
                if stagnant_count >= 5:
                    log.g().i("[Scraper] No new tweets appearing. Ending collection.")
                    break
            else:
                stagnant_count = 0

            page.evaluate("window.scrollBy(0, 1500);")
            page.wait_for_timeout(1500)

        log.g().i(f"[Scraper] Successfully extracted {len(collected_cards)} tweets.")
        return list(collected_cards.values())

    def parse_leak_data(self, page: Page):
        try:
            log.g().i(f"[Scraper] Initializing session on {self.m_seed_url}")
            page.goto(self.m_seed_url, wait_until="domcontentloaded")

            page.wait_for_timeout(random.randint(500, 1500))

            username = self._helper_methods.extract_username(self.seed_url)
            if not username:
                username = self.seed_url.rstrip('/').split('/')[-1].split('?')[0]

            if self._scope == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY:
                log.g().i("[Scraper] Info Mode: TRUE. Extracting Surface Profile...")
                surface = self.surface_info(page, username)

                if surface:
                    parsed_join_date = None
                    if surface.get("join_date"):
                        try:
                            parsed_join_date = datetime.strptime(surface["join_date"], "%B %Y").date()
                        except Exception:
                            pass

                    surface_card = social_model(
                        m_title=f"@{surface['username']}",
                        m_sender_name=surface.get("real_name", surface["username"]),
                        m_message_sharable_link=surface['target_url'],
                        m_network="clearnet",
                        m_bio=surface.get("formatted_info", ""),
                        m_content_type=["user_profile"],
                        m_platform="twitter",
                        m_group_info=surface.get("formatted_info", ""),
                        m_followers=surface.get("followers", "0"),
                        m_following=surface.get("following", "0"),
                        m_total_posts=surface.get("total_posts", "0"),
                        m_profile_pic=surface.get("profile_photo", "None"),
                        m_cover_pic=surface.get("background_photo", "None"),
                        m_message_date=parsed_join_date
                    )
                    self.append_leak_data(
                        surface_card,
                        entity_model(m_team="twitter_scraper", m_scrap_file=self.__class__.__name__)
                    )
                    log.g().i(f"[Scraper] Committed Surface Profile.")
                else:
                    log.g().i("[Scraper] No surface metadata to extract for Twitter target. Proceeding.")

                self._is_crawled = True
                log.g().i("[Scraper] Info Mode complete. Skipping heavy extraction.")
                return

            if self._scope == SOCIAL_REQUEST_COMMANDS.S_POSTS:

                 desired_count = self._requested_posts_limit or (10 if self.is_crawled else 100)
                 log.g().i("[Scraper] Deep Content Mode: TRUE. Extracting Tweets...")

                 cards = self.heavy_content(page, username, desired_count)

                 for card in cards:


                     entity_data = entity_model(
                    m_scrap_file=self.__class__.__name__,
                    m_name=username,
                     )
                     self.append_leak_data(card, entity_data)

            self._is_crawled = True
            log.g().i(f"[Scraper] Full execution completed for class {self.__class__.__name__}")

        except Exception as ex:
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
            raise