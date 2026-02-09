from playwright.sync_api import Page

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class ImageScraper(BaseScraper):
    requires_login = False

    def __init__(self, name: str, platform: str, limit: int = 100):
        super().__init__()
        self._name = name
        self._platform = platform.lower()
        self._limit = limit

        if self._platform not in ["facebook", "instagram"]:
            raise ValueError("platform must be 'facebook' or 'instagram'")

    @property
    def base_url(self) -> str:

        query = f'site:{self._platform}.com "{self._name}"'
        return f"https://duckduckgo.com/?q={query}&iax=images&ia=images"

    @property
    def seed_url(self) -> str:
        return self.base_url

    @property
    def name(self) -> str:
        return f"{self._platform.capitalize()} Image Search"

    def parse_page(self, page: Page):

        page.wait_for_selector("ol li figure img", timeout=10000)

        imgs = page.eval_on_selector_all(
            "ol li figure img",
            "els => els.map(e => e.src)"
        )

        image_urls = []
        for img in imgs:
            if not img:
                continue

            img = img if img.startswith("http") else "https:" + img

            if img not in image_urls:
                image_urls.append(img)

            if len(image_urls) >= self._limit:
                break

        print(f"\nTotal Images Found: {len(image_urls)}")

        print(image_urls)

        card = social_model(
            m_username=self._name,
            m_platform=self._platform,
            m_content_type=[f"{self._platform}_images"],
            m_image_urls=image_urls,
            m_content=f"Total Images Found: {len(image_urls)}"
        )

        self.data.append(card.model_dump())
        cross_platform_mapper.add_card(card)