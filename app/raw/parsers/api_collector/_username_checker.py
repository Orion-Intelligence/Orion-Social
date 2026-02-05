from abc import ABC
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from crawler.crawler_instance.local_interface_model.api.api_collector_interface import api_collector_interface
from crawler.crawler_instance.local_interface_model.api.api_data_model import api_data_model
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.leak_model import leak_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.shared.helper_method import helper_method


class _username_checker(api_collector_interface, ABC):
    _instance = None

    SOCIAL_URLS = [
        "facebook.com/x",
        "instagram.com/x",
        "tiktok.com/x",
        "twitter.com/x",
        "x.com/x",
        "youtube.com/x",
        "whatsapp.com/x",
        "t.me/x",
        "snapchat.com/x",
        "wechat.com/x",
        "qq.com/x",
        "douyin.com/x",
        "weibo.com/x",
        "kuaishou.com/x",
        "bilibili.com/x",
        "zhihu.com/people/x",
        "reddit.com/user/x",
        "pinterest.com/x",
        "linkedin.com/in/x",
        "tumblr.com/x",
        "vimeo.com/x",
        "twitch.tv/x",
        "quora.com/profile/x",
        "medium.com/@x",
        "flickr.com/x",
        "signal.org/x",
        "skype.com/x",
        "clubhouse.com/@x",
        "mastodon.social/@x",
        "bluesky.social/profile/x",
        "dribbble.com/x",
        "behance.net/x",
        "vk.com/x",
    ]

    _NOT_FOUND_PHRASES = tuple(
        s.lower()
        for s in [
            "404",
            "Couldn't find this page",
            "This account doesn’t exist",
            "Try searching for another.",
            "This page isn't available. Sorry about that.",
            "Try searching for something else.",
            "This page doesn't exist.",
            "This site can’t be reached",
            "Sorry, This content was not found",
            "This www.wechat.com page can’t be found",
            "The page is gone",
            "Sorry, the page you specified cannot be accessed",
            "This account has been banned",
            "Page not found",
            "Sorry, we couldn’t find that page",
            "is offline",
            "hasn't shared, answered or posted anything yet.",
            "hasn't written any stories yet.",
            "The requested page could not be found.",
            "Uh-oh! The profile you’re trying to view isn’t public yet.",
            "The page you are looking for isn't here.",
            "Oops! We can’t find that page.",
            "Invalid Invalid",
            "The invite may be invalid or you might not have permission to join"
            "not found",
            "doesn't exist",
            "page not available",
            "page isn’t available",
            "user does not exist",
            "sorry, this page isn't available",
            "couldn’t find",
            "does not exist",
            "page doesn't exist",
            "we couldn't find",
            "sorry, this page isn't available.",
            "sorry, this account does not exist",
        ]
    )

    _LOGIN_SIGNUP_KEYWORDS = (
        "login", "sign up", "signup", "register", "log in", "create account", "sign-in", "sign in"
    )

    def __init__(self):
        self._card_data: List[leak_model] = []
        self._entity_data: List[entity_model] = []
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (compatible; UsernameCheckerBot/1.0)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_username_checker, cls).__new__(cls)
        return cls._instance

    @property
    def developer_signature(self) -> str:
        return "Muhammad Hassan Arshad: owEBeAKH/ZANAwAKAbKjqaChU0IoAcsxYgBoei5jVmVyaWZpZWQgZGV2ZWxvcGVyOiBNdWhhbW1hZCBIYXNzYW4gQXJzaGFkCokCMwQAAQoAHRYhBD5p3c9aqX5fJ9SIZbKjqaChU0IoBQJoei5jAAoJELKjqaChU0Io2i8QAKRGGxAbMJGV97ym5wcir4mn2es2/npd+MFDa/LZFnkcoPOP9/fKtg9pZ1a2PVa0h9s5ewU6wGJ4HIvjP/2gxd1maDIjv6IM+5mtlpJvQJhzoqHdAg//IRwJU5QO2krqxBQrtcvNwfkW1IoNSEaJCr0EmXht3rkGhkJ3J3XqEvrBeH0DtaZLnCLOJ3eTIRleqbBOUdq2Uf9hDZZY9rdqynjjsADo1lhchdyPjwBz1g8M/q1Ud3sTUA+/8gas5l15jR9SGQZxbgnzZRjG19oq5GAhLwUYgKuoH+zANQEB7leF9jBudzYz2Ey/4BglnVE6kszUo7RxPoqtNOFvq6WzCcRKPLO323sLfFYtwXDwvJ0iviVTOwrbXlA80GFANcAbSR76nN0XrsaLM2L/KT6oe0wTVq35j1QZnt4Jq5PWALA8hQNr7w1KtuwnpN5PmE741h+9OfZP2ogd9ERbmGb10DROsd9t4RL4hpxpsCoekHRbLI3XmHFZqFAB/GgF194Tmh3LcoIAcwOYty/PVDuPYMGMmm5Nttg2vvVrMg82P0LeOrIN2Mq03HCiZm/HaOvePniPg+EeaWPMiVmGWvCJUOMI/TJRz4jVLR4BUlvoiUSNBWrJhxMRQZpViam2rVUaojPaZhzoIF4sqS6hYqzZbbXHwtYjJfNOHh00gucABJHw=gmDH"

    @property
    def base_url(self) -> str:
        return "https://socialusernamehunter.com"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(m_fetch_proxy=FetchProxy.NONE, m_fetch_config=FetchConfig.PLAYRIGHT, m_threat_type=ThreatType.API)

    @property
    def card_data(self) -> List[leak_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def append_leak_data(self, leak: leak_model, entity: entity_model):
        self._card_data.append(leak)
        self._entity_data.append(entity)

    @staticmethod
    def _make_url(url_pattern: str, username: str) -> str:
        if url_pattern.startswith("http"):
            pattern = url_pattern
        else:
            pattern = "https://" + url_pattern
        if "/x" in pattern:
            return pattern.replace("/x", f"/{username}")
        if "@x" in pattern:
            return pattern.replace("@x", f"@{username}")
        if pattern.endswith("x"):
            return pattern[:-1] + username
        return pattern

    @staticmethod
    def _extract_base_url(url_pattern: str) -> str:
        if url_pattern.startswith("http"):
            url_pattern = url_pattern.replace("https://", "")
        base = url_pattern.split("/")[0]
        return f"https://{base}"

    def _check_profile(self, url_pattern: str, username: str, timeout: int = 8) -> dict:
        profile_url = self._make_url(url_pattern, username)
        try:
            r = self._session.head(profile_url, timeout=timeout, allow_redirects=True)
            code = r.status_code
            if code == 404 or code in (301, 302, 303, 307, 308) or code not in (200,):
                return {}
            g = self._session.get(profile_url, timeout=timeout, allow_redirects=True)
            if g.status_code != 200:
                return {}
            content_lower = g.text.lower()
            for phrase in self._NOT_FOUND_PHRASES:
                if "some name" in phrase:
                    phrase_variants = [
                        phrase,
                        phrase.replace("some name", username),
                        phrase.replace("some name", username.lower()),
                        phrase.replace("some name", username.capitalize()),
                    ]
                    if any(p in content_lower for p in phrase_variants):
                        return {}
                else:
                    if phrase in content_lower:
                        return {}
            final_url = g.url.lower()
            if any(kw in final_url for kw in self._LOGIN_SIGNUP_KEYWORDS):
                return {}
            if any(kw in content_lower for kw in self._LOGIN_SIGNUP_KEYWORDS):
                return {}
            if username.lower() not in final_url:
                return {}
            return {"platform_url": profile_url, "base_url": self._extract_base_url(url_pattern)}
        except Exception:
            try:
                g = self._session.get(profile_url, timeout=timeout, allow_redirects=True)
                if g.status_code != 200:
                    return {}
                content_lower = g.text.lower()
                for phrase in self._NOT_FOUND_PHRASES:
                    if "some name" in phrase:
                        phrase_variants = [
                            phrase,
                            phrase.replace("some name", username),
                            phrase.replace("some name", username.lower()),
                            phrase.replace("some name", username.capitalize()),
                        ]
                        if any(p in content_lower for p in phrase_variants):
                            return {}
                    else:
                        if phrase in content_lower:
                            return {}
                final_url = g.url.lower()
                if any(kw in final_url for kw in self._LOGIN_SIGNUP_KEYWORDS):
                    return {}
                if any(kw in content_lower for kw in self._LOGIN_SIGNUP_KEYWORDS):
                    return {}
                if username.lower() not in final_url:
                    return {}
                return {"platform_url": profile_url, "base_url": self._extract_base_url(url_pattern)}
            except Exception:
                return {}

    async def parse_leak_data(self, query: Dict[str, str], context=None):
        username = query.get("username")
        if not username:
            return api_data_model(base_url=self.base_url, content_type=["username"])

        found_cards: List[leak_model] = []
        found_entities: List[entity_model] = []

        urls_to_check = self.SOCIAL_URLS
        max_workers = 15

        futures = {}
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            for urlp in urls_to_check:
                log.g().i(f"[CHECKING] {self._make_url(urlp, username)}")
                fut = ex.submit(self._check_profile, urlp, username)
                futures[fut] = urlp
            for fut in as_completed(futures):
                profile = fut.result()
                if profile:
                    log.g().i(f"[FOUND] {profile['platform_url']}")
                    card = leak_model(
                        m_title=f"User {username} found on {profile['base_url']}",
                        m_url=profile["platform_url"],
                        m_base_url=profile["base_url"],
                        m_screenshot="",
                        m_content="",
                        m_important_content=f"Found on: {profile['platform_url']}",
                        m_network=helper_method.get_network_type(profile["base_url"]),
                        m_content_type=["stolen"],
                        m_weblink=[profile["platform_url"]],
                        m_dumplink=[profile["platform_url"]],
                    )
                    entity = entity_model(m_email=[], m_name=username)
                    found_cards.append(card)
                    found_entities.append(entity)

        self._card_data.extend(found_cards)
        self._entity_data.extend(found_entities)

        model = api_data_model(base_url=self.base_url, content_type=["username"])
        model.cards_data = self.card_data
        return model