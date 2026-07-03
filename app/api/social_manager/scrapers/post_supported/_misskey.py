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
    "name": "Misskey",
    "profile_url": "https://misskey.io/@{username}",
    "domains": [
        "misskey.io"
    ]
}


class _misskey(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.platform = "misskey"
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
        return (platform or "").strip().lower() == "misskey"

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
        return ["misskey"]

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
            m_threat_type=ThreatType.MISSKEY,
            m_rule_type=RuleType.MISSKEY,
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
                const meta = (() => {
                    try {
                        return JSON.parse(document.querySelector('#misskey_meta')?.textContent || '{}');
                    } catch (_) {
                        return {};
                    }
                })();
                const pathParts = location.pathname.split('/').filter(Boolean);
                const tag = pathParts[0] === 'tags' ? pathParts[1] || '' : '';
                const account = pathParts.find(part => part.startsWith('@')) || '';
                let user = null;
                let postsCount = 0;
                if (tag) {
                    try {
                        const response = await fetch('/api/notes/search-by-tag', {
                            method: 'POST',
                            headers: {'content-type': 'application/json'},
                            body: JSON.stringify({tag, limit: 20}),
                        });
                        if (response.ok) {
                            const notes = await response.json();
                            postsCount = Array.isArray(notes) ? notes.filter(note => !note.replyId).length : 0;
                        }
                    } catch (_) {}
                } else if (account) {
                    const raw = account.slice(1);
                    const at = raw.indexOf('@');
                    const username = at >= 0 ? raw.slice(0, at) : raw;
                    const host = at >= 0 ? raw.slice(at + 1) : null;
                    try {
                        const response = await fetch('/api/users/show', {
                            method: 'POST',
                            headers: {'content-type': 'application/json'},
                            body: JSON.stringify({username, host}),
                        });
                        if (response.ok) user = await response.json();
                    } catch (_) {}
                }
                const title = tag
                    ? `Misskey tag: ${tag}`
                    : clean(user?.name || user?.username || document.title || meta.name || 'Misskey');
                const stats = [
                    tag ? `TAG: ${tag}` : '',
                    user?.notesCount != null ? `POSTS: ${user.notesCount}` : (tag ? `POSTS: ${postsCount}` : ''),
                ].filter(Boolean).join(' | ');
                return {
                    title,
                    bio: clean(htmlToText(user?.description) || meta.description || ''),
                    canonical: location.href,
                    profileIcon: absolutize(user?.avatarUrl || meta.iconUrl || document.querySelector('link[rel*="icon"]')?.getAttribute('href')),
                    coverpage: absolutize(user?.bannerUrl || meta.bannerUrl || ''),
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
                const postJson = async (path, body) => {
                    try {
                        const response = await fetch(path, {
                            method: 'POST',
                            headers: {'content-type': 'application/json'},
                            body: JSON.stringify(body),
                        });
                        if (!response.ok) return null;
                        return await response.json();
                    } catch (_) {
                        return null;
                    }
                };
                const pathParts = location.pathname.split('/').filter(Boolean);
                const tag = pathParts[0] === 'tags' ? pathParts[1] || '' : '';
                const account = pathParts.find(part => part.startsWith('@')) || '';
                let notes = [];
                if (tag) {
                    const result = await postJson('/api/notes/search-by-tag', {tag, limit: Math.min(Math.max(limit * 2, 10), 100)});
                    notes = Array.isArray(result) ? result : [];
                } else if (account) {
                    const raw = account.slice(1);
                    const at = raw.indexOf('@');
                    const username = at >= 0 ? raw.slice(0, at) : raw;
                    const host = at >= 0 ? raw.slice(at + 1) : null;
                    const user = await postJson('/api/users/show', {username, host});
                    if (user?.id) {
                        const result = await postJson('/api/users/notes', {userId: user.id, limit: Math.min(Math.max(limit * 2, 10), 100), withReplies: false, withFiles: false});
                        notes = Array.isArray(result) ? result : [];
                    }
                }
                const seen = new Set();
                return notes.filter(note => !note.replyId && clean(note.text || note.cw)).map(note => {
                    const user = note.user || {};
                    const username = user.host ? `${user.username}@${user.host}` : user.username;
                    const caption = clean([note.cw, note.text].filter(Boolean).join('\\n'));
                    const title = clean(caption.split('\\n')[0] || caption).slice(0, 180);
                    const firstFile = Array.isArray(note.files) ? note.files[0] : null;
                    return {
                        url: absolutize(note.url || `/notes/${note.id}`),
                        title,
                        caption,
                        image: absolutize(firstFile?.thumbnailUrl || firstFile?.url || user.avatarUrl || ''),
                        timestamp: note.createdAt || '',
                        author: clean(user.name || username || ''),
                        username: clean(username || ''),
                        messageId: clean(note.id || note.url || ''),
                        likeCount: note.reactionCount,
                        repostCount: note.renoteCount,
                        tags: Array.isArray(note.tags) ? note.tags.map(clean).filter(Boolean) : [],
                    };
                }).filter(item => {
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
                    m_platform=[self.platform],
                    m_img_src=media_url or None,
                    m_group_name=username,
                    m_likes=helper_method.scalar_text(post.get("likeCount")) or None,
                    m_retweets=helper_method.scalar_text(post.get("repostCount")) or None,
                    m_post_tags=[helper_method.scalar_text(tag) for tag in (post.get("tags") or []) if helper_method.scalar_text(tag)],
                    m_scrap_file=self.__class__.__name__,
                )
                entity_usernames = [value for value in {username, helper_method.scalar_text(post.get("username"))} if value]
                self.append_leak_data(card_data, entity_model(m_username=entity_usernames))
        except Exception as ex:
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
