from abc import ABC
from datetime import datetime
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method


PLATFORM_CONFIG: Dict[str, Any] = {
    "name": "Blogger",
    "profile_url": "https://{username}.blogspot.com/",
    "domains": [
        "blogspot.com"
    ],
    "subdomain": True,
    "page_url": "https://{username}.blogspot.com/",
}


class _blogger(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.platform = "blogger"
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self.m_seed_url = ""
        self._initialized = None
        self._redis_instance = redis_controller()
        self._is_crawled = False

    def init_callback(self, callback=None):
        self.callback = callback

    @classmethod
    def supports(cls, platform: str) -> bool:
        return (platform or "").strip().lower() == "blogger"

    @staticmethod
    def _safe_direct_url(value: str) -> str | None:
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return None
        if parsed.scheme == "https":
            return value
        return parsed._replace(scheme="https").geturl()

    @staticmethod
    def _seed_parts(username: str, target_type: str | None = None) -> tuple[str, str]:
        target = (target_type or "profile").strip().lower()
        target = target if target in {"profile", "page", "group"} else "profile"
        value = (username or "").strip().strip("/")
        lower_value = value.lower()
        aliases = {
            "profile": ("profile:", "profile/", "profiles/", "user:", "user/", "users/", "u/", "@"),
            "page": ("page:", "page/", "pages/", "org:", "org/", "organization:", "organization/", "company:", "company/", "shop:", "shop/", "channel:", "channel/", "channels/"),
            "group": ("group:", "group/", "groups/", "community:", "community/", "communities/", "team:", "team/", "teams/"),
        }
        for mode, prefixes in aliases.items():
            for prefix in prefixes:
                if lower_value.startswith(prefix):
                    return mode, value[len(prefix):].strip().strip("/")
        return target, value

    @classmethod
    def build_seed_url(cls, username: str, data_type: SocialDataType | None = None, target_type: str | None = None) -> str:
        username = (username or "").strip()
        direct_url = cls._safe_direct_url(username)
        if direct_url:
            return direct_url
        cfg = PLATFORM_CONFIG
        target, raw_username = cls._seed_parts(username, target_type)
        clean = raw_username.strip().strip("/").lstrip("@")
        if target in {"page", "group"} and cfg.get(f"{target}_url"):
            template_key = f"{target}_url"
        else:
            template_key = "posts_url" if data_type == SocialDataType.POSTS and cfg.get("posts_url") else "profile_url"
        return str(cfg[template_key]).format(username=clean)

    @classmethod
    def public_platforms(cls) -> list[str]:
        return ["blogger"]

    @property
    def is_crawled(self) -> bool:
        return self._is_crawled

    @property
    def seed_url(self) -> str:
        return self.m_seed_url

    @property
    def base_url(self) -> str:
        try:
            parsed = urlparse(self.seed_url)
            return f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
        except Exception:
            return self.seed_url.rstrip("/")

    @property
    def developer_signature(self) -> str:
        return "Orion generic public web social scraper"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.NONE,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_resoource_block=False,
            m_threat_type=ThreatType.SOCIAL,
            m_rule_type=RuleType.BLOGGER,
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
        return self.base_url

    def _config(self) -> dict:
        return PLATFORM_CONFIG

    def _display_platform(self) -> str:
        return helper_method.scalar_text(self._config().get("name")) or self.platform

    def _username_from_url(self) -> str:
        raw = self.seed_url.rstrip("/")
        try:
            parsed = urlparse(raw)
            query = parse_qs(parsed.query)
            for key in ("user", "id", "acct"):
                value = query.get(key, [""])[0]
                if value:
                    return str(value).lstrip("@").strip()
            host = parsed.netloc.split(":")[0]
            parts = [part for part in parsed.path.split("/") if part]
            if self._config().get("subdomain"):
                first = host.split(".")[0]
                if first and first not in {"www", "m"}:
                    return first
            if parts:
                last = parts[-1]
                if last.lower() in {"profile", "profiles", "posts", "with_replies", "users", "user", "people", "member", "members", "shop", "channel", "channels", "group", "groups", "u", "id"} and len(parts) > 1:
                    last = parts[-2]
                return last.lstrip("@").replace("User:", "")
        except Exception:
            pass
        return raw.split("/")[-1].lstrip("@")

    @staticmethod
    def _clean_date(value: Any):
        raw = helper_method.scalar_text(value)
        if not raw:
            return datetime.now().date()
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
        except Exception:
            return datetime.now().date()

    @staticmethod
    def _extract_profile(page) -> dict:
        try:
            return page.evaluate("""async () => {
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                const absolutize = value => {
                    if (!value) return '';
                    let raw = String(value || '').trim();
                    if (raw.startsWith('//')) raw = `https:${raw}`;
                    try { return new URL(raw, location.href).href; } catch (_) { return raw; }
                };
                const meta = (...names) => {
                    for (const name of names) {
                        const node = document.querySelector(`meta[property="${name}"], meta[name="${name}"]`);
                        const value = clean(node?.getAttribute('content'));
                        if (value) return value;
                    }
                    return '';
                };
                const text = selector => clean(document.querySelector(selector)?.innerText);
                const feedValue = value => clean(value?.$t || value);
                const feedUrl = `${location.origin}/feeds/posts/default?alt=json&max-results=1`;
                let feed = null;
                try {
                    const res = await fetch(feedUrl, {headers: {accept: 'application/json'}, credentials: 'omit'});
                    if (res.ok) feed = await res.json();
                } catch (_) {}
                const images = Array.from(document.images).map(img => {
                    const rect = img.getBoundingClientRect();
                    return {
                        src: absolutize(img.currentSrc || img.src || img.getAttribute('src')),
                        width: rect.width || img.naturalWidth || img.width || 0,
                        height: rect.height || img.naturalHeight || img.height || 0,
                        top: rect.top || 0,
                    };
                }).filter(img => img.src && !img.src.startsWith('data:'));
                const feedAuthor = Array.isArray(feed?.feed?.author) ? feed.feed.author[0] : null;
                const profileIcon = absolutize(feedAuthor?.gd$image?.src)
                    || absolutize(meta('og:image', 'twitter:image'))
                    || images.find(img => img.width >= 48 && img.height >= 48 && img.width <= 320 && img.height <= 320)?.src
                    || '';
                const coverpage = images.find(img => img.width >= 500 && img.height >= 120 && img.top < 650 && img.src !== profileIcon)?.src || '';
                const alternate = (feed?.feed?.link || []).find(link => link.rel === 'alternate')?.href;
                const postCount = feedValue(feed?.feed?.openSearch$totalResults);
                const categories = (feed?.feed?.category || []).map(item => clean(item.term)).filter(Boolean).slice(0, 12);
                const statMatches = [
                    postCount ? `POSTS: ${postCount}` : '',
                    categories.length ? `CATEGORIES: ${categories.join(', ')}` : '',
                ].filter(Boolean);
                return {
                    title: feedValue(feed?.feed?.title) || clean(meta('og:title', 'twitter:title') || document.title || text('h1')),
                    bio: feedValue(feed?.feed?.subtitle) || clean(meta('og:description', 'twitter:description', 'description') || text('.description, header p, main p')),
                    canonical: absolutize(alternate || document.querySelector('link[rel="canonical"]')?.getAttribute('href')) || location.href,
                    profileIcon,
                    coverpage,
                    stats: statMatches.join(' | '),
                };
            }""") or {}
        except Exception:
            return {}

    @staticmethod
    def _extract_posts(page, limit: int) -> list[dict]:
        try:
            return page.evaluate("""async limit => {
                const clean = value => String(value || '')
                    .replace(/<script[\\s\\S]*?<\\/script>/gi, ' ')
                    .replace(/<style[\\s\\S]*?<\\/style>/gi, ' ')
                    .replace(/<div[^>]*class=["'][^"']*blogger-post-footer[^"']*["'][\\s\\S]*?<\\/div>/gi, ' ')
                    .replace(/<[^>]+>/g, ' ')
                    .replace(/&nbsp;/g, ' ')
                    .replace(/&amp;/g, '&')
                    .replace(/&#39;/g, "'")
                    .replace(/&quot;/g, '"')
                    .replace(/\\s+/g, ' ')
                    .trim();
                const absolutize = value => {
                    if (!value) return '';
                    let raw = String(value || '').trim();
                    if (raw.startsWith('//')) raw = `https:${raw}`;
                    try { return new URL(raw, location.href).href; } catch (_) { return raw; }
                };
                const feedValue = value => clean(value?.$t || value);
                const entryLink = (entry, rel) => {
                    const link = (entry.link || []).find(item => item.rel === rel);
                    return absolutize(link?.href || '');
                };
                const imageFromHtml = html => {
                    const doc = new DOMParser().parseFromString(String(html || ''), 'text/html');
                    const img = doc.querySelector('img[src], img[data-src]');
                    return absolutize(img?.getAttribute('src') || img?.getAttribute('data-src') || '');
                };
                const isPostUrl = value => {
                    const url = absolutize(value);
                    if (!url) return false;
                    try {
                        const parsed = new URL(url, location.href);
                        if (parsed.hostname !== location.hostname) return false;
                        if (/\\/feeds\\/|\\/comments\\/default|#comments/i.test(parsed.href)) return false;
                        return /\\/\\d{4}\\/\\d{2}\\/.+\\.html$/i.test(parsed.pathname) || parsed.pathname !== '/';
                    } catch (_) {
                        return false;
                    }
                };
                const fromFeed = [];
                try {
                    const feedUrl = `${location.origin}/feeds/posts/default?alt=json&max-results=${Math.max(1, Math.min(limit, 100))}`;
                    const res = await fetch(feedUrl, {headers: {accept: 'application/json'}, credentials: 'omit'});
                    if (res.ok) {
                        const data = await res.json();
                        for (const entry of data?.feed?.entry || []) {
                            const rawHtml = entry.content?.$t || entry.summary?.$t || '';
                            const url = entryLink(entry, 'alternate');
                            const title = feedValue(entry.title);
                            const id = feedValue(entry.id).split('.post-').pop();
                            fromFeed.push({
                                url,
                                title,
                                caption: clean(rawHtml || title).slice(0, 1200),
                                image: absolutize(entry.media$thumbnail?.url) || imageFromHtml(rawHtml),
                                timestamp: feedValue(entry.published) || feedValue(entry.updated),
                                updated: feedValue(entry.updated),
                                author: feedValue(entry.author?.[0]?.name),
                                messageId: id || url,
                                tags: (entry.category || []).map(item => clean(item.term)).filter(Boolean),
                            });
                        }
                    }
                } catch (_) {}
                const fromDom = [];
                const roots = Array.from(document.querySelectorAll('article.post, .post-outer, .blog-post, .post, article')).slice(0, Math.max(limit * 4, 20));
                for (const root of roots) {
                    const link = Array.from(root.querySelectorAll('a[href]'))
                        .map(a => ({href: absolutize(a.getAttribute('href')), text: clean(a.innerText || a.getAttribute('title'))}))
                        .find(item => isPostUrl(item.href) && item.href !== location.href);
                    const title = clean(root.querySelector('.post-title, .entry-title, h1, h2, h3')?.innerText || link?.text || '');
                    const caption = clean(root.querySelector('.post-body, .entry-content, [itemprop="articleBody"], p')?.innerText || root.innerText || title).slice(0, 1200);
                    const image = absolutize(root.querySelector('.post-body img, .entry-content img, img')?.currentSrc || root.querySelector('.post-body img, .entry-content img, img')?.src || '');
                    const timestamp = root.querySelector('time[datetime], abbr.published, abbr.updated')?.getAttribute('datetime') || clean(root.querySelector('.published, .post-timestamp, time')?.innerText || '');
                    if (link?.href || title || caption) fromDom.push({url: link?.href || '', title, caption, image, timestamp, messageId: link?.href || title});
                }
                const seen = new Set();
                return [...fromFeed, ...fromDom].filter(item => {
                    item.url = absolutize(item.url);
                    item.image = absolutize(item.image);
                    item.title = clean(item.title);
                    item.caption = clean(item.caption || item.title);
                    if (!isPostUrl(item.url) || !item.caption) return false;
                    const key = item.url;
                    if (seen.has(key)) return false;
                    seen.add(key);
                    return true;
                }).slice(0, limit);
            }""", limit) or []
        except Exception:
            return []

    def _append_profile_info(self, page):
        username = self._username_from_url()
        profile = self._extract_profile(page)
        title = helper_method.scalar_text(profile.get("title")) or username
        content = helper_method.scalar_text(profile.get("bio"))
        card_data = social_model(
            m_title=title,
            m_channel_url=self.seed_url,
            m_sender_name=username,
            m_url=helper_method.scalar_text(profile.get("canonical")) or self.seed_url,
            m_weblink=[helper_method.scalar_text(profile.get("canonical")) or self.seed_url],
            m_content=content,
            m_content_type=["social_collector", f"{self.platform}_profile", "profile_info"],
            m_network="clearnet",
            m_date=datetime.now().date(),
            m_message_id=username,
            m_platform=self.platform,
            m_group_name=username,
            m_group_info=helper_method.scalar_text(profile.get("stats")) or None,
            m_img_src=helper_method.scalar_text(profile.get("profileIcon")) or None,
            m_coverpage=helper_method.scalar_text(profile.get("coverpage")) or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))

    def parse_leak_data(self, page):
        self._card_data = []
        self._entity_data = []
        try:
            data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
            if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL):
                self._append_profile_info(page)
                return
            if data_type in (SocialDataType.VIDEOS, SocialDataType.SHORTS):
                data_type = SocialDataType.POSTS
            limit = max(1, min(int(getattr(self, "m_item_limit", 10) or 10), 100))
            try:
                for _ in range(3):
                    page.mouse.wheel(0, 1800)
                    page.wait_for_timeout(600)
            except Exception:
                pass
            username = self._username_from_url()
            posts = self._extract_posts(page, limit)
            for post in posts:
                post_url = helper_method.scalar_text(post.get("url")) or self.seed_url
                title = helper_method.scalar_text(post.get("title")) or "Post"
                caption = helper_method.scalar_text(post.get("caption")) or title
                media_url = helper_method.scalar_text(post.get("image"))
                sender_name = helper_method.scalar_text(post.get("author")) or username
                message_id = helper_method.scalar_text(post.get("messageId")) or post_url
                post_tags = post.get("tags") if isinstance(post.get("tags"), list) else []
                card_data = social_model(
                    m_title=title,
                    m_channel_url=self.seed_url,
                    m_sender_name=sender_name,
                    m_url=post_url,
                    m_message_sharable_link=post_url,
                    m_weblink=[post_url],
                    m_content=caption,
                    m_content_type=["social_collector", f"{self.platform}_post", "posts"],
                    m_network="clearnet",
                    m_date=self._clean_date(post.get("timestamp")),
                    m_message_id=message_id,
                    m_platform=self.platform,
                    m_img_src=media_url or None,
                    m_post_tags=[helper_method.scalar_text(tag) for tag in post_tags if helper_method.scalar_text(tag)],
                    m_group_name=username,
                    m_scrap_file=self.__class__.__name__,
                )
                self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))
        except Exception as ex:
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
