from abc import ABC
from datetime import datetime
from typing import List
import html
import json
import random
import re
from urllib import parse as urlparse, request as urlrequest

from crawler.crawler_instance.genbot_service.helpers.mastodon.mastodon_helper_methods import MastodonHelperMethods
from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_comment_model, social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method


class _mastodon(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self._initialized = None
        self.m_seed_url = "https://mastodon.social/@falconfeedsio/"
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._helper_methods = MastodonHelperMethods()

    def init_callback(self, callback=None):
        self.callback = callback

    def __new__(cls):
        return super().__new__(cls)

    @property
    def is_crawled(self) -> bool:
        return self._is_crawled

    @property
    def seed_url(self) -> str:
        return self.m_seed_url

    @property
    def developer_signature(self) -> str:
        return "Muhammad Hannan Zahid:mQINBGmAm/8BEAC77RE+8Q6kBAb6dO549O0nE/GQ9RL0n7w8e9zuOsl4olq/PlFCxMG0qvchqhpEjnF/hKGyvBlwduICpbVKfK5dTLa8juq9pSRNpBiM9jCxvEOBrCAiQqaShA4QKGAHdk17OJMMxoK65SmOrUirkRgCb9atXiM1YW7mcKFB/opDzfmvlA6du6jgZ8JZ9GSZ5bM35mXGiVuEVaVb0X5M+c3hgZG4qpEckPJCOohxyYg6JW2WPfnE+6UVSG75EYyM0USLmBPoBgJD/X6+CQxhyroLwIrhHyb4oGy/yOcgv9jju/588sDRSvh9Jlx5UZ/twX/GNH7yUTVtyuZoku2/41G3FHesQleahmCCe0S21Jy0ojYLMsDU8fWWqzVoZrhcVcYfvUtFwJdpBnJSZpvkqy4WiLErngIq6iDCZ4J4XzKMda8QHLMTkCD69Pks8ZA1kE23PLT+n31IQj9OboTt6xB5ZpPR1wbhjdmA6pBzfopo5gMpIUgewjNoUYkjbpS0Qrm0A58OeLbLFHQx3XaWNzfrTv7HYdBUH6LAwfBCRUOsZggiVie6cK7xz/3nj8pAAzsbySbIFAtlSl+hCM34jipiaHrof+tVup/HcX0pos9LgLhHmllgE6zQaDerDEHp3OoM0k57INdH9bEIUSxt6FKvg2LhOJvii2mFd0SCm2f7ywARAQABtEdNdWhhbW1hZCBIYW5uYW4gWmFoaWQgKFdvcmsgU2lnbmF0dXJlKSA8bXVoYW1tYWRoYW5uYWFuemFoaWRAZ21haWwuY29tPokCUQQTAQoAOxYhBNEPoJJW+qDGZkeaiig7Swhg/cA3BQJpgJv/AhsDBQsJCAcCAiICBhUKCQgLAgQWAgMBAh4HAheAAAoJECg7Swhg/cA3ZHcQALlYjcK1hJK83iGCNavwlfsKM87XjqMqXvZvDhwFyGN45lwMnkisglpi4psnD7TgfOe/ksg4EUqC4wgu2QLbmp2YxPBVWE2rSv5N2eg6hTFNpaJdhUbW4njiPrY7AB9c8Cmy3sRv1w844fduZ9lZWEEAM5Rb/x5oUo42+8FUTDGLpf5MU1HWqBg4bzc+kQ6JkDtWn87oaaHNkJiOhgQnYbtnrc/+etCSruSD2IhmCR0pnq+MbxImIs9jtDaO/xGEaAGsTr7AG80sv4vbuWXo4/Tj1A9RqEHDwU4qkeXNq6LdtHelnHO4emuHFl7pao6DR1qFayu9rNIQq8bDVROfSsG6CHo5uKfeTem0130z3TAfrkbRzspj0V0zVZl0riQpDNu2dD68I65fmDuy5d2aVpfApmCv90grvQdYXfctDX9jdUPEQ6YmXmLQ8ZUgcLKgouYpLJvstYI88UIgHm5P8CpkvzbPAFl3dgFoFSJz9UnFUVVN6K4Ab1mTScuaYBtu8mOi+Nc+brys6r9CeF2tdTaa/2mAAYjyJhYQAKFCMyiFI8YeWkVRbgZaBPh45WMVcxkCQhx1f5bWmhnl7HN+k4ID4YGkpajqx4XyoXDP0n+Y0GUylVBbe6YYfCHPr+kWuItUY5uLsBF4Y3QD69r3aIVGtvafbyrYUNlvIKVsy/DDuQINBGmAm/8BEADbd5EDSsdaARByKE/VXdBsf1s+7mnR3YPx6rEr1vq7oH9We/d/hyQWzxF3A8YH1NF4MRXmlSUtFTzg170D4+gy3vBSegJwFL6//ZBUx5lZWxC/J2fJMD3SaskHTiyYztAdVtRGqMOl0OkOTBY53jKf4HXhv7jOg5McGs9ve5RvnGQyBRQmeSh3L+IhLOGm6bQ84jGXauCdsbzsFEnaOH7yExymkHAX3qCXaeP1i3HHBYJEzWjDCAF4d4BNSfCcmhFunaqKRn0+/qfqqVeZBvwjZV1B0YQOi25ouV84dpEeIUu6F/ppwAxnZixB2SB40VhZpXEn9W7kB9paNG92FYHfkckKfXFvmE/6F474+VTVGd4Dg3SWUws/BLWSWmEJL+KwN8QlKeEGha5silhk3jRH80+7A4DKcy2T7W1q4GWdDXqJPNO/9fO3EWPrTL4o6EisBRCOM71eNtevAekauiyWTuBINnrICAAeh/pErivYnnxvGaI5mHT7tCm36/LXKVDJQly+bEyxI/ChJ4zEQlhwcS4PE8tFR0VLW2swIJpOdP9VQEL6dRbTQKkRe8y2fL8NKobLPjFgnKLp5U/SdAl6WHwlOEm42j+DVNKNMY05ttFu6BIfjCUkqC0uS8rqSxCl5Bw+Bfxduo3lIZPY/047DBJQ2EXQ7T2D3Sd72xy4IwARAQABiQI2BBgBCgAgFiEE0Q+gklb6oMZmR5qKKDtLCGD9wDcFAmmAm/8CGwwACgkQKDtLCGD9wDfPShAAijNQZlVmtxmiEvsgkSq9JGejpDOp271Ga7fbgw9wIopVjCpxHC+JTKoPSe7Athm+tCwYnPj9pui99WMyIFrAn0YP8zaKKvFTGuaRHInCcZjE1MLszLm835jrIPcDBkSmJZf4uLAI3J/H4aGXCgdbCfRiRlPMZi0OMdtSyikz5hSAg+tpMjai3xFsi+jvrfF3Uje+5Ri6pCIW8P2Sp1mudSyeTPtm6ANeSl0f6yKbN8rJkr+qZImHkoRDgRKPPFxpk1tzvOw8qSQP1Z+8YEOXdUeOWmsN1THaN1p2XUTTobtiuDYAf2+RzsRsXnCq00BJN+2h4axGi8lBYoz7b4DPeWBytSuXbq9TUL+CCupRXkHV7ihS509ARRhzV1PICxHlJdjMHUEhE1OTQDZ8WZXgKPZjsD52O5sSYHppM5mUWiTJ53R0Hgq1WbRIh2XbxWhRqrckL49ZDSe9Z/hPw4PqumTKHPiHVBkJRj9btvkhzrNizRbs7Bb4yP5tC9ioElnIjCX7Ndw+QgyEmx4be5vgbmARnKHqsy3uy3mpZqqk6qiI69bOkBd7t13ZmTahrHnktN59GrSVTu5qRWHeeZdktCbOuL9eb9XPBHj/U6Mo737xCLFqjBdIH4pYfTv5OHfDA1Tvw3dZkA9bsa5L70bnvVTGPcQDxRVOKto5E55cP6g==hOii"

    @property
    def base_url(self) -> str:
        return "https://mastodon.social"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.NONE,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_threat_type=ThreatType.MASTODON,
            m_rule_type=RuleType.MASTODON,
            m_social_data_type=getattr(self, "m_social_data_type", SocialDataType.DEFAULT),
            m_resoource_block=False,
        )

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def invoke_db(self, command: int, key: str, default_value, expiry: int | None = None):
        return self._redis_instance.invoke_trigger(command, [key + self.__class__.__name__, default_value, expiry])

    def contact_page(self) -> str:
        return self.seed_url

    @staticmethod
    def _first_media(post: dict) -> str | None:
        media = post.get("media") or []
        if isinstance(media, list):
            for item in media:
                if item:
                    return str(item)
        return None

    def _comment_limit(self) -> int:
        try:
            return max(1, min(int(getattr(self, "m_comment_limit", 10) or 10), 10))
        except Exception:
            return 10

    def _comment_offset(self) -> int:
        try:
            return max(0, int(getattr(self, "m_comment_offset", 0) or 0))
        except Exception:
            return 0

    def _is_target_hash_request(self, data_type: SocialDataType) -> bool:
        return data_type == SocialDataType.COMMENTS and bool(str(getattr(self, "m_hash_id", "") or "").strip())

    def _is_requested_hash_url(self, url: str) -> bool:
        requested_hash_id = str(getattr(self, "m_hash_id", "") or "").strip()
        return bool(requested_hash_id and url and social_model.unique_identifier("mastodon", url, "", "", "") == requested_hash_id)

    def _target_account_parts(self) -> tuple[str, str]:
        split_url = urlparse.urlsplit(self.seed_url)
        base_url = f"{split_url.scheme or 'https'}://{split_url.netloc}"
        path_parts = [part for part in split_url.path.split("/") if part]
        username = ""
        for part in path_parts:
            if part.startswith("@"):
                username = part.lstrip("@")
                break
        if not username and len(path_parts) >= 2 and path_parts[0] == "users":
            username = path_parts[1]
        if not username and path_parts:
            username = path_parts[-1].lstrip("@")
        return base_url.rstrip("/"), username

    @staticmethod
    def _html_to_text(value: str | None) -> str:
        text = re.sub(r"<br\s*/?>", "\n", str(value or ""), flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        return re.sub(r"\s+", " ", html.unescape(text)).strip()

    @staticmethod
    def _parse_api_date(value: str | None):
        try:
            return datetime.fromisoformat(str(value or "").replace("Z", "+00:00")).date()
        except Exception:
            return None

    @staticmethod
    def _first_api_media(status: dict) -> str | None:
        attachments = status.get("media_attachments") or []
        if isinstance(attachments, list):
            for attachment in attachments:
                if not isinstance(attachment, dict):
                    continue
                media_url = attachment.get("preview_url") or attachment.get("url")
                if media_url:
                    return str(media_url)
        return None

    def _fetch_json(self, page, url: str):
        try:
            raw_text = page.evaluate(
                """async url => {
                    try {
                        const response = await fetch(url, {headers: {accept: 'application/json'}});
                        if (!response.ok) return '';
                        return await response.text();
                    } catch (_) {
                        return '';
                    }
                }""",
                url,
            )
            if raw_text:
                return json.loads(raw_text)
        except Exception:
            pass
        try:
            req = urlrequest.Request(
                url,
                headers={
                    "accept": "application/json",
                    "user-agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                    ),
                },
            )
            with urlrequest.urlopen(req, timeout=20) as response:
                return json.loads(response.read().decode("utf-8", errors="replace") or "{}")
        except Exception:
            return None

    def _fetch_public_account(self, page) -> dict:
        base_url, username = self._target_account_parts()
        if not base_url or not username:
            return {}
        account = self._fetch_json(
            page,
            f"{base_url}/api/v1/accounts/lookup?acct={urlparse.quote(username)}",
        )
        if not isinstance(account, dict) or not account.get("id"):
            return {}
        return account

    def _fetch_public_statuses(self, page, limit: int) -> tuple[dict, list[dict]]:
        account = self._fetch_public_account(page)
        if not account:
            return {}, []
        base_url, _ = self._target_account_parts()
        statuses = self._fetch_json(
            page,
            f"{base_url}/api/v1/accounts/{account['id']}/statuses?"
            f"limit={max(1, min(int(limit or 10), 40))}&exclude_replies=true",
        )
        if not isinstance(statuses, list):
            statuses = []
        return account, [status for status in statuses if isinstance(status, dict)]

    def _append_api_status_cards(self, account: dict, statuses: list[dict], data_type: SocialDataType) -> int:
        desired_count = max(1, min(int(getattr(self, "m_item_limit", 10) or 10), 100))
        target_hash = self._is_target_hash_request(data_type)
        appended = 0
        for status in statuses:
            source = status.get("reblog") if isinstance(status.get("reblog"), dict) else status
            status_url = helper_method.scalar_text(source.get("url")) or helper_method.scalar_text(status.get("url"))
            if target_hash and not self._is_requested_hash_url(status_url):
                continue
            if not target_hash and self._is_requested_hash_url(status_url):
                break

            status_account = source.get("account") if isinstance(source.get("account"), dict) else account
            username = (
                helper_method.scalar_text(status_account.get("acct"))
                or helper_method.scalar_text(status_account.get("username"))
                or helper_method.scalar_text(account.get("acct"))
                or helper_method.scalar_text(account.get("username"))
            )
            content = self._html_to_text(source.get("content")) or self._html_to_text(source.get("spoiler_text"))
            card_data = social_model(
                m_channel_url=self.seed_url,
                m_title=(content[:80] or helper_method.scalar_text(status_account.get("display_name")) or "Mastodon post"),
                m_sender_name=username,
                m_url=status_url,
                m_message_sharable_link=status_url,
                m_weblink=[status_url] if status_url else [],
                m_content=content,
                m_content_type=["social_collector", "mastodon_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                m_network="clearnet",
                m_date=self._parse_api_date(source.get("created_at")),
                m_message_id=helper_method.scalar_text(source.get("id")) or helper_method.scalar_text(status.get("id")),
                m_platform="mastodon",
                m_post_shares=helper_method.scalar_text(source.get("reblogs_count")),
                m_post_likes=helper_method.scalar_text(source.get("favourites_count")),
                m_likes=helper_method.scalar_text(source.get("favourites_count")),
                m_retweets=helper_method.scalar_text(source.get("reblogs_count")),
                m_comment_count=helper_method.scalar_text(source.get("replies_count")),
                m_comments=[],
                m_img_src=self._first_api_media(source),
                m_group_name=username,
                m_scrap_file=self.__class__.__name__,
            )
            if target_hash:
                if self._is_requested_hash_id(card_data):
                    self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))
                return len(self._card_data)
            self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))
            appended += 1
            if appended >= desired_count:
                break
        return appended

    def _collect_comments_from_post(self, page, post_url: str, root_post_id: str | None, limit: int, offset: int) -> list[social_comment_model]:
        if not post_url:
            return []
        limit = max(1, min(int(limit or 10), 10))
        offset = max(0, int(offset or 0))
        target_count = offset + limit
        comments: list[social_comment_model] = []
        seen = set()

        try:
            page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(random.randint(1000, 2000))
        except Exception:
            return []

        idle_rounds = 0
        for _ in range(12):
            try:
                rows = page.evaluate("""rootId => Array.from(document.querySelectorAll('article[data-id]')).map(article => {
                    const id = article.getAttribute('data-id') || '';
                    if (rootId && id === rootId) return null;
                    const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                    const username = clean(article.querySelector('.display-name__account')?.innerText || article.querySelector('.display-name__html')?.innerText || '');
                    const text = clean(article.querySelector('.status__content__text, .status__content')?.innerText || '');
                    const time = article.querySelector('time')?.getAttribute('datetime') || clean(article.querySelector('time')?.innerText || '');
                    const favourites = clean(article.querySelector('.detailed-status__favorites, button:has(svg.icon-star) .icon-button__counter')?.innerText || '');
                    return text ? {id, username, text, time, favourites} : null;
                }).filter(Boolean)""", root_post_id or "")
            except Exception:
                rows = []

            before_count = len(comments)
            for row in rows:
                text = helper_method.scalar_text(row.get("text"))
                if not text:
                    continue
                key = "|".join([
                    helper_method.scalar_text(row.get("username")),
                    helper_method.scalar_text(row.get("time")),
                    text,
                ])
                if key in seen:
                    continue
                seen.add(key)
                comments.append(
                    social_comment_model(
                        m_username=helper_method.scalar_text(row.get("username")) or None,
                        m_time=helper_method.scalar_text(row.get("time")) or None,
                        m_likes=helper_method.scalar_text(row.get("favourites")) or None,
                        m_text=text,
                    )
                )
                if len(comments) >= target_count:
                    return comments[offset:target_count]

            idle_rounds = idle_rounds + 1 if len(comments) == before_count else 0
            if idle_rounds >= 4:
                break
            try:
                page.evaluate("""() => {
                    for (const button of document.querySelectorAll('button')) {
                        const text = (button.innerText || '').toLowerCase();
                        if (text.includes('show more') || text.includes('load more')) {
                            try { button.click(); } catch (e) {}
                        }
                    }
                    window.scrollBy(0, 2500);
                }""")
                page.wait_for_timeout(750)
            except Exception:
                break
        return comments[offset:target_count]

    @staticmethod
    def _extract_profile_assets(page) -> dict:
        try:
            return page.evaluate("""() => {
                const cleanUrl = value => {
                    if (!value) return '';
                    const match = String(value).match(/url\\(["']?([^"')]+)["']?\\)/);
                    const raw = match ? match[1] : String(value);
                    if (!raw || raw.startsWith('data:') || /^(none|initial|inherit|unset)$/i.test(raw.trim())) return '';
                    try { return new URL(raw, location.href).href; } catch (_) { return raw; }
                };
                const firstAttr = (selectors, attr) => {
                    for (const selector of selectors) {
                        const node = document.querySelector(selector);
                        const value = node?.getAttribute(attr) || node?.[attr] || '';
                        const url = cleanUrl(value);
                        if (url) return url;
                    }
                    return '';
                };
                const bgUrl = selectors => {
                    for (const selector of selectors) {
                        const node = document.querySelector(selector);
                        if (!node) continue;
                        const url = cleanUrl(getComputedStyle(node).backgroundImage);
                        if (url) return url;
                    }
                    return '';
                };
                const firstText = selectors => {
                    for (const selector of selectors) {
                        const text = document.querySelector(selector)?.innerText?.trim() || '';
                        if (text) return text;
                    }
                    return '';
                };
                const profileIcon = firstAttr([
                    '.account__avatar img',
                    '.account__header__avatar img',
                    '.account__avatar-overlay-base img',
                    'meta[property="og:image"]',
                    'meta[name="twitter:image"]'
                ], 'src') || firstAttr([
                    'meta[property="og:image"]',
                    'meta[name="twitter:image"]'
                ], 'content');
                const coverpage = firstAttr([
                    '.account__header__image img',
                    '.account__header__image picture img'
                ], 'src') || bgUrl(['.account__header__image', '.account__header']);
                const displayName = firstText(['.account__header__tabs__name h1', '.display-name__html']);
                const bio = firstText(['.account__header__content', '.account__header__fields']);
                return {profileIcon, coverpage, displayName, bio};
            }""") or {}
        except Exception:
            return {}

    def _append_profile_info(self, profile_info: dict, profile_assets: dict | None = None, data_type: SocialDataType = SocialDataType.PROFILE):
        profile_assets = profile_assets or {}
        username = helper_method.scalar_text(profile_info.get("username"))
        display_name = helper_method.scalar_text(profile_assets.get("displayName")) or username
        content = helper_method.scalar_text(profile_assets.get("bio")) or username
        content_type = "profile_info"
        card_data = social_model(
            m_channel_url=self.seed_url,
            m_title=display_name or self.seed_url,
            m_sender_name=username or display_name,
            m_url=self.seed_url,
            m_weblink=[self.seed_url],
            m_content=content,
            m_content_type=["social_collector", "mastodon_profile", content_type],
            m_network="clearnet",
            m_date=datetime.now().date(),
            m_message_id=username or self.seed_url.rstrip("/").split("/")[-1],
            m_platform="mastodon",
            m_group_name=username,
            m_img_src=profile_assets.get("profileIcon") or None,
            m_coverpage=profile_assets.get("coverpage") or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))

    def parse_leak_data(self, page):
        self._card_data = []
        self._entity_data = []
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
        if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL, SocialDataType.FOLLOWERS, SocialDataType.FOLLOWING):
            try:
                page.wait_for_selector('.account__header, body', timeout=15000)
            except Exception:
                pass
        else:
            try:
                page.wait_for_selector('article', timeout=15000)
            except Exception:
                pass
        page.wait_for_timeout(1000)
        profile_info = self._helper_methods.get_profile_info(page)
        profile_assets = self._extract_profile_assets(page)
        if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL, SocialDataType.FOLLOWERS, SocialDataType.FOLLOWING):
            account = self._fetch_public_account(page)
            if account:
                profile_info["username"] = (
                    helper_method.scalar_text(profile_info.get("username"))
                    or helper_method.scalar_text(account.get("acct"))
                    or helper_method.scalar_text(account.get("username"))
                )
                profile_assets = dict(profile_assets or {})
                profile_assets["displayName"] = (
                    helper_method.scalar_text(profile_assets.get("displayName"))
                    or helper_method.scalar_text(account.get("display_name"))
                    or profile_info.get("username")
                )
                profile_assets["bio"] = (
                    helper_method.scalar_text(profile_assets.get("bio"))
                    or self._html_to_text(account.get("note"))
                )
                profile_assets["profileIcon"] = (
                    helper_method.scalar_text(profile_assets.get("profileIcon"))
                    or helper_method.scalar_text(account.get("avatar_static"))
                    or helper_method.scalar_text(account.get("avatar"))
                )
                header_url = helper_method.scalar_text(account.get("header_static") or account.get("header"))
                if header_url and not header_url.rstrip("/").endswith("/missing.png"):
                    profile_assets["coverpage"] = helper_method.scalar_text(profile_assets.get("coverpage")) or header_url
            self._append_profile_info(profile_info, profile_assets, data_type)
            return
        if data_type in (SocialDataType.VIDEOS, SocialDataType.SHORTS):
            return

        username = profile_info.get("username", "")
        existing_ids = set()

        desired_count = max(1, min(int(getattr(self, "m_item_limit", 10) or 10), 100))
        target_hash = self._is_target_hash_request(data_type)
        search_count = 100 if target_hash else desired_count

        if data_type != SocialDataType.COMMENTS:
            account, statuses = self._fetch_public_statuses(page, search_count)
            if statuses and self._append_api_status_cards(account, statuses, data_type):
                return

        posts = self._helper_methods.scroll_and_collect(page, username, existing_ids, search_count)
        parsed_post = []

        if not posts:
            return

        for post_id in posts:
            article = page.locator(f'article[data-id="{post_id}"]')
            article.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            post = self._helper_methods.extract_post_details(page, post_id, self.seed_url)
            try:
                title_loc = article.locator('.display-name__html')
                if title_loc.count() > 0:
                    raw_title_text = title_loc.first.inner_text()
                    title_text = raw_title_text.strip() if raw_title_text else ""
                    post['card_title'] = title_text
            except Exception as e:
                log.g().w(f"Failed to extract title for {post_id}: {e}")
            try:
                boost_detail = article.locator('.detailed-status__reblogs')
                boost_timeline = article.locator('button:has(svg.icon-retweet) .icon-button__counter')

                if boost_detail.count() > 0:
                    raw_boost_text = boost_detail.first.inner_text()
                    boost_text = raw_boost_text.strip() if raw_boost_text else ""
                    post['boosts'] = boost_text if boost_text else "0"
                elif boost_timeline.count() > 0:
                    raw_boost_text = boost_timeline.first.inner_text()
                    boost_text = raw_boost_text.strip() if raw_boost_text else ""
                    post['boosts'] = boost_text if boost_text else "0"
                else:
                    post['boosts'] = "0"
            except Exception as e:
                log.g().w(f"Failed to extract boosts for {post_id}: {e}")

            try:
                fav_detail = article.locator('.detailed-status__favorites')
                fav_timeline = article.locator('button:has(svg.icon-star) .icon-button__counter')

                if fav_detail.count() > 0:
                    raw_fav_text = fav_detail.first.inner_text()
                    fav_text = raw_fav_text.strip() if raw_fav_text else ""
                    post['favourites'] = fav_text if fav_text else "0"
                elif fav_timeline.count() > 0:
                    raw_fav_text = fav_timeline.first.inner_text()
                    fav_text = raw_fav_text.strip() if raw_fav_text else ""
                    post['favourites'] = fav_text if fav_text else "0"
                else:
                    post['favourites'] = "0"
            except Exception as e:
                log.g().w(f"Failed to extract likes for {post_id}: {e}")

            parsed_post.append(post)

        for post in parsed_post:
            try:
                page.wait_for_timeout(250)
                date_str = post.get("date", "")
                parsed_date = None
                if date_str:
                    try:
                        parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
                    except Exception:
                        continue

                if not post.get("url", ""):
                    continue

                msg_link = post.get("url", "")
                msg_sharable_link = msg_link if str(msg_link).startswith("http") else self.base_url + msg_link
                username = helper_method.scalar_text(post.get("username"))
                raw_weblinks = post.get("weblinks", [])
                weblinks = [
                    weblink for link in raw_weblinks
                    if (weblink := helper_method.scalar_text(link))
                ] if isinstance(raw_weblinks, list) else []
                load_comments = data_type == SocialDataType.COMMENTS
                structured_comments = self._collect_comments_from_post(
                    page,
                    msg_sharable_link,
                    helper_method.scalar_text(post.get("id")),
                    self._comment_limit(),
                    self._comment_offset(),
                ) if load_comments else []
                content = helper_method.scalar_text(post.get("content"))
                title = helper_method.scalar_text(post.get("card_title")) or content[:80] or "Mastodon post"

                card_data = social_model(
                    m_channel_url=self.seed_url,
                    m_title=title,
                    m_sender_name=username,
                    m_url=msg_sharable_link,
                    m_message_sharable_link=msg_sharable_link,
                    m_weblink=weblinks or [msg_sharable_link],
                    m_content=content,
                    m_content_type=["social_collector", "mastodon_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                    m_network="clearnet",
                    m_date=parsed_date,
                    m_message_id=helper_method.scalar_text(post.get("id")),
                    m_platform="mastodon",
                    m_post_shares=post.get("boosts", None),
                    m_post_likes=post.get("favourites", None),
                    m_likes=post.get("favourites", None),
                    m_retweets=post.get("boosts", None),
                    m_comment_count=str(len(structured_comments)) if load_comments else None,
                    m_comments=structured_comments,
                    m_img_src=self._first_media(post),
                    m_group_name=username,
                    m_scrap_file=self.__class__.__name__,
                )
                if target_hash:
                    if self._is_requested_hash_id(card_data):
                        self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))
                        return
                    continue
                if self._is_requested_hash_id(card_data):
                    break
                entity_data = entity_model(
                    m_username=[username] if username else [],
                )

                self.append_leak_data(card_data, entity_data)
            except Exception as ex:
                log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
