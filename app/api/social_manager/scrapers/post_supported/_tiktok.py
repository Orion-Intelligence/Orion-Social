import re
import gzip
import json
import os
from abc import ABC
from typing import List
import asyncio
import threading
import random
from datetime import datetime, UTC
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from TikTokApi import TikTokApi

from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_comment_model, social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method


class _tiktok(extraction_interface, ABC):
    _instance = None
    MS_TOKEN_WAIT_ATTEMPTS = 12

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self._initialized = None
        self._is_crawled = False
        self.m_seed_url = "https://www.tiktok.com/@mannan_marketing"
        self._redis_instance = redis_controller()
        self._profile_metadata = {}

        self.MIN_VIEWS = 100_000
        self.MIN_LIKES = 100_000
        self.MAX_VIDEOS = 50

        self.MS_TOKEN = ""
        self._profile_user_detail = {}
        self._item_list_payloads = []
        self._profile_missing = False

    def init_callback(self, callback=None):
        self.callback = callback

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
            m_rule_type=RuleType.TIKTOK,
            m_social_data_type=getattr(self, "m_social_data_type", SocialDataType.DEFAULT),
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

    def _use_saved_session(self) -> bool:
        return bool(getattr(self, "m_use_saved_session", False))

    def _apply_saved_session(self, page) -> bool:
        page = self._page(page)
        if page is None:
            return False

        context_id = id(page.context)
        if getattr(self, "_tiktok_session_context_id", None) == context_id:
            return True

        sessions_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sessions")
        session_paths = [
            os.path.join(sessions_dir, "tiktokscraper_session.json.gz"),
            os.path.join(sessions_dir, "_tiktok_session.json.gz"),
        ]
        for session_path in session_paths:
            if not os.path.exists(session_path):
                continue
            try:
                with gzip.open(session_path, "rt", encoding="utf-8") as f:
                    state = json.load(f)
                cookies = state.get("cookies") or []
                if cookies:
                    page.context.add_cookies(cookies)
                try:
                    for key, value in (state.get("local_storage") or {}).items():
                        page.evaluate("([key, value]) => window.localStorage.setItem(key, value)", [key, value])
                    for key, value in (state.get("session_storage") or {}).items():
                        page.evaluate("([key, value]) => window.sessionStorage.setItem(key, value)", [key, value])
                except Exception:
                    pass
                self._tiktok_session_context_id = context_id
                return True
            except Exception:
                continue
        self._tiktok_session_context_id = context_id
        return False

    def _item_limit(self) -> int:
        try:
            return max(1, min(int(getattr(self, "m_item_limit", 10 if self.is_crawled else self.MAX_VIDEOS) or 10), 100))
        except Exception:
            return 10

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

    @staticmethod
    def _page(page):
        if page is None or hasattr(page, "goto"):
            return page
        return getattr(page, "page", None)

    @staticmethod
    def _video_data_types():
        return (SocialDataType.POSTS, SocialDataType.VIDEOS, SocialDataType.SHORTS, SocialDataType.COMMENTS)

    @staticmethod
    def _first_text(*values) -> str | None:
        for value in values:
            if isinstance(value, list):
                nested = _tiktok._first_text(*value)
                if nested:
                    return nested
                continue
            if isinstance(value, dict):
                nested = _tiktok._first_text(
                    value.get("url"),
                    value.get("uri"),
                    value.get("src"),
                    value.get("cover"),
                    value.get("originCover"),
                    value.get("dynamicCover"),
                )
                if nested:
                    return nested
                continue
            text = helper_method.scalar_text(value)
            if text:
                return text
        return None

    @staticmethod
    def _first_present(*values):
        for value in values:
            if value is not None:
                return value
        return None

    def _install_item_list_response_collector(self, page):
        page = self._page(page)
        self._item_list_payloads = []
        if page is None:
            return None

        def _capture(response):
            if "/api/post/item_list/" not in response.url:
                return
            try:
                raw_text = response.text()
                if not raw_text:
                    return
                payload = json.loads(raw_text)
                if isinstance(payload, dict):
                    self._item_list_payloads.append(payload)
            except Exception:
                return

        try:
            page.on("response", _capture)
            return _capture
        except Exception:
            return None

    @staticmethod
    def _looks_like_video_item(item: dict) -> bool:
        if not isinstance(item, dict):
            return False
        if not helper_method.scalar_text(item.get("id") or item.get("itemId") or item.get("aweme_id")):
            return False
        return any(key in item for key in ("desc", "stats", "statsV2", "video", "shareInfo", "music"))

    def _video_items_from_payload(self, payload: dict) -> list[dict]:
        items: list[dict] = []
        seen = set()

        def add(item):
            if not self._looks_like_video_item(item):
                return
            video_id = helper_method.scalar_text(item.get("id") or item.get("itemId") or item.get("aweme_id"))
            if not video_id or video_id in seen:
                return
            seen.add(video_id)
            items.append(item)

        direct_items = []
        if isinstance(payload, dict):
            direct_items = payload.get("itemList") or payload.get("items") or []
            item_module = payload.get("ItemModule")
            if isinstance(item_module, dict):
                direct_items = list(item_module.values()) + list(direct_items or [])
        if isinstance(direct_items, list):
            for item in direct_items:
                add(item)

        def walk(value):
            if len(items) >= self._item_limit():
                return
            if isinstance(value, dict):
                add(value)
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value[:200]:
                    walk(child)

        if not items:
            walk(payload)
        return items

    @staticmethod
    def _public_metadata_item(row: dict, username: str) -> dict:
        author_data = row.get("author") if isinstance(row.get("author"), dict) else {}
        author = (
            helper_method.scalar_text(author_data.get("unique_id"))
            or helper_method.scalar_text(author_data.get("uniqueId"))
            or username
        )
        video_id = helper_method.scalar_text(row.get("video_id") or row.get("id") or row.get("aweme_id"))
        title = helper_method.scalar_text(row.get("title") or row.get("desc"))
        if not title and isinstance(row.get("content_desc"), list):
            title = "\n".join(helper_method.scalar_text(part) or "" for part in row.get("content_desc") if helper_method.scalar_text(part))
        return {
            "id": video_id,
            "desc": title or video_id,
            "author": {"uniqueId": author},
            "stats": {
                "diggCount": _tiktok._first_present(row.get("digg_count"), row.get("like_count")),
                "commentCount": row.get("comment_count"),
                "shareCount": row.get("share_count"),
                "playCount": row.get("play_count"),
            },
            "video": {
                "cover": row.get("cover"),
                "originCover": row.get("origin_cover"),
                "dynamicCover": row.get("ai_dynamic_cover"),
            },
            "createTime": row.get("create_time"),
            "shareInfo": {"shareUrl": f"https://www.tiktok.com/@{author}/video/{video_id}" if author and video_id else ""},
        }

    @staticmethod
    def _page_has_hard_limit(page) -> bool:
        page = _tiktok._page(page)
        if page is None:
            return False
        try:
            text = page.evaluate("""() => (document.body?.innerText || '').toLowerCase()""") or ""
        except Exception:
            return False
        return "drag the slider to fit the puzzle" in text or "captcha" in text

    @staticmethod
    def _missing_account_markers() -> tuple[str, ...]:
        return (
            "couldn't find this account",
            "couldn\u2019t find this account",
            "couldn\\u2019t find this account",
            "couldn&#39;t find this account",
            "couldn&#x27;t find this account",
            "looking for videos? try browsing",
            "trending creators, hashtags, and sounds",
            "user doesn't exist",
            "user doesn\u2019t exist",
            "user-not-found",
        )

    @classmethod
    def _is_missing_account_text(cls, text: str | None) -> bool:
        value = (helper_method.scalar_text(text) or "").lower()
        if not value:
            return False
        return any(marker in value for marker in cls._missing_account_markers())

    @classmethod
    def _page_shows_missing_account(cls, page) -> bool:
        page = cls._page(page)
        if page is None:
            return False
        try:
            text = page.evaluate(
                """() => {
                    const body = document.body?.innerText || '';
                    const html = document.documentElement?.innerHTML || '';
                    return [document.title || '', body, html.slice(0, 300000)].join('\\n');
                }"""
            ) or ""
        except Exception:
            return False
        return cls._is_missing_account_text(text)

    @classmethod
    def _user_info_shows_missing_account(cls, user_info) -> bool:
        if not isinstance(user_info, dict):
            return False
        try:
            text = json.dumps(user_info, ensure_ascii=False)
        except Exception:
            text = str(user_info)
        return cls._is_missing_account_text(text)

    @staticmethod
    def _extract_profile_assets(page) -> dict:
        page = _tiktok._page(page)
        if page is None:
            return {}
        try:
            return page.evaluate("""() => {
                const cleanUrl = value => {
                    if (!value) return '';
                    const text = String(value).trim();
                    const match = text.match(/url\\(["']?([^"')]+)["']?\\)/);
                    const raw = (match ? match[1] : text).trim();
                    if (
                        !raw ||
                        raw.startsWith('data:') ||
                        /^(none|initial|inherit|unset)$/i.test(raw) ||
                        /^(linear-gradient|radial-gradient|conic-gradient|repeating-linear-gradient|repeating-radial-gradient|var|calc)\\(/i.test(raw)
                    ) return '';
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
                const profileIcon = firstAttr([
                    'meta[property="og:image"]',
                    'meta[name="twitter:image"]',
                    '[data-e2e="user-avatar"] img',
                    'img[alt*="avatar" i]',
                    'img[class*="Avatar" i]'
                ], 'content') || firstAttr([
                    '[data-e2e="user-avatar"] img',
                    'img[alt*="avatar" i]',
                    'img[class*="Avatar" i]'
                ], 'src');
                const coverpage = firstAttr([
                    '[data-e2e*="banner" i] img',
                    '[class*="banner" i] img',
                    '[class*="cover" i] img'
                ], 'src') || bgUrl([
                    '[data-e2e*="banner" i]',
                    '[class*="banner" i]',
                    '[class*="cover" i]'
                ]);
                return {profileIcon, coverpage};
            }""") or {}
        except Exception:
            return {}

    @staticmethod
    def _extract_user_detail_from_page(page) -> dict:
        page = _tiktok._page(page)
        if page is None:
            return {}
        try:
            raw_json = page.locator("script#__UNIVERSAL_DATA_FOR_REHYDRATION__").first.text_content(timeout=2000)
            payload = json.loads(raw_json or "{}")
            scope = payload.get("__DEFAULT_SCOPE__") or {}
            detail = scope.get("webapp.user-detail") or {}
            return detail if isinstance(detail, dict) else {}
        except Exception:
            return {}

    @staticmethod
    def _tiktok_count(value) -> str | None:
        try:
            return str(int(value))
        except Exception:
            return helper_method.scalar_text(value) or None

    @staticmethod
    def _stat_count(stats: dict, *keys: str) -> str | None:
        if not isinstance(stats, dict):
            return None
        for key in keys:
            if key in stats and stats.get(key) is not None:
                return _tiktok._tiktok_count(stats.get(key))
        return None

    @staticmethod
    def _tiktok_date(value):
        if not value:
            return datetime.now(UTC).date()
        try:
            return datetime.fromtimestamp(int(value), UTC).date()
        except Exception:
            return datetime.now(UTC).date()

    @staticmethod
    def _comment_time(comment) -> str | None:
        raw_time = getattr(comment, "as_dict", {}).get("create_time")
        if not raw_time:
            return None
        try:
            return datetime.fromtimestamp(int(raw_time), UTC).isoformat()
        except Exception:
            return helper_method.scalar_text(raw_time) or None

    @staticmethod
    def _comment_model(comment) -> social_comment_model | None:
        raw_text = helper_method.scalar_text(getattr(comment, "text", "") or getattr(comment, "as_dict", {}).get("text"))
        text = helper_method.filter_comments(raw_text) or raw_text
        if not text:
            return None

        author = getattr(comment, "author", None)
        raw_user = getattr(author, "username", None)
        if not raw_user:
            raw_user = (getattr(comment, "as_dict", {}).get("user") or {}).get("unique_id")

        return social_comment_model(
            m_username=helper_method.scalar_text(raw_user) or None,
            m_time=_tiktok._comment_time(comment),
            m_likes=_tiktok._tiktok_count(getattr(comment, "likes_count", None)),
            m_text=text,
        )

    async def _collect_video_comments(self, video) -> list[social_comment_model]:
        offset = self._comment_offset()
        limit = self._comment_limit()
        target_count = offset + limit
        collected: list[social_comment_model] = []
        seen = set()

        try:
            async for comment in video.comments(count=target_count, cursor=0):
                model = self._comment_model(comment)
                if not model or not model.m_text:
                    continue
                key = "|".join([model.m_username or "", model.m_time or "", model.m_text or ""])
                if key in seen:
                    continue
                seen.add(key)
                collected.append(model)
                if len(collected) >= target_count:
                    break
        except Exception as ex:
            log.g().e(f"Failed to fetch TikTok comments for video {getattr(video, 'id', '')}: {ex}")

        return collected[offset:target_count]

    def _append_video_card(self, video_url: str, video_id: str, author: str | None, content: str, likes: str | None, comments: str | None, shares: str | None, views: str | None, media_url: str | None, data_type: SocialDataType, structured_comments: list[social_comment_model] | None = None):
        structured_comments = structured_comments or []
        content_group = "tiktok_short" if data_type == SocialDataType.SHORTS else "tiktok_video"
        content_kind = data_type.value if data_type in (SocialDataType.COMMENTS, SocialDataType.VIDEOS, SocialDataType.SHORTS) else "posts"
        card_data = social_model(
            m_title=content[:80] if content else video_id,
            m_message_id=video_id,
            m_url=video_url,
            m_message_sharable_link=video_url,
            m_weblink=[video_url] if video_url else [],
            m_sender_name=author,
            m_channel_url=f"https://www.tiktok.com/@{author}" if author else self.seed_url,
            m_post_likes=likes,
            m_likes=likes,
            m_post_shares=shares,
            m_post_views=views,
            m_comment_count=str(len(structured_comments)) if data_type == SocialDataType.COMMENTS else comments,
            m_comments=structured_comments,
            m_content=content,
            m_content_type=["social_collector", content_group, content_kind],
            m_img_src=media_url,
            m_platform="tiktok",
            m_network="clearnet",
            m_post_tags=[tag.lower().strip("#") for tag in re.findall(r"#\w+", content or "")],
            m_date=datetime.now(UTC).date(),
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[author or "unknown"]))

    def _fallback_collect_videos_from_page(self, page, username: str, data_type: SocialDataType):
        page = self._page(page)
        if page is None or data_type not in self._video_data_types():
            return

        target_count = self._item_limit()
        seen = set()
        collected_rows = []
        try:
            for _ in range(6):
                rows = page.evaluate("""() => {
                    const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                    const srcsetUrl = value => String(value || '').split(',').pop().trim().split(/\\s+/)[0] || '';
                    const anchors = Array.from(document.querySelectorAll('a[href*="/video/"]'));
                    return anchors.map(anchor => {
                        const href = anchor.href || anchor.getAttribute('href') || '';
                        const img = anchor.querySelector('img');
                        const media = img?.currentSrc || img?.src || img?.getAttribute('src') || srcsetUrl(img?.getAttribute('srcset')) || '';
                        const text = clean(anchor.getAttribute('aria-label') || anchor.innerText || img?.alt || '');
                        return href ? {url: href, media, text} : null;
                    }).filter(Boolean);
                }""") or []
                for row in rows:
                    url = helper_method.scalar_text(row.get("url"))
                    if url and url not in seen:
                        seen.add(url)
                        collected_rows.append(row)
                if len(seen) >= target_count:
                    break
                page.mouse.wheel(0, random.randint(1600, 2600))
                page.wait_for_timeout(random.randint(1000, 2500))
        except Exception as ex:
            log.g().e(f"Failed TikTok Playwright fallback for {username}: {ex}")
            return

        appended = 0
        seen.clear()
        for row in collected_rows:
            if appended >= target_count:
                break
            video_url = helper_method.scalar_text(row.get("url"))
            if not video_url or video_url in seen:
                continue
            seen.add(video_url)
            match = re.search(r"/video/([^/?#]+)", video_url)
            video_id = match.group(1) if match else video_url.rstrip("/").split("/")[-1]
            content = helper_method.scalar_text(row.get("text")) or video_id
            media_url = helper_method.scalar_text(row.get("media")) or None
            self._append_video_card(
                video_url=video_url,
                video_id=video_id,
                author=username,
                content=content,
                likes=None,
                comments=None,
                shares=None,
                views=None,
                media_url=media_url,
                data_type=data_type,
            )
            appended += 1

    def _append_video_items(self, items: list[dict], username: str, data_type: SocialDataType) -> int:
        if data_type not in self._video_data_types():
            return 0

        count = self._item_limit()
        appended = 0
        existing_ids = {helper_method.scalar_text(getattr(card, "m_message_id", "")) for card in self._card_data}
        existing_urls = {helper_method.scalar_text(getattr(card, "m_url", "")) for card in self._card_data}
        for item in items:
            if appended >= count or not isinstance(item, dict):
                break
            video_id = helper_method.scalar_text(item.get("id") or item.get("itemId") or item.get("aweme_id"))
            if not video_id or video_id in existing_ids:
                continue
            author_data = item.get("author") or item.get("authorInfo") or {}
            stats = item.get("stats") or item.get("statsV2") or item.get("statistics") or {}
            video = item.get("video") or {}
            author = helper_method.scalar_text(
                author_data.get("uniqueId")
                or author_data.get("unique_id")
                or author_data.get("nickname")
            ) or username
            share_info = item.get("shareInfo") or {}
            video_url = (
                helper_method.scalar_text(share_info.get("shareUrl"))
                or helper_method.scalar_text(item.get("shareUrl"))
                or f"https://www.tiktok.com/@{author}/video/{video_id}"
            )
            if video_url in existing_urls:
                continue
            media_url = self._first_text(
                video.get("cover"),
                video.get("originCover"),
                video.get("dynamicCover"),
                video.get("coverAddr"),
                item.get("imagePost"),
            )
            self._append_video_card(
                video_url=video_url,
                video_id=video_id,
                author=author,
                content=helper_method.scalar_text(item.get("desc") or item.get("description")) or video_id,
                likes=self._tiktok_count(self._first_present(stats.get("diggCount"), stats.get("digg_count"), stats.get("likeCount"))),
                comments=self._tiktok_count(self._first_present(stats.get("commentCount"), stats.get("comment_count"))),
                shares=self._tiktok_count(self._first_present(stats.get("shareCount"), stats.get("share_count"))),
                views=self._tiktok_count(self._first_present(stats.get("playCount"), stats.get("play_count"), stats.get("viewCount"))),
                media_url=media_url,
                data_type=data_type,
            )
            self._card_data[-1].m_date = self._tiktok_date(item.get("createTime") or item.get("create_time"))
            existing_ids.add(video_id)
            existing_urls.add(video_url)
            appended += 1
        return appended

    def _fallback_collect_videos_from_payloads(self, username: str, data_type: SocialDataType):
        if data_type not in self._video_data_types():
            return
        for payload in self._item_list_payloads:
            self._append_video_items(self._video_items_from_payload(payload), username, data_type)
            if self._card_data:
                return

    def _fallback_collect_videos_from_rehydration(self, page, username: str, data_type: SocialDataType):
        page = self._page(page)
        if page is None or data_type not in self._video_data_types():
            return
        try:
            raw_json = page.locator("script#__UNIVERSAL_DATA_FOR_REHYDRATION__").first.text_content(timeout=2000)
            payload = json.loads(raw_json or "{}")
        except Exception:
            return
        self._append_video_items(self._video_items_from_payload(payload), username, data_type)

    def _fallback_collect_videos_from_item_list(self, page, username: str, data_type: SocialDataType):
        page = self._page(page)
        if page is None or data_type not in self._video_data_types():
            return

        detail = self._profile_user_detail or self._extract_user_detail_from_page(page)
        user_info = detail.get("userInfo") or {}
        user_data = user_info.get("user") or {}
        sec_uid = helper_method.scalar_text(user_data.get("secUid"))
        if not sec_uid:
            return

        count = self._item_limit()
        try:
            endpoint = (
                "https://www.tiktok.com/api/post/item_list/"
                f"?aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US"
                f"&browser_name=Mozilla&browser_online=true&browser_platform=Linux%20x86_64"
                f"&browser_version=5.0&channel=tiktok_web&count={count}&cursor=0"
                f"&device_platform=web_pc&focus_state=true&from_page=user&history_len=2"
                f"&is_fullscreen=false&is_page_visible=true&language=en&os=linux"
                f"&priority_region=&referer=&region=PK&screen_height=900&screen_width=1366"
                f"&secUid={quote(sec_uid)}&tz_name=Asia%2FKarachi&webcast_language=en"
            )
            raw_text = page.evaluate(
                """async endpoint => {
                    try {
                        const response = await fetch(endpoint, {credentials: 'include'});
                        return await response.text();
                    } catch (_) {
                        return '';
                    }
                }""",
                endpoint,
            )
            payload = json.loads(raw_text or "{}")
        except Exception as ex:
            log.g().e(f"Failed TikTok item-list fallback for {username}: {ex}")
            return

        self._append_video_items(self._video_items_from_payload(payload), username, data_type)

    def _fallback_collect_videos_from_public_metadata(self, username: str, data_type: SocialDataType):
        if data_type not in (SocialDataType.POSTS, SocialDataType.VIDEOS, SocialDataType.SHORTS):
            return

        target_count = self._item_limit()
        cursor: str | int = 0
        seen_cursors = set()
        headers = {
            "Accept": "application/json,text/plain,*/*",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }

        while len(self._card_data) < target_count:
            if str(cursor) in seen_cursors:
                break
            seen_cursors.add(str(cursor))
            try:
                query = urlencode(
                    {
                        "unique_id": username,
                        "count": min(max(target_count - len(self._card_data), 1), 35),
                        "cursor": cursor,
                    }
                )
                request = Request(f"https://www.tikwm.com/api/user/posts?{query}", headers=headers)
                with urlopen(request, timeout=20) as response:
                    raw_text = response.read(2_000_000).decode("utf-8", "replace")
                payload = json.loads(raw_text or "{}")
            except Exception as ex:
                log.g().e(f"Failed TikTok public metadata fallback for {username}: {ex}")
                return

            data = payload.get("data") if isinstance(payload, dict) else {}
            rows = data.get("videos") if isinstance(data, dict) else []
            if not isinstance(rows, list) or not rows:
                return
            items = [self._public_metadata_item(row, username) for row in rows if isinstance(row, dict)]
            before_count = len(self._card_data)
            self._append_video_items(items, username, data_type)

            next_cursor = helper_method.scalar_text(data.get("cursor") if isinstance(data, dict) else None)
            has_more = bool(isinstance(data, dict) and (data.get("hasMore") or data.get("has_more")))
            if len(self._card_data) == before_count or not has_more or not next_cursor or next_cursor == "0":
                return
            cursor = next_cursor

    def _fetch_public_profile_info(self, username: str) -> dict:
        headers = {
            "Accept": "application/json,text/plain,*/*",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }
        try:
            query = urlencode({"unique_id": username})
            request = Request(f"https://www.tikwm.com/api/user/info?{query}", headers=headers)
            with urlopen(request, timeout=20) as response:
                raw_text = response.read(1_000_000).decode("utf-8", "replace")
            payload = json.loads(raw_text or "{}")
        except Exception as ex:
            log.g().e(f"Failed TikTok public profile fallback for {username}: {ex}")
            return {}

        data = payload.get("data") if isinstance(payload, dict) else {}
        if not isinstance(data, dict):
            return {}
        info = data.get("userInfo") if isinstance(data.get("userInfo"), dict) else data
        user_data = info.get("user") if isinstance(info.get("user"), dict) else data.get("user")
        stats_data = info.get("stats") if isinstance(info.get("stats"), dict) else data.get("stats")
        if not isinstance(user_data, dict):
            user_data = data
        if not isinstance(stats_data, dict):
            stats_data = {}

        unique_id = (
            helper_method.scalar_text(user_data.get("uniqueId"))
            or helper_method.scalar_text(user_data.get("unique_id"))
            or helper_method.scalar_text(user_data.get("unique_id_str"))
            or username
        )
        has_identity = any(
            helper_method.scalar_text(value)
            for value in (
                user_data.get("id"),
                user_data.get("uid"),
                unique_id,
                user_data.get("nickname"),
                user_data.get("signature"),
                user_data.get("avatarLarger"),
                user_data.get("avatar_larger"),
                user_data.get("avatar"),
            )
        )
        if not has_identity or self._user_info_shows_missing_account(data):
            return {}

        normalized_user = {
            "id": user_data.get("id") or user_data.get("uid") or unique_id,
            "secUid": user_data.get("secUid") or user_data.get("sec_uid"),
            "uniqueId": unique_id,
            "nickname": user_data.get("nickname") or user_data.get("nickName") or unique_id,
            "signature": user_data.get("signature") or user_data.get("bio") or "",
            "avatarLarger": (
                user_data.get("avatarLarger")
                or user_data.get("avatar_larger")
                or user_data.get("avatarMedium")
                or user_data.get("avatar_medium")
                or user_data.get("avatarThumb")
                or user_data.get("avatar_thumb")
                or user_data.get("avatar")
            ),
            "avatarMedium": user_data.get("avatarMedium") or user_data.get("avatar_medium") or user_data.get("avatar"),
            "avatarThumb": user_data.get("avatarThumb") or user_data.get("avatar_thumb") or user_data.get("avatar"),
            "coverUrl": user_data.get("coverUrl") or user_data.get("cover") or user_data.get("profileCover"),
        }
        normalized_stats = {
            "heartCount": self._first_present(
                stats_data.get("heartCount"),
                stats_data.get("heart_count"),
                stats_data.get("heart"),
                stats_data.get("diggCount"),
                stats_data.get("digg_count"),
            ),
            "videoCount": self._first_present(stats_data.get("videoCount"), stats_data.get("video_count")),
        }
        return {"userInfo": {"user": normalized_user, "stats": normalized_stats}}

    def _browser_collect_videos_with_retries(self, page, username: str, data_type: SocialDataType):
        for attempt in range(3):
            self._fallback_collect_videos_from_payloads(username, data_type)
            if not self._card_data:
                self._fallback_collect_videos_from_rehydration(page, username, data_type)
            if not self._card_data:
                self._fallback_collect_videos_from_item_list(page, username, data_type)
            if not self._card_data:
                self._fallback_collect_videos_from_page(page, username, data_type)
            if self._card_data:
                return
            self._fallback_collect_videos_from_public_metadata(username, data_type)
            if self._card_data:
                return
            if self._page_has_hard_limit(page):
                log.g().e(f"TikTok hard limit/captcha while fetching {data_type.value} for {username}.")
                return
            if page is None or attempt >= 2:
                break
            try:
                cache_buster = random.randint(100000, 999999)
                page.goto(f"{self.seed_url}?lang=en&_retry={cache_buster}", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(random.randint(2500, 5000))
                self._profile_missing = self._page_shows_missing_account(page)
                if self._profile_missing:
                    log.g().e(f"Skipping TikTok retry for {username}: account not found.")
                    return
                self._profile_metadata = self._extract_profile_assets(page)
                self._profile_user_detail = self._extract_user_detail_from_page(page)
            except Exception as ex:
                log.g().e(f"Failed TikTok browser retry {attempt + 1} for {username}: {ex}")
                break

    def _append_profile_card(self, username: str, user_info: dict):
        if getattr(self, "_profile_missing", False):
            return
        if not user_info and self._profile_user_detail:
            user_info = self._profile_user_detail
        if not isinstance(user_info, dict) or self._user_info_shows_missing_account(user_info):
            return
        info = user_info.get("userInfo") or user_info
        user_data = info.get("user") or {}
        stats = info.get("stats") or {}
        nickname = user_data.get("nickname") or username
        unique_id = user_data.get("uniqueId") or user_data.get("unique_id") or username
        profile_url = f"https://www.tiktok.com/@{unique_id}" if unique_id else self.seed_url
        likes_count = self._stat_count(stats, "heartCount", "heart_count")
        video_count = self._stat_count(stats, "videoCount", "video_count")
        content_type = "profile_info"
        profile_icon = (
            user_data.get("avatarLarger")
            or user_data.get("avatarMedium")
            or user_data.get("avatarThumb")
            or self._profile_metadata.get("profileIcon")
        )
        coverpage = (
            user_data.get("coverUrl")
            or user_data.get("cover")
            or user_data.get("profileCover")
            or self._profile_metadata.get("coverpage")
        )
        has_profile_identity = any(
            helper_method.scalar_text(value)
            for value in (
                user_data.get("id"),
                user_data.get("secUid"),
                user_data.get("sec_uid"),
                user_data.get("nickname"),
                user_data.get("avatarLarger"),
                user_data.get("avatarMedium"),
                user_data.get("avatarThumb"),
                user_data.get("signature"),
            )
        )
        has_profile_stats = any(
            isinstance(stats, dict) and key in stats and stats.get(key) is not None
            for key in (
                "heartCount",
                "heart_count",
                "videoCount",
                "video_count",
            )
        )
        if not has_profile_identity and not has_profile_stats:
            log.g().e(f"Skipping TikTok profile card for {username}: no profile data found.")
            return
        group_info = json.dumps(
            {
                "likes": likes_count,
                "videos": video_count,
            },
            ensure_ascii=False,
        )

        card_data = social_model(
            m_title=unique_id,
            m_sender_name=nickname,
            m_url=profile_url,
            m_weblink=[profile_url],
            m_content=user_data.get("signature") or "",
            m_content_type=["social_collector", "tiktok_profile", content_type],
            m_network="clearnet",
            m_date=datetime.now(UTC).date(),
            m_channel_url=profile_url,
            m_message_id=str(user_data.get("id") or unique_id),
            m_platform="tiktok",
            m_group_name=unique_id,
            m_group_info=group_info,
            m_img_src=profile_icon or None,
            m_coverpage=coverpage or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[unique_id] if unique_id else []))

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
        page = self._page(page)
        if page is None:
            return ""
        local_token = page.evaluate("() => window.localStorage.getItem('msToken')") or ""
        if local_token:
            return local_token
        return self._extract_ms_token_from_cookies(page.context.cookies())

    def _tiktok_api_proxies(self) -> list[dict] | None:
        if self.rule_config.m_fetch_proxy != FetchProxy.TOR:
            return None
        tor_url = os.getenv("TOR_PROXY_URL") or "socks5://trusted-social_tor_instace_1:9552"
        return [{"server": tor_url.replace("socks5h://", "socks5://")}]


    def _fetch_ms_token_with_playwright(self, page=None) -> str:
        try:
            page = self._page(page)
            if page is None:
                return ""
            page.goto(self.seed_url or self.base_url, wait_until="domcontentloaded", timeout=60000)

            ms_token = ""
            for _ in range(self.MS_TOKEN_WAIT_ATTEMPTS):
                page.wait_for_timeout(random.randint(1000, 10000))
                ms_token = self._read_ms_token(page)
                if ms_token:
                    break

            return ms_token or ""
        except Exception as ex:
            log.g().e(f"Failed to fetch MS token via Playwright: {ex}")
            return ""


    def parse_leak_data(self, page=None):
        self._card_data = []
        self._entity_data = []
        self._profile_missing = False
        page = self._page(page)
        item_list_listener = self._install_item_list_response_collector(page)
        try:
            if self._use_saved_session():
                self._apply_saved_session(page)
            data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
            username_match = re.search(r"tiktok\.com/@([^/?]+)", self.seed_url or "")
            username = username_match.group(1) if username_match else ""

            if username and data_type in (SocialDataType.POSTS, SocialDataType.VIDEOS, SocialDataType.SHORTS):
                self._fallback_collect_videos_from_public_metadata(username, data_type)
                if self._card_data:
                    return
                try:
                    if page is not None:
                        page.goto(self.seed_url or self.base_url, wait_until="domcontentloaded", timeout=60000)
                        page.wait_for_timeout(random.randint(6000, 9000))
                except Exception as ex:
                    log.g().e(f"Failed to load TikTok list page for {username}: {ex}")
                self._profile_missing = self._page_shows_missing_account(page)
                if self._profile_missing:
                    log.g().e(f"TikTok browser page reports account not found for {username}; trying no-session fallbacks.")
                else:
                    self._profile_metadata = self._extract_profile_assets(page)
                    self._profile_user_detail = self._extract_user_detail_from_page(page)
                self._browser_collect_videos_with_retries(page, username, data_type)
                return

            if username and data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL):
                self._profile_user_detail = self._fetch_public_profile_info(username)
                if self._profile_user_detail:
                    self._append_profile_card(username, self._profile_user_detail)
                    if self._card_data:
                        return

            self.MS_TOKEN = self._fetch_ms_token_with_playwright(page)
            self._profile_missing = self._page_shows_missing_account(page)
            if self._profile_missing:
                log.g().e(f"Skipping TikTok profile for {username}: account not found.")
                return
            self._profile_metadata = self._extract_profile_assets(page)
            self._profile_user_detail = self._extract_user_detail_from_page(page)

            if username and self._profile_user_detail and data_type in (
                SocialDataType.PROFILE,
                SocialDataType.CHANNEL,
            ):
                self._append_profile_card(username, self._profile_user_detail)
                return

            def runner():
                try:
                    asyncio.run(self._parse_leak_data_async())
                except Exception as ex:
                    log.g().e(f"Failed to fetch TikTok data: {ex}")

            t = threading.Thread(target=runner, daemon=False)
            t.start()
            t.join()

            if not self._card_data and username and data_type in self._video_data_types():
                self._browser_collect_videos_with_retries(page, username, data_type)
        except Exception as ex:
            log.g().e(f"CRITICAL SCRIPT ERROR: {ex}")
        finally:
            if page is not None and item_list_listener is not None:
                try:
                    page.remove_listener("response", item_list_listener)
                except Exception:
                    pass

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

        data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
        count = self._item_limit()
        fetched = 0

        async with TikTokApi() as api:
            await api.create_sessions(
                ms_tokens=[self.MS_TOKEN],
                num_sessions=1,
                proxies=self._tiktok_api_proxies(),
                sleep_after=random.randint(1, 10),
            )
            user = api.user(username=username)

            if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL):
                try:
                    user_info = await user.info()
                except Exception as ex:
                    log.g().e(f"Failed to fetch TikTok profile info for {username}: {ex}")
                    user_info = {}
                self._append_profile_card(username, user_info)
                return

            async for video in user.videos(count=count):
                if fetched >= count:
                    break
                fetched += 1

                stats = getattr(video, "stats", {}) or {}
                video_dict = getattr(video, "as_dict", {}) or {}
                desc = video_dict.get("desc", "") or ""

                views = int(stats.get("playCount", 0) or 0)
                likes = int(stats.get("diggCount", 0) or 0)
                comments = int(stats.get("commentCount", 0) or 0)
                shares = int(stats.get("shareCount", 0) or 0)

                status = views >= self.MIN_VIEWS or likes >= self.MIN_LIKES

                content = desc

                share_url = video_dict.get("shareInfo", {}).get("shareUrl")
                author = getattr(video.author, "username", None)
                fallback_url = f"https://www.tiktok.com/@{author}/video/{video.id}" if author else ""
                video_url = share_url or fallback_url
                video_id = str(video.id)
                structured_comments = await self._collect_video_comments(video) if data_type == SocialDataType.COMMENTS else []
                video_date = self._tiktok_date(video_dict.get("createTime") or video_dict.get("create_time"))

                self._append_video_card(
                    video_url=video_url,
                    video_id=video_id,
                    author=author,
                    content=content,
                    likes=str(likes),
                    comments=str(comments),
                    shares=str(shares),
                    views=str(views),
                    media_url=None,
                    data_type=data_type,
                    structured_comments=structured_comments,
                )
                self._card_data[-1].m_date = video_date
                self._card_data[-1].m_viral = status
                await asyncio.sleep(random.randint(1, 10))
