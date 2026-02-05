from typing import Dict, Any
from playwright.sync_api import Page

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class VimeoScraper(BaseScraper):

    requires_login = False

    def __init__(self, username: str, max_followers: int, max_following: int):
        super().__init__()
        self._username = username
        self._max_followers = max_followers
        self._max_following = max_following

    @property
    def base_url(self) -> str:
        return f"https://vimeo.com/{self._username}"

    @property
    def seed_url(self) -> str:
        return f"https://vimeo.com/{self._username}"

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

    def parse_page(self, page: Page) -> Dict[str, Any]:
        username = page.locator("div.sc-aa85dd4c-2 span div.sc-aa85dd4c-7").first.inner_text().strip()

        followers_anchor = page.locator("a[href*='following/followers']")
        followers_link = followers_anchor.get_attribute("href")

        following_anchor = page.locator("a[href$='/following']")
        following_link = following_anchor.get_attribute("href")

        followers_data = self._collect_paginated_data(page, followers_link, self._max_followers)
        following_data = self._collect_paginated_data(page, following_link, self._max_following)
        mutual = list(set(followers_data) & set(following_data))

        card = social_model(
            m_username=username,
            m_weblink=[followers_link, following_link],
            m_content_type=["vimeo_followers", "vimeo_following", "vimeo_mutual"],
            m_network="clearnet",
            m_platform="vimeo",
            m_followers=followers_data,
            m_following=following_data,
            m_mutual_usernames=mutual
        )

        self.data.append(card.model_dump())
        cross_platform_mapper.add_card(card)

        return card.model_dump()
