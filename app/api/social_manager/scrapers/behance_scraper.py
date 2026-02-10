import time
from typing import Dict, Any, List
from playwright.sync_api import Page

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class BehanceScraper(BaseScraper):

    requires_login = False

    def __init__(self, username: str, max_followers: int = 50, max_following: int = 50):
        super().__init__(username, max_followers, max_following)

    @property
    def base_url(self) -> str:
        return "https://www.behance.net"

    @property
    def follower_url(self) -> str:
        return f"https://www.behance.net/{self._username}/followers"

    @property
    def following_url(self) -> str:
        return f"https://www.behance.net/{self._username}/following"

    @property
    def seed_url(self) -> str:
        return f"https://www.behance.net/{self._username}"

    @property
    def name(self) -> str:
        return "Behance"

    def _collect_names(self, page: Page, url: str, max_items: int) -> list:
        page.goto(url)
        page.wait_for_selector('div.ScrollableModal-content-SvL', timeout=30000)

        collected = set()
        no_progress_rounds = 0
        max_no_progress = 10

        while len(collected) < max_items and no_progress_rounds < max_no_progress:
            names = page.evaluate('''
                () => Array.from(document.querySelectorAll('h3.ProfileRow-displayName-ZZg a'))
                           .map(a => a.innerText.trim())
                           .filter(Boolean)
            ''')

            added = 0
            for n in names:
                if len(collected) >= max_items:
                    break

                if n not in collected:
                    collected.add(n)
                    added += 1

            if len(collected) >= max_items:
                break

            if added == 0:
                no_progress_rounds += 1
                time.sleep(1)
            else:
                no_progress_rounds = 0

            page.evaluate('''
                const modal = document.querySelector('div.ScrollableModal-scrollableTarget-IZX');
                if (modal) modal.scrollBy(0, modal.clientHeight * 5);
            ''')

            time.sleep(1.5)

        return list(collected)[:max_items]

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        name_el = page.query_selector('h1.ProfileCard-userFullName-f5A')
        name = name_el.inner_text().strip() if name_el else ""

        username_el = page.query_selector('span.ProfileCard-userName-qCN')
        username = username_el.inner_text().strip() if username_el else self._username

        bio_el = page.query_selector('p.ProfileCard-line-Fpm')
        bio = bio_el.inner_text().strip() if bio_el else ""

        location_el = page.query_selector('span.ProfileCard-location-MhL')
        location = location_el.inner_text().strip() if location_el else ""

        followers_el = page.query_selector('a[href$="/followers"] span.ProfileCard-count-jFB')
        followers_count = followers_el.inner_text().strip() if followers_el else ""

        following_el = page.query_selector('a[href$="/following"] span.ProfileCard-count-jFB')
        following_count = following_el.inner_text().strip() if following_el else ""

        return {
            "username": username,
            "real_name": name,
            "bio": bio,
            "location": location,
            "total_posts": "",
            "total_followers": followers_count,
            "total_following": following_count,
            "profile_url": self.seed_url
        }

    def scrape_followers(self, page: Page) -> List[str]:
        return self._collect_names(page, url=self.follower_url, max_items=self._max_followers)

    def scrape_following(self, page: Page) -> List[str]:
        return self._collect_names(page, url=self.following_url, max_items=self._max_following)
