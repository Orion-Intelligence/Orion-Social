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


PLATFORM_CONFIG: Dict[str, Any] = {
    "name": "LinkedIn",
    "profile_url": "https://www.linkedin.com/in/{username}/",
    "page_url": "https://www.linkedin.com/company/{username}/",
    "posts_url": "https://www.linkedin.com/company/{username}/",
    "domains": [
        "linkedin.com"
    ],
}


class _linkedin(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.platform = "linkedin"
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self.m_seed_url = ""
        self._initialized = None
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._last_status = ""
        self._last_reason = ""

    def init_callback(self, callback=None):
        self.callback = callback

    @classmethod
    def supports(cls, platform: str) -> bool:
        return (platform or "").strip().lower() == "linkedin"

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
        target = (target_type or "company").strip().lower()
        target = target if target in {"profile", "page", "company", "showcase", "in"} else "company"
        value = (username or "").strip().strip("/")
        lower_value = value.lower()
        aliases = {
            "profile": ("profile:", "profile/", "profiles/", "user:", "user/", "users/", "in/", "@"),
            "company": ("company:", "company/", "companies/", "org:", "org/", "organization:", "organization/"),
            "showcase": ("showcase:", "showcase/", "page:", "page/", "pages/"),
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
        target, raw_username = cls._seed_parts(username, target_type)
        clean = raw_username.strip().strip("/").lstrip("@")
        if target in {"showcase", "page"}:
            return f"https://www.linkedin.com/showcase/{clean}/"
        if target in {"profile", "in"}:
            return f"https://www.linkedin.com/in/{clean}/"
        return f"https://www.linkedin.com/company/{clean}/"

    @classmethod
    def public_platforms(cls) -> list[str]:
        return ["linkedin"]

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
            return "https://www.linkedin.com"

    @property
    def developer_signature(self) -> str:
        return "Orion LinkedIn public updates scraper"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.TOR,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_resoource_block=False,
            m_threat_type=ThreatType.LINKEDIN,
            m_rule_type=RuleType.LINKEDIN,
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
        return "https://www.linkedin.com/help/linkedin"

    def _config(self) -> dict:
        return PLATFORM_CONFIG

    def _display_platform(self) -> str:
        return helper_method.scalar_text(self._config().get("name")) or self.platform

    def _username_from_url(self) -> str:
        raw = self.seed_url.rstrip("/")
        try:
            parts = [part for part in urlparse(raw).path.split("/") if part]
            if len(parts) >= 2 and parts[0].lower() in {"company", "showcase", "in"}:
                return parts[1]
            if parts:
                return parts[-1]
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
    def _extract_posts(page, limit: int) -> list[dict]:
        try:
            return page.evaluate("""limit => {
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                const absolutize = value => {
                    if (!value) return '';
                    let raw = String(value || '').trim();
                    if (raw.startsWith('//')) raw = `https:${raw}`;
                    try { return new URL(raw, location.href).href; } catch (_) { return raw; }
                };
                const visibleText = node => clean(node?.innerText || node?.textContent || '');
                const attrUrl = (node, ...attrs) => {
                    for (const attr of attrs) {
                        const value = absolutize(node?.getAttribute(attr));
                        if (value) return value;
                    }
                    return '';
                };
                const section = document.querySelector('section[data-test-id="updates"], section.updates, section.core-section-container.updates') || document;
                const cardRoots = Array.from(section.querySelectorAll([
                    'article[data-id="main-feed-card"]',
                    'article.main-feed-activity-card',
                    '[data-test-id="updates"] article',
                    '.updates__list article'
                ].join(',')));
                const seen = new Set();
                const posts = [];
                for (const card of cardRoots) {
                    const wrapper = card.closest('[data-id="entire-feed-card-link"]') || card.closest('li') || card.parentElement || card;
                    const overlay = wrapper.querySelector('a[data-id="main-feed-card__full-link"], a.main-feed-card__overlay-link, a[href*="/posts/"]');
                    const postUrl = absolutize(overlay?.getAttribute('href') || card.querySelector('a[href*="/posts/"]')?.getAttribute('href') || '');
                    const commentary = card.querySelector('p[data-test-id="main-feed-activity-card__commentary"], .attributed-text-segment-list__content');
                    const content = visibleText(commentary);
                    const actorLink = card.querySelector('a[data-tracking-control-name*="feed-actor-name"], [data-test-id="main-feed-activity-card__entity-lockup"] a[href]');
                    const actor = visibleText(actorLink) || clean(actorLink?.getAttribute('aria-label') || '').replace(/^View organization page for /i, '');
                    const actorUrl = absolutize(actorLink?.getAttribute('href') || '');
                    const icon = card.querySelector('img.hue-web-entity__image, [data-test-id="main-feed-activity-card__entity-lockup"] img');
                    const profileIcon = attrUrl(icon, 'src', 'data-delayed-url', 'data-ghost-url');
                    const media = Array.from(card.querySelectorAll('[data-test-id="feed-images-content"] img, .feed-images-content img, img'))
                        .map(img => attrUrl(img, 'src', 'data-delayed-url'))
                        .filter(src => src && !src.includes('static.licdn.com/aero-v1/sc/h/') && src !== profileIcon);
                    const reactionsNode = card.querySelector('[data-test-id="social-actions__reaction-count"], [data-id="social-actions__reactions"]');
                    const reactions = clean(reactionsNode?.getAttribute('data-num-reactions') || visibleText(reactionsNode));
                    const hashtags = Array.from(card.querySelectorAll('a[href*="/feed/hashtag/"]'))
                        .map(a => visibleText(a).replace(/^#/, ''))
                        .filter(Boolean);
                    const activityUrn = clean(card.getAttribute('data-activity-urn') || card.getAttribute('data-featured-activity-urn') || card.getAttribute('data-attributed-urn'));
                    const timestamp = visibleText(card.querySelector('time')) || clean(card.querySelector('time')?.getAttribute('datetime'));
                    if ((!postUrl && !activityUrn) || !content) continue;
                    const key = postUrl || activityUrn || content;
                    if (seen.has(key)) continue;
                    seen.add(key);
                    posts.push({
                        url: postUrl,
                        title: content.slice(0, 160),
                        caption: content.slice(0, 2000),
                        image: media[0] || '',
                        media,
                        timestamp,
                        author: actor,
                        authorUrl: actorUrl,
                        profileIcon,
                        messageId: activityUrn || postUrl,
                        reactions,
                        tags: hashtags,
                    });
                    if (posts.length >= limit) break;
                }
                return posts;
            }""", limit) or []
        except Exception:
            return []

    @staticmethod
    def _page_gate_status(page) -> tuple[str, str]:
        try:
            state = page.evaluate("""() => {
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                return {
                    url: location.href,
                    title: document.title || '',
                    body: clean(document.body?.innerText || '').slice(0, 1200),
                    updates: !!document.querySelector('section[data-test-id="updates"], article.main-feed-activity-card, article[data-id="main-feed-card"]'),
                };
            }""") or {}
        except Exception:
            return "", ""
        if state.get("updates"):
            return "", ""
        url = helper_method.scalar_text(state.get("url")).lower()
        title = helper_method.scalar_text(state.get("title")).lower()
        body = helper_method.scalar_text(state.get("body")).lower()
        if (
            "/uas/login" in url
            or "linkedin: log in or sign up" in title
            or "welcome to your professional community" in body
            or "sign in with email" in body
        ):
            return "auth_required", helper_method.scalar_text(state.get("body"))[:220]
        return "", ""

    def parse_leak_data(self, page):
        self._card_data = []
        self._entity_data = []
        try:
            data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
            if data_type not in (SocialDataType.DEFAULT, SocialDataType.POSTS):
                self._last_status = "unsupported_data_type"
                self._last_reason = "LinkedIn scraper supports posts only"
                return
            limit = max(1, min(int(getattr(self, "m_item_limit", 10) or 10), 100))
            try:
                page.wait_for_selector('section[data-test-id="updates"], article.main-feed-activity-card, article[data-id="main-feed-card"]', timeout=8000)
            except Exception:
                pass
            gate_status, gate_reason = self._page_gate_status(page)
            if gate_status:
                self._last_status = gate_status
                self._last_reason = gate_reason
                return
            try:
                for _ in range(3):
                    page.mouse.wheel(0, 1800)
                    page.wait_for_timeout(500)
            except Exception:
                pass
            username = self._username_from_url()
            posts = self._extract_posts(page, limit)
            if not posts:
                self._last_status = "no_public_posts"
                self._last_reason = "No public LinkedIn Updates cards were found"
                return
            for post in posts:
                post_url = helper_method.scalar_text(post.get("url")) or self.seed_url
                title = helper_method.scalar_text(post.get("title")) or "LinkedIn update"
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
                    m_content_type=["social_collector", "linkedin_post", "posts"],
                    m_network="clearnet",
                    m_date=self._clean_date(post.get("timestamp")),
                    m_message_id=message_id,
                    m_platform=[self.platform],
                    m_group_name=sender_name,
                    m_post_likes=helper_method.scalar_text(post.get("reactions")) or None,
                    m_likes=helper_method.scalar_text(post.get("reactions")) or None,
                    m_img_src=media_url or helper_method.scalar_text(post.get("profileIcon")) or None,
                    m_post_tags=[helper_method.scalar_text(tag) for tag in post_tags if helper_method.scalar_text(tag)],
                    m_scrap_file=self.__class__.__name__,
                )
                self.append_leak_data(
                    card_data,
                    entity_model(
                        m_username=[username] if username else [],
                        m_company_name=sender_name,
                        m_social_media_profiles=[helper_method.scalar_text(post.get("authorUrl")) or self.seed_url],
                    ),
                )
            self._last_status = "active"
            self._last_reason = ""
        except Exception as ex:
            self._last_status = "parse_error"
            self._last_reason = str(ex)
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
