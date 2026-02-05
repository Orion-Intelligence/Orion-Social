from playwright.sync_api import Page
from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class InstagramScraper(BaseScraper):
    requires_login = True

    def __init__(self, username: str, max_followers: int, max_following: int):
        super().__init__()
        self._username = username
        self._max_followers = max_followers
        self._max_following = max_following

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

    def parse_page(self, page: Page):
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

        page.click("a[href$='/following/']")
        page.wait_for_timeout(3000)
        following_users = self._scroll_and_collect(page, self._max_following)

        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        page.click("a[href$='/followers/']")
        page.wait_for_timeout(3000)
        followers_users = self._scroll_and_collect(page, self._max_followers)

        mutual = list(set(followers_users) & set(following_users))

        card = social_model(
            m_username=username,
            m_real_name=real_name,
            m_bio=bio_text,
            m_total_posts=total_posts,
            m_total_followers=followers_count,
            m_total_following=following_count,
            m_weblink=[f"{self.seed_url}/followers/", f"{self.seed_url}/following/"],
            m_content_type=["instagram_followers", "instagram_following", "instagram_mutual"],
            m_platform="instagram",
            m_network="clearnet",
            m_followers=followers_users,
            m_following=following_users,
            m_mutual_usernames=mutual
        )

        self.data.append(card.model_dump())
        cross_platform_mapper.add_card(card)

        return card.model_dump()
