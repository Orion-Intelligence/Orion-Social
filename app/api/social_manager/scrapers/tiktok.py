from typing import Dict, Any, List
from playwright.sync_api import Page

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class TikTokScraper(BaseScraper):
    requires_login = False

    def __init__(self, username: str, max_followers: int = 50, max_following: int = 50):
        super().__init__(username, max_followers, max_following)
        self._username = username.lstrip('@')

    @property
    def base_url(self) -> str:
        return "https://www.tiktok.com"

    @property
    def seed_url(self) -> str:
        return f"https://www.tiktok.com/@{self._username}"

    @property
    def name(self) -> str:
        return "TikTok"

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_selector('[data-e2e="user-title"]', timeout=15000)
        page.wait_for_timeout(3000)

        username_loc = page.locator('[data-e2e="user-subtitle"]')
        username = username_loc.inner_text() if username_loc.count() > 0 else ""

        real_name_loc = page.locator('[data-e2e="user-title"]')
        real_name = real_name_loc.inner_text() if real_name_loc.count() > 0 else ""

        bio_loc = page.locator('[data-e2e="user-bio"]')
        bio_text = bio_loc.inner_text() if bio_loc.count() > 0 else ""

        followers_loc = page.locator('[data-e2e="followers-count"]')
        total_followers = followers_loc.inner_text() if followers_loc.count() > 0 else ""

        following_loc = page.locator('[data-e2e="following-count"]')
        total_following = following_loc.inner_text() if following_loc.count() > 0 else ""

        likes_loc = page.locator('[data-e2e="likes-count"]')
        total_likes = likes_loc.inner_text() if likes_loc.count() > 0 else ""

        return {
            "real_name": real_name,
            "bio": bio_text,
            "location": "",
            "total_posts": "",
            "total_followers": total_followers,
            "total_following": total_following,
            "total_likes": total_likes,
            "profile_url": self.seed_url
        }

    def scrape_posts(self, page: Page, max_posts: int = 5) -> List[Dict[str, Any]]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_selector('[data-e2e="user-title"]', timeout=15000)
        page.wait_for_timeout(3000)

        for i in range(3):
            page.evaluate("window.scrollBy(0, 1000)")
            page.wait_for_timeout(1500)

        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(2000)

        collected_posts = []
        seen_post_urls = set()

        video_containers = page.locator('div[data-e2e="user-post-item"]').all()

        for container in video_containers:
            if len(collected_posts) >= max_posts:
                break

            try:
                link_elem = container.locator('a[href*="/video/"]').first
                if link_elem.count() == 0:
                    continue

                post_url = link_elem.get_attribute('href')
                if not post_url or post_url in seen_post_urls:
                    continue

                seen_post_urls.add(post_url)

                post_data = {"post_url": post_url}

                views_elem = container.locator('[data-e2e="video-views"]')
                post_data['views'] = views_elem.inner_text().strip() if views_elem.count() > 0 else "0"

                img_elem = container.locator('img').first
                post_data['media_url'] = img_elem.get_attribute('src') or "" if img_elem.count() > 0 else ""

                post_data['datetime'] = ""
                post_data['caption'] = ""
                post_data['media_type'] = "video"
                post_data['likes'] = "0"
                post_data['comments'] = "0"
                post_data['shares'] = "0"

                collected_posts.append(post_data)

            except:
                continue

        return collected_posts

    def scrape_posts_with_profile(self, page: Page, max_posts: int = 5) -> Dict[str, Any]:
        profile_data = self.scrape_profile(page)
        posts_data = self.scrape_posts(page, max_posts)

        for post in posts_data:
            card = social_model(
                m_username=profile_data.get("username", ""),
                m_real_name=profile_data.get("real_name", ""),
                m_bio=profile_data.get("bio", ""),
                m_total_posts="",
                m_total_followers=profile_data.get("total_followers", ""),
                m_total_following=profile_data.get("total_following", ""),
                m_weblink=[post.get("post_url", "")],
                m_content=post.get("caption", ""),
                m_content_type=[post.get("media_type", "video")],
                m_platform="tiktok",
                m_post_datetime=post.get("datetime", ""),
                m_post_comments=post.get("comments", "0"),
                m_post_likes=post.get("likes", "0"),
                m_retweets=post.get("shares", "0"),
                m_post_views=post.get("views", "0"),
                m_channel_url=post.get("media_url", ""),
                m_network=self.seed_url
            )

            self.data.append(card.model_dump())
            cross_platform_mapper.add_card(card)

        return {
            "profile": profile_data,
            "posts": posts_data,
            "total_posts": len(posts_data)
        }

    def scrape_followers(self, page: Page) -> List[str]:
        return []

    def scrape_following(self, page: Page) -> List[str]:
        return []