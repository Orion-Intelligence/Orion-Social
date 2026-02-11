from typing import Dict, Any, List
from playwright.sync_api import Page


from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper

class DuckDuckGoScraper(BaseScraper):

    def __init__(self, username: str, platform: str = "instagram.com", max_followers: int = 0, max_following: int = 0):
        super().__init__(username, max_followers, max_following)
        self._search_username = username
        self._platform = platform

    @property
    def base_url(self) -> str:
        return "https://html.duckduckgo.com/html"

    @property
    def seed_url(self) -> str:
        return "https://html.duckduckgo.com/html"

    @property
    def name(self) -> str:
        return "DuckDuckGo"

    def _build_search_query(self) -> str:
        return f'site:{self._platform} "{self._search_username}"'

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        return {}

    def scrape_followers(self, page: Page) -> List[str]:
        return []

    def scrape_following(self, page: Page) -> List[str]:
        return []

    def parse_page(self, page: Page) -> Dict[str, Any]:
        search_query = self._build_search_query()
        encoded_query = search_query.replace(" ", "+").replace(":", "%3A").replace('"', "%22")
        search_url = f"{self.base_url}/?q={encoded_query}"

        page.goto(search_url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        self._extract_results(page)

        try:
            next_button = page.query_selector('input.btn[value="Next"]')
            if next_button:
                next_button.click()
                page.wait_for_timeout(2000)
                self._extract_results(page)
        except Exception:
            pass

        print(self.data)
        return {
            "platform": "duckduckgo",
            "query": self._search_username,
            "target_platform": self._platform,
            "results": self.data,
            "total_results": len(self.data)
        }

    def _extract_results(self, page: Page) -> None:
        try:
            result_links = page.query_selector_all('div.result__body')

            for result in result_links:
                try:
                    title_element = result.query_selector('a.result__a')
                    if not title_element:
                        continue

                    href = title_element.get_attribute('href')
                    title_text = title_element.text_content().strip()

                    snippet_element = result.query_selector('a.result__snippet')
                    snippet_text = snippet_element.text_content().strip() if snippet_element else ""

                    url_element = result.query_selector('a.result__url')
                    url_text = url_element.text_content().strip() if url_element else ""

                    username = None
                    if '/' in url_text:
                        parts = url_text.rstrip('/').split('/')
                        username = parts[-1] if parts else None

                    real_name = None
                    if '(' in title_text and ')' in title_text:
                        real_name = title_text.split('(')[0].strip()
                    elif ' - ' in title_text:
                        real_name = title_text.split(' - ')[0].strip()
                    elif '@' in title_text:
                        real_name = title_text.split('@')[0].strip()

                    if not real_name and snippet_text:
                        if ' from ' in snippet_text.lower():
                            parts = snippet_text.lower().split(' from ')
                            if len(parts) > 1:
                                name_part = parts[-1]
                                if '(' in name_part:
                                    real_name = name_part.split('(')[0].strip().title()

                    if username and real_name:
                        existing = [d for d in self.data if d.get('m_username') == username]
                        if not existing:
                            card = social_model(
                                m_username=username,
                                m_real_name=real_name,
                                m_platform=self._platform,
                                m_weblink=[href] if href else [],
                            )

                            self.data.append(card.model_dump())
                            cross_platform_mapper.add_card(card)

                except Exception:
                    continue

        except Exception:
            pass