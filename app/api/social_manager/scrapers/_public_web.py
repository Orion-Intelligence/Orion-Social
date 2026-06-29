from abc import ABC
from datetime import datetime
from typing import Any, Dict, List
from urllib.parse import urlparse

from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from crawler.crawler_services.shared.helper_method import helper_method


PUBLIC_WEB_PLATFORM_CONFIG: Dict[str, Dict[str, Any]] = {
    "pixelfed": {"name": "Pixelfed", "profile_url": "https://pixelfed.social/@{username}", "domains": ["pixelfed.social"]},
    "peertube": {"name": "PeerTube", "profile_url": "https://peertube.tv/a/{username}", "domains": ["peertube.tv"]},
    "lemmy": {"name": "Lemmy", "profile_url": "https://lemmy.world/u/{username}", "domains": ["lemmy.world"]},
    "misskey": {"name": "Misskey", "profile_url": "https://misskey.io/@{username}", "domains": ["misskey.io"]},
    "pleroma": {"name": "Pleroma", "profile_url": "https://pleroma.io/users/{username}", "domains": ["pleroma.io"]},
    "akkoma": {"name": "Akkoma", "profile_url": "https://akkoma.dev/users/{username}", "domains": ["akkoma.dev"]},
    "friendica": {"name": "Friendica", "profile_url": "https://friendica.social/profile/{username}", "domains": ["friendica.social"]},
    "hubzilla": {"name": "Hubzilla", "profile_url": "https://hubzilla.org/channel/{username}", "domains": ["hubzilla.org"]},
    "gotosocial": {"name": "GoToSocial", "profile_url": "https://gts.superseriousbusiness.org/@{username}", "domains": ["gts.superseriousbusiness.org"]},
    "bluesky": {"name": "Bluesky", "profile_url": "https://bsky.app/profile/{username}", "domains": ["bsky.app"]},
    "nostr": {"name": "Nostr", "profile_url": "https://primal.net/p/{username}", "domains": ["primal.net"]},
    "tumblr": {"name": "Tumblr", "profile_url": "https://{username}.tumblr.com/", "domains": ["tumblr.com"], "subdomain": True},
    "pinterest": {"name": "Pinterest", "profile_url": "https://www.pinterest.com/{username}/", "domains": ["pinterest.com"]},
    "flickr": {"name": "Flickr", "profile_url": "https://www.flickr.com/people/{username}/", "domains": ["flickr.com"]},
    "vimeo": {"name": "Vimeo", "profile_url": "https://vimeo.com/{username}", "domains": ["vimeo.com"]},
    "soundcloud": {"name": "SoundCloud", "profile_url": "https://soundcloud.com/{username}", "domains": ["soundcloud.com"]},
    "twitch": {"name": "Twitch", "profile_url": "https://www.twitch.tv/{username}", "domains": ["twitch.tv"]},
    "deviantart": {"name": "DeviantArt", "profile_url": "https://www.deviantart.com/{username}", "domains": ["deviantart.com"]},
    "behance": {"name": "Behance", "profile_url": "https://www.behance.net/{username}", "domains": ["behance.net"]},
    "dribbble": {"name": "Dribbble", "profile_url": "https://dribbble.com/{username}", "domains": ["dribbble.com"]},
    "artstation": {"name": "ArtStation", "profile_url": "https://www.artstation.com/{username}", "domains": ["artstation.com"]},
    "medium": {"name": "Medium", "profile_url": "https://medium.com/@{username}", "domains": ["medium.com"]},
    "substack": {"name": "Substack", "profile_url": "https://{username}.substack.com/", "domains": ["substack.com"], "subdomain": True},
    "wordpress": {"name": "WordPress.com", "profile_url": "https://{username}.wordpress.com/", "domains": ["wordpress.com"], "subdomain": True},
    "blogger": {"name": "Blogger", "profile_url": "https://{username}.blogspot.com/", "domains": ["blogspot.com"], "subdomain": True},
    "ghost": {"name": "Ghost", "profile_url": "https://{username}.ghost.io/", "domains": ["ghost.io"], "subdomain": True},
    "hashnode": {"name": "Hashnode", "profile_url": "https://hashnode.com/@{username}", "domains": ["hashnode.com"]},
    "devto": {"name": "DEV.to", "profile_url": "https://dev.to/{username}", "domains": ["dev.to"]},
    "forem": {"name": "Forem", "profile_url": "https://forem.com/{username}", "domains": ["forem.com"]},
    "microblog": {"name": "Micro.blog", "profile_url": "https://micro.blog/{username}", "domains": ["micro.blog"]},
    "github": {"name": "GitHub", "profile_url": "https://github.com/{username}", "domains": ["github.com"]},
    "gitlab": {"name": "GitLab", "profile_url": "https://gitlab.com/{username}", "domains": ["gitlab.com"]},
    "codeberg": {"name": "Codeberg", "profile_url": "https://codeberg.org/{username}", "domains": ["codeberg.org"]},
    "sourceforge": {"name": "SourceForge", "profile_url": "https://sourceforge.net/u/{username}/profile/", "domains": ["sourceforge.net"]},
    "stackoverflow": {"name": "Stack Overflow", "profile_url": "https://stackoverflow.com/users/{username}", "domains": ["stackoverflow.com"]},
    "hackernews": {"name": "Hacker News", "profile_url": "https://news.ycombinator.com/user?id={username}", "posts_url": "https://news.ycombinator.com/submitted?id={username}", "domains": ["news.ycombinator.com"]},
    "lobsters": {"name": "Lobsters", "profile_url": "https://lobste.rs/u/{username}", "domains": ["lobste.rs"]},
    "slashdot": {"name": "Slashdot", "profile_url": "https://slashdot.org/~{username}", "domains": ["slashdot.org"]},
    "tildes": {"name": "Tildes", "profile_url": "https://tildes.net/user/{username}", "domains": ["tildes.net"]},
    "producthunt": {"name": "Product Hunt", "profile_url": "https://www.producthunt.com/@{username}", "domains": ["producthunt.com"]},
    "indiehackers": {"name": "Indie Hackers", "profile_url": "https://www.indiehackers.com/{username}", "domains": ["indiehackers.com"]},
    "letterboxd": {"name": "Letterboxd", "profile_url": "https://letterboxd.com/{username}/", "domains": ["letterboxd.com"]},
    "lastfm": {"name": "Last.fm", "profile_url": "https://www.last.fm/user/{username}", "domains": ["last.fm"]},
    "steam": {"name": "Steam Community", "profile_url": "https://steamcommunity.com/id/{username}", "domains": ["steamcommunity.com"]},
    "bandcamp": {"name": "Bandcamp", "profile_url": "https://{username}.bandcamp.com/", "domains": ["bandcamp.com"], "subdomain": True},
    "mixcloud": {"name": "Mixcloud", "profile_url": "https://www.mixcloud.com/{username}/", "domains": ["mixcloud.com"]},
    "dailymotion": {"name": "Dailymotion", "profile_url": "https://www.dailymotion.com/{username}", "domains": ["dailymotion.com"]},
    "imgur": {"name": "Imgur", "profile_url": "https://imgur.com/user/{username}", "domains": ["imgur.com"]},
    "wikimedia_commons": {"name": "Wikimedia Commons", "profile_url": "https://commons.wikimedia.org/wiki/User:{username}", "domains": ["commons.wikimedia.org"]},
    "unsplash": {"name": "Unsplash", "profile_url": "https://unsplash.com/@{username}", "domains": ["unsplash.com"]},
    "500px": {"name": "500px", "profile_url": "https://500px.com/p/{username}", "domains": ["500px.com"]},
    "archive_org": {"name": "Internet Archive", "profile_url": "https://archive.org/details/@{username}", "domains": ["archive.org"]},
    "vk": {"name": "VK", "profile_url": "https://vk.com/{username}", "domains": ["vk.com"]},
    "ok_ru": {"name": "OK.ru", "profile_url": "https://ok.ru/{username}", "domains": ["ok.ru"]},
    "zhihu": {"name": "Zhihu", "profile_url": "https://www.zhihu.com/people/{username}", "domains": ["zhihu.com"]},
    "bilibili": {"name": "Bilibili", "profile_url": "https://space.bilibili.com/{username}", "domains": ["bilibili.com"]},
    "naver_blog": {"name": "Naver Blog", "profile_url": "https://blog.naver.com/{username}", "domains": ["blog.naver.com"]},
    "plurk": {"name": "Plurk", "profile_url": "https://www.plurk.com/{username}", "domains": ["plurk.com"]},
    "hatena_blog": {"name": "Hatena Blog", "profile_url": "https://{username}.hatenablog.com/", "domains": ["hatenablog.com"], "subdomain": True},
    "ameblo": {"name": "Ameba Blog", "profile_url": "https://ameblo.jp/{username}/", "domains": ["ameblo.jp"]},
    "telegram_public": {"name": "Telegram Public Channel", "profile_url": "https://t.me/s/{username}", "domains": ["t.me"]},
}


class _public_web(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None, platform: str | None = None):
        super().__init__()
        self.callback = callback
        self.platform = (platform or "").strip().lower()
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self.m_seed_url = ""
        self._initialized = None
        self._redis_instance = redis_controller()
        self._is_crawled = False

    def init_callback(self, callback=None):
        self.callback = callback

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @classmethod
    def supports(cls, platform: str) -> bool:
        return (platform or "").strip().lower() in PUBLIC_WEB_PLATFORM_CONFIG

    @classmethod
    def build_seed_url(cls, platform: str, username: str, data_type: SocialDataType | None = None) -> str:
        username = (username or "").strip()
        if username.startswith(("http://", "https://")):
            return username
        cfg = PUBLIC_WEB_PLATFORM_CONFIG.get((platform or "").strip().lower())
        if not cfg:
            return username
        clean = username.strip().strip("/").lstrip("@")
        template_key = "posts_url" if data_type == SocialDataType.POSTS and cfg.get("posts_url") else "profile_url"
        return str(cfg[template_key]).format(username=clean)

    @classmethod
    def public_platforms(cls) -> list[str]:
        return sorted(PUBLIC_WEB_PLATFORM_CONFIG)

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
            m_rule_type=RuleType.GENERIC,
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
        return PUBLIC_WEB_PLATFORM_CONFIG.get(self.platform, {})

    def _display_platform(self) -> str:
        return helper_method.scalar_text(self._config().get("name")) or self.platform

    def _username_from_url(self) -> str:
        raw = self.seed_url.rstrip("/")
        try:
            parsed = urlparse(raw)
            host = parsed.netloc.split(":")[0]
            parts = [part for part in parsed.path.split("/") if part]
            if self._config().get("subdomain"):
                first = host.split(".")[0]
                if first and first not in {"www", "m"}:
                    return first
            if parts:
                last = parts[-1]
                if last.lower() in {"profile", "posts", "with_replies"} and len(parts) > 1:
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
                const statMatches = Array.from(body.matchAll(/([0-9][0-9.,]*\\s*[KMBkmb]?)\\s+(followers|following|posts|articles|videos|tracks|projects|likes|photos)/g))
                    .slice(0, 16)
                    .map(match => `${match[2].toUpperCase()}: ${match[1]}`);
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
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                const absolutize = value => {
                    if (!value) return '';
                    try { return new URL(value, location.href).href; } catch (_) { return String(value || ''); }
                };
                const sameHost = value => {
                    try { return new URL(value, location.href).hostname === location.hostname; } catch (_) { return false; }
                };
                const badUrl = value => /\\/(login|signin|signup|register|settings|privacy|terms|about|help)(\\/|$)/i.test(value || '');
                const fromJsonLd = [];
                for (const node of document.querySelectorAll('script[type="application/ld+json"]')) {
                    try {
                        const parsed = JSON.parse(node.textContent || 'null');
                        const items = Array.isArray(parsed) ? parsed : [parsed];
                        for (const item of items) {
                            const graph = Array.isArray(item?.['@graph']) ? item['@graph'] : [item];
                            for (const entry of graph) {
                                const type = Array.isArray(entry?.['@type']) ? entry['@type'].join(' ') : String(entry?.['@type'] || '');
                                if (!/Posting|Article|VideoObject|ImageObject|CreativeWork|BlogPosting/i.test(type)) continue;
                                const url = absolutize(entry.url || entry.mainEntityOfPage?.['@id'] || entry['@id'] || '');
                                const title = clean(entry.headline || entry.name || entry.caption || '');
                                const caption = clean(entry.description || title);
                                const image = Array.isArray(entry.image) ? entry.image[0] : entry.image?.url || entry.thumbnailUrl || entry.image || '';
                                if (url || title || caption) fromJsonLd.push({url, title, caption, image: absolutize(image), timestamp: entry.datePublished || entry.uploadDate || ''});
                            }
                        }
                    } catch (_) {}
                }
                const roots = Array.from(document.querySelectorAll([
                    'article',
                    '[role="article"]',
                    '[data-testid*="post" i]',
                    '[class*="post" i]',
                    '[class*="entry" i]',
                    '[class*="article" i]',
                    '[class*="feed" i] > *',
                    'tr.athing',
                    '.pinWrapper',
                    '.streamItem',
                    '.sound',
                    '.video',
                    '.projectCover'
                ].join(','))).slice(0, Math.max(limit * 6, 30));
                const fromDom = roots.map(root => {
                    if (root.matches('tr.athing')) {
                        const titleNode = root.querySelector('.titleline a, .storylink');
                        const url = absolutize(titleNode?.getAttribute('href') || '');
                        const title = clean(titleNode?.innerText || '');
                        const subtext = clean(root.nextElementSibling?.innerText || '');
                        return {url, title, caption: subtext || title, image: '', timestamp: ''};
                    }
                    const linkNode = Array.from(root.querySelectorAll('a[href]')).find(a => {
                        const href = absolutize(a.getAttribute('href'));
                        return href && sameHost(href) && !badUrl(href) && href !== location.href;
                    });
                    const mediaNode = root.querySelector('img, video, source');
                    const title = clean(root.querySelector('h1,h2,h3,[class*="title" i],[class*="headline" i]')?.innerText || linkNode?.innerText || root.getAttribute('aria-label') || '');
                    const caption = clean(root.querySelector('[class*="content" i], [class*="description" i], [class*="caption" i], p')?.innerText || title || root.innerText || '');
                    const timestamp = root.querySelector('time[datetime]')?.getAttribute('datetime') || '';
                    const url = absolutize(linkNode?.getAttribute('href') || '');
                    const image = absolutize(mediaNode?.currentSrc || mediaNode?.src || mediaNode?.getAttribute('src') || '');
                    return {url, title, caption, image, timestamp};
                });
                const seen = new Set();
                return [...fromJsonLd, ...fromDom].filter(item => {
                    item.url = absolutize(item.url);
                    item.image = absolutize(item.image);
                    item.title = clean(item.title);
                    item.caption = clean(item.caption || item.title);
                    if (!item.url && !item.caption) return false;
                    const key = item.url || item.caption;
                    if (seen.has(key)) return false;
                    seen.add(key);
                    return true;
                }).slice(0, limit);
            }""", limit) or []
        except Exception:
            return []

    def _append_profile_info(self, page, data_type: SocialDataType):
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
            if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL, SocialDataType.FOLLOWERS, SocialDataType.FOLLOWING):
                self._append_profile_info(page, data_type)
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
                card_data = social_model(
                    m_title=title,
                    m_channel_url=self.seed_url,
                    m_sender_name=username,
                    m_url=post_url,
                    m_message_sharable_link=post_url,
                    m_weblink=[post_url],
                    m_content=caption,
                    m_content_type=["social_collector", f"{self.platform}_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                    m_network="clearnet",
                    m_date=self._clean_date(post.get("timestamp")),
                    m_message_id=post_url,
                    m_platform=self.platform,
                    m_img_src=media_url or None,
                    m_group_name=username,
                    m_scrap_file=self.__class__.__name__,
                )
                self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))
        except Exception as ex:
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
