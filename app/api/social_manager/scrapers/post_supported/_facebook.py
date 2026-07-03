from abc import ABC
from typing import List
from datetime import date, datetime, UTC
import gzip
import hashlib
import json
import os
import random
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_comment_model, social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_instance.genbot_service.helpers.facebook.facebook_helper_method import FacebookScraper
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method


class _facebook(extraction_interface, ABC):
    _instance = None
    SCRIPT_TIMEOUT_SECONDS = 5 * 60

    def __init__(self, callback=None):
        super().__init__()
        self.platform = "facebook"
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self._initialized = None
        self._is_crawled = False
        self.m_seed_url = "https://www.facebook.com/groups/itsecphillippines"
        self._redis_instance = redis_controller()
        self._profile_metadata = {}
        self._last_status = ""
        self._last_reason = ""

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
        return "https://www.facebook.com/"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_timeout=self.SCRIPT_TIMEOUT_SECONDS,
            m_fetch_proxy=FetchProxy.TOR,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_threat_type=ThreatType.FACEBOOK,
            m_rule_type=RuleType.FACEBOOK,
            m_social_data_type=getattr(self, "m_social_data_type", SocialDataType.DEFAULT),
            m_resoource_block=False
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

    def _make_message_id(self, post: dict) -> str:
        content = post.get("content") or ""
        post_url = post.get("url") or ""
        title = post.get("m_title") or ""
        date_str = post.get("date") or ""
        raw_id = "|".join([post_url, title, date_str, content])
        return hashlib.sha256(raw_id.encode("utf-8")).hexdigest()

    def _use_saved_session(self) -> bool:
        return bool(getattr(self, "m_use_saved_session", False))

    @staticmethod
    def _json_string_value(raw: str, key: str) -> str:
        match = re.search(rf'"{re.escape(key)}"\s*:\s*"((?:\\.|[^"\\])*)"', raw or "")
        if not match:
            return ""
        try:
            return json.loads(f'"{match.group(1)}"')
        except Exception:
            return match.group(1)

    @staticmethod
    def _json_array_value(raw: str, key: str) -> list:
        needle = f'"{key}":'
        idx = (raw or "").find(needle)
        if idx < 0:
            return []
        start = raw.find("[", idx + len(needle))
        if start < 0:
            return []
        depth = 0
        in_string = False
        escaped = False
        for pos in range(start, len(raw)):
            char = raw[pos]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
                if depth == 0:
                    try:
                        value = json.loads(raw[start:pos + 1])
                        return value if isinstance(value, list) else []
                    except Exception:
                        return []
        return []

    def _facebook_plugin_url(self) -> str:
        seed = (self.seed_url or "").strip() or self.base_url
        return (
            "https://www.facebook.com/plugins/page.php"
            f"?href={quote(seed, safe='')}"
            "&tabs=timeline&width=500&height=800&small_header=false"
            "&adapt_container_width=true&hide_cover=false&show_facepile=false"
            "&locale=en_US"
        )

    def _fetch_public_plugin_raw(self) -> str:
        try:
            request = Request(
                self._facebook_plugin_url(),
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "User-Agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
                    ),
                },
            )
            with urlopen(request, timeout=25) as response:
                return response.read(4_000_000).decode("utf-8", "replace")
        except Exception as ex:
            self._last_status = "public_plugin_error"
            self._last_reason = f"facebook public plugin request failed: {ex}"
            return ""

    def _fetch_public_plugin_profile(self) -> dict:
        raw = self._fetch_public_plugin_raw()
        if not raw:
            return {}
        profile = {
            "title": self._json_string_value(raw, "pageName"),
            "description": self._json_string_value(raw, "pageDescription"),
            "profileIcon": self._json_string_value(raw, "profilePicURL"),
            "coverpage": self._json_string_value(raw, "coverPhotoURL"),
            "url": self._json_string_value(raw, "pageURL"),
        }
        return {key: value for key, value in profile.items() if value}

    def _fetch_public_plugin_posts(self, max_posts: int) -> list[dict]:
        raw = self._fetch_public_plugin_raw()
        if not raw:
            return []

        posts = self._json_array_value(raw, "timelinePosts")
        if not posts:
            self._last_status = "public_plugin_no_posts"
            self._last_reason = "facebook public page plugin exposed no timelinePosts"
            return []

        page_name = self._json_string_value(raw, "pageName") or self.seed_url.rstrip("/").split("/")[-1]
        page_url = self._json_string_value(raw, "pageURL") or self.seed_url
        profile_pic = self._json_string_value(raw, "profilePicURL")
        normalized_posts: list[dict] = []
        for post in posts[:max_posts]:
            if not isinstance(post, dict):
                continue
            message = helper_method.scalar_text(post.get("message"))
            created_time = post.get("createdTime")
            date_iso = ""
            try:
                date_iso = datetime.fromtimestamp(int(created_time), UTC).date().isoformat()
            except Exception:
                pass
            images = []
            for value in [post.get("photoURL"), *(post.get("albumPhotoURLs") or [])]:
                text = helper_method.scalar_text(value)
                if text and text not in images:
                    images.append(text)
            post_url = page_url or self.seed_url
            normalized_posts.append({
                "m_title": page_name,
                "date": date_iso,
                "url": post_url,
                "type": helper_method.scalar_text(post.get("attachmentType")) or "post",
                "content": message,
                "likes": post.get("reactionCount"),
                "comments": post.get("commentCount"),
                "shares": post.get("shareCount"),
                "images": images or ([profile_pic] if profile_pic else []),
                "videos": [],
                "video_blobs": 1 if post.get("videoDurationMs") else 0,
                "attachment_urls": [],
            })
        return normalized_posts

    def _apply_saved_session(self, page) -> bool:
        context_id = id(page.context)
        if getattr(self, "_facebook_session_context_id", None) == context_id:
            return True

        sessions_dir = os.getenv("ORION_SESSION_ROOT") or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sessions")
        session_paths = [
            os.path.join(sessions_dir, "facebookscraper_session.json.gz"),
            os.path.join(sessions_dir, "_facebook_session.json.gz"),
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
                self._facebook_session_context_id = context_id
                return True
            except Exception:
                continue
        self._facebook_session_context_id = context_id
        return False

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
    def _comment_models(raw_comments: list[dict]) -> list[social_comment_model]:
        return [
            social_comment_model(
                m_username=helper_method.scalar_text(comment.get("username")) or None,
                m_time=helper_method.scalar_text(comment.get("time")) or None,
                m_likes=helper_method.scalar_text(comment.get("likes")) or None,
                m_text=helper_method.scalar_text(comment.get("text")) or None,
            )
            for comment in raw_comments
            if helper_method.scalar_text(comment.get("text"))
        ]

    def _extract_profile_assets(self, page) -> dict:
        try:
            if page.url.rstrip("/") != self.seed_url.rstrip("/"):
                page.goto(self.seed_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(random.randint(1500, 3000))
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
                const firstText = selectors => {
                    for (const selector of selectors) {
                        const text = document.querySelector(selector)?.innerText?.trim() || '';
                        if (text) return text;
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
                const images = Array.from(document.images).map(img => {
                    const rect = img.getBoundingClientRect();
                    return {
                        src: cleanUrl(img.currentSrc || img.src || img.getAttribute('src')),
                        width: rect.width || img.naturalWidth || img.width || 0,
                        height: rect.height || img.naturalHeight || img.height || 0,
                        top: rect.top
                    };
                }).filter(img => img.src && !img.src.includes('static.xx.fbcdn.net'));
                const profileIcon = firstAttr([
                    'meta[property="og:image"]',
                    'meta[name="twitter:image"]',
                    'div[role="main"] a[href*="/photo"] img',
                    'div[role="main"] image',
                    'svg image'
                ], 'content') || firstAttr([
                    'div[role="main"] a[href*="/photo"] img',
                    'div[role="main"] image',
                    'svg image',
                    'img[alt*="profile" i]'
                ], 'src') || images.find(img => img.width >= 80 && img.width <= 260 && img.height >= 80 && img.height <= 260)?.src || '';
                const coverpage = firstAttr([
                    'img[data-imgperflogname="profileCoverPhoto"]',
                    'div[data-pagelet*="Cover"] img',
                    'div[aria-label*="Cover photo" i] img',
                    'img[alt*="cover photo" i]'
                ], 'src') || bgUrl([
                    'div[data-pagelet*="Cover"]',
                    'div[aria-label*="Cover photo" i]',
                    'div[style*="background-image"]'
                ]) || images.find(img => img.width > 320 && img.height > 90 && img.top < 700 && img.src !== profileIcon)?.src || '';
                const title = document.querySelector('meta[property="og:title"]')?.content ||
                    firstText(['h1', 'h2', 'div[role="main"] strong']) ||
                    document.title.replace(/\\s*\\|\\s*Facebook.*$/i, '').trim();
                const description = document.querySelector('meta[property="og:description"]')?.content ||
                    document.querySelector('meta[name="description"]')?.content || '';
                const pageText = document.body?.innerText || '';
                const unavailable = /this content isn't available|this page isn't available|content isn't available at the moment|page not found/i.test(pageText);
                const members = pageText.match(/[\\d.,]+[KMB]?\\s+members/i)?.[0] || '';
                return {title, description, members, profileIcon, coverpage, unavailable};
            }""") or {}
        except Exception:
            return {}

    def _append_profile_info(self, page):
        profile_assets = self._fetch_public_plugin_profile()
        browser_assets = self._extract_profile_assets(page) if page is not None else {}
        profile_assets.update({key: value for key, value in browser_assets.items() if value})
        if profile_assets.get("unavailable") and not (profile_assets.get("profileIcon") or profile_assets.get("coverpage")):
            self._last_status = "unavailable"
            self._last_reason = "facebook reported that the public content is not available"
            return
        username = helper_method.scalar_text(profile_assets.get("title")) or self.seed_url.rstrip("/").split("/")[-1]
        content_type = "profile_info"
        group_info = " | ".join(
            item for item in [
                helper_method.scalar_text(profile_assets.get("members")),
            ]
            if item
        )
        card_data = social_model(
            m_title=username,
            m_channel_url=self.seed_url,
            m_sender_name=username,
            m_url=self.seed_url,
            m_message_sharable_link=self.seed_url,
            m_weblink=[self.seed_url],
            m_content=helper_method.scalar_text(profile_assets.get("description")) or username,
            m_content_type=["social_collector", "facebook_profile", content_type],
            m_network="clearnet",
            m_date=date.today(),
            m_message_id=self.seed_url.rstrip("/").split("/")[-1],
            m_platform=[self.platform],
            m_group_name=username,
            m_group_info=group_info or None,
            m_img_src=profile_assets.get("profileIcon") or None,
            m_coverpage=profile_assets.get("coverpage") or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))

    def _collect_comments(self, page, post_url: str, limit: int = 10, offset: int = 0) -> list[dict]:
        if not post_url:
            return []
        comments: list[dict] = []
        seen = set()
        limit = max(1, min(int(limit or 10), 10))
        offset = max(0, int(offset or 0))
        target_count = offset + limit

        try:
            page.goto(post_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(random.randint(1500, 3000))
        except Exception:
            return []

        idle_scrolls = 0
        for _ in range(20):
            try:
                page.evaluate("""() => {
                    for (const node of document.querySelectorAll('div[role="button"], span[role="button"], a[role="link"], span')) {
                        const text = (node.innerText || node.textContent || '').trim().toLowerCase();
                        if (text.includes('view more comments') || text.includes('more comments') || text.includes('all comments') || text.includes('previous comments')) {
                            try { node.click(); } catch (e) {}
                        }
                    }
                }""")
            except Exception:
                pass

            try:
                rows = page.evaluate("""() => {
                    const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                    const parseCount = value => {
                        const match = clean(value).replace(/,/g, '').match(/([\\d.]+)\\s*([KM]?)/i);
                        if (!match) return '';
                        const multiplier = {K: 1000, M: 1000000}[match[2].toUpperCase()] || 1;
                        const parsed = parseFloat(match[1]);
                        return Number.isFinite(parsed) ? String(Math.round(parsed * multiplier)) : '';
                    };
                    const roots = Array.from(document.querySelectorAll('[aria-label^="Comment by"], [data-commentid], div[role="article"]'))
                        .filter(root => {
                            const text = clean(root.innerText || root.textContent);
                            return text && !/write a comment|view more comments|most relevant/i.test(text);
                        });
                    return roots.map(root => {
                        const label = root.getAttribute('aria-label') || '';
                        let username = '';
                        const labelMatch = label.match(/^Comment by\\s+(.+?)(?:\\s+\\d|$)/i);
                        if (labelMatch) username = clean(labelMatch[1]);
                        if (!username) {
                            username = clean(root.querySelector('a[role="link"] strong, strong, h3, h4')?.innerText || '');
                        }
                        const time = clean(root.querySelector('a[href*="comment_id"], a[aria-label*="Reply"], abbr, time')?.innerText || '');
                        const likes = parseCount(clean(root.querySelector('[aria-label*="Like"], [aria-label*="like"]')?.getAttribute('aria-label') || ''));
                        const lines = clean(root.innerText || root.textContent).split(/(?<=\\S)\\s{2,}|\\n/).map(clean).filter(Boolean);
                        const filtered = lines.filter(line => {
                            const low = line.toLowerCase();
                            if (!line || line === username) return false;
                            if (['like', 'reply', 'share', 'edited', 'author'].includes(low)) return false;
                            if (/^\\d+[smhdw]$/.test(low) || /^\\d+\\s*(like|likes|reply|replies)$/i.test(line)) return false;
                            return true;
                        });
                        const text = filtered.find(line => line.length > 2 && line !== username) || '';
                        return text ? {username, time, likes, text} : null;
                    }).filter(Boolean);
                }""")
            except Exception:
                rows = []

            before_count = len(comments)
            for row in rows:
                raw_text = helper_method.scalar_text(row.get("text"))
                text = helper_method.filter_comments(raw_text) or raw_text
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
                row["text"] = text
                comments.append(row)
                if len(comments) >= target_count:
                    return comments[offset:target_count]

            idle_scrolls = idle_scrolls + 1 if len(comments) == before_count else 0
            if idle_scrolls >= 5:
                break
            try:
                page.mouse.wheel(0, 2500)
                page.wait_for_timeout(1000)
            except Exception:
                break
        return comments[offset:target_count]

    def parse_leak_data(self, page):
        self._last_status = ""
        self._last_reason = ""
        if not self.seed_url:
            self._last_status = "invalid_seed"
            self._last_reason = "seed URL is empty"
            log.g().e("Seed URL is empty.")
            return

        if self._use_saved_session() and page is not None:
            self._apply_saved_session(page)
        data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
        if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL):
            self._append_profile_info(page)
            return
        if data_type in (SocialDataType.VIDEOS, SocialDataType.SHORTS):
            self._last_status = "unsupported_data_type"
            self._last_reason = "facebook video/short extraction is not implemented separately"
            return

        max_posts = max(1, min(int(getattr(self, "m_item_limit", 10 if self.is_crawled else 20) or 10), 100))
        posts = self._fetch_public_plugin_posts(max_posts)
        if posts:
            self._last_status = "ok_public_plugin"
            self._last_reason = f"facebook public plugin returned {len(posts)} post cards"
        else:
            self._last_status = ""
            self._last_reason = ""
            posts = []

        scraper = FacebookScraper(seed_url=self.seed_url, max_posts=max_posts)
        if not posts:
            scraper.STARTUP_TIMEOUT_MS = 35_000
            scraper.INITIAL_WAIT_MS = (1500, 2500)
            scraper.SHORT_WAIT_MS = (250, 700)
            scraper.ACTION_WAIT_MS = (500, 1200)
            scraper.SCROLL_WAIT_MS = (900, 1800)
            try:
                posts = scraper.scrape_posts(page)
            except Exception as ex:
                self._last_status = "navigation_error"
                self._last_reason = str(ex)
                log.g().w(f"Facebook scrape_posts failed for {self.seed_url}: {ex}")
                posts = []

        if not posts:
            if not self._last_status:
                self._last_status = "no_public_posts"
                self._last_reason = "facebook public page exposed no post containers"
            return

        for post in posts:
            if page is not None:
                page.wait_for_timeout(random.randint(1000, 10000))
            raw_date_str = post.get("date")
            date_str = raw_date_str if isinstance(raw_date_str, str) else ""
            msg_id = self._make_message_id(post)
            msg_date = date.fromisoformat(date_str) if date_str else None
            post_url = post.get("url") or self.seed_url
            raw_comments = self._collect_comments(page, post_url, self._comment_limit(), self._comment_offset()) if page is not None and data_type == SocialDataType.COMMENTS and post_url else []
            structured_comments = self._comment_models(raw_comments)

            card_data = social_model(
                m_title=post.get("m_title"),
                m_channel_url=self.seed_url,
                m_url=post_url,
                m_message_sharable_link=post_url,
                m_weblink=[post_url],
                m_post_likes=helper_method.scalar_text(post.get("likes") or 0),
                m_comment_count=str(len(structured_comments)) if structured_comments else helper_method.scalar_text(post.get("comments") or 0),
                m_post_shares=helper_method.scalar_text(post.get("shares") or 0),
                m_comments=structured_comments,
                m_content=post.get("content") or "",
                m_content_type=["social_collector", "facebook_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                m_platform=[self.platform],
                m_network="clearnet",
                m_post_tags=[],
                m_date=msg_date,
                m_message_id=msg_id,
                m_img_src=(post.get("images") or [None])[0],
                m_scrap_file=self.__class__.__name__,
            )

            entity_data = entity_model()

            self.append_leak_data(card_data, entity_data)

        self._last_status = "ok"
        self._last_reason = f"facebook returned {len(posts)} post cards"
