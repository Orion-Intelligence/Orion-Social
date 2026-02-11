from typing import Dict, Any, List
from playwright.sync_api import Page
from api.social_manager.scrapers.base_scraper import BaseScraper


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
            current = []
            try:
                current = loc.all_inner_texts()
            except Exception:
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

        loc = page.locator("header h2, header span._ap3a")
        username = loc.first.inner_text() if loc.count() > 0 else ""

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
            "username": username,
            "real_name": real_name,
            "bio": bio_text,
            "total_posts": total_posts,
            "total_followers": followers_count,
            "total_following": following_count,
            "profile_url": self.seed_url
        }

    def scrape_followers(self, page: Page) -> List[str]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        page.click("a[href$='/followers/']")
        page.wait_for_timeout(3000)
        return self._scroll_and_collect(page, self._max_followers)

    def scrape_following(self, page: Page) -> List[str]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        page.click("a[href$='/following/']")
        page.wait_for_timeout(3000)
        return self._scroll_and_collect(page, self._max_following)
