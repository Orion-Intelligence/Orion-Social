import re
from datetime import datetime
from abc import ABC
from typing import List
from collections import OrderedDict
from playwright.sync_api import Page

from crawler.crawler_instance.local_interface_model.leak.leak_extractor_interface import leak_extractor_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, \
    RuleType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class _pastebin(leak_extractor_interface, ABC):
    _instance = None

    def __init__(self, username: str = "", callback=None):

        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self._scope = SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY
        self._requested_posts_limit = None
        self._username = (username or "").strip()
        self.m_seed_url = f"https://pastebin.com/u/{self._username}"
        self._initialized = None
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._title_seen = OrderedDict()

    def init_callback(self, callback=None):
        self.callback = callback

    def set_scope(self, scope: int):
        self._scope = scope

    @property
    def name(self) -> str:
        return "Pastebin"

    def parse_page(self, page) -> dict:
        self._card_data = []
        self._entity_data = []
        self.parse_leak_data(page)
        return {
            "username": self._username,
            "profile_url": self.seed_url,
            "platform": "pastebin",
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
            cls._instance = super(_pastebin, cls).__new__(cls)
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
        return "Muhammad Huzaifa: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=OU1e"
    @property
    def base_url(self) -> str:
        return "https://pastebin.com"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(m_fetch_proxy=FetchProxy.TOR, m_fetch_config=FetchConfig.PLAYRIGHT, m_resoource_block=False, m_threat_type=ThreatType.PASTEBIN, m_rule_type=RuleType.PASTEBIN)

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:

        return self._entity_data

    def invoke_db(self, command: int, key: str, default_value, expiry: int = None):
        return self._redis_instance.invoke_trigger(command, [key + self.__class__.__name__, default_value, expiry])

    def contact_page(self) -> str:
        return "https://pastebin.com/contact"

    def append_leak_data(self, leak: social_model, entity: entity_model):

        self._card_data.append(leak)
        self._entity_data.append(entity)
        if self.callback:
            if self.callback():
                self._card_data.clear()
                self._entity_data.clear()


    def parse_leak_data(self, page: Page):
            try:
                page.goto(self.m_seed_url, wait_until="domcontentloaded")
                if self._scope == SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY:
                    data = {
                        "username": page.locator(".user-icon img").first.get_attribute("alt") or "",
                        "profile_image": page.locator(".user-icon img").first.get_attribute("src") or "",
                        "profile_title": page.locator(".info-top h1").first.inner_text().strip(),
                        "message_url": page.locator(".info-top a.message").first.get_attribute("href") or "",
                        "profile_views": page.locator("span.views").first.inner_text().strip(),
                        "total_views": page.locator("span.views.-all").first.inner_text().strip(),
                        "rating": page.locator("span.rating").first.inner_text().strip(),
                        "joined_relative": page.locator(".date-text").first.inner_text().strip(),
                        "joined_exact": page.locator(".date-text").first.get_attribute("title") or "",
                    }

                    card_data = social_model(
                        m_title=data.get("profile_title"),
                        m_sender_name=data.get("username"),
                        m_channel_url=page.url,
                        m_profile_pic=f"{self.base_url}{data.get('profile_image')}",
                        m_message_sharable_link=data.get("message_url") or page.url,
                        m_profile_views=data.get("profile_views"),
                        m_total_views=data.get("total_views"),
                        m_rating=data.get("rating"),
                        m_joined_relative=data.get("joined_relative"),
                        m_joined_exact=data.get("joined_exact"),
                        m_network=helper_method.get_network_type(self.base_url),
                        m_content_type=["user_profile"],
                        m_platform="pastebin",
                        m_message_date=None,
                    )

                    entity_data = entity_model(
                        m_scrap_file=self.__class__.__name__,
                    )

                    self.append_leak_data(card_data, entity_data)

                if self._scope == SOCIAL_REQUEST_COMMANDS.S_POSTS:

                    url_lists = []

                    links = page.locator("td:has(span) a")

                    for i in range(links.count()):

                        href = links.nth(i).get_attribute("href")
                        if href:
                          full_url = self.base_url + href
                          url_lists.append(full_url)

                    limit = self._requested_posts_limit or (2 if self._is_crawled else len(url_lists))
                    url_lists = url_lists[:limit]

                    for url in url_lists:
                        try:
                            page.goto(url, wait_until="load", timeout=25000)
                        except:
                            pass

                        title = page.locator("div.info-top").inner_text()

                        username = page.locator("div.info-bar div.info-bottom div.username a").first.inner_text()

                        raw_date = page.locator("div.info-bar div.info-bottom div.date").first.inner_text()
                        clean_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', raw_date, flags=re.IGNORECASE)
                        clean_date = re.sub(r'\(.*?\)', '', clean_date).strip()
                        clean_date = clean_date.title()
                        month = clean_date.split()[0]
                        fmt = "%b %d, %Y" if len(month) <= 3 else "%B %d, %Y"
                        date = datetime.strptime(clean_date, fmt).date()

                        tags_locator = page.locator("div.tags a")
                        if tags_locator.count():
                            tags = tags_locator.all_inner_texts()
                        else:
                            tags = []

                        visits_locator = page.locator("div.visits")
                        visits = visits_locator.inner_text().strip()

                        expire_locator = page.locator("div.expire")
                        expire = expire_locator.inner_text().strip()

                        try:
                            source = page.locator("ol.diff , .post-view ol").first.inner_text(timeout=5000)
                        except:
                            source = None

                        m_content = source.replace("\xa0", " ").strip()

                        cleaned = source.replace("\xa0", " ")
                        cleaned = re.sub(r'[ \t]+', ' ', cleaned)

                        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                        ip_pattern = r'\b\d{1,3}(?:\.\d{1,3}){3}\b'
                        domain_pattern = r'\b(?:https?://[^\s@]+|www\.[^\s@]+)'

                        emails = list(set(re.findall(email_pattern, cleaned)))
                        ips = list(set(re.findall(ip_pattern, cleaned)))
                        domains = list(set(re.findall(domain_pattern, cleaned)))

                        content_type = ["leak"]
                        if helper_method.is_code(m_content):
                            content_type.append('code')

                        card_data = social_model(
                            m_title=title,
                            m_channel_url=page.url,
                            m_message_sharable_link=page.url,
                            m_content=m_content,
                            m_network=helper_method.get_network_type(self.base_url),
                            m_content_type=content_type,
                            m_platform="pastebin",
                            m_message_date=date,
                            m_post_tags=tags,
                            m_post_views=visits,
                            m_post_expiry=expire,
                        )

                        entity_data = entity_model(
                            m_scrap_file=self.__class__.__name__,
                            m_username=[username],
                            m_ip=ips,
                            m_email=emails,
                            m_weblink=domains,
                        )

                        self.append_leak_data(card_data, entity_data)

            except Exception as ex:
                log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))

