import hashlib
import random
import re
from datetime import datetime, timedelta, UTC
from abc import ABC
from typing import List
from urllib.parse import parse_qs, unquote, urlsplit

from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_comment_model, social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.redis_manager.redis_controller import redis_controller


class _linkedin(extraction_interface, ABC):
    _instance = None
    persistent_session = True
    PAGE_READY_SELECTOR = "h1, h2"
    POST_SELECTOR = "div.feed-shared-update-v2"

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self.soup = None
        self._initialized = None
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self.m_seed_url = "https://www.linkedin.com/company/hackerone/"
        self._subreddit_metadata = {}
        self._last_status = ""
        self._last_reason = ""

    def init_callback(self, callback=None):
        self.callback = callback

    def __new__(cls):
        return super().__new__(cls)

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
        return "https://www.linkedin.com/feed/"

    @property
    def rule_config(self) -> RuleModel:
        return RuleModel(
            m_fetch_proxy=FetchProxy.NONE,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_threat_type=ThreatType.LINKEDIN,
            m_rule_type=RuleType.LINKEDIN,
            m_social_data_type=getattr(self, "m_social_data_type", SocialDataType.DEFAULT),
            m_resoource_block=False,
        )

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def contact_page(self) -> str:
        return "https://www.linkedin.com/help/linkedin"

    def invoke_db(self, command: int, key: str, default_value, expiry: int | None = None):
        return self._redis_instance.invoke_trigger(
            command, [key + self.__class__.__name__, default_value, expiry]
        )

    @staticmethod
    def _public_identifier(seed_url):
        path_parts = [part for part in urlsplit(seed_url).path.split("/") if part]
        for marker in ("company", "in", "school"):
            if marker in path_parts:
                marker_index = path_parts.index(marker)
                if marker_index + 1 < len(path_parts):
                    return path_parts[marker_index + 1]
        return path_parts[-1] if path_parts else ""

    @staticmethod
    def _activity_url(seed_url, is_company, username):
        split_url = urlsplit(seed_url)
        base_url = f"{split_url.scheme or 'https'}://{split_url.netloc or 'www.linkedin.com'}"
        if is_company:
            return f"{base_url}/company/{username}/posts/?feedView=all"
        return f"{base_url}/in/{username}/recent-activity/all/"

    @staticmethod
    def _session_required(page):
        current_url = page.url.lower()
        if "/login" in current_url or "/checkpoint" in current_url or "/uas/" in current_url:
            return True
        login_inputs = page.locator(
            "input[name='session_key'], input#session_key, "
            "input[name='session_password'], input#session_password, input#password"
        )
        return login_inputs.count() > 0

    def _item_limit(self) -> int:
        try:
            explicit_limit = int(getattr(self, "m_item_limit", 0) or 0)
            if explicit_limit:
                return max(1, min(explicit_limit, 100))
        except Exception:
            pass
        return 10 if self.is_crawled else 3

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
        return bool(requested_hash_id and url and social_model.unique_identifier("linkedin", url, "", "", "") == requested_hash_id)

    @staticmethod
    def _clean_text(value) -> str:
        return re.sub(r"\s+", " ", str(value or "")).strip()

    @staticmethod
    def _strip_tracking_url(url: str) -> str:
        if not url:
            return ""
        try:
            split_url = urlsplit(url)
            if split_url.netloc.endswith("linkedin.com") and split_url.path.startswith("/redir/redirect"):
                target = parse_qs(split_url.query).get("url", [""])[0]
                return unquote(target) if target else url
            if split_url.query:
                kept_query = "&".join(
                    part for part in split_url.query.split("&")
                    if part and not part.startswith("trk=") and not part.startswith("trkInfo=")
                )
                return split_url._replace(query=kept_query).geturl()
        except Exception:
            pass
        return url

    @staticmethod
    def _parse_relative_date(value: str):
        text = _linkedin._clean_text(value).lower()
        today = datetime.now(UTC).date()
        if not text:
            return today
        if text in {"now", "today"}:
            return today
        match = re.match(r"^(\d+)\s*([mhdw])$", text)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            if unit in {"m", "h"}:
                return today
            if unit == "d":
                return today - timedelta(days=amount)
            if unit == "w":
                return today - timedelta(days=amount * 7)
        match = re.match(r"^(\d+)\s*(month|months|mo|mos)$", text)
        if match:
            return today - timedelta(days=int(match.group(1)) * 30)
        match = re.match(r"^(\d+)\s*(year|years|yr|yrs)$", text)
        if match:
            return today - timedelta(days=int(match.group(1)) * 365)
        return today

    @staticmethod
    def _public_post_rows(page, limit: int) -> list[dict]:
        try:
            return page.evaluate("""(limit) => {
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                const srcsetUrl = value => String(value || '').split(',').pop().trim().split(/\\s+/)[0] || '';
                const roots = [
                    document.querySelector('[data-test-id="updates"], .updates'),
                    document.querySelector('main'),
                    document.body
                ].filter(Boolean);
                const cards = [];
                const seenCards = new Set();
                for (const root of roots) {
                    for (const card of root.querySelectorAll('article.main-feed-activity-card, article, [data-test-id*="feed" i], [class*="feed-activity-card"]')) {
                        if (seenCards.has(card)) continue;
                        seenCards.add(card);
                        cards.push(card);
                    }
                }
                const rows = [];
                for (const card of cards) {
                    if (rows.length >= limit) break;
                    const content = clean(
                        card.querySelector('.attributed-text-segment-list__content')?.innerText ||
                        card.querySelector('[class*="attributed-text"]')?.innerText ||
                        ''
                    );
                    const articleTitle = clean(card.querySelector('.tw-feed-content-title')?.innerText || '');
                    const articleSubtitle = clean(card.querySelector('.tw-feed-content-subtitle')?.innerText || '');
                    const actorRoot = card.querySelector('.base-main-feed-card__entity-lockup') || card;
                    const actorName = clean(
                        actorRoot.querySelector('a[href*="/company/"], a[href*="/showcase/"], a[href*="/in/"]')?.innerText ||
                        actorRoot.querySelector('a')?.innerText ||
                        ''
                    );
                    const followerText = clean(
                        actorRoot.querySelector('p')?.innerText ||
                        card.innerText.match(/[\\d,.]+\\s*(?:K|M|B)?\\s+followers/i)?.[0] ||
                        ''
                    );
                    const timeText = clean(card.querySelector('time')?.innerText || '');
                    const reactionsLabel = card.querySelector('a[aria-label*="Reaction" i], a[aria-label*="Like" i]')?.getAttribute('aria-label') || '';
                    const reactionsText = clean(
                        card.querySelector('a[aria-label*="Reaction" i] span, a[aria-label*="Like" i] span')?.innerText ||
                        reactionsLabel
                    );
                    const commentsText = clean(
                        Array.from(card.querySelectorAll('a')).find(a => /comments?/i.test(clean(a.innerText)))?.innerText ||
                        ''
                    );
                    const links = Array.from(card.querySelectorAll('a[href]')).map(a => a.href || a.getAttribute('href') || '')
                        .filter(href => href && !/\\/signup|\\/uas\\/login|\\/authwall|guest-reporting|social-actions|like-cta|comment-cta|share-cta/i.test(href));
                    const media = Array.from(card.querySelectorAll('img')).map(img => {
                        const rect = img.getBoundingClientRect();
                        return {
                            src: img.currentSrc || img.src || img.getAttribute('src') || srcsetUrl(img.getAttribute('srcset')) || '',
                            alt: img.alt || '',
                            width: rect.width || img.naturalWidth || img.width || 0,
                            height: rect.height || img.naturalHeight || img.height || 0
                        };
                    }).filter(img => img.src && !/profile|logo|avatar|icon/i.test(img.alt));
                    const text = content || articleTitle;
                    if (!text) continue;
                    rows.push({
                        actorName,
                        followerText,
                        timeText,
                        content,
                        articleTitle,
                        articleSubtitle,
                        reactionsText,
                        commentsText,
                        links,
                        mediaUrl: media[0]?.src || ''
                    });
                }
                return rows;
            }""", limit)
        except Exception:
            return []

    @staticmethod
    def _extract_public_profile_info(page, username: str) -> dict:
        try:
            return page.evaluate("""(username) => {
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                const removeHeading = (text, heading) => clean(text).replace(new RegExp('^' + heading + '\\\\s*', 'i'), '').trim();
                const title = clean(document.querySelector('h1')?.innerText) ||
                    clean(document.querySelector('meta[property="og:title"]')?.content).replace(/\\s*\\|\\s*LinkedIn.*$/i, '') ||
                    username;
                const bodyText = document.body?.innerText || '';
                const followers = clean((bodyText.match(/[\\d,.]+\\s*(?:K|M|B)?\\s+followers/i) || [''])[0]);
                const topCard = document.querySelector('.top-card-layout') || document.querySelector('main');
                const topText = clean(topCard?.innerText || '');
                const aboutSection = document.querySelector('[data-test-id="about-us"]');
                const aboutText = removeHeading(aboutSection?.innerText || '', 'About us');
                const industry = clean(topCard?.querySelector('h2, h3')?.innerText || '');
                const location = clean((topText.match(/(?:^|\\s)([A-Z][A-Za-z .'-]+,\\s*[A-Z]{2})(?:\\s|$)/) || [,''])[1]);
                return {title, followers, topText, aboutText, industry, location};
            }""", username) or {}
        except Exception:
            return {}

    def _append_public_update_cards(
        self,
        page,
        username: str,
        real_name: str,
        about_text: str,
        connections_text: str,
        data_type: SocialDataType,
    ) -> int:
        desired_count = self._item_limit()
        target_hash = self._is_target_hash_request(data_type)
        rows = self._public_post_rows(page, 100 if target_hash else desired_count)
        appended = 0
        seen = set()
        for index, row in enumerate(rows):
            content = self._clean_text(row.get("content"))
            article_title = self._clean_text(row.get("articleTitle"))
            actor_name = self._clean_text(row.get("actorName")) or real_name or username
            raw_links = row.get("links") or []
            links = []
            for link in raw_links:
                clean_link = self._strip_tracking_url(str(link))
                if clean_link and clean_link not in links:
                    links.append(clean_link)
            stable_source = "|".join([
                self.seed_url,
                actor_name,
                self._clean_text(row.get("timeText")),
                content,
                article_title,
            ])
            fallback_hash = hashlib.sha256(stable_source.encode("utf-8")).hexdigest()
            post_url = next((link for link in links if "/feed/update/" in link or "/posts/" in link or "activity-" in link), "")
            post_url = post_url or f"{self.seed_url.rstrip('/')}#update-{fallback_hash[:16]}"
            if post_url in seen:
                continue
            seen.add(post_url)
            if target_hash and not self._is_requested_hash_url(post_url):
                continue
            if not target_hash and self._is_requested_hash_url(post_url):
                break
            comments_text = self._clean_text(row.get("commentsText"))
            comments_match = re.search(r"([\d,]+)", comments_text)
            comment_count = comments_match.group(1).replace(",", "") if comments_match else None
            reactions_text = self._clean_text(row.get("reactionsText"))
            likes_match = re.search(r"([\d,]+)", reactions_text)
            likes = likes_match.group(1).replace(",", "") if likes_match else reactions_text or "0"
            full_content = content
            if article_title and article_title not in full_content:
                full_content = f"{full_content}\n\n{article_title}".strip()
            if row.get("articleSubtitle") and row["articleSubtitle"] not in full_content:
                full_content = f"{full_content}\n{self._clean_text(row['articleSubtitle'])}".strip()
            post_id = hashlib.sha256(post_url.encode("utf-8")).hexdigest()
            card_data = social_model(
                m_channel_url=self.seed_url,
                m_title=(content or article_title or username)[:80],
                m_sender_name=actor_name,
                m_url=post_url,
                m_message_sharable_link=post_url,
                m_weblink=links or [post_url],
                m_content=full_content,
                m_content_type=["social_collector", "linkedin_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                m_network="clearnet",
                m_date=self._parse_relative_date(self._clean_text(row.get("timeText"))),
                m_message_id=post_id,
                m_platform="linkedin",
                m_group_name=username,
                m_group_info=f"{connections_text} | {about_text}".strip(" |") or self._clean_text(row.get("followerText")) or None,
                m_post_likes=likes,
                m_comment_count=comment_count,
                m_img_src=self._clean_text(row.get("mediaUrl")) or None,
                m_scrap_file=self.__class__.__name__,
            )
            if target_hash:
                if self._is_requested_hash_id(card_data):
                    self.append_leak_data(card_data, entity_model(m_username=[username, actor_name] if actor_name != username else [username]))
                return len(self._card_data)
            self.append_leak_data(card_data, entity_model(m_username=[username, actor_name] if actor_name != username else [username]))
            appended += 1
            if appended >= desired_count:
                break
        return appended

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
                const profileIcon = firstAttr([
                    '.org-top-card-primary-content__logo img',
                    '.org-top-card-summary__logo-image',
                    '.pv-top-card-profile-picture__image',
                    '.profile-photo-edit__preview',
                    'img[alt*="logo" i]',
                    'img[alt*="profile" i]',
                    'meta[property="og:image"]'
                ], 'src') || firstAttr(['meta[property="og:image"]'], 'content');
                const coverpage = firstAttr([
                    '.profile-background-image__image',
                    '.org-top-card__hero-image img',
                    '.org-top-card-primary-content__cover-image',
                    'img[alt*="background" i]',
                    'img[alt*="cover" i]'
                ], 'src') || bgUrl([
                    '.profile-background-image',
                    '.org-top-card__hero-image',
                    '[class*="background"]',
                    '[class*="cover"]'
                ]);
                return {profileIcon, coverpage};
            }""") or {}
        except Exception:
            return {}

    def _append_profile_info(
        self,
        username: str,
        real_name: str,
        about_text: str,
        connections_text: str,
        profile_assets: dict,
        data_type: SocialDataType,
    ):
        content_type = "profile_info"
        card_data = social_model(
            m_channel_url=self.seed_url,
            m_title=real_name or username,
            m_sender_name=real_name or username,
            m_url=self.seed_url,
            m_weblink=[self.seed_url],
            m_content=about_text,
            m_content_type=["social_collector", "linkedin_profile", content_type],
            m_network="clearnet",
            m_date=datetime.now(UTC).date(),
            m_message_id=username,
            m_platform="linkedin",
            m_group_name=username,
            m_group_info=connections_text or None,
            m_img_src=profile_assets.get("profileIcon") or None,
            m_coverpage=profile_assets.get("coverpage") or None,
            m_scrap_file=self.__class__.__name__,
        )
        self.append_leak_data(card_data, entity_model(m_username=[username] if username else []))

    @staticmethod
    def _post_url_from_card(card, fallback_url: str) -> str:
        try:
            href = card.evaluate("""node => {
                const selectors = [
                    'a[href*="/feed/update/"]',
                    'a[href*="/posts/"]',
                    'a[href*="/activity-"]',
                    'a[href*="urn:li:activity"]',
                    'a[href*="/pulse/"]'
                ];
                for (const selector of selectors) {
                    const href = node.querySelector(selector)?.href || node.querySelector(selector)?.getAttribute('href') || '';
                    if (href) return href;
                }
                return '';
            }""")
            if href:
                return href
        except Exception:
            pass
        return fallback_url

    @staticmethod
    def _post_media_from_card(card) -> str | None:
        try:
            return card.evaluate("""node => {
                const srcsetUrl = value => String(value || '').split(',').pop().trim().split(/\\s+/)[0] || '';
                const images = Array.from(node.querySelectorAll('img')).map(img => {
                    const rect = img.getBoundingClientRect();
                    return {
                        src: img.currentSrc || img.src || img.getAttribute('src') || srcsetUrl(img.getAttribute('srcset')) || '',
                        width: rect.width || img.naturalWidth || img.width || 0,
                        height: rect.height || img.naturalHeight || img.height || 0,
                        alt: img.alt || ''
                    };
                }).filter(img => img.src && !img.src.startsWith('data:'));
                const media = images.find(img => img.width > 120 && img.height > 80 && !/logo|profile|avatar/i.test(img.alt)) ||
                    images.find(img => img.width > 80 && img.height > 80 && !/profile|avatar/i.test(img.alt));
                return media?.src || '';
            }""") or None
        except Exception:
            return None

    @staticmethod
    def _post_share_count(card) -> str | None:
        try:
            text = card.inner_text() or ""
        except Exception:
            return None
        match = re.search(r"([\d,]+)\s+(?:reposts?|shares?)", text, re.IGNORECASE)
        return match.group(1).replace(",", "") if match else None

    @staticmethod
    def _expand_post_text(card):
        try:
            buttons = card.locator("button, span[role='button']").all()
            for button in buttons[:20]:
                try:
                    text = (button.inner_text(timeout=500) or "").strip().lower()
                    if text in {"see more", "...see more"} or "see more" in text:
                        button.click(timeout=1000)
                        break
                except Exception:
                    continue
        except Exception:
            pass

    def _collect_comments_from_card(self, page, card, limit: int, offset: int) -> list[social_comment_model]:
        limit = max(1, min(int(limit or 10), 10))
        offset = max(0, int(offset or 0))
        target_count = offset + limit
        comments: list[social_comment_model] = []
        seen = set()

        try:
            buttons = card.locator(
                ".social-details-social-counts__comments button, "
                "button[aria-label*='comment' i], button:has-text('comment')"
            )
            if buttons.count() > 0:
                buttons.first.click(timeout=3000)
                page.wait_for_timeout(random.randint(1000, 2500))
        except Exception:
            pass

        idle_rounds = 0
        for _ in range(10):
            try:
                rows = card.evaluate("""node => {
                    const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                    const roots = Array.from(node.querySelectorAll(
                        '.comments-comment-item, article.comments-comment-item, [class*="comments-comment-item"]'
                    ));
                    return roots.map(root => {
                        const username = clean(
                            root.querySelector('.comments-post-meta__name-text, .comments-post-meta__name, a[href*="/in/"], span[aria-hidden="true"]')?.innerText
                        );
                        const text = clean(
                            root.querySelector('.comments-comment-item__main-content, .comments-comment-item-content-body, .update-components-text, [dir="ltr"]')?.innerText
                        );
                        const time = clean(root.querySelector('time, .comments-comment-item__timestamp, .comments-post-meta__headline')?.innerText);
                        const likesLabel = root.querySelector('[aria-label*="reaction" i], [aria-label*="like" i]')?.getAttribute('aria-label') || '';
                        const likesText = clean(root.querySelector('.social-details-social-counts__reactions-count')?.innerText || likesLabel);
                        return text ? {username, text, time, likes: likesText} : null;
                    }).filter(Boolean);
                }""")
            except Exception:
                rows = []

            before_count = len(comments)
            for row in rows:
                text = str(row.get("text") or "").strip()
                if not text:
                    continue
                key = "|".join([
                    str(row.get("username") or "").strip(),
                    str(row.get("time") or "").strip(),
                    text,
                ])
                if key in seen:
                    continue
                seen.add(key)
                comments.append(
                    social_comment_model(
                        m_username=str(row.get("username") or "").strip() or None,
                        m_time=str(row.get("time") or "").strip() or None,
                        m_likes=str(row.get("likes") or "").strip() or None,
                        m_text=text,
                    )
                )
                if len(comments) >= target_count:
                    return comments[offset:target_count]

            idle_rounds = idle_rounds + 1 if len(comments) == before_count else 0
            if idle_rounds >= 3:
                break
            try:
                for button in card.locator("button").all()[:30]:
                    text = (button.inner_text(timeout=500) or "").strip().lower()
                    if "load more comments" in text or "show previous comments" in text or "more comments" in text:
                        button.click(timeout=1000)
                        break
                page.wait_for_timeout(1000)
            except Exception:
                break

        return comments[offset:target_count]

    def parse_leak_data(self, page):
        self._card_data = []
        self._entity_data = []
        self._last_status = ""
        self._last_reason = ""
        try:
            if page.url.rstrip("/") != self.seed_url.rstrip("/"):
                page.goto(self.seed_url, wait_until="domcontentloaded", timeout=45000)
            else:
                page.wait_for_load_state("domcontentloaded", timeout=15000)
            page.wait_for_timeout(random.randint(1000, 10000))
            try:
                page.wait_for_selector(self.PAGE_READY_SELECTOR, timeout=10000)
            except Exception:
                pass

            is_company = "/company/" in self.seed_url
            name_loc = page.locator(
                "h1.org-top-card-summary__title, h1, h2._1d496a86._562a64d6._5ef4d293._89abd4e7"
            ).first
            raw_real_name = name_loc.inner_text() if name_loc.count() > 0 else ""
            real_name = raw_real_name.strip() if raw_real_name else ""
            username = self._public_identifier(self.seed_url)
            public_profile = self._extract_public_profile_info(page, username)
            real_name = self._clean_text(public_profile.get("title")) or real_name or username

            about_text = ""
            about_loc = page.locator(
                "[data-test-id='about-us'], p.org-top-card-summary__tagline, div.org-top-card-summary__tagline, "
                "div.text-body-medium, p"
            ).first
            if about_loc.count() > 0:
                raw_about_text = about_loc.inner_text()
                about_text = raw_about_text.strip() if raw_about_text else ""
            about_text = self._clean_text(public_profile.get("aboutText")) or self._clean_text(about_text).removeprefix("About us").strip()

            connections_text = ""
            conn_loc = page.locator("p:has-text('followers'), p:has-text('connections')").first
            if conn_loc.count() > 0:
                raw_connections_text = conn_loc.inner_text()
                connections_text = raw_connections_text.strip() if raw_connections_text else ""
            connections_text = self._clean_text(public_profile.get("followers")) or connections_text

            activity_url = self._activity_url(self.seed_url, is_company, username)
            profile_assets = self._extract_profile_assets(page)
            data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
            if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL, SocialDataType.FOLLOWERS, SocialDataType.FOLLOWING):
                self._append_profile_info(username, real_name, about_text, connections_text, profile_assets, data_type)
                return True
            if data_type in (SocialDataType.VIDEOS, SocialDataType.SHORTS):
                self._last_status = "unsupported_data_type"
                self._last_reason = "linkedin video/short extraction is not implemented"
                return True

            public_count = self._append_public_update_cards(
                page,
                username,
                real_name,
                about_text,
                connections_text,
                data_type,
            )
            if public_count:
                self._last_status = "ok"
                self._last_reason = "public updates section returned posts"
                return True

            if self._session_required(page):
                self._last_status = "auth_required"
                self._last_reason = "linkedin public page is behind authwall"
                log.g().w(
                    "LinkedIn public page is behind authwall and no Updates cards were visible; "
                    "run RequestParser(...).parse(session=True) for logged-in feed extraction."
                )
                return False

            desired_count = self._item_limit()
            target_hash = self._is_target_hash_request(data_type)
            search_count = 100 if target_hash else desired_count
            page.goto(activity_url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(random.randint(1000, 10000))

            public_count = self._append_public_update_cards(
                page,
                username,
                real_name,
                about_text,
                connections_text,
                data_type,
            )
            if public_count:
                self._last_status = "ok"
                self._last_reason = "public activity page returned posts"
                return True

            if self._session_required(page):
                self._last_status = "auth_required"
                self._last_reason = "linkedin activity page requires login"
                log.g().w(
                    "linkedin session missing or expired; run RequestParser(...).parse(session=True)"
                )
                return False
            try:
                page.wait_for_selector(self.POST_SELECTOR, timeout=15000)
            except Exception:
                self._last_status = "no_public_posts"
                self._last_reason = "no public updates/feed cards were visible"
                return False

            max_scrolls = 14 if self.is_crawled else 6
            prev_count = 0
            same_count_rounds = 0

            for _ in range(max_scrolls):
                posts = page.locator(self.POST_SELECTOR)
                count = posts.count()

                if count >= search_count:
                    break

                if count == prev_count:
                    same_count_rounds += 1
                    if same_count_rounds >= 2:
                        break
                else:
                    same_count_rounds = 0

                prev_count = count
                page.mouse.wheel(0, random.randint(1400, 2600))
                page.wait_for_timeout(random.randint(1000, 10000))

            posts = page.locator(self.POST_SELECTOR)
            total = min(posts.count(), search_count)

            if total < 1:
                self._last_status = "no_public_posts"
                self._last_reason = "linkedin feed returned no post cards"
                return False

            for i in range(total):
                card = posts.nth(i)
                page.wait_for_timeout(random.randint(1000, 10000))
                self._expand_post_text(card)

                post_text = ""
                text_loc = card.locator(
                    "div.feed-shared-update-v2__description .update-components-text span[dir='ltr']"
                ).first
                if text_loc.count() > 0:
                    raw_post_text = text_loc.inner_text()
                    post_text = raw_post_text.strip() if raw_post_text else ""

                likes = "0"
                likes_loc = card.locator(".social-details-social-counts__reactions-count").first
                if likes_loc.count() > 0:
                    raw_likes = likes_loc.inner_text()
                    likes = raw_likes.strip() if raw_likes else "0"

                comments = "0"
                comments_loc = card.locator(".social-details-social-counts__comments button span").first
                if comments_loc.count() > 0:
                    raw_comments = comments_loc.inner_text()
                    comments = raw_comments.strip() if raw_comments else "0"

                fallback_post_id = hashlib.sha256((post_text or str(i)).encode("utf-8")).hexdigest()
                post_url = self._post_url_from_card(card, f"{activity_url}#post-{fallback_post_id}")
                if target_hash and not self._is_requested_hash_url(post_url):
                    continue
                if not target_hash and self._is_requested_hash_url(post_url):
                    break

                structured_comments = self._collect_comments_from_card(page, card, self._comment_limit(), self._comment_offset()) if data_type == SocialDataType.COMMENTS else []
                media_url = self._post_media_from_card(card)
                shares = self._post_share_count(card)
                post_id = hashlib.sha256((post_url or post_text).encode("utf-8")).hexdigest()

                card_data = social_model(
                    m_channel_url=self.seed_url,
                    m_title=post_text[:80] or username,
                    m_sender_name=real_name,
                    m_url=post_url,
                    m_message_sharable_link=post_url,
                    m_weblink=[post_url],
                    m_content=post_text,
                    m_content_type=["social_collector", "linkedin_post", data_type.value if data_type == SocialDataType.COMMENTS else "posts"],
                    m_network="clearnet",
                    m_date=datetime.now(UTC).date(),
                    m_message_id=post_id,
                    m_platform="linkedin",
                    m_group_name=username,
                    m_group_info=f"{connections_text} | {about_text}".strip(" |"),
                    m_post_likes=likes,
                    m_post_shares=shares,
                    m_comment_count=str(len(structured_comments)) if structured_comments else comments,
                    m_comments=structured_comments,
                    m_img_src=media_url,
                    m_scrap_file=self.__class__.__name__,
                )
                if target_hash:
                    if self._is_requested_hash_id(card_data):
                        self.append_leak_data(card_data, entity_model(m_username=[username]))
                    return

                entity_data = entity_model(
                    m_username=[username],
                )

                self.append_leak_data(card_data, entity_data)

            return True

        except Exception as ex:
            self._last_status = "error"
            self._last_reason = str(ex)
            log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
            return False
