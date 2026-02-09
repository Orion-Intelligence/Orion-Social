from typing import Dict, Any, List
from playwright.sync_api import Page

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class VimeoScraper(BaseScraper):

    requires_login = False

    def __init__(self, username: str, max_followers: int = 50, max_following: int = 50):
        super().__init__(username, max_followers, max_following)

    @property
    def base_url(self) -> str:
        return f"https://vimeo.com/{self._username}"

    @property
    def seed_url(self) -> str:
        return f"https://vimeo.com/{self._username}"

    @property
    def followers_url(self) -> str:
        return f"https://vimeo.com/{self._username}/following/followers"

    @property
    def following_url(self) -> str:
        return f"https://vimeo.com/{self._username}/following"

    @property
    def name(self) -> str:
        return "Vimeo"

    def _collect_paginated_data(self, page: Page, url: str, max_items: int) -> list:
        base_url = "https://www.vimeo.com"
        page.goto(url)

        collected = []
        seen = set()

        while len(collected) < max_items:
            blocks = page.query_selector_all("div.data")

            for b in blocks:
                if len(collected) >= max_items:
                    break
                title_el = b.query_selector("p.title")
                title = title_el.inner_text().strip() if title_el else ""
                if title and title not in seen:
                    seen.add(title)
                    collected.append(title)

            next_btn = page.query_selector("li.pagination_next a")

            if next_btn:
                next_href = next_btn.get_attribute("href")
                if not next_href:
                    break

                next_page_url = base_url + next_href
                page.goto(next_page_url)
            else:
                break

        return collected[:max_items]

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        username_el = page.locator("div.sc-aa85dd4c-2 span div.sc-aa85dd4c-7").first
        username = username_el.inner_text().strip() if username_el.count() > 0 else self._username

        name_el = page.query_selector('h1')
        name = name_el.inner_text().strip() if name_el else ""

        bio_el = page.query_selector('div.sc-aa85dd4c-5')
        bio = bio_el.inner_text().strip() if bio_el else ""

        location_el = page.query_selector('span.sc-aa85dd4c-8')
        location = location_el.inner_text().strip() if location_el else ""

        return {
            "username": username,
            "real_name": name,
            "bio": bio,
            "location": location,
            "profile_url": self.seed_url
        }

    def scrape_followers(self, page: Page) -> List[str]:
        return self._collect_paginated_data(page, self.followers_url, self._max_followers)

    def scrape_following(self, page: Page) -> List[str]:
        return self._collect_paginated_data(page, self.following_url, self._max_following)
