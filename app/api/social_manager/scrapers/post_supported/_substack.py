from abc import ABC
from datetime import datetime
from email.utils import parsedate_to_datetime
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
    "name": "Substack",
    "profile_url": "https://{username}.substack.com/",
    "domains": [
        "substack.com"
    ],
    "subdomain": True,
    "page_url": "https://{username}.substack.com/",
}


class _substack(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.platform = "substack"
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
        return (platform or "").strip().lower() == "substack"

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
        return ["substack"]

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
            m_rule_type=RuleType.SUBSTACK,
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
            pass
        try:
            return parsedate_to_datetime(raw).date()
        except Exception:
            return datetime.now().date()

    @staticmethod
    def _extract_profile(page) -> dict:
        try:
            return page.evaluate("""async () => {
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
                const getText = node => clean(node?.textContent || '');
                let channel = {};
                try {
                    const response = await fetch('/feed', {headers: {accept: 'application/rss+xml, text/xml'}});
                    if (response.ok) {
                        const xml = new DOMParser().parseFromString(await response.text(), 'text/xml');
                        const root = xml.querySelector('channel');
                        channel = {
                            title: getText(root?.querySelector('title')),
                            description: getText(root?.querySelector('description')),
                            link: getText(root?.querySelector('link')),
                            image: getText(root?.querySelector('image url')),
                        };
                    }
                } catch (_) {}
                let postsCount = '';
                try {
                    const response = await fetch('/api/v1/archive?sort=new&search=&offset=0&limit=20', {headers: {accept: 'application/json'}});
                    if (response.ok) {
                        const posts = await response.json();
                        postsCount = Array.isArray(posts) ? posts.length : '';
                    }
                } catch (_) {}
                const stats = postsCount !== '' && postsCount != null ? `POSTS: ${postsCount}` : '';
                return {
                    title: clean(channel.title || meta('og:title', 'twitter:title') || document.title).replace(/\\s+\\|\\s+Substack$/i, ''),
                    bio: clean(channel.description || meta('og:description', 'twitter:description', 'description')),
                    canonical: absolutize(channel.link || document.querySelector('link[rel="canonical"]')?.getAttribute('href')) || location.href,
                    profileIcon: absolutize(channel.image || meta('og:image', 'twitter:image') || document.querySelector('link[rel*="icon"]')?.getAttribute('href')),
                    coverpage: absolutize(meta('og:image', 'twitter:image')),
                    stats,
                };
            }""") or {}
        except Exception:
            return {}

    @staticmethod
    def _extract_posts(page, limit: int) -> list[dict]:
        try:
            return page.evaluate("""async limit => {
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                const absolutize = value => {
                    if (!value) return '';
                    try { return new URL(value, location.href).href; } catch (_) { return String(value || ''); }
                };
                const htmlToText = html => {
                    if (!html) return '';
                    try {
                        return clean(new DOMParser().parseFromString(String(html), 'text/html').body?.innerText || '');
                    } catch (_) {
                        return clean(String(html || '').replace(/<[^>]+>/g, ' '));
                    }
                };
                let posts = [];
                try {
                    const response = await fetch(`/api/v1/archive?sort=new&search=&offset=0&limit=${Math.min(Math.max(limit, 1), 100)}`, {headers: {accept: 'application/json'}});
                    if (response.ok) {
                        const data = await response.json();
                        if (Array.isArray(data)) {
                            posts = data.map(post => {
                                const byline = Array.isArray(post.publishedBylines) ? post.publishedBylines[0] : null;
                                const tags = Array.isArray(post.postTags) ? post.postTags.map(tag => clean(tag.name || tag.slug || tag)).filter(Boolean) : [];
                                return {
                                    url: absolutize(post.canonical_url || (post.slug ? `/p/${post.slug}` : '')),
                                    title: clean(post.title || post.social_title || ''),
                                    caption: clean(post.description || post.truncated_body_text || htmlToText(post.body_html) || post.title || ''),
                                    image: absolutize(post.cover_image || byline?.photo_url || ''),
                                    timestamp: post.post_date || '',
                                    author: clean(byline?.name || ''),
                                    username: clean(byline?.handle || ''),
                                    messageId: clean(post.id || post.slug || post.canonical_url || ''),
                                    likeCount: post.reaction_count,
                                    tags,
                                };
                            });
                        }
                    }
                } catch (_) {}
                if (!posts.length) {
                    try {
                        const response = await fetch('/feed', {headers: {accept: 'application/rss+xml, text/xml'}});
                        if (response.ok) {
                            const xml = new DOMParser().parseFromString(await response.text(), 'text/xml');
                            posts = Array.from(xml.querySelectorAll('item')).map(item => {
                                const encoded = item.getElementsByTagName('content:encoded')[0]?.textContent || '';
                                const creator = item.getElementsByTagName('dc:creator')[0]?.textContent || '';
                                return {
                                    url: absolutize(item.querySelector('link')?.textContent || ''),
                                    title: clean(item.querySelector('title')?.textContent || ''),
                                    caption: clean(item.querySelector('description')?.textContent || htmlToText(encoded) || ''),
                                    image: absolutize(new DOMParser().parseFromString(encoded, 'text/html').querySelector('img')?.getAttribute('src') || ''),
                                    timestamp: item.querySelector('pubDate')?.textContent || '',
                                    author: clean(creator),
                                    username: clean(creator),
                                    messageId: clean(item.querySelector('guid')?.textContent || item.querySelector('link')?.textContent || ''),
                                    tags: Array.from(item.querySelectorAll('category')).map(node => clean(node.textContent)).filter(Boolean),
                                };
                            });
                        }
                    } catch (_) {}
                }
                const seen = new Set();
                return posts.filter(item => {
                    item.url = absolutize(item.url);
                    item.image = absolutize(item.image);
                    item.title = clean(item.title);
                    item.caption = clean(item.caption || item.title);
                    if (!item.url || !item.title) return false;
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
                    m_group_name=username,
                    m_likes=helper_method.scalar_text(post.get("likeCount")) or None,
                    m_post_tags=[helper_method.scalar_text(tag) for tag in (post.get("tags") or []) if helper_method.scalar_text(tag)],
                    m_scrap_file=self.__class__.__name__,
                )
                entity_usernames = [value for value in {username, helper_method.scalar_text(post.get("username"))} if value]
                self.append_leak_data(card_data, entity_model(m_username=entity_usernames))
        except Exception as ex:
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
