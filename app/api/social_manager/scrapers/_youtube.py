import re
import json
from typing import Dict, Any, List
from playwright.sync_api import Page
from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class YoutubeScraper(BaseScraper):
    requires_login = False

    def __init__(self, username: str, max_followers: int = 0, max_following: int = 0):
        super().__init__(username, max_followers, max_following)

    @property
    def base_url(self) -> str:
        return "https://www.youtube.com/"

    @property
    def seed_url(self) -> str:
        return f"https://www.youtube.com/@{self._username}"

    @property
    def name(self) -> str:
        return "YouTube"

    def _dismiss_consent(self, page: Page):
        try:
            accept_btn = page.locator(
                'button:has-text("Accept all"), '
                'button:has-text("Accept All"), '
                'button:has-text("Agree"), '
                'form[action*="consent"] button'
            ).first
            if accept_btn.count() > 0:
                accept_btn.click()
                page.wait_for_timeout(2000)
        except Exception:
            pass

    def _wait_for_channel_page(self, page: Page):
        page.wait_for_load_state("domcontentloaded")
        self._dismiss_consent(page)
        page.wait_for_load_state("networkidle", timeout=15000)
        page.wait_for_timeout(2000)

    @staticmethod
    def _with_english_locale(url: str) -> str:
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}hl=en&gl=US"

    def _extract_yt_initial_data(self, page: Page) -> dict:
        try:
            data = page.evaluate("""
                () => {
                    if (window.ytInitialData) return window.ytInitialData;
                    const scripts = document.querySelectorAll('script');
                    for (const s of scripts) {
                        const t = s.textContent || '';
                        const idx = t.indexOf('var ytInitialData = ');
                        if (idx !== -1) {
                            const start = idx + 'var ytInitialData = '.length;
                            let depth = 0, i = start;
                            while (i < t.length) {
                                if (t[i] === '{') depth++;
                                else if (t[i] === '}') { depth--; if (depth === 0) { i++; break; } }
                                i++;
                            }
                            try { return JSON.parse(t.slice(start, i)); } catch(e) {}
                        }
                    }
                    return null;
                }
            """)
            return data or {}
        except Exception:
            return {}

    def _extract_videos_from_yt_data(self, yt_data: dict) -> List[Dict[str, Any]]:
        videos = []
        try:
            tabs = (
                yt_data.get("contents", {})
                .get("twoColumnBrowseResultsRenderer", {})
                .get("tabs", [])
            )
            videos_tab = None
            for tab in tabs:
                tab_renderer = tab.get("tabRenderer", {})
                if tab_renderer.get("selected") or "videos" in tab_renderer.get("endpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", "").lower():
                    videos_tab = tab_renderer
                    break
                if tab_renderer.get("title", "").lower() == "videos":
                    videos_tab = tab_renderer
                    break

            if not videos_tab:
                for tab in tabs:
                    tab_renderer = tab.get("tabRenderer", {})
                    content = tab_renderer.get("content", {})
                    if content:
                        videos_tab = tab_renderer
                        break

            if not videos_tab:
                return videos

            content = videos_tab.get("content", {})
            section_list = content.get("richGridRenderer", {}) or content.get("sectionListRenderer", {})

            items_to_search = []
            if "contents" in section_list:
                items_to_search = section_list["contents"]

            def recursive_find_videos(obj, depth=0):
                if depth > 10:
                    return
                if isinstance(obj, dict):
                    if "videoRenderer" in obj:
                        vr = obj["videoRenderer"]
                        video_id = vr.get("videoId", "")
                        if video_id:
                            title = ""
                            title_runs = vr.get("title", {}).get("runs", [])
                            if title_runs:
                                title = title_runs[0].get("text", "")

                            views = ""
                            view_count_text = vr.get("viewCountText", {})
                            if view_count_text:
                                views = view_count_text.get("simpleText", "") or "".join(
                                    r.get("text", "") for r in view_count_text.get("runs", [])
                                )

                            posted_time = ""
                            published_time = vr.get("publishedTimeText", {})
                            if published_time:
                                posted_time = published_time.get("simpleText", "")

                            thumbnail_url = ""
                            thumbnails = vr.get("thumbnail", {}).get("thumbnails", [])
                            if thumbnails:
                                thumbnail_url = thumbnails[-1].get("url", "")

                            videos.append({
                                "status": "active",
                                "post_url": f"https://www.youtube.com/watch?v={video_id}",
                                "datetime": posted_time,
                                "caption": title,
                                "media_url": thumbnail_url,
                                "media_type": "video",
                                "comments": "0",
                                "likes": "0",
                                "shares": "0",
                                "views": views,
                                "top_commenters": [],
                                "comments_text": [],
                            })
                    else:
                        for v in obj.values():
                            recursive_find_videos(v, depth + 1)
                elif isinstance(obj, list):
                    for item in obj:
                        recursive_find_videos(item, depth + 1)

            recursive_find_videos(items_to_search)
        except Exception:
            pass

        return videos

    def _extract_about_stats(self, page: Page) -> Dict[str, str]:
        location = ""
        joined_date = ""
        total_subscribers = ""
        total_videos = ""
        total_views = ""

        icon_map = {
            "privacy_public": "location",
            "info_outline": "joined_date",
            "person_radar": "total_subscribers",
            "my_videos": "total_videos",
            "trending_up": "total_views",
        }

        for tr in page.locator("#additional-info-container tr").all():
            for icon_name, field in icon_map.items():
                icon = tr.locator(f"yt-icon[icon='{icon_name}']")
                if icon.count() > 0:
                    text_td = tr.locator("td").last
                    try:
                        value = text_td.inner_text(timeout=2000).strip()
                    except Exception:
                        value = ""
                    if field == "location":
                        location = value
                    elif field == "joined_date":
                        loc2 = tr.locator("yt-attributed-string span.yt-core-attributed-string").first
                        try:
                            joined_date = loc2.inner_text(timeout=2000).strip() if loc2.count() > 0 else value
                        except Exception:
                            joined_date = value
                    elif field == "total_subscribers":
                        total_subscribers = value
                    elif field == "total_videos":
                        total_videos = value
                    elif field == "total_views":
                        total_views = value
                    break

        return {
            "location": location,
            "joined_date": joined_date,
            "total_subscribers": total_subscribers,
            "total_videos": total_videos,
            "total_views": total_views,
        }

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self._with_english_locale(self.seed_url), wait_until="domcontentloaded")
        self._wait_for_channel_page(page)

        real_name = ""
        for selector in [
            "#page-header yt-dynamic-text-view-model",
            "#channel-header yt-dynamic-text-view-model",
            "ytd-channel-name yt-formatted-string#text",
            "#channel-header-container #text",
            "h1.ytd-channel-name",
        ]:
            loc = page.locator(selector).first
            if loc.count() > 0:
                try:
                    real_name = loc.inner_text(timeout=3000).strip()
                    if real_name:
                        break
                except Exception:
                    continue

        more_btn = page.locator("button.yt-truncated-text__absolute-button").first
        if more_btn.count() > 0:
            try:
                more_btn.click()
                page.wait_for_timeout(1500)
            except Exception:
                pass

        bio_text = ""
        for selector in [
            "#description-container span.yt-core-attributed-string",
            "ytd-about-channel-renderer #description-container",
            "#about-container #description-container",
        ]:
            loc = page.locator(selector).first
            if loc.count() > 0:
                try:
                    bio_text = loc.inner_text(timeout=3000).strip()
                    if bio_text:
                        break
                except Exception:
                    continue

        stats = self._extract_about_stats(page)
        location = stats["location"]
        joined_date = stats["joined_date"]
        total_subscribers = stats["total_subscribers"]
        total_videos = stats["total_videos"]
        total_views = stats["total_views"]

        if not (bio_text and total_subscribers and total_videos and total_views):
            about_url = f"{self.seed_url}/about"
            page.goto(self._with_english_locale(about_url), wait_until="domcontentloaded")
            self._wait_for_channel_page(page)

            if not bio_text:
                for selector in [
                    "#description-container span.yt-core-attributed-string",
                    "ytd-about-channel-renderer #description-container",
                    "#about-container #description-container",
                    "yt-attributed-string#description span.yt-core-attributed-string",
                ]:
                    loc = page.locator(selector).first
                    if loc.count() > 0:
                        try:
                            bio_text = loc.inner_text(timeout=3000).strip()
                            if bio_text:
                                break
                        except Exception:
                            continue

            stats = self._extract_about_stats(page)
            location = location or stats["location"]
            joined_date = joined_date or stats["joined_date"]
            total_subscribers = total_subscribers or stats["total_subscribers"]
            total_videos = total_videos or stats["total_videos"]
            total_views = total_views or stats["total_views"]

            try:
                page_text = page.locator("body").inner_text(timeout=3000)
            except Exception:
                page_text = ""

            if page_text:
                if not total_subscribers:
                    m = re.search(r"([\d.,]+\s*[KkMm]?\s*subscribers?)", page_text)
                    if m:
                        total_subscribers = m.group(1).strip()
                if not total_videos:
                    m = re.search(r"([\d.,]+\s*[KkMm]?\s*videos?)", page_text)
                    if m:
                        total_videos = m.group(1).strip()
                if not total_views:
                    m = re.search(r"([\d.,]+\s*[KkMm]?\s*views?)", page_text)
                    if m:
                        total_views = m.group(1).strip()
                if not joined_date:
                    m = re.search(r"(Joined\s+[A-Za-z]+\s+\d{1,2},\s+\d{4}|Joined\s+[A-Za-z]+\s+\d{4})", page_text)
                    if m:
                        joined_date = m.group(1).strip()

        return {
            "real_name": real_name,
            "bio": bio_text,
            "location": location,
            "total_posts": total_videos,
            "total_followers": total_subscribers,
            "total_following": "",
            "profile_url": self.seed_url
        }

    def scrape_posts(self, page: Page, max_posts: int = 10) -> List[Dict[str, Any]]:
        videos_url = f"{self.seed_url}/videos"
        page.goto(
            self._with_english_locale(videos_url),
            wait_until="domcontentloaded"
        )
        self._dismiss_consent(page)
        page.wait_for_timeout(3000)

        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass

        page.wait_for_timeout(2000)

        yt_data = self._extract_yt_initial_data(page)
        collected_posts = self._extract_videos_from_yt_data(yt_data)

        if not collected_posts:
            scroll_attempts = 0
            while scroll_attempts < 5:
                page.mouse.wheel(0, 900)
                page.wait_for_timeout(2000)
                yt_data = self._extract_yt_initial_data(page)
                collected_posts = self._extract_videos_from_yt_data(yt_data)
                if collected_posts:
                    break
                scroll_attempts += 1

        if not collected_posts:
            collected_posts = self._scrape_posts_dom_fallback(page, max_posts)

        collected_posts = collected_posts[:max_posts]

        seen_video_urls = set()
        unique_posts = []
        for post in collected_posts:
            if post["post_url"] not in seen_video_urls:
                seen_video_urls.add(post["post_url"])
                unique_posts.append(post)
        collected_posts = unique_posts[:max_posts]

        for post_data in collected_posts:
            post_url = post_data["post_url"]
            comments_data = []

            try:
                captured_comment_responses = []

                def handle_response(response):
                    try:
                        url = response.url
                        if "youtubei/v1/next" in url or "youtubei/v1/browse" in url:
                            if response.status == 200:
                                try:
                                    body = response.json()
                                    captured_comment_responses.append(body)
                                except Exception:
                                    pass
                    except Exception:
                        pass

                page.on("response", handle_response)

                page.goto(self._with_english_locale(post_url), wait_until="domcontentloaded")
                self._dismiss_consent(page)
                page.wait_for_timeout(3000)

                likes_loc = page.locator('like-button-view-model button[aria-label*="like"]').first
                if likes_loc.count() == 0:
                    likes_loc = page.locator(
                        'ytd-segmented-like-dislike-button-renderer #segmented-like-button button'
                    ).first
                try:
                    post_data["likes"] = likes_loc.inner_text(timeout=3000).strip() if likes_loc.count() > 0 else "0"
                except Exception:
                    post_data["likes"] = "0"

                page.mouse.wheel(0, 1200)
                page.wait_for_timeout(3000)
                page.mouse.wheel(0, 1200)
                page.wait_for_timeout(3000)

                comments_data = self._parse_comments_from_responses(captured_comment_responses)

                if not comments_data:
                    scroll_attempts = 0
                    while len(comments_data) < 20 and scroll_attempts < 10:
                        page.mouse.wheel(0, 1500)
                        page.wait_for_timeout(2500)
                        comments_data = self._parse_comments_from_responses(captured_comment_responses)
                        scroll_attempts += 1
                        if len(comments_data) >= 20:
                            break

                if not comments_data:
                    comments_data = self._scrape_comments_dom(page)

                page.remove_listener("response", handle_response)

            except Exception:
                try:
                    page.remove_listener("response", handle_response)
                except Exception:
                    pass
                comments_data = []

            post_data["top_commenters"] = [c["username"] for c in comments_data]
            post_data["comments_text"] = [c["text"] for c in comments_data]

        return collected_posts

    def _parse_comments_from_responses(self, responses: list) -> List[Dict[str, str]]:
        comments_data = []
        seen_keys = set()

        def recursive_find_comments(obj, depth=0):
            if depth > 15 or len(comments_data) >= 20:
                return
            if isinstance(obj, dict):
                if "commentRenderer" in obj:
                    cr = obj["commentRenderer"]
                    username = ""
                    author_runs = cr.get("authorText", {}).get("runs", [])
                    if author_runs:
                        username = author_runs[0].get("text", "").strip().lstrip("@")
                    if not username:
                        username = cr.get("authorText", {}).get("simpleText", "").strip().lstrip("@")

                    comment_text = ""
                    content_runs = cr.get("contentText", {}).get("runs", [])
                    if content_runs:
                        comment_text = "".join(r.get("text", "") for r in content_runs).strip()
                    if not comment_text:
                        comment_text = cr.get("contentText", {}).get("simpleText", "").strip()

                    if username and comment_text:
                        dedup_key = f"{username}::{comment_text[:60]}"
                        if dedup_key not in seen_keys:
                            seen_keys.add(dedup_key)
                            comments_data.append({"username": username, "text": comment_text})
                else:
                    for v in obj.values():
                        recursive_find_comments(v, depth + 1)
            elif isinstance(obj, list):
                for item in obj:
                    recursive_find_comments(item, depth + 1)

        for response_body in responses:
            if len(comments_data) >= 20:
                break
            recursive_find_comments(response_body)

        return comments_data

    def _scrape_comments_dom(self, page: Page) -> List[Dict[str, str]]:
        comments_data = []
        seen_keys = set()

        try:
            page.wait_for_selector("ytd-comment-thread-renderer", timeout=8000)
        except Exception:
            return comments_data

        scroll_attempts = 0
        no_prog = 0
        prev_len = 0

        while len(comments_data) < 20 and scroll_attempts < 15:
            threads = page.locator("ytd-comment-thread-renderer")
            count = threads.count()

            for i in range(count):
                if len(comments_data) >= 20:
                    break

                thread = threads.nth(i)

                username = ""
                try:
                    u_loc = thread.locator("a#author-text span").first
                    if u_loc.count() > 0:
                        username = u_loc.inner_text().strip().lstrip("@")
                except Exception:
                    pass

                if not username:
                    continue

                comment_text = ""
                try:
                    t_loc = thread.locator(
                        "yt-attributed-string#content-text span.yt-core-attributed-string"
                    ).first
                    if t_loc.count() > 0:
                        comment_text = t_loc.inner_text().strip()
                except Exception:
                    pass

                if not comment_text:
                    continue

                dedup_key = f"{username}::{comment_text[:60]}"
                if dedup_key in seen_keys:
                    continue
                seen_keys.add(dedup_key)
                comments_data.append({"username": username, "text": comment_text})

            if len(comments_data) == prev_len:
                no_prog += 1
            else:
                no_prog = 0

            prev_len = len(comments_data)
            scroll_attempts += 1

            if no_prog >= 5:
                break

            page.mouse.wheel(0, 1200)
            page.wait_for_timeout(2000)

        return comments_data

    def _scrape_posts_dom_fallback(self, page: Page, max_posts: int) -> List[Dict[str, Any]]:
        videos_loaded = False
        for selector in [
            "ytd-rich-item-renderer",
            "ytd-rich-grid-media",
            "ytd-grid-video-renderer",
            'a#video-title-link',
            'a#video-title',
            'a[href*="/watch?v="]',
        ]:
            try:
                page.wait_for_selector(selector, timeout=8000)
                videos_loaded = True
                break
            except Exception:
                continue

        if not videos_loaded:
            return []

        page.wait_for_timeout(2000)
        collected_posts = []
        seen_video_urls = set()

        while len(collected_posts) < max_posts:
            items = page.locator("ytd-rich-item-renderer")
            if items.count() == 0:
                items = page.locator("ytd-rich-grid-media")
            if items.count() == 0:
                items = page.locator("ytd-grid-video-renderer")
            count = items.count()

            if count == 0:
                link_candidates = page.locator('a#video-title-link, a#video-title, a[href*="/watch?v="]')
                link_count = link_candidates.count()
                if link_count == 0:
                    break
                for i in range(link_count):
                    if len(collected_posts) >= max_posts:
                        break
                    link = link_candidates.nth(i)
                    href = link.get_attribute("href")
                    if not href or "/watch?v=" not in href:
                        continue
                    full_url = f"https://www.youtube.com{href}" if href.startswith("/") else href
                    if full_url in seen_video_urls:
                        continue
                    seen_video_urls.add(full_url)

                    title = ""
                    try:
                        title = (link.get_attribute("title") or "").strip()
                    except Exception:
                        pass
                    if not title:
                        try:
                            title = link.inner_text(timeout=1000).strip()
                        except Exception:
                            pass

                    collected_posts.append({
                        "status": "active",
                        "post_url": full_url,
                        "datetime": "",
                        "caption": title,
                        "media_url": "",
                        "media_type": "video",
                        "comments": "0",
                        "likes": "0",
                        "shares": "0",
                        "views": "0",
                        "top_commenters": [],
                        "comments_text": [],
                    })

                if len(collected_posts) < max_posts:
                    page.mouse.wheel(0, 900)
                    page.wait_for_timeout(1500)
                continue

            for i in range(count):
                if len(collected_posts) >= max_posts:
                    break

                item = items.nth(i)
                link_loc = item.locator("a#video-title-link").first
                if link_loc.count() == 0:
                    continue

                href = link_loc.get_attribute("href")
                if not href:
                    continue

                full_url = f"https://www.youtube.com{href}"
                if full_url in seen_video_urls:
                    continue
                seen_video_urls.add(full_url)

                title_loc = item.locator("yt-formatted-string#video-title").first
                title = title_loc.inner_text().strip() if title_loc.count() > 0 else ""

                meta_spans = item.locator("span.inline-metadata-item")
                views = meta_spans.nth(0).inner_text().strip() if meta_spans.count() > 0 else "0"
                posted_time = meta_spans.nth(1).inner_text().strip() if meta_spans.count() > 1 else ""

                thumb_loc = item.locator("ytd-thumbnail img").first
                thumbnail_url = thumb_loc.get_attribute("src") if thumb_loc.count() > 0 else ""

                collected_posts.append({
                    "status": "active",
                    "post_url": full_url,
                    "datetime": posted_time,
                    "caption": title,
                    "media_url": thumbnail_url,
                    "media_type": "video",
                    "comments": "0",
                    "likes": "0",
                    "shares": "0",
                    "views": views,
                    "top_commenters": [],
                    "comments_text": [],
                })

            if len(collected_posts) < max_posts:
                page.mouse.wheel(0, 900)
                page.wait_for_timeout(1500)
            else:
                break

        return collected_posts

    def parse_page(self, page: Page) -> Dict[str, Any]:
        if self._scope in {
            SOCIAL_REQUEST_COMMANDS.PROFILE_ONLY,
            SOCIAL_REQUEST_COMMANDS.FOLLOWERS_ONLY,
            SOCIAL_REQUEST_COMMANDS.FOLLOWING_ONLY,
        }:
            return super().parse_page(page)
        return self.scrape_posts_with_profile(page, max_posts=2)

    def scrape_followers(self, page: Page) -> List[str]:
        return []

    def scrape_following(self, page: Page) -> List[str]:
        return []

    def scrape_posts_with_profile(self, page: Page, max_posts: int = 2) -> Dict[str, Any]:
        profile_data = self.scrape_profile(page)
        posts_data = self.scrape_posts(page, max_posts)

        for post in posts_data:
            card = social_model(
                m_username=self._username,
                m_real_name=profile_data.get("real_name", ""),
                m_bio=profile_data.get("bio", ""),
                m_location=profile_data.get("location", ""),
                m_total_followers=profile_data.get("total_followers", ""),
                m_total_following=profile_data.get("total_following", ""),
                m_weblink=[post.get("post_url", "")],
                m_content=post.get("caption", ""),
                m_content_type=[post.get("media_type", "video")],
                m_platform="youtube",
                m_post_datetime=post.get("datetime", ""),
                m_post_comments=post.get("comments", "0"),
                m_post_likes=post.get("likes", "0"),
                m_channel_url=post.get("media_url", ""),
                m_network=self.seed_url,
                m_top_commenters=post.get("top_commenters", []),
                m_comments_text=post.get("comments_text", []),
            )

            self.data.append(card.model_dump())
            cross_platform_mapper.add_card(card)

        return {
            "profile": profile_data,
            "posts": posts_data,
            "total_posts": len(posts_data)
        }