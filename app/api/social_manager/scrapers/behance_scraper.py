import time
from typing import Dict, Any
from playwright.sync_api import Page

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class BehanceScraper(BaseScraper):

    requires_login = False

    def __init__(self, username: str, max_followers: int, max_following: int):
        super().__init__()
        self._username = username
        self._max_followers = max_followers
        self._max_following = max_following

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
        return "https://www.behance.net"

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

    def parse_page(self, page: Page) -> Dict[str, Any]:
        followers = self._collect_names(page, url=self.follower_url, max_items=self._max_followers)
        following = self._collect_names(page, url=self.following_url, max_items=self._max_following)
        mutual_usernames = list(set(followers) & set(following))

        card = social_model(
            m_weblink=[self.follower_url, self.following_url],
            m_content_type=["behance_followers", "behance_following", "behance_mutual"],
            m_network="clearnet",
            m_platform="behance",
            m_followers=followers,
            m_following=following,
            m_mutual_usernames=mutual_usernames
        )

        self.data.append(card.model_dump())
        cross_platform_mapper.add_card(card)

        return card.model_dump()
