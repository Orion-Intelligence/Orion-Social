from datetime import datetime
from abc import ABC
from typing import List
import gzip
import json
import os
import random
import re

from crawler.crawler_instance.genbot_service.helpers.twitter.tweet_helper_methods import TweetHelperMethods
from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_comment_model, social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method


class _twitter(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.platform = "twitter"
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self._initialized = None
        self.m_seed_url = "https://x.com/DarkReading/"
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._helper_methods = TweetHelperMethods()

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
        return "Muhammad Hannan Zahid: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hOii"

    @property
    def base_url(self) -> str:
        return "https://www.x.com"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.TOR,
            m_resoource_block=False,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_threat_type=ThreatType.TWITTER,
            m_rule_type=RuleType.TWITTER,
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
        return "https://x.com/contact"

    @staticmethod
    def safe_find(page, selector, attr=None):
        try:
            element = page.query_selector(selector)
            if element:
                if attr:
                    return element.get_attribute(attr)
                text = element.inner_text()
                return text.strip() if text else None
        except Exception:
            return None

    @staticmethod
    def _parse_iso(s: str | None):
        if not isinstance(s, str) or not s:
            return None
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
        except Exception:
            parsed_date = helper_method.parse_date(s)
            return parsed_date.date() if isinstance(parsed_date, datetime) else None

    @staticmethod
    def _first_media(tweet: dict) -> str | None:
        media = tweet.get("media") or []
        if isinstance(media, list):
            for item in media:
                if item:
                    return str(item)
        return None

    def _is_target_hash_request(self, data_type: SocialDataType) -> bool:
        return data_type == SocialDataType.COMMENTS and bool(str(getattr(self, "m_hash_id", "") or "").strip())

    def _apply_saved_session(self, page) -> bool:
        context_id = id(page.context)
        if getattr(self, "_twitter_session_context_id", None) == context_id:
            return True

        sessions_dir = os.getenv("ORION_SESSION_ROOT") or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sessions")
        session_paths = [
            os.path.join(sessions_dir, "twitterscraper_session.json.gz"),
            os.path.join(sessions_dir, "_twitter_session.json.gz"),
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
                    local_storage = state.get("local_storage") or {}
                    session_storage = state.get("session_storage") or {}
                    for key, value in local_storage.items():
                        page.evaluate("([key, value]) => window.localStorage.setItem(key, value)", [key, value])
                    for key, value in session_storage.items():
                        page.evaluate("([key, value]) => window.sessionStorage.setItem(key, value)", [key, value])
                except Exception:
                    pass
                try:
                    page.goto(self.seed_url, wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(random.randint(1000, 2500))
                except Exception:
                    pass
                self._twitter_session_context_id = context_id
                return True
            except Exception:
                continue
        self._twitter_session_context_id = context_id
        return False

    def _item_limit(self) -> int:
        try:
            return max(1, min(int(getattr(self, "m_item_limit", 10) or 10), 100))
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
    def _normalize_profile_count(value) -> str:
        text = helper_method.scalar_text(value)
        if not text:
            return ""
        text = text.replace(",", "").strip()
        match = re.search(r"([\d.]+)\s*([KMB]?)", text, re.IGNORECASE)
        if not match:
            return text
        multiplier = {"K": 1000, "M": 1000000, "B": 1000000000}.get(match.group(2).upper(), 1)
        try:
            return str(int(float(match.group(1)) * multiplier))
        except Exception:
            return text

    @staticmethod
    def _comment_models(top_comments: list[dict]) -> tuple[list[str], list[str], list[social_comment_model]]:
        comment_texts = [helper_method.scalar_text(comment.get("text")) for comment in top_comments if helper_method.scalar_text(comment.get("text"))]
        commenters = [helper_method.scalar_text(comment.get("username")) for comment in top_comments if helper_method.scalar_text(comment.get("username"))]
        comments = [
            social_comment_model(
                m_username=helper_method.scalar_text(comment.get("username")) or None,
                m_time=helper_method.scalar_text(comment.get("time")) or None,
                m_likes=helper_method.scalar_text(comment.get("likes")) or None,
                m_text=helper_method.scalar_text(comment.get("text")) or None,
            )
            for comment in top_comments
            if helper_method.scalar_text(comment.get("text"))
        ]
        return comment_texts, commenters, comments

    @staticmethod
    def _extract_profile_assets(page, username: str) -> dict:
        try:
            page.wait_for_selector(
                'a[href$="/photo"] img, a[href*="/photo?"] img, '
                'a[href$="/header_photo"] img, a[href*="/header_photo?"] img, '
                'img[src*="profile_images"], img[src*="profile_banners"]',
                timeout=5000,
            )
        except Exception:
            pass

        try:
            return page.evaluate("""(username) => {
                const handle = String(username || '').replace(/^@/, '').toLowerCase();
                const cleanUrl = value => {
                    if (!value) return '';
                    let url = String(value).trim();
                    const cssUrl = url.match(/url\\(["']?([^"')]+)["']?\\)/);
                    if (cssUrl) url = cssUrl[1];
                    url = url.replace(/&amp;/g, '&').replace(/\\\\\\//g, '/');
                    if (!url || url.startsWith('data:') || /^(none|initial|inherit|unset)$/i.test(url.trim())) return '';
                    if (url.startsWith('//')) url = `https:${url}`;
                    if (url.startsWith('/')) url = `${location.origin}${url}`;
                    return url;
                };
                const srcFromImage = img => {
                    if (!img) return '';
                    const srcset = img.getAttribute('srcset') || '';
                    if (srcset) {
                        const candidates = srcset.split(',')
                            .map(item => item.trim().split(/\\s+/)[0])
                            .filter(Boolean);
                        if (candidates.length) return cleanUrl(candidates[candidates.length - 1]);
                    }
                    return cleanUrl(img.currentSrc || img.src || img.getAttribute('src'));
                };
                const pathMatches = (href, suffix) => {
                    try {
                        const url = new URL(href, location.href);
                        const parts = url.pathname.split('/').filter(Boolean).map(part => decodeURIComponent(part).toLowerCase());
                        return parts.length >= 2 && parts[0] === handle && parts[1] === suffix;
                    } catch {
                        return false;
                    }
                };
                const imageFromProfileLink = suffix => {
                    for (const link of document.querySelectorAll('a[href]')) {
                        if (!pathMatches(link.getAttribute('href') || link.href || '', suffix)) continue;
                        const src = srcFromImage(link.querySelector('img'));
                        if (src) return src;
                    }
                    return '';
                };
                const firstImage = selectors => {
                    for (const selector of selectors) {
                        const src = srcFromImage(document.querySelector(selector));
                        if (src) return src;
                    }
                    return '';
                };
                const metaImage = cleanUrl(
                    document.querySelector('meta[property="og:image"]')?.content ||
                    document.querySelector('meta[name="twitter:image"]')?.content ||
                    ''
                );
                const html = (document.documentElement.innerHTML || '').replace(/\\\\\\//g, '/').replace(/&amp;/g, '&');
                const htmlUrl = kind => {
                    const match = html.match(new RegExp(`https?://pbs\\\\.twimg\\\\.com/${kind}/[^"'<>\\\\s)]+`));
                    return match ? cleanUrl(match[0]) : '';
                };
                const firstText = selectors => {
                    for (const selector of selectors) {
                        const node = document.querySelector(selector);
                        const text = (node?.innerText || node?.textContent || '').trim();
                        if (text) return text;
                    }
                    return '';
                };
                const bodyLines = (document.body.innerText || '').split('\\n').map(line => line.trim()).filter(Boolean);
                const handleLineIndex = bodyLines.findIndex(line => line.toLowerCase() === `@${handle}`);
                const countText = label => {
                    for (const link of document.querySelectorAll('a[href]')) {
                        const text = (link.innerText || link.textContent || '').replace(/\\s+/g, ' ').trim();
                        if (!text || !text.toLowerCase().includes(label.toLowerCase())) continue;
                        try {
                            const url = new URL(link.getAttribute('href') || link.href || '', location.href);
                            const parts = url.pathname.split('/').filter(Boolean).map(part => decodeURIComponent(part).toLowerCase());
                            if (parts[0] === handle) return text;
                        } catch {}
                    }
                    return '';
                };
                const countFromLabel = (text, label) => {
                    const match = String(text || '').replace(/,/g, '').match(new RegExp(`([\\\\d.]+)\\\\s*([KMB]?)\\\\s*${label}`, 'i'));
                    if (!match) return '';
                    const value = parseFloat(match[1]);
                    const multiplier = {K: 1000, M: 1000000, B: 1000000000}[match[2].toUpperCase()] || 1;
                    return Number.isFinite(value) ? String(Math.round(value * multiplier)) : '';
                };
                const profileIcon = imageFromProfileLink('photo') ||
                    firstImage([
                        'main [data-testid^="UserAvatar-Container"] img',
                        '[data-testid^="UserAvatar-Container"] img',
                        'img[src*="profile_images"]'
                    ]) ||
                    (metaImage.includes('profile_images') ? metaImage : '') ||
                    htmlUrl('profile_images');
                const coverpage = imageFromProfileLink('header_photo') ||
                    firstImage([
                        'main img[src*="profile_banners"]',
                        'img[src*="profile_banners"]'
                    ]) ||
                    htmlUrl('profile_banners');
                const fullName = firstText([
                    '[data-testid="UserName"] div[dir="auto"] span span',
                    '[data-testid="UserName"] div[dir="auto"] span',
                    'h1[role="heading"]'
                ]) || (handleLineIndex > 0 ? bodyLines[handleLineIndex - 1] : '');
                const bio = firstText(['[data-testid="UserDescription"]']) ||
                    (handleLineIndex >= 0 && handleLineIndex + 1 < bodyLines.length ? bodyLines[handleLineIndex + 1] : '');
                const joined = firstText(['[data-testid="UserJoinDate"]']);
                const locationText = firstText(['[data-testid="UserLocation"]']);
                return {
                    profileIcon,
                    coverpage,
                    fullName,
                    bio,
                    joined,
                    location: locationText
                };
            }""", username)
        except Exception:
            return {}

    def _collect_comments(self, page, tweet_url: str, tweet_id: str | None, limit: int = 10, offset: int = 0) -> list[dict]:
        comments: list[dict] = []
        seen = set()
        idle_scrolls = 0
        limit = max(1, min(int(limit or 10), 10))
        offset = max(0, int(offset or 0))
        target_count = offset + limit

        try:
            page.goto(tweet_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(random.randint(1000, 2500))
        except Exception:
            return []

        for _ in range(30):
            try:
                page.evaluate("""() => {
                    for (const button of document.querySelectorAll('button, div[role="button"]')) {
                        const text = (button.innerText || button.textContent || '').toLowerCase();
                        if ((text.includes('show') || text.includes('more')) && (text.includes('reply') || text.includes('replies'))) {
                            try { button.click(); } catch (e) {}
                        }
                    }
                }""")
            except Exception:
                pass

            try:
                rows = page.evaluate("""(sourceTweetId) => {
                    const parseCount = value => {
                        const text = String(value || '').replace(/,/g, ' ');
                        const match = text.match(/([\\d.]+)\\s*([KMB]?)/i);
                        if (!match) return '';
                        const multiplier = {K: 1000, M: 1000000, B: 1000000000}[match[2].toUpperCase()] || 1;
                        const parsed = parseFloat(match[1]);
                        return Number.isFinite(parsed) ? String(Math.round(parsed * multiplier)) : '';
                    };
                    const handleFromArticle = article => {
                        for (const link of article.querySelectorAll('a[href^="/"], a[href^="https://x.com/"]')) {
                            try {
                                const url = new URL(link.getAttribute('href') || link.href || '', location.href);
                                const parts = url.pathname.split('/').filter(Boolean);
                                if (parts.length !== 1) continue;
                                const handle = decodeURIComponent(parts[0] || '');
                                if (/^[A-Za-z0-9_]{1,15}$/.test(handle) && !['i', 'home', 'search', 'explore', 'settings'].includes(handle.toLowerCase())) {
                                    return `@${handle}`;
                                }
                            } catch {}
                        }
                        return '';
                    };
                    const tweetIdFromArticle = article => {
                        const time = article.querySelector('time');
                        const timeLink = time?.closest('a[href*="/status/"]');
                        const timeMatch = String(timeLink?.getAttribute('href') || timeLink?.href || '').match(/\\/status\\/(\\d+)/);
                        if (timeMatch) return timeMatch[1];
                        const links = Array.from(article.querySelectorAll('a[href*="/status/"]'));
                        for (const link of links) {
                            if (!link.querySelector('time')) continue;
                            const match = String(link.getAttribute('href') || link.href || '').match(/\\/status\\/(\\d+)/);
                            if (match) return match[1];
                        }
                        for (const link of links) {
                            const match = String(link.getAttribute('href') || link.href || '').match(/\\/status\\/(\\d+)/);
                            if (match) return match[1];
                        }
                        return '';
                    };
                    return Array.from(document.querySelectorAll('article[data-testid="tweet"], article')).map((article, index) => {
                        const rowTweetId = tweetIdFromArticle(article);
                        if (index === 0 && sourceTweetId && rowTweetId === sourceTweetId) return null;
                        const text = Array.from(article.querySelectorAll('div[data-testid="tweetText"], div[lang]'))
                            .map(node => (node.innerText || node.textContent || '').trim())
                            .filter(Boolean)
                            .join(' ')
                            .trim();
                        if (!text) return null;
                        const likeButton = article.querySelector('button[data-testid="like"]');
                        const likes = parseCount(likeButton?.getAttribute('aria-label') || likeButton?.innerText || '');
                        return {
                            username: handleFromArticle(article),
                            time: article.querySelector('time')?.getAttribute('datetime') || article.querySelector('time')?.innerText || '',
                            likes,
                            text
                        };
                    }).filter(Boolean);
                }""", tweet_id or "")
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
                row["text"] = helper_method.filter_comments(text)
                if not row["text"]:
                    continue
                comments.append(row)
                if len(comments) >= target_count:
                    return comments[offset:target_count]

            idle_scrolls = idle_scrolls + 1 if len(comments) == before_count else 0
            if idle_scrolls >= 5:
                break
            try:
                page.mouse.wheel(0, 3500)
                page.wait_for_timeout(750)
            except Exception:
                break
        return comments[offset:target_count]

    def _append_profile_info(self, page, username: str):
        profile_assets = self._extract_profile_assets(page, username)
        group_info = " | ".join(
            item for item in [
                profile_assets.get("joined") or "",
                profile_assets.get("location") or "",
            ]
            if item
        )
        profile_content = profile_assets.get("bio") or (f"@{username}" if username else "")
        card_data = social_model(
            m_channel_url=self.seed_url,
            m_title=profile_assets.get("fullName") or (f"@{username}" if username else self.seed_url),
            m_sender_name=f"@{username}" if username else "",
            m_url=self.seed_url,
            m_message_sharable_link=self.seed_url,
            m_weblink=[self.seed_url],
            m_content=profile_content,
            m_content_type=["social_collector", "twitter_profile", "profile_info"],
            m_network="clearnet",
            m_date=datetime.now().date(),
            m_message_id=username,
            m_platform=[self.platform],
            m_group_name=f"@{username}" if username else None,
            m_group_info=group_info or None,
            m_img_src=profile_assets.get("profileIcon") or None,
            m_coverpage=profile_assets.get("coverpage") or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))

    def parse_leak_data(self, page):
        self._card_data = []
        self._entity_data = []
        try:
            page.wait_for_load_state("domcontentloaded", timeout=10000)
        except Exception:
            pass
        self._apply_saved_session(page)
        page.wait_for_timeout(1000)
        username = self._helper_methods.extract_username(self.seed_url)
        data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
        if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL):
            self._append_profile_info(page, username)
            return
        if data_type in (SocialDataType.VIDEOS, SocialDataType.SHORTS):
            return
        existing_ids = set()

        desired_count = self._item_limit()
        target_hash = self._is_target_hash_request(data_type)
        search_count = 100 if target_hash else desired_count
        load_comments = data_type == SocialDataType.COMMENTS

        tweets = self._helper_methods.scroll_and_collect(page, username, existing_ids, search_count, max_scrolls=20)
        new_tweets = []
        if not tweets:
            return

        for t in tweets:
            new_tweets.append(t)

        for tweet in new_tweets:
            raw_tweet_date = tweet.get("date")
            tweet_date = raw_tweet_date if isinstance(raw_tweet_date, str) else ""
            parsed_date = self._parse_iso(tweet_date)
            tweet_url = helper_method.scalar_text(tweet.get("url"))
            tweet_content = helper_method.scalar_text(tweet.get("content"))
            tweet_id = helper_method.scalar_text(tweet.get("id"))
            if not tweet_url or not tweet_id:
                continue
            tweet_weblink_value = tweet.get("weblink")
            tweet_weblink = [str(url) for url in tweet_weblink_value if url] if isinstance(tweet_weblink_value, list) else []
            title = tweet_content[:80] or f"Tweet by @{username}"
            card_data = social_model(
                m_title=title,
                m_channel_url=self.seed_url,
                m_sender_name=f"@{username}",
                m_url=tweet_url,
                m_message_sharable_link=tweet_url,
                m_weblink=tweet_weblink or ([tweet_url] if tweet_url else []),
                m_content=tweet_content,
                m_content_type=["social_collector", "twitter_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                m_network="clearnet",
                m_date=parsed_date,
                m_message_id=tweet_id,
                m_platform=[self.platform],
                m_post_likes=helper_method.scalar_text(tweet.get('likes') or 0),
                m_post_shares=helper_method.scalar_text(tweet.get('retweets')),
                m_likes=helper_method.scalar_text(tweet.get('likes') or 0),
                m_comment_count=helper_method.scalar_text(tweet.get('comment_count')),
                m_retweets=helper_method.scalar_text(tweet.get('retweets')),
                m_views=helper_method.scalar_text(tweet.get('views')),
                m_post_views=helper_method.scalar_text(tweet.get('views')),
                m_img_src=self._first_media(tweet),
                m_group_name=f"@{username}",
                m_scrap_file=self.__class__.__name__,
            )
            if target_hash:
                if not self._is_requested_hash_id(card_data):
                    continue
            elif self._is_requested_hash_id(card_data):
                break

            if load_comments and tweet_url:
                raw_comments = self._collect_comments(page, tweet_url, tweet_id, self._comment_limit(), self._comment_offset())
                comment_texts, commenters, comments = self._comment_models(raw_comments)
                card_data.m_comments = comments
                if comment_texts:
                    card_data.m_comment_count = str(len(comment_texts))
                card_data.m_commenters = commenters

            if target_hash:
                self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))
                return
            entity_data = entity_model(
                m_username=[username] if username else [],
            )

            self.append_leak_data(card_data, entity_data)
            page.wait_for_timeout(250)
