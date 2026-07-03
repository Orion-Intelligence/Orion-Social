import re
import random
from abc import ABC
from typing import List
from datetime import datetime

from crawler.crawler_instance.local_interface_model.extractor.extraction_interface import extraction_interface
from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_comment_model, social_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, FetchProxy, FetchConfig, ThreatType, RuleType, SocialDataType
from crawler.crawler_services.redis_manager.redis_controller import redis_controller


class _youtube(extraction_interface, ABC):
    _instance = None

    def __init__(self, callback=None):
        super().__init__()
        self.platform = "youtube"
        self.callback = callback
        self._card_data = []
        self._entity_data = []
        self._initialized = None
        self.m_seed_url = "https://www.youtube.com/@BrutalBikes"
        self._redis_instance = redis_controller()
        self._is_crawled = False
        self._last_status = ""
        self._last_reason = ""

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
        return "Dilshad Ghauri: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jL82"

    @property
    def base_url(self) -> str:
        return "https://www.youtube.com"

    @property
    def rule_config(self) -> RuleModel:
        rule = RuleModel(
            m_fetch_proxy=FetchProxy.NONE,
            m_fetch_config=FetchConfig.PLAYRIGHT,
            m_threat_type=ThreatType.YOUTUBE,
            m_rule_type=RuleType.YOUTUBE,
            m_social_data_type=getattr(self, "m_social_data_type", SocialDataType.DEFAULT)
        )
        rule.m_resoource_block = False
        rule.m_resource_block = False
        return rule

    @property
    def card_data(self) -> List[social_model]:
        return self._card_data

    @property
    def entity_data(self) -> List[entity_model]:
        return self._entity_data

    def invoke_db(self, command: int, key: str, default_value, expiry: int | None = None):
        return self._redis_instance.invoke_trigger(command, [key + self.__class__.__name__, default_value, expiry])

    def contact_page(self) -> str:
        return "https://www.youtube.com/t/contact_us"

    @staticmethod
    def _parse_counts(text: str) -> int:
        if not text: return 0
        text = str(text)
        text = text.upper().replace(' VIEWS', '').replace(' SUBSCRIBERS', '').strip()
        text = re.sub(r'[^\x00-\x7F]+', '', text).strip()

        try:
            if 'K' in text: return int(float(text.replace('K', '').strip()) * 1000)
            if 'M' in text: return int(float(text.replace('M', '').strip()) * 1000000)
            if 'B' in text: return int(float(text.replace('B', '').strip()) * 1000000000)
            return int(re.sub(r'[^0-9]', '', text))
        except Exception:
            return 0

    @staticmethod
    def _video_id_from_url(url: str) -> str:
        match = re.search(r"(?:[?&]v=|/shorts/)([^?&#/]+)", url or "")
        return match.group(1) if match else ""

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

    def _requested_hash_id(self) -> str:
        return str(getattr(self, "m_hash_id", "") or "").strip()

    def _is_target_hash_request(self, data_type: SocialDataType) -> bool:
        return data_type == SocialDataType.COMMENTS and bool(self._requested_hash_id())

    def _is_requested_hash_url(self, url: str) -> bool:
        requested_hash_id = self._requested_hash_id()
        return bool(requested_hash_id and social_model.unique_identifier("youtube", url, "", "", "") == requested_hash_id)

    def _is_requested_hash_id(self, card_data: social_model) -> bool:
        requested_hash_id = self._requested_hash_id()
        return bool(requested_hash_id and getattr(card_data, "m_hash_id", "") == requested_hash_id)

    @staticmethod
    def _message_id(*values) -> str:
        for value in values:
            text = str(value or "").strip()
            if text:
                return text
        return social_model.unique_identifier("youtube", *values)

    def _append_card_data(self, card_data: social_model) -> bool:
        message_id = str(getattr(card_data, "m_message_id", "") or "").strip()
        if not message_id:
            return False
        card_data.m_message_id = message_id
        self.append_leak_data(card_data, entity_model())
        return True

    def _collect_comments(self, page, limit: int = 10, offset: int = 0) -> list[dict]:
        comments: list[dict] = []
        seen = set()
        idle_scrolls = 0
        limit = max(1, min(int(limit or 10), 10))
        offset = max(0, int(offset or 0))
        target_count = offset + limit
        try:
            for _ in range(4):
                page.keyboard.press("PageDown")
                page.wait_for_timeout(500)
        except Exception:
            pass

        for _ in range(30):
            try:
                page.evaluate("""() => {
                    for (const button of document.querySelectorAll('#more, #more-replies, ytd-button-renderer, tp-yt-paper-button')) {
                        const text = (button.innerText || '').toLowerCase();
                        if (text.includes('more') || text.includes('reply')) {
                            try { button.click(); } catch (e) {}
                        }
                    }
                }""")
            except Exception:
                pass
            try:
                rows = page.evaluate("""() => Array.from(document.querySelectorAll('ytd-comment-thread-renderer')).map(thread => ({
                    username: thread.querySelector('#author-text')?.innerText.trim() || '',
                    text: thread.querySelector('#content-text')?.innerText.trim() || '',
                    time: thread.querySelector('#published-time-text a, #published-time-text')?.innerText.trim() || '',
                    likes: thread.querySelector('#vote-count-middle')?.innerText.trim() || ''
                })).filter(comment => comment.text)""")
            except Exception:
                rows = []

            before_count = len(comments)
            for row in rows:
                key = "|".join([str(row.get("username") or ""), str(row.get("time") or ""), str(row.get("text") or "")])
                if key in seen:
                    continue
                seen.add(key)
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

    @staticmethod
    def _comment_models(top_comments: list[dict]) -> tuple[list[str], list[str], list[social_comment_model]]:
        comment_texts = [str(comment.get("text", "")).strip() for comment in top_comments if comment.get("text")]
        commenters = [str(comment.get("username", "")).strip() for comment in top_comments if comment.get("username")]
        comments = [
            social_comment_model(
                m_username=str(comment.get("username", "")).strip() or None,
                m_time=str(comment.get("time", "")).strip() or None,
                m_likes=str(comment.get("likes", "")).strip() or None,
                m_text=str(comment.get("text", "")).strip() or None,
            )
            for comment in top_comments
            if comment.get("text")
        ]
        return comment_texts, commenters, comments

    def _append_channel_info(self, page, channel_url: str, data_type: SocialDataType):
        page.goto(channel_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(random.randint(1000, 10000))
        info = page.evaluate("""() => {
            const cleanUrl = value => {
                if (!value) return '';
                const match = String(value).match(/url\\(["']?([^"')]+)["']?\\)/);
                const url = match ? match[1] : String(value);
                if (!url || url.startsWith('data:') || /^(none|initial|inherit|unset)$/i.test(url.trim())) return '';
                return url.startsWith('//') ? `https:${url}` : url;
            };
            const firstAttr = (selectors, attr) => {
                for (const selector of selectors) {
                    const node = document.querySelector(selector);
                    const value = node?.getAttribute(attr) || node?.[attr] || '';
                    if (value) return cleanUrl(value);
                }
                return '';
            };
            const title = document.querySelector('meta[property="og:title"]')?.content || document.title.replace(' - YouTube', '');
            const description = document.querySelector('meta[name="description"]')?.content || '';
            const text = document.body.innerText || '';
            const subs = text.match(/[\\d.,]+[KMB]?\\s+subscribers/i);
            const profileIcon = firstAttr([
                'meta[property="og:image"]',
                'link[itemprop="thumbnailUrl"]',
                '#avatar img',
                'yt-decorated-avatar-view-model img',
                'yt-avatar-shape img'
            ], 'content') || firstAttr(['#avatar img', 'yt-decorated-avatar-view-model img', 'yt-avatar-shape img'], 'src');
            const coverpage = firstAttr([
                'ytd-c4-tabbed-header-renderer #banner img',
                '#page-header-banner img',
                'yt-page-header-view-model img',
                'yt-image-banner-view-model img'
            ], 'src') || cleanUrl(getComputedStyle(document.querySelector('#banner, #page-header-banner') || document.body).backgroundImage);
            return {title, description, subscribers: subs ? subs[0] : '', profileIcon, coverpage};
        }""")
        title = info.get("title") or "Unknown"
        subscribers = info.get("subscribers") or ""
        description = info.get("description") or ""
        content_type = (
            "profile_info"
            if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL)
            else str(data_type.value)
        )
        card_data = social_model(
            m_title=title,
            m_channel_url=channel_url,
            m_sender_name=title,
            m_url=channel_url,
            m_message_sharable_link=channel_url,
            m_weblink=[channel_url],
            m_content=description,
            m_content_type=["social_collector", "youtube_profile", content_type],
            m_network="clearnet",
            m_date=datetime.now().date(),
            m_message_id=self._message_id(f"profile:{channel_url.rstrip('/')}", title),
            m_platform=[self.platform],
            m_group_name=title,
            m_group_info=f"SUBSCRIBERS: {subscribers}" if subscribers else None,
            m_img_src=info.get("profileIcon") or None,
            m_coverpage=info.get("coverpage") or None,
            m_scrap_file=self.__class__.__name__,
        )
        self._append_card_data(card_data)

    def _collect_video_links(self, page, channel_url: str, is_shorts: bool, limit: int = 10, target_hash: bool = False) -> list[str]:
        page.goto(channel_url.rstrip("/") + ("/shorts" if is_shorts else "/videos"), wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        if not is_shorts:
            page.evaluate("""() => {
                for (let chip of document.querySelectorAll('yt-chip-cloud-chip-renderer')) {
                    if (chip.innerText.trim().toLowerCase() === 'latest') {
                        if (!chip.classList.contains('selected')) chip.click();
                        break;
                    }
                }
            }""")
            page.wait_for_timeout(1000)

        links = []
        seen_links = set()
        no_new_scrolls = 0
        max_scrolls = 20 if target_hash else (5 if limit <= 5 else 20)
        for _ in range(max_scrolls):
            before_count = len(seen_links)
            for href in page.evaluate("""() => Array.from(document.querySelectorAll('ytd-rich-item-renderer a[href]'))
                .map(a => a.getAttribute('href'))
                .filter(Boolean)"""):
                if (is_shorts and "/shorts/" not in href) or (not is_shorts and "/shorts/" in href):
                    continue
                full_link = self.base_url + href if href.startswith("/") else href
                if self._is_requested_hash_url(full_link):
                    return [full_link] if target_hash else links
                if full_link in seen_links:
                    continue
                seen_links.add(full_link)
                if target_hash:
                    continue
                links.append(full_link)
                if len(links) >= limit:
                    return links
            if len(seen_links) == before_count:
                no_new_scrolls += 1
            else:
                no_new_scrolls = 0
            if no_new_scrolls >= 3:
                break
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(750)
        return links

    def _parse_video_data(self, page, channel_url: str, data_type: SocialDataType, is_shorts: bool, check_latest: bool = False):
        video_content_type = "youtube_short" if is_shorts else "youtube_video"
        social_data_type = str(data_type.value)
        target_hash = self._is_target_hash_request(data_type)
        for video_idx, video_url in enumerate(self._collect_video_links(page, channel_url, is_shorts, self._item_limit(), target_hash), 1):
            try:
                if not target_hash and self._is_requested_hash_url(video_url):
                    return
                video_id = self._video_id_from_url(video_url)
                page.goto(f"{self.base_url}/watch?v={video_id}" if is_shorts and video_id else video_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(1000)
                page.wait_for_selector("h1.ytd-watch-metadata", state="visible", timeout=15000)
                page.wait_for_selector("ytd-video-owner-renderer", state="visible", timeout=10000)

                title_elem = page.locator("h1.ytd-watch-metadata yt-formatted-string").first
                title = title_elem.inner_text(timeout=3000) if title_elem.count() > 0 else "Unknown"

                views_text = page.evaluate("""() => {
                    const metaViews = Array.from(document.querySelectorAll('meta[itemprop="interactionCount"], meta[itemprop="userInteractionCount"]'))
                        .map(meta => Number((meta.content || '').replace(/[^0-9]/g, '')))
                        .filter(Boolean)
                        .sort((a, b) => b - a)[0];
                    if (metaViews) return metaViews;
                    const viewAria = document.querySelector('[aria-label*="views" i]')?.getAttribute('aria-label');
                    if (viewAria) return viewAria;
                    return document.querySelector('yt-formatted-string#info span')?.innerText || '0';
                }""")
                views_count = self._parse_counts(views_text)

                likes_count = 0
                try:
                    likes_count = self._parse_counts(page.evaluate("""() => {
                        let btn = document.querySelector('like-button-view-model button');
                        if (!btn) return '0';
                        let aria = btn.getAttribute('aria-label');
                        if (aria) {
                            let match = aria.match(/with\\s+([\\d,]+)\\s+other/i) || aria.match(/([\\d,]+)\\s+likes/i);
                            if (match) return match[1];
                        }
                        let textDiv = btn.querySelector('.ytSpecButtonShapeNextButtonTextContent');
                        if (textDiv && textDiv.innerText) return textDiv.innerText;
                        return btn.innerText;
                    }"""))
                except Exception:
                    pass

                channel_elem = page.locator("ytd-video-owner-renderer #channel-name a").first
                channel_name = channel_elem.inner_text(timeout=3000) if channel_elem.count() > 0 else "Unknown"
                subs_elem = page.locator("ytd-video-owner-renderer #owner-sub-count").first
                subs_count = self._parse_counts(subs_elem.inner_text(timeout=3000) if subs_elem.count() > 0 else "0")
                is_viral = (views_count / subs_count) > 0.20 if subs_count > 0 else False

                video_content = page.evaluate("""() => {
                    const expand = document.querySelector('#expand, tp-yt-paper-button#expand');
                    if (expand) expand.click();
                    const selectors = [
                        'ytd-watch-metadata #description-inline-expander',
                        'ytd-watch-metadata ytd-text-inline-expander',
                        '#description #content',
                    ];
                    for (const selector of selectors) {
                        const el = document.querySelector(selector);
                        if (el && el.innerText.trim()) return el.innerText.trim();
                    }
                    return document.querySelector('meta[name="description"]')?.content || '';
                }""")
                thumbnail = page.evaluate("""() => {
                    const value = document.querySelector('meta[property="og:image"], link[itemprop="thumbnailUrl"]')?.content || '';
                    return value.startsWith('//') ? `https:${value}` : value;
                }""") or (f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else "")

                load_comments = data_type == SocialDataType.COMMENTS
                top_comments = self._collect_comments(page, self._comment_limit(), self._comment_offset()) if load_comments else []
                comment_texts, _, comments = self._comment_models(top_comments)
                card_data = social_model(
                    m_title=title,
                    m_channel_url=channel_url,
                    m_sender_name=channel_name,
                    m_url=video_url,
                    m_message_sharable_link=video_url,
                    m_weblink=[],
                    m_content=video_content,
                    m_content_type=["social_collector", video_content_type, social_data_type],
                    m_network="clearnet",
                    m_date=datetime.now().date(),
                    m_message_id=self._message_id(video_id, video_url, f"{video_content_type}:{video_idx}"),
                    m_platform=[self.platform],
                    m_likes=str(likes_count),
                    m_comment_count=str(len(comment_texts)) if load_comments else None,
                    m_comments=comments,
                    m_views=str(views_count),
                    m_viral=is_viral,
                    m_group_name=channel_name,
                    m_group_info=f"SUBSCRIBERS: {subs_count}" if subs_count else None,
                    m_img_src=thumbnail or None,
                    m_scrap_file=self.__class__.__name__,
                )
                if target_hash:
                    if self._is_requested_hash_id(card_data):
                        self._append_card_data(card_data)
                    return
                if self._is_requested_hash_id(card_data):
                    return
                self._append_card_data(card_data)
            except Exception:
                continue

    def _parse_posts(self, page, channel_url: str, data_type: SocialDataType, check_latest: bool = False):
        seen_urls = set()
        limit = self._item_limit()
        social_data_type = str(data_type.value)
        target_hash = self._is_target_hash_request(data_type)
        collected_posts = []
        hit_hash_cut = False
        navigation_errors = []
        for suffix in ("/community", "/posts"):
            try:
                page.goto(channel_url.rstrip("/") + suffix, wait_until="domcontentloaded", timeout=60000)
            except Exception as ex:
                navigation_errors.append(f"{suffix}: {ex}")
                continue
            page.wait_for_timeout(random.randint(1000, 3000))
            no_new_scrolls = 0
            max_scrolls = 20 if target_hash else (5 if limit <= 5 else 20)
            for _ in range(max_scrolls):
                before_count = len(seen_urls)
                posts = page.evaluate("""() => Array.from(document.querySelectorAll(
                    'ytd-backstage-post-thread-renderer, ytd-backstage-post-renderer, ytd-post-renderer, ytd-rich-item-renderer'
                )).map((post, index) => {
                    const content = post.querySelector('#content-text, yt-formatted-string#content-text, #content')?.innerText.trim() || '';
                    const author = post.querySelector('#author-text, #author-name, #channel-name')?.innerText.trim() || '';
                    const url = post.querySelector('a[href*="/post/"]')?.href || `${location.href}#post-${index}-${content.slice(0, 24)}`;
                    const likes = post.querySelector('#vote-count-middle, #vote-count-left')?.innerText.trim() || '';
                    const comments = post.querySelector('a[href*="/post/"] #count, #reply-count')?.innerText.trim() || '';
                    const cssUrl = value => {
                        const match = String(value || '').match(/url\\(["']?([^"')]+)["']?\\)/);
                        return match ? match[1] : '';
                    };
                    const srcsetUrl = value => String(value || '').split(',').pop().trim().split(/\\s+/)[0] || '';
                    const imageMedia = Array.from(post.querySelectorAll('img'))
                        .filter(img => !img.closest('#author-thumbnail, #avatar, yt-avatar-shape'))
                        .filter(img => {
                            const box = img.getBoundingClientRect();
                            return (img.naturalWidth || img.width || box.width) > 80 && (img.naturalHeight || img.height || box.height) > 80;
                        })
                        .map(img => img.currentSrc || img.src || img.getAttribute('src') || img.getAttribute('data-thumb') || srcsetUrl(img.getAttribute('srcset')));
                    const backgroundMedia = Array.from(post.querySelectorAll('*'))
                        .filter(node => {
                            const box = node.getBoundingClientRect();
                            return box.width > 120 && box.height > 80;
                        })
                        .map(node => cssUrl(getComputedStyle(node).backgroundImage));
                    const videoThumbs = Array.from(post.querySelectorAll('a[href*="/watch?v="]'))
                        .map(a => {
                            const match = String(a.href || a.getAttribute('href') || '').match(/[?&]v=([^&]+)/);
                            return match ? `https://i.ytimg.com/vi/${match[1]}/hqdefault.jpg` : '';
                        });
                    const media = Array.from(new Set([...imageMedia, ...backgroundMedia, ...videoThumbs]))
                        .filter(src => src && !src.startsWith('data:'));
                    return {content, author, url, likes, comments, media};
                }).filter(post => post.content)""")
                for post in posts:
                    post_url = post.get("url") or ""
                    if not post_url or post_url in seen_urls:
                        continue
                    seen_urls.add(post_url)
                    if self._is_requested_hash_url(post_url):
                        if target_hash:
                            collected_posts.append(post)
                        else:
                            hit_hash_cut = True
                        break
                    if target_hash:
                        continue
                    collected_posts.append(post)
                    if len(collected_posts) >= limit:
                        break
                if collected_posts and target_hash:
                    break
                if hit_hash_cut:
                    break
                if not target_hash and len(collected_posts) >= limit:
                    break
                if len(seen_urls) == before_count:
                    no_new_scrolls += 1
                else:
                    no_new_scrolls = 0
                if no_new_scrolls >= 3:
                    break
                page.mouse.wheel(0, 3000)
                page.wait_for_timeout(random.randint(1000, 3000))
            if collected_posts or hit_hash_cut:
                break

        if not collected_posts:
            if navigation_errors:
                self._last_status = "navigation_error"
                self._last_reason = " | ".join(navigation_errors)[-500:]
            else:
                self._last_status = "no_public_posts"
                self._last_reason = "youtube channel exposed no community post cards"
            return

        for post in collected_posts:
            post_url = post.get("url") or ""
            top_comments = []
            if data_type == SocialDataType.COMMENTS and post_url and "#post-" not in post_url:
                try:
                    page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(1000)
                    top_comments = self._collect_comments(page, self._comment_limit(), self._comment_offset())
                except Exception:
                    top_comments = []
            comment_texts, _, comments = self._comment_models(top_comments)
            card_data = social_model(
                m_title=post.get("content", "")[:80] or "YouTube post",
                m_channel_url=channel_url,
                m_sender_name=post.get("author") or "",
                m_url=post_url,
                m_message_sharable_link=post_url,
                m_weblink=[post_url],
                m_content=post.get("content") or "",
                m_content_type=["social_collector", "youtube_post", social_data_type],
                m_network="clearnet",
                m_date=datetime.now().date(),
                m_message_id=self._message_id(post_url, post.get("content"), post.get("author")),
                m_platform=[self.platform],
                m_post_likes=post.get("likes") or None,
                m_comment_count=str(len(comment_texts)) if comment_texts else post.get("comments") or None,
                m_comments=comments,
                m_img_src=(post.get("media") or [None])[0],
                m_scrap_file=self.__class__.__name__,
            )
            if target_hash:
                if self._is_requested_hash_id(card_data):
                    self._append_card_data(card_data)
                return
            if self._is_requested_hash_id(card_data):
                return
            self._append_card_data(card_data)
        self._last_status = "ok"
        self._last_reason = f"youtube returned {len(collected_posts)} community post cards"

    def parse_leak_data(self, page):
        try:
            self._card_data = []
            self._entity_data = []
            self._last_status = ""
            self._last_reason = ""
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
            seed_url = self.seed_url
            data_type = (self.rule_config.m_social_data_types or [SocialDataType.DEFAULT])[0]
            if data_type in (SocialDataType.PROFILE, SocialDataType.CHANNEL):
                self._append_channel_info(page, seed_url, data_type)
            elif data_type == SocialDataType.VIDEOS:
                self._parse_video_data(page, seed_url, data_type, is_shorts=False)
            elif data_type == SocialDataType.SHORTS:
                self._parse_video_data(page, seed_url, data_type, is_shorts=True)
            elif data_type == SocialDataType.POSTS:
                self._parse_posts(page, seed_url, data_type)
            elif data_type == SocialDataType.COMMENTS:
                request_kind = getattr(self, "m_request_kind", "posts")
                if request_kind == "videos":
                    self._parse_video_data(page, seed_url, data_type, is_shorts=False)
                elif request_kind == "shorts":
                    self._parse_video_data(page, seed_url, data_type, is_shorts=True)
                else:
                    self._parse_posts(page, seed_url, data_type)
            elif data_type == SocialDataType.DEFAULT:
                self._append_channel_info(page, seed_url, SocialDataType.DEFAULT)
                self._parse_video_data(page, seed_url, SocialDataType.VIDEOS, is_shorts=False, check_latest=True)
                self._parse_video_data(page, seed_url, SocialDataType.SHORTS, is_shorts=True, check_latest=True)
                self._parse_posts(page, seed_url, SocialDataType.POSTS, check_latest=True)
        except Exception:
            raise
