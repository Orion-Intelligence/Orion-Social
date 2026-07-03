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
    "name": "HackerNoon",
    "profile_url": "https://hackernoon.com/u/{username}",
    "domains": [
        "hackernoon.com"
    ]
}


class _hackernoon(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.platform = "hackernoon"
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
        return (platform or "").strip().lower() == "hackernoon"

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
        return ["hackernoon"]

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
            m_rule_type=RuleType.HACKERNOON,
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
            return page.evaluate("""() => {
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                const absolutize = value => {
                    if (!value) return '';
                    try { return new URL(value, location.href).href; } catch (_) { return String(value || ''); }
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
                const images = Array.from(document.images).map(img => {
                    const rect = img.getBoundingClientRect();
                    return {
                        src: absolutize(img.currentSrc || img.src || img.getAttribute('src')),
                        width: rect.width || img.naturalWidth || img.width || 0,
                        height: rect.height || img.naturalHeight || img.height || 0,
                        top: rect.top || 0,
                    };
                }).filter(img => img.src && !img.src.startsWith('data:'));
                const profileIcon = absolutize(meta('og:image', 'twitter:image'))
                    || images.find(img => img.width >= 48 && img.height >= 48 && img.width <= 320 && img.height <= 320)?.src
                    || '';
                const coverpage = images.find(img => img.width >= 500 && img.height >= 120 && img.top < 650 && img.src !== profileIcon)?.src || '';
                const body = clean(document.body?.innerText || '');
                const tag = decodeURIComponent(location.pathname.split('/').filter(Boolean).pop() || '');
                const postCount = body.match(/([0-9][0-9.,]*)\\s+Blog Posts/i)?.[1] || '';
                const statMatches = [
                    tag ? `TAG: ${tag}` : '',
                    postCount ? `POSTS: ${postCount}` : '',
                ].filter(Boolean);
                return {
                    title: clean(meta('og:title', 'twitter:title') || document.title || text('h1')),
                    bio: clean(meta('og:description', 'twitter:description', 'description') || text('[data-testid*="bio" i], .bio, .description, header p, main p')),
                    canonical: absolutize(document.querySelector('link[rel="canonical"]')?.getAttribute('href')) || location.href,
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
            return page.evaluate("""limit => {
                const clean = value => String(value || '')
                    .replace(/<script[\\s\\S]*?<\\/script>/gi, ' ')
                    .replace(/<style[\\s\\S]*?<\\/style>/gi, ' ')
                    .replace(/<[^>]+>/g, ' ')
                    .replace(/&nbsp;/g, ' ')
                    .replace(/&amp;/g, '&')
                    .replace(/&quot;/g, '"')
                    .replace(/&#39;/g, "'")
                    .replace(/\\s+/g, ' ')
                    .trim();
                const absolutize = value => {
                    if (!value) return '';
                    try { return new URL(value, location.href).href; } catch (_) { return String(value || ''); }
                };
                const isArticleUrl = value => {
                    try {
                        const url = new URL(value, location.href);
                        if (url.hostname.replace(/^www\\./, '') !== 'hackernoon.com') return false;
                        const path = url.pathname.replace(/^\\//, '').replace(/\\/$/, '');
                        if (!path || path.includes('/')) return false;
                        if (/^(tagged|u|c|new|about|login|signup|newsletter|archive|careers|contact|privacy|terms)$/i.test(path)) return false;
                        return path.length > 12;
                    } catch (_) {
                        return false;
                    }
                };
                const cards = [];
                const cardRoot = (link, title) => {
                    let node = link;
                    for (let index = 0; node && index < 9; index += 1) {
                        const text = clean(node.innerText || node.textContent || '');
                        const lower = text.toLowerCase();
                        if (text.includes(title) && !lower.includes('trending stories')) return node;
                        node = node.parentElement;
                    }
                    return link.parentElement;
                };
                for (const link of Array.from(document.querySelectorAll('a[href]'))) {
                    const url = absolutize(link.getAttribute('href'));
                    const title = clean(link.innerText || link.getAttribute('aria-label') || link.getAttribute('title')).replace(/^Read story:\\s*/i, '');
                    if (!isArticleUrl(url) || title.length < 16) continue;
                    const root = cardRoot(link, title);
                    const text = clean(root?.innerText || title);
                    if (text.toLowerCase().includes('trending stories')) continue;
                    const media = root?.querySelector('img');
                    const author = clean(root?.querySelector('a[href^="/u/"], a[href*="hackernoon.com/u/"]')?.innerText || '');
                    const timestamp = text.match(/[A-Z][a-z]{2}\\s+\\d{1,2},\\s+\\d{4}/)?.[0] || '';
                    const tags = Array.from(root?.querySelectorAll('a[href*="/tagged/"]') || []).map(a => clean(a.innerText).replace(/^#/, '')).filter(Boolean);
                    cards.push({
                        url,
                        title,
                        caption: text || title,
                        image: absolutize(media?.currentSrc || media?.src || media?.getAttribute('src') || ''),
                        timestamp,
                        author,
                        messageId: new URL(url).pathname.replace(/^\\//, ''),
                        tags,
                    });
                }
                const seen = new Set();
                return cards.filter(item => {
                    item.url = absolutize(item.url);
                    item.image = absolutize(item.image);
                    item.title = clean(item.title);
                    item.caption = clean(item.caption || item.title);
                    if (!isArticleUrl(item.url) || !item.caption) return false;
                    const key = item.url || item.caption;
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
