from datetime import datetime, timedelta, UTC
from abc import ABC
from typing import Any, Dict, List
import json
import os
import random
from urllib.parse import urlsplit, urlunsplit

from crawler.crawler_instance.genbot_service.helpers.reddit.reddit_helper_method import RedditHelperMethod
from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_comment_model, social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method


class _reddit(extraction_interface, ABC):
    _instance = None
    REDDIT_ONION_BASE_URL = "https://www.reddittorjg6rue252oqsxryoxengawnmo46qy4kyii5wtqnwfj4ooad.onion"

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self._initialized = None
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self.m_seed_url = ""
        self._subreddit_metadata = {}

    def init_callback(self, callback=None):
        self.callback = callback

    @classmethod
    def _configured_onion_base_url(cls) -> str:
        configured = (os.getenv("REDDIT_ONION_BASE_URL") or cls.REDDIT_ONION_BASE_URL).strip()
        if "://" not in configured:
            configured = f"https://{configured}"
        parts = urlsplit(configured)
        return urlunsplit((parts.scheme or "https", parts.netloc, "", "", "")).rstrip("/")

    @classmethod
    def _is_reddit_url(cls, url: str | None) -> bool:
        if not url:
            return False
        raw = str(url).strip()
        if raw.startswith("//"):
            raw = f"https:{raw}"
        if "://" not in raw:
            return raw.startswith("/")
        hostname = (urlsplit(raw).hostname or "").lower()
        onion_hostname = (urlsplit(cls._configured_onion_base_url()).hostname or "").lower()
        onion_root_hostname = onion_hostname[4:] if onion_hostname.startswith("www.") else onion_hostname
        host_root = hostname[4:] if hostname.startswith("www.") else hostname
        return bool(
            host_root == onion_root_hostname
            or hostname == "reddit.com"
            or hostname.endswith(".reddit.com")
        )

    @classmethod
    def _to_reddit_tor_url(cls, url: str | None) -> str:
        onion_base = cls._configured_onion_base_url()
        onion_parts = urlsplit(onion_base)
        if not url:
            return onion_base

        raw = str(url).strip()
        if raw.startswith("//"):
            raw = f"https:{raw}"
        elif "://" not in raw:
            raw = f"https://www.reddit.com{'' if raw.startswith('/') else '/'}{raw}"

        try:
            parts = urlsplit(raw)
        except Exception:
            return onion_base

        hostname = (parts.hostname or "").lower()
        onion_hostname = (onion_parts.hostname or "").lower()
        onion_root_hostname = onion_hostname[4:] if onion_hostname.startswith("www.") else onion_hostname
        host_root = hostname[4:] if hostname.startswith("www.") else hostname
        if host_root == onion_root_hostname or hostname == "reddit.com" or hostname.endswith(".reddit.com"):
            return urlunsplit((
                onion_parts.scheme or "http",
                onion_parts.netloc,
                parts.path or "/",
                parts.query,
                parts.fragment,
            ))
        return str(url).strip()

    @property
    def is_crawled(self) -> bool:
        return self._is_crawled

    @property
    def seed_url(self) -> str:
        return self._to_reddit_tor_url(self.m_seed_url)

    @property
    def developer_signature(self) -> str:
        return "Muhammad Hassan Arshad: owEBeAKH/ZANAwAKAbKjqaChU0IoAcsxYgBoei5jVmVyaWZpZWQgZGV2ZWxvcGVyOiBNdWhhbW1hZCBIYXNzYW4gQXJzaGFk..."

    @property
    def base_url(self) -> str:
        return self._configured_onion_base_url()

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.TOR,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_threat_type=ThreatType.REDDIT,
            m_rule_type=RuleType.REDDIT,
            m_social_data_type=getattr(self, "m_social_data_type", SocialDataType.DEFAULT),
        )

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def contact_page(self) -> str:
        return self._to_reddit_tor_url("https://www.reddit.com/contact")

    def invoke_db(self, command: int, key: str, default_value, expiry: int | None = None):
        return self._redis_instance.invoke_trigger(
            command, [key + self.__class__.__name__, default_value, expiry]
        )

    @staticmethod
    def data_parsre(s: str | None):
        try:
            if not isinstance(s, str) or not s:
                return None
            return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
        except Exception:
            return None

    @staticmethod
    def _reddit_identity_from_url(url: str) -> tuple[str, str]:
        try:
            path_parts = [part for part in urlsplit(url).path.split("/") if part]
        except Exception:
            path_parts = []
        if len(path_parts) >= 2 and path_parts[0].lower() == "r":
            return "subreddit", path_parts[1]
        if len(path_parts) >= 2 and path_parts[0].lower() in {"u", "user"}:
            return "user", path_parts[1]
        return "subreddit", path_parts[-1] if path_parts else ""

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
        if not requested_hash_id or not url:
            return False
        candidates = {url, self._to_reddit_tor_url(url)}
        return any(
            social_model.unique_identifier("reddit", candidate, "", "", "") == requested_hash_id
            for candidate in candidates
            if candidate
        )

    def _collect_comments_from_post(self, page, post_url: str, max_comments: int, comment_offset: int) -> List[Dict[str, Any]]:
        comments: List[Dict[str, Any]] = []
        seen = set()
        max_comments = max(1, min(int(max_comments or 10), 10))
        comment_offset = max(0, int(comment_offset or 0))
        target_count = comment_offset + max_comments
        try:
            post_url = self._to_reddit_tor_url(post_url)
            page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
            idle_scrolls = 0
            for _ in range(30):
                before_count = len(comments)
                try:
                    rows = page.evaluate("""() => {
                        const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                        const roots = Array.from(document.querySelectorAll([
                            'shreddit-comment',
                            '[data-testid="comment"]',
                            '[id^="t1_"]',
                            '.Comment',
                            '.comment'
                        ].join(',')));
                        return roots.map(comment => {
                            const content = clean(
                                comment.querySelector('div[id*="comment"] p, [slot="comment"], [data-testid="comment"] p, .usertext-body, .md, p')?.innerText
                                || comment.getAttribute('body')
                                || ''
                            );
                            const username = clean(
                                comment.getAttribute('author')
                                || comment.querySelector('a[href*="/user/"], a[href*="/u/"], .author, [data-testid="comment_author_link"]')?.innerText
                                || ''
                            ).replace(/^u\\//i, '');
                            const timestamp = (
                                comment.querySelector('time[datetime]')?.getAttribute('datetime')
                                || comment.querySelector('faceplate-timeago')?.getAttribute('ts')
                                || ''
                            );
                            const likes = clean(
                                comment.getAttribute('score')
                                || comment.querySelector('[id*="score"], .score, [aria-label*="upvote" i]')?.innerText
                                || ''
                            );
                            return content ? {username, timestamp, likes, content} : null;
                        }).filter(Boolean);
                    }""")
                except Exception:
                    rows = []

                for row in rows:
                    if len(comments) >= target_count:
                        return comments[comment_offset:target_count]
                    content = helper_method.scalar_text(row.get("content"))
                    if not content:
                        continue
                    key = "|".join([
                        helper_method.scalar_text(row.get("username")),
                        helper_method.scalar_text(row.get("timestamp")),
                        content,
                    ])
                    if key in seen:
                        continue
                    seen.add(key)
                    row["content"] = content
                    comments.append(row)

                idle_scrolls = idle_scrolls + 1 if len(comments) == before_count else 0
                if len(comments) >= target_count or idle_scrolls >= 5:
                    break
                try:
                    page.evaluate("""() => {
                        for (const button of document.querySelectorAll('button')) {
                            const text = (button.innerText || '').toLowerCase();
                            if (text.includes('more comments') || text.includes('view more') || text.includes('load more')) {
                                try { button.click(); } catch (e) {}
                            }
                        }
                        window.scrollBy(0, 4000);
                    }""")
                    page.wait_for_timeout(750)
                except Exception:
                    break
        except Exception:
            pass
        return comments[comment_offset:target_count]

    def _collect_html_posts(self, page, desired_count: int, max_scrolls: int, filter_date) -> List[Dict[str, Any]]:
        posts: List[Dict[str, Any]] = []
        seen = set()
        desired_count = max(1, min(int(desired_count or 10), 100))
        max_scrolls = max(1, min(int(max_scrolls or 20), 50))

        for _ in range(max_scrolls):
            try:
                rows = page.evaluate("""() => {
                    const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                    const absolute = value => {
                        if (!value) return '';
                        try { return new URL(value, location.href).href; } catch (_) { return String(value || ''); }
                    };
                    const roots = Array.from(document.querySelectorAll([
                        'shreddit-post',
                        'article',
                        '[data-testid="post-container"]',
                        '[id^="t3_"]',
                        '.Post',
                        '.thing.link'
                    ].join(',')));
                    return roots.map(root => {
                        const titleLink = root.querySelector('a[slot="title"], a[href*="/comments/"], a.title, h3 a');
                        const commentsLink = root.querySelector('a[href*="/comments/"], a.comments');
                        const title = clean(
                            root.getAttribute('post-title')
                            || titleLink?.innerText
                            || root.querySelector('h1, h2, h3, [slot="title"]')?.innerText
                            || ''
                        );
                        const postUrl = absolute(
                            root.getAttribute('permalink')
                            || root.dataset?.permalink
                            || commentsLink?.getAttribute('href')
                            || titleLink?.getAttribute('href')
                            || ''
                        );
                        const externalUrl = absolute(titleLink?.getAttribute('href') || '');
                        const username = clean(
                            root.getAttribute('author')
                            || root.querySelector('a[href*="/user/"], a[href*="/u/"], .author')?.innerText
                            || ''
                        ).replace(/^u\\//i, '');
                        const timestamp = (
                            root.getAttribute('created-timestamp')
                            || root.querySelector('time[datetime]')?.getAttribute('datetime')
                            || root.querySelector('faceplate-timeago')?.getAttribute('ts')
                            || ''
                        );
                        const score = clean(
                            root.getAttribute('score')
                            || root.querySelector('[id*="score"], .score, [aria-label*="upvote" i]')?.innerText
                            || ''
                        );
                        const commentCount = clean(
                            root.getAttribute('comment-count')
                            || commentsLink?.innerText
                            || root.querySelector('[href*="/comments/"] span, [aria-label*="comment" i]')?.innerText
                            || ''
                        );
                        const content = clean(
                            root.querySelector('[slot="text-body"], [data-click-id="text"], .usertext-body, .md, p')?.innerText
                            || ''
                        );
                        const media = Array.from(root.querySelectorAll('img, video, source'))
                            .map(node => absolute(node.currentSrc || node.src || node.getAttribute('src')))
                            .filter(src => src && !src.startsWith('data:'));
                        const id = clean(root.getAttribute('id') || root.getAttribute('post-id') || root.dataset?.fullname || postUrl);
                        const weblinks = [postUrl, externalUrl].filter(Boolean);
                        return title || postUrl ? {id, title, url: postUrl, username, timestamp, score, comment_count: commentCount, content, media, weblinks} : null;
                    }).filter(Boolean);
                }""")
            except Exception:
                rows = []

            for row in rows:
                post_url = self._to_reddit_tor_url(helper_method.scalar_text(row.get("url")))
                if not post_url or post_url in seen:
                    continue
                parsed_date = self.data_parsre(helper_method.scalar_text(row.get("timestamp")))
                if filter_date and parsed_date and parsed_date < filter_date.date():
                    continue
                seen.add(post_url)
                row["url"] = post_url
                row["weblinks"] = [
                    self._to_reddit_tor_url(link) if self._is_reddit_url(link) else helper_method.scalar_text(link)
                    for link in (row.get("weblinks") or [])
                    if helper_method.scalar_text(link)
                ]
                posts.append(row)
                if len(posts) >= desired_count:
                    return posts

            try:
                page.evaluate("""() => {
                    for (const button of document.querySelectorAll('button')) {
                        const text = (button.innerText || '').toLowerCase();
                        if (text.includes('show more') || text.includes('load more') || text.includes('view more')) {
                            try { button.click(); } catch (e) {}
                        }
                    }
                    window.scrollBy(0, 4000);
                }""")
                page.wait_for_timeout(750)
            except Exception:
                break

        return posts[:desired_count]

    def _collect_posts(self, page, subreddit_name: str, desired_count: int, max_scrolls: int, filter_date) -> List[Dict[str, Any]]:
        posts = RedditHelperMethod.scroll_and_collect_posts(
            page, subreddit_name, desired_count, max_scrolls=max_scrolls, filter_date=filter_date
        )
        if posts:
            return posts
        return self._collect_html_posts(page, desired_count, max_scrolls, filter_date)

    @staticmethod
    def _clean_asset_url(value: Any) -> str:
        url = helper_method.scalar_text(value)
        if not url:
            return ""
        url = url.replace("&amp;", "&")
        if url.startswith("//"):
            return f"https:{url}"
        return url

    def _fetch_subreddit_about(self, page, subreddit_name: str) -> dict:
        about_url = f"{self.base_url}/r/{subreddit_name}/about.json"
        try:
            response = page.context.request.get(about_url, headers={"accept": "application/json"}, timeout=12000)
            if response.ok:
                payload = response.json()
                if isinstance(payload, dict):
                    return payload.get("data") or {}
        except Exception:
            pass
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
                about_url,
            )
            payload = json.loads(raw_text or "{}")
            return payload.get("data") or {}
        except Exception:
            return {}

    def _fetch_user_about(self, page, username: str) -> dict:
        about_url = f"{self.base_url}/user/{username}/about.json"
        try:
            response = page.context.request.get(about_url, headers={"accept": "application/json"}, timeout=12000)
            if response.ok:
                payload = response.json()
                if isinstance(payload, dict):
                    return payload.get("data") or {}
        except Exception:
            pass
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
                about_url,
            )
            payload = json.loads(raw_text or "{}")
            return payload.get("data") or {}
        except Exception:
            return {}

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
                const images = Array.from(document.images).map(img => {
                    const rect = img.getBoundingClientRect();
                    return {
                        src: cleanUrl(img.currentSrc || img.src || img.getAttribute('src')),
                        width: rect.width || img.naturalWidth || img.width || 0,
                        height: rect.height || img.naturalHeight || img.height || 0,
                        top: rect.top
                    };
                }).filter(img => img.src && /redditmedia|redd\\.it|styles\\.reddit|reddit[a-z0-9]+\\.onion|communityIcon_|profileIcon_/i.test(img.src));
                const profileIcon = firstAttr([
                    'shreddit-subreddit-header img[slot="icon"]',
                    '[slot="icon"] img',
                    'img.shreddit-subreddit-icon__icon[src*="communityIcon_"]',
                    'img[src*="/styles/communityIcon_"]',
                    'faceplate-img[src*="/styles/communityIcon_"]',
                    'img[alt*="r/" i]',
                    'img[src*="styles.redditmedia.com"]',
                    'img[src*="styles.reddit"][src*="communityIcon_"]',
                    'img[src*="styles.reddit"][src*="profileIcon_"]'
                ], 'src') || firstAttr([
                    'meta[property="og:image"]',
                    'meta[name="twitter:image"]'
                ], 'content') || images.find(img => img.width >= 40 && img.height >= 40 && img.width <= 220 && img.height <= 220)?.src || '';
                const coverpage = firstAttr([
                    'shreddit-subreddit-header img[slot="banner"]',
                    '[slot="banner"] img',
                    'img[alt*="banner" i]',
                    'img[alt*="cover" i]'
                ], 'src') || bgUrl([
                    'shreddit-subreddit-header',
                    '[slot="banner"]',
                    '[style*="background-image"]'
                ]) || images.find(img => img.width > 320 && img.height > 80 && img.top < 500 && img.src !== profileIcon)?.src || '';
                return {profileIcon, coverpage};
            }""") or {}
        except Exception:
            return {}

    def _user_metadata_from_about(self, about_data: dict) -> dict:
        profile_subreddit = about_data.get("subreddit") if isinstance(about_data.get("subreddit"), dict) else {}
        return {
            "bio": helper_method.scalar_text(
                profile_subreddit.get("public_description")
                or profile_subreddit.get("description")
                or about_data.get("subreddit_public_description")
                or about_data.get("description")
            ),
            "karma": (
                about_data.get("total_karma")
                or ((about_data.get("link_karma") or 0) + (about_data.get("comment_karma") or 0))
            ),
            "created_utc": about_data.get("created_utc"),
        }

    def _user_profile_assets_from_about(self, about_data: dict) -> dict:
        profile_subreddit = about_data.get("subreddit") if isinstance(about_data.get("subreddit"), dict) else {}
        return {
            "profileIcon": (
                self._clean_asset_url(about_data.get("icon_img"))
                or self._clean_asset_url(about_data.get("snoovatar_img"))
                or self._clean_asset_url(profile_subreddit.get("icon_img"))
                or self._clean_asset_url(profile_subreddit.get("community_icon"))
            ),
            "coverpage": (
                self._clean_asset_url(profile_subreddit.get("banner_background_image"))
                or self._clean_asset_url(profile_subreddit.get("banner_img"))
                or self._clean_asset_url(profile_subreddit.get("mobile_banner_image"))
                or self._clean_asset_url(profile_subreddit.get("header_img"))
            ),
        }

    def _append_profile_info(self, subreddit_name: str, metadata: dict, profile_assets: dict | None = None):
        profile_assets = profile_assets or {}
        content = helper_method.scalar_text(metadata.get("bio"))
        members = metadata.get("members") or 0
        content_type = "profile_info"
        card_data = social_model(
            m_title=subreddit_name,
            m_channel_url=self.seed_url,
            m_sender_name=subreddit_name,
            m_url=self.seed_url,
            m_weblink=[self.seed_url],
            m_content=content,
            m_content_type=["social_collector", "reddit_profile", content_type],
            m_network="tor",
            m_date=datetime.now(UTC).date(),
            m_message_id=subreddit_name,
            m_platform="reddit",
            m_group_name=subreddit_name,
            m_group_info=f"MEMBERS: {members}" if members else None,
            m_img_src=profile_assets.get("profileIcon") or None,
            m_coverpage=profile_assets.get("coverpage") or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[subreddit_name] if subreddit_name else []))

    def _append_user_profile_info(self, username: str, metadata: dict, profile_assets: dict | None = None):
        profile_assets = profile_assets or {}
        handle = f"user/{username}"
        content = helper_method.scalar_text(metadata.get("bio"))
        karma = metadata.get("karma") or 0
        content_type = "profile_info"
        card_data = social_model(
            m_title=handle,
            m_channel_url=self.seed_url,
            m_sender_name=username,
            m_url=self.seed_url,
            m_weblink=[self.seed_url],
            m_content=content,
            m_content_type=["social_collector", "reddit_profile", content_type],
            m_network="tor",
            m_date=datetime.now(UTC).date(),
            m_message_id=handle,
            m_platform="reddit",
            m_group_name=handle,
            m_group_info=f"KARMA: {karma}" if karma else None,
            m_img_src=profile_assets.get("profileIcon") or None,
            m_coverpage=profile_assets.get("coverpage") or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[handle, username] if username else [handle]))

    def parse_leak_data(self, page):
        self._card_data = []
        self._entity_data = []
        try:
            try:
                page.wait_for_load_state("domcontentloaded", timeout=10000)
                page.wait_for_selector("body", timeout=15000)
            except Exception:
                pass
            raw_url = self.seed_url.rstrip('/')
            reddit_type, reddit_name = self._reddit_identity_from_url(raw_url)
            log.g().i(f"Starting deep extraction for {reddit_type}:{reddit_name}")
            if reddit_type == "user":
                about_data = self._fetch_user_about(page, reddit_name)
                metadata = self._user_metadata_from_about(about_data) if about_data else {}
                profile_assets = self._user_profile_assets_from_about(about_data) if about_data else {}
                group_name = f"user/{reddit_name}"
                group_info = f"KARMA: {metadata.get('karma')}" if metadata.get("karma") else None
            else:
                metadata = RedditHelperMethod.get_subreddit_metadata(page, reddit_name)
                profile_assets = self._extract_profile_assets(page)
                about_data = self._fetch_subreddit_about(page, reddit_name)
                if about_data:
                    metadata["bio"] = metadata.get("bio") or helper_method.scalar_text(
                        about_data.get("public_description") or about_data.get("description")
                    )
                    metadata["members"] = metadata.get("members") or about_data.get("subscribers") or 0
                    profile_assets = dict(profile_assets or {})
                    profile_assets["profileIcon"] = (
                        helper_method.scalar_text(profile_assets.get("profileIcon"))
                        or self._clean_asset_url(about_data.get("community_icon"))
                        or self._clean_asset_url(about_data.get("icon_img"))
                    )
                    profile_assets["coverpage"] = (
                        helper_method.scalar_text(profile_assets.get("coverpage"))
                        or self._clean_asset_url(about_data.get("banner_background_image"))
                        or self._clean_asset_url(about_data.get("banner_img"))
                        or self._clean_asset_url(about_data.get("mobile_banner_image"))
                        or self._clean_asset_url(about_data.get("header_img"))
                    )
                group_name = reddit_name
                group_info = f"MEMBERS: {metadata.get('members')}" if metadata.get("members") else None
            data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
            if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL):
                if reddit_type == "user":
                    self._append_user_profile_info(reddit_name, metadata, profile_assets)
                else:
                    self._append_profile_info(reddit_name, metadata, profile_assets)
                return
            if data_type in (SocialDataType.VIDEOS, SocialDataType.SHORTS):
                return

            last_height = page.evaluate("document.body ? document.body.scrollHeight : 0")

            for i in range(3):
                page.mouse.wheel(0, 1500)
                page.wait_for_timeout(750)

                new_height = page.evaluate("document.body ? document.body.scrollHeight : 0")
                if new_height == last_height:
                    break
                last_height = new_height

            desired_posts = max(1, min(int(getattr(self, "m_item_limit", 10) or 10), 100))
            target_hash = self._is_target_hash_request(data_type)
            search_posts = 100 if target_hash else desired_posts
            filter_date = datetime.now(UTC) - timedelta(days=60)

            posts = []
            for attempt in range(3):
                if reddit_type == "user":
                    posts = self._collect_html_posts(page, search_posts, max_scrolls=20, filter_date=filter_date)
                else:
                    posts = self._collect_posts(page, reddit_name, search_posts, max_scrolls=20, filter_date=filter_date)
                if posts:
                    break
                try:
                    page.goto(f"{self.seed_url}?_retry={random.randint(100000, 999999)}", wait_until="domcontentloaded", timeout=45000)
                    page.wait_for_timeout(random.randint(1000, 2500))
                except Exception as ex:
                    log.g().e(f"Failed Reddit post retry {attempt + 1} for {group_name}: {ex}")
                    break

            if not posts:
                return None

            for post in posts:
                try:
                    raw_post_url = helper_method.scalar_text(post.get("url"))
                    post_url = self._to_reddit_tor_url(raw_post_url) if raw_post_url else ""
                    post_id = helper_method.scalar_text(post.get("id"))
                    post_title = helper_method.scalar_text(post.get("title"))
                    if not post_url or "/comments/" not in post_url:
                        log.g().e(f"Skipping Reddit non-post row for {group_name}: {post_id or post_title or 'missing_url'}")
                        continue
                    if target_hash and not self._is_requested_hash_url(post_url):
                        continue
                    if not target_hash and self._is_requested_hash_url(post_url):
                        break

                    load_comments = data_type == SocialDataType.COMMENTS
                    comments = self._collect_comments_from_post(
                        page,
                        post_url,
                        self._comment_limit(),
                        self._comment_offset(),
                    ) if load_comments and post_url else []
                    structured_comments = [
                        social_comment_model(
                            m_username=helper_method.scalar_text(comment.get("username")) or None,
                            m_time=helper_method.scalar_text(comment.get("timestamp")) or None,
                            m_likes=helper_method.scalar_text(comment.get("likes")) or None,
                            m_text=helper_method.scalar_text(comment.get("content")) or None,
                        )
                        for comment in comments
                        if helper_method.scalar_text(comment.get("content"))
                    ]

                    post_content = helper_method.scalar_text(post.get("content"))
                    full_body = post_content or helper_method.scalar_text(post.get("title"))
                    username_value = helper_method.scalar_text(post.get("username")) or "unknown"
                    timestamp_value = post.get("timestamp")
                    post_timestamp = timestamp_value if isinstance(timestamp_value, str) else None
                    weblinks = post.get("weblinks") or []
                    weblinks = [
                        self._to_reddit_tor_url(link) if self._is_reddit_url(link) else helper_method.scalar_text(link)
                        for link in weblinks
                        if helper_method.scalar_text(link)
                    ]

                    card_data = social_model(
                        m_title=post_title or 'No Title',
                        m_channel_url=self.seed_url,
                        m_sender_name=username_value,
                        m_url=post_url or None,
                        m_message_sharable_link=post_url or None,
                        m_weblink=weblinks or ([post_url] if post_url else []),
                        m_content=full_body,
                        m_content_type=["social_collector", "reddit_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                        m_network="tor",
                        m_date=self.data_parsre(post_timestamp),
                        m_message_id=post_id,
                        m_platform="reddit",
                        m_post_likes=helper_method.scalar_text(post.get("score")) or None,
                        m_likes=helper_method.scalar_text(post.get("score")) or None,
                        m_comment_count=helper_method.scalar_text(post.get("comment_count")) or (str(len(structured_comments)) if load_comments else None),
                        m_comments=structured_comments,
                        m_img_src=self._first_media(post),
                        m_group_name=group_name,
                        m_group_info=group_info,
                        m_scrap_file=self.__class__.__name__,
                    )
                    if target_hash:
                        if self._is_requested_hash_id(card_data):
                            self.append_leak_data(card_data, entity_model(m_username=[username_value] if username_value else []))
                        return

                    entity_data = entity_model(
                        m_username=[username_value],
                    )

                    self.append_leak_data(card_data, entity_data)

                except Exception as post_ex:
                    log.g().e(f"Skipping post {post.get('id')}: {post_ex}")
                    continue

        except Exception as ex:
            log.g().e(f"CRITICAL SCRIPT ERROR: {ex}")
