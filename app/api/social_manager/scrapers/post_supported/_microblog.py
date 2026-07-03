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
    "name": "Micro.blog",
    "profile_url": "https://micro.blog/{username}",
    "domains": [
        "micro.blog"
    ]
}


class _microblog(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.platform = "microblog"
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
        return (platform or "").strip().lower() == "microblog"

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
        return ["microblog"]

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
            m_threat_type=ThreatType.MICROBLOG,
            m_rule_type=RuleType.MICROBLOG,
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
                if host.endswith("micro.blog") and len(parts) > 1 and parts[0].lower() not in {"discover", "posts"}:
                    return parts[0].lstrip("@")
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
                const pathParts = location.pathname.split('/').filter(Boolean);
                const tag = pathParts[0] === 'discover' ? pathParts[1] || '' : '';
                const username = pathParts[0] && pathParts[0] !== 'discover' && pathParts[0] !== 'posts' ? pathParts[0].replace(/^@/, '') : '';
                const feedLink = document.querySelector('link[rel="alternate"][type*="json" i]')?.getAttribute('href');
                const fetchPath = document.querySelector('#fetch_path')?.getAttribute('value');
                const feedUrl = absolutize(feedLink || fetchPath || (tag ? `/posts/discover/${tag}` : (username ? `/posts/${username}` : '')));
                let feed = null;
                let items = [];
                if (feedUrl) {
                    try {
                        const response = await fetch(feedUrl, {headers: {accept: 'application/feed+json, application/json'}});
                        if (response.ok) {
                            feed = await response.json();
                            items = Array.isArray(feed?.items) ? feed.items : [];
                        }
                    } catch (_) {}
                }
                const author = feed?.author || {};
                const micro = feed?._microblog || {};
                const title = tag
                    ? `Micro.blog discover: ${tag}`
                    : clean(author.name || feed?.title || text('#timeline_info b, h1') || meta('og:title', 'twitter:title') || document.title).replace(/^Micro\\.blog\\s+-\\s*/i, '');
                const stats = [
                    tag ? `TAG: ${tag}` : '',
                    `POSTS: ${items.length}`,
                ].filter(Boolean).join(' | ');
                return {
                    title,
                    bio: clean(micro.bio || text('.info_about_me') || meta('og:description', 'twitter:description', 'description')),
                    canonical: absolutize(author.url || document.querySelector('link[rel="canonical"]')?.getAttribute('href')) || location.href,
                    profileIcon: absolutize(author.avatar || meta('og:image', 'twitter:image') || document.querySelector('#timeline_info img')?.getAttribute('src') || document.querySelector('link[rel*="icon"]')?.getAttribute('href')),
                    coverpage: '',
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
                const fromHtml = html => {
                    if (!html) return {text: '', image: ''};
                    try {
                        const doc = new DOMParser().parseFromString(String(html), 'text/html');
                        return {
                            text: clean(doc.body?.innerText || ''),
                            image: absolutize(doc.querySelector('img')?.getAttribute('src') || ''),
                        };
                    } catch (_) {
                        return {text: clean(String(html || '').replace(/<[^>]+>/g, ' ')), image: ''};
                    }
                };
                const fromDom = Array.from(document.querySelectorAll('article.h-entry, article.post, .h-entry')).map(root => {
                    const contentNode = root.querySelector('.e-content') || root;
                    const caption = clean(contentNode?.innerText || root.innerText || '');
                    const title = clean(root.querySelector('.p-name, h1, h2')?.innerText || caption.split('\\n')[0] || document.title).slice(0, 180);
                    const parts = location.pathname.split('/').filter(Boolean);
                    const isMicroPermalink = location.hostname.endsWith('micro.blog') && parts.length > 1 && !['discover', 'posts'].includes(parts[0]);
                    const isMicroProfile = location.hostname.endsWith('micro.blog') && parts.length === 1 && !['discover', 'posts'].includes(parts[0]);
                    if (isMicroProfile) return null;
                    return {
                        url: isMicroPermalink ? location.href : absolutize(root.querySelector('.u-url[href]')?.getAttribute('href') || document.querySelector('link[rel="canonical"]')?.getAttribute('href') || location.href),
                        title,
                        caption,
                        image: absolutize(contentNode?.querySelector('img')?.getAttribute('src') || root.querySelector('img')?.getAttribute('src') || ''),
                        timestamp: root.querySelector('time[datetime], .dt-published')?.getAttribute('datetime') || '',
                        author: clean(document.querySelector('#timeline_info b, .site-title')?.innerText || ''),
                        username: '',
                        avatar: absolutize(document.querySelector('#timeline_info img, link[rel*="icon"]')?.getAttribute('src') || document.querySelector('link[rel*="icon"]')?.getAttribute('href') || ''),
                        messageId: ''
                    };
                }).filter(item => item && item.url && item.caption);
                const pathParts = location.pathname.split('/').filter(Boolean);
                const tag = pathParts[0] === 'discover' ? pathParts[1] || '' : '';
                const username = pathParts[0] && pathParts[0] !== 'discover' && pathParts[0] !== 'posts' ? pathParts[0].replace(/^@/, '') : '';
                const feedLink = document.querySelector('link[rel="alternate"][type*="json" i]')?.getAttribute('href');
                const fetchPath = document.querySelector('#fetch_path')?.getAttribute('value');
                const feedUrl = absolutize(feedLink || fetchPath || (tag ? `/posts/discover/${tag}` : (username ? `/posts/${username}` : '')));
                let feed = null;
                let items = [];
                try {
                    if (feedUrl) {
                        const response = await fetch(feedUrl, {headers: {accept: 'application/feed+json, application/json'}});
                        if (response.ok) {
                            feed = await response.json();
                            items = Array.isArray(feed?.items) ? feed.items : [];
                        }
                    }
                } catch (_) {
                }
                const seen = new Set();
                return [...fromDom, ...items.map(item => {
                    const parsed = fromHtml(item.content_html || item.summary || '');
                    const caption = clean(item.content_text || parsed.text || item.summary || item.title || '');
                    const title = clean(item.title || caption.split('\\n')[0] || caption).slice(0, 180);
                    const author = item.author || feed.author || {};
                    return {
                        url: absolutize(item.url || (author._microblog?.username && item.id ? `/${author._microblog.username}/${item.id}` : '')),
                        title,
                        caption,
                        image: absolutize(item.image || item.banner_image || parsed.image || author.avatar || ''),
                        timestamp: item.date_published || item.date_modified || '',
                        author: clean(author.name || author._microblog?.username || ''),
                        username: clean(author._microblog?.username || ''),
                        avatar: absolutize(author.avatar || ''),
                        messageId: clean(item.id || item.url || ''),
                        tags: Array.isArray(item.tags) ? item.tags.map(clean).filter(Boolean) : [],
                    };
                })].filter(item => {
                    if (!item.url || !item.caption) return false;
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
            m_message_sharable_link=helper_method.scalar_text(profile.get("canonical")) or self.seed_url,
            m_weblink=[helper_method.scalar_text(profile.get("canonical")) or self.seed_url],
            m_content=content,
            m_content_type=["social_collector", f"{self.platform}_profile", "profile_info"],
            m_network="clearnet",
            m_date=datetime.now().date(),
            m_message_id=username,
            m_platform=[self.platform],
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
            raw_limit = getattr(self, "m_item_limit", 10)
            limit = max(0, min(int(raw_limit if raw_limit is not None else 10), 100))
            if limit == 0:
                return
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
                    m_platform=[self.platform],
                    m_img_src=media_url or None,
                    m_group_name=username,
                    m_post_tags=[helper_method.scalar_text(tag) for tag in (post.get("tags") or []) if helper_method.scalar_text(tag)],
                    m_scrap_file=self.__class__.__name__,
                )
                entity_usernames = [value for value in {username, helper_method.scalar_text(post.get("username"))} if value]
                self.append_leak_data(card_data, entity_model(m_username=entity_usernames))
        except Exception as ex:
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
