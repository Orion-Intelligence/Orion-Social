from typing import Dict, Any, List
from urllib.parse import quote_plus
from playwright.sync_api import Page

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class ImageScraper(BaseScraper):
    requires_login = False

    def __init__(self, name: str, limit: int = 100, max_followers: int = 0, max_following: int = 0):
        super().__init__(name, max_followers, max_following)
        self._name = name
        self._limit = limit

    @property
    def base_url(self) -> str:
        encoded_query = quote_plus(self._name)
        return f"https://duckduckgo.com/?q={encoded_query}&t=h_&iax=images&ia=images"

    @property
    def seed_url(self) -> str:
        return self.base_url

    @property
    def name(self) -> str:
        return "DuckDuckGoImages"

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        return {}

    def scrape_followers(self, page: Page) -> List[str]:
        return []

    def scrape_following(self, page: Page) -> List[str]:
        return []

    def parse_page(self, page: Page) -> Dict[str, Any]:
        page.wait_for_timeout(3000)

        image_urls = []

        try:
            page.wait_for_selector("img.tile--img__img", timeout=15000)

            for _ in range(3):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1500)

            imgs = page.eval_on_selector_all(
                "img.tile--img__img",
                "els => els.map(e => e.getAttribute('data-src') || e.src).filter(s => s)"
            )

            for img in imgs:
                if not img:
                    continue

                if img.startswith("//"):
                    img = "https:" + img
                elif not img.startswith("http"):
                    continue

                if img not in image_urls:
                    image_urls.append(img)

                if len(image_urls) >= self._limit:
                    break

        except Exception:
            try:
                imgs = page.eval_on_selector_all(
                    "img",
                    "els => els.map(e => e.src).filter(s => s && s.startsWith('http') && !s.includes('duckduckgo'))"
                )
                for img in imgs:
                    if img not in image_urls:
                        image_urls.append(img)
                    if len(image_urls) >= self._limit:
                        break
            except Exception:
                pass
        print(image_urls)
        card = social_model(
            m_username=self._name,
            m_platform="duckduckgo_images",
            m_content_type=["images"],
            m_image_urls=image_urls,
            m_content=f"Total Images Found: {len(image_urls)}"
        )

        print(card)

        self.data.append(card.model_dump())
        cross_platform_mapper.add_card(card)

        return {
            "platform": "duckduckgo_images",
            "query": self._name,
            "images": image_urls,
            "total_images": len(image_urls)
        }