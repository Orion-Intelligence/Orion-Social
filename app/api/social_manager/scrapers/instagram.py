from typing import Dict, Any, List
from playwright.sync_api import Page
from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper
import re


class InstagramScraper(BaseScraper):
    requires_login = True

    def __init__(self, username: str, max_followers: int = 50, max_following: int = 50):
        super().__init__(username, max_followers, max_following)

    @property
    def base_url(self) -> str:
        return "https://www.instagram.com/"

    @property
    def seed_url(self) -> str:
        return f"https://www.instagram.com/{self._username}"

    @property
    def name(self) -> str:
        return "Instagram"

    def _scroll_and_collect(self, page: Page, max_items: int) -> list:
        page.wait_for_selector("div[role='dialog'] a.notranslate")

        loc = page.locator("div[role='dialog'] a.notranslate").first
        box = loc.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] + 20, box["y"] + 10)

        collected = set()
        prev_count = 0
        no_progress_rounds = 0
        max_no_progress = 5

        while len(collected) < max_items and no_progress_rounds < max_no_progress:
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(5000)

            loc = page.locator("div[role='dialog'] a.notranslate")
            try:
                current = loc.all_inner_texts()
            except:
                current = []

            collected.update(current)

            if len(collected) == prev_count:
                no_progress_rounds += 1
            else:
                no_progress_rounds = 0

            prev_count = len(collected)

        return list(collected)[:max_items]

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_selector("header")

        loc = page.locator("header section h1, header section span[dir='auto']")
        real_name = loc.first.inner_text() if loc.count() > 0 else ""

        posts = page.locator("header section span span span").first
        total_posts = posts.inner_text() if posts.count() > 0 else ""

        loc = page.locator("a[href$='/followers/'] span")
        followers_count = loc.nth(1).inner_text() if loc.count() > 1 else ""

        loc = page.locator("a[href$='/following/'] span")
        following_count = loc.nth(1).inner_text() if loc.count() > 1 else ""

        bio = page.locator("header section span._ap3a._aaco._aacu._aacx._aad7._aade").first
        bio_text = bio.inner_text() if bio.count() > 0 else ""

        return {
            "real_name": real_name,
            "bio": bio_text,
            "location": "",
            "total_posts": total_posts,
            "total_followers": followers_count,
            "total_following": following_count,
            "profile_url": self.seed_url
        }

    def _dismiss_popups(self, page: Page):
        popup_selectors = [
            "button:has-text('Not Now')",
            "button:has-text('Not now')",
            "button:has-text('Cancel')",
            "button:has-text('Decline')",
            "[role='dialog'] button[type='button']",
            "div[role='dialog'] svg[aria-label='Close']",
        ]
        for selector in popup_selectors:
            try:
                loc = page.locator(selector).first
                if loc.count() > 0 and loc.is_visible():
                    loc.click(timeout=2000)
                    page.wait_for_timeout(500)
            except:
                pass

    def _click_link(self, page: Page, selector: str):
        self._dismiss_popups(page)
        try:
            page.click(selector, timeout=5000)
        except:
            page.locator(selector).first.evaluate("el => el.click()")

    def scrape_followers(self, page: Page) -> List[str]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        self._click_link(page, "a[href$='/followers/']")
        page.wait_for_timeout(3000)
        return self._scroll_and_collect(page, self._max_followers)

    def scrape_following(self, page: Page) -> List[str]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        self._click_link(page, "a[href$='/following/']")
        page.wait_for_timeout(3000)
        return self._scroll_and_collect(page, self._max_following)

    def _extract_number_from_text(self, text: str) -> str:
        if not text:
            return "0"

        text = text.strip()

        if 'K' in text.upper():
            match = re.search(r'([\d.]+)\s*K', text, re.IGNORECASE)
            if match:
                return str(int(float(match.group(1)) * 1000))
        elif 'M' in text.upper():
            match = re.search(r'([\d.]+)\s*M', text, re.IGNORECASE)
            if match:
                return str(int(float(match.group(1)) * 1000000))

        match = re.search(r'([\d,]+)', text)
        if match:
            return match.group(1).replace(',', '')

        return "0"

    def scrape_posts(self, page: Page, max_posts: int = 5) -> List[Dict[str, Any]]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        collected_urls = []
        seen_urls = set()
        prev_count = 0
        no_progress_rounds = 0
        max_no_progress = 5

        while len(collected_urls) < max_posts and no_progress_rounds < max_no_progress:
            post_elements = page.locator("a[href*='/p/'], a[href*='/reel/']").all()

            for elem in post_elements:
                if len(collected_urls) >= max_posts:
                    break

                try:
                    href = elem.get_attribute("href")
                    if not href:
                        continue

                    if href.startswith("/"):
                        post_url = f"https://www.instagram.com{href}"
                    else:
                        post_url = href

                    base_url = post_url.split("?")[0]
                    if base_url not in seen_urls:
                        seen_urls.add(base_url)
                        collected_urls.append(base_url)
                except:
                    continue

            if len(collected_urls) == prev_count:
                no_progress_rounds += 1
            else:
                no_progress_rounds = 0

            prev_count = len(collected_urls)

            if len(collected_urls) < max_posts:
                page.mouse.wheel(0, 1500)
                page.wait_for_timeout(2000)

        collected_posts = []

        for post_url in collected_urls[:max_posts]:
            try:
                page.goto(post_url, wait_until="domcontentloaded")
                page.wait_for_timeout(3000)

                post_data = {"post_url": post_url}

                time_elem = page.locator("time").first
                post_data["datetime"] = time_elem.get_attribute("datetime") if time_elem.count() > 0 else ""

                caption_text = ""
                likes_count = "0"
                comments_count = "0"

                meta_desc = page.locator("meta[property='og:description']").first
                if meta_desc.count() > 0:
                    meta_content = meta_desc.get_attribute("content") or ""

                    likes_match = re.search(r'([\d.,KkMm]+)\s+likes', meta_content)
                    comments_match = re.search(r'([\d.,KkMm]+)\s+comments', meta_content)

                    if likes_match:
                        likes_count = self._extract_number_from_text(likes_match.group(1))

                    if comments_match:
                        comments_count = self._extract_number_from_text(comments_match.group(1))

                    caption_match = re.search(r':\s*"(.*)"', meta_content)
                    if caption_match:
                        caption_text = caption_match.group(1)

                if not caption_text:
                    h1_loc = page.locator("h1").first
                    if h1_loc.count() > 0:
                        caption_text = h1_loc.inner_text().strip()

                post_data["caption"] = caption_text.strip()
                post_data["likes"] = likes_count
                post_data["comments"] = comments_count
                post_data["shares"] = "0"
                post_data["views"] = "0"

                video_loc = page.locator("video")
                if video_loc.count() > 0:
                    post_data["media_type"] = "video"
                    post_data["media_url"] = video_loc.first.get_attribute("src") or ""
                else:
                    img_loc = page.locator("article img[src]").first
                    if img_loc.count() > 0:
                        post_data["media_type"] = "image"
                        post_data["media_url"] = img_loc.get_attribute("src") or ""
                    else:
                        post_data["media_type"] = "text"
                        post_data["media_url"] = ""

                collected_posts.append(post_data)

            except:
                collected_posts.append({
                    "post_url": post_url,
                    "datetime": "",
                    "caption": "",
                    "media_url": "",
                    "media_type": "unknown",
                    "likes": "0",
                    "comments": "0",
                    "shares": "0",
                    "views": "0"
                })

        return collected_posts

    def scrape_posts_with_profile(self, page: Page, max_posts: int = 5) -> Dict[str, Any]:
        profile_data = self.scrape_profile(page)
        posts_data = self.scrape_posts(page, max_posts)

        for post in posts_data:
            card = social_model(
                m_username=profile_data.get("username", ""),
                m_real_name=profile_data.get("real_name", ""),
                m_bio=profile_data.get("bio", ""),
                m_total_followers=profile_data.get("total_followers", ""),
                m_total_following=profile_data.get("total_following", ""),
                m_weblink=[post.get("post_url", "")],
                m_content=post.get("caption", ""),
                m_content_type=[post.get("media_type", "text")],
                m_platform="instagram",
                m_post_datetime=post.get("datetime", ""),
                m_post_comments=post.get("comments", "0"),
                m_post_likes=post.get("likes", "0"),
                m_channel_url=post.get("media_url", ""),
                m_network=self.seed_url
            )

            self.data.append(card.model_dump())
            cross_platform_mapper.add_card(card)

        return {
            "profile": profile_data,
            "posts": posts_data,
            "total_posts": len(posts_data)
        }
