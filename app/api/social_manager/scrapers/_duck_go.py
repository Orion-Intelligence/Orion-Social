from playwright.sync_api import Page


from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper

class DuckDuckGoScraper(BaseScraper):

    def __init__(self, username: str, platform: str = "instagram.com"):
        super().__init__()
        self._search_username = username
        self._platform = platform

    @property
    def base_url(self) -> str:
        return "https://duckduckgo.com"

    @property
    def seed_url(self) -> str:
        return "https://duckduckgo.com"

    @property
    def name(self) -> str:
        return "DuckDuckGo"

    def _build_search_query(self) -> str:
        return f'site:{self._platform} "{self._search_username}"'

    def print_results(self) -> None:
        if not self.data:
            print(f"\n[{self.name}] No data collected yet.")
            return

        print("\n" + "=" * 80)
        print(f"[{self.name}] SEARCH RESULTS")
        print("=" * 80)
        print(f"{'#':<4} {'@Username':<30} {'Real Name':<40}")
        print("-" * 80)

        for idx, data in enumerate(self.data, 1):
            username = data.get('m_username', 'N/A')
            real_name = data.get('m_real_name', 'N/A')
            print(f"{idx:<4} {username:<30} {real_name:<40}")

        print("=" * 80 + "\n")

    def parse_page(self, page: Page) -> None:
        search_query = self._build_search_query()
        search_url = f"{self.base_url}/?q={search_query.replace(' ', '+').replace(':', '%3A').replace('"', '%22')}"

        print(f"[{self.name}] Searching for: {search_query}")

        page.goto(search_url, wait_until="networkidle")
        page.wait_for_selector('article[data-testid="result"]', timeout=15000)

        print(f"[{self.name}] Collecting results from page 1...")
        self._extract_results(page)

        try:
            more_button = page.query_selector('button#more-results')
            if more_button:
                print(f"[{self.name}] Clicking 'More results' button...")
                more_button.click()
                page.wait_for_selector('article[data-testid="result"]', timeout=15000)
                page.wait_for_timeout(2000)

                print(f"[{self.name}] Collecting results from page 2...")
                self._extract_results(page)
            else:
                print(f"[{self.name}] 'More results' button not found")
        except Exception as e:
            print(f"[{self.name}] Error: {str(e)}")

        print(f"[{self.name}] Total collected: {len(self.data)}")

    def _extract_results(self, page: Page) -> None:
        try:
            result_articles = page.query_selector_all('article[data-testid="result"]')
            print(f"[{self.name}] Found {len(result_articles)} results")

            for article in result_articles:
                try:
                    url_element = article.query_selector('a[data-testid="result-extras-url-link"]')
                    if not url_element:
                        continue

                    url_text = url_element.text_content().strip()
                    username = None
                    if '›' in url_text:
                        username = url_text.split('›')[-1].strip()

                    real_name = None
                    snippet_element = article.query_selector('div[data-result="snippet"]')
                    if snippet_element:
                        snippet_text = snippet_element.text_content().strip()
                        if ' from ' in snippet_text:
                            real_name_part = snippet_text.split(' from ')[-1]
                            if '(' in real_name_part:
                                real_name = real_name_part.split('(')[0].strip()

                    if not real_name:
                        title_element = article.query_selector('h2.LnpumSThxEWMIsDdAT17 a')
                        if title_element:
                            title_text = title_element.text_content().strip()
                            if '(' in title_text:
                                real_name = title_text.split('(')[0].strip()

                    if username and real_name:
                        existing = [d for d in self.data if d.get('m_username') == username]
                        if not existing:
                            card = social_model(
                                m_username=username,
                                m_real_name=real_name,
                                m_platform=self._platform,
                                m_weblink=[url_element.get_attribute('href')],
                            )

                            print(f"  → {real_name} (@{username})")
                            self.data.append(card.model_dump())
                            cross_platform_mapper.add_card(card)

                except Exception as e:
                    continue

        except Exception as e:
            print(f"[{self.name}] Error extracting results: {str(e)}")