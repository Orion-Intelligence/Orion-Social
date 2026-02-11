from playwright.sync_api import Page

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class tiktok(BaseScraper):
    requires_login = False

    def __init__(self, username: str):
        super().__init__()
        self._username = username.lstrip('@')

    @property
    def base_url(self) -> str:
        return f"https://www.tiktok.com/@{self._username}"

    @property
    def seed_url(self) -> str:
        return f"https://www.tiktok.com/@{self._username}"

    @property
    def name(self) -> str:
        return "TikTok"

    def parse_page(self, page: Page):

        page.wait_for_selector('[data-e2e="user-title"]', timeout=15000)
        page.wait_for_timeout(3000)

        username_loc = page.locator('[data-e2e="user-subtitle"]')
        username = username_loc.inner_text() if username_loc.count() > 0 else ""
        print("Username:", username)

        real_name_loc = page.locator('[data-e2e="user-title"]')
        real_name = real_name_loc.inner_text() if real_name_loc.count() > 0 else ""
        print("Real name:", real_name)

        bio_loc = page.locator('[data-e2e="user-bio"]')
        bio_text = bio_loc.inner_text() if bio_loc.count() > 0 else ""
        print("Bio:", bio_text)

        followers_loc = page.locator('[data-e2e="followers-count"]')
        total_followers = followers_loc.inner_text() if followers_loc.count() > 0 else ""
        print("Followers:", total_followers)

        following_loc = page.locator('[data-e2e="following-count"]')
        total_following = following_loc.inner_text() if following_loc.count() > 0 else ""
        print("Following:", total_following)

        likes_loc = page.locator('[data-e2e="likes-count"]')
        total_likes = likes_loc.inner_text() if likes_loc.count() > 0 else ""
        print("Total Likes:", total_likes)

        print("\nScrolling to load videos...")
        for i in range(3):
            page.evaluate(f"window.scrollBy(0, 1000)")
            page.wait_for_timeout(1500)

        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(2000)

        MAX_POSTS = 5
        collected_posts = []
        seen_post_urls = set()

        video_containers = page.locator('div[data-e2e="user-post-item"]').all()
        print(f"\nFound {len(video_containers)} total videos on page")

        for idx, container in enumerate(video_containers):
            if len(collected_posts) >= MAX_POSTS:
                break

            try:
                post_data = {}

                link_elem = container.locator('a[href*="/video/"]').first
                if link_elem.count() == 0:
                    continue

                post_url = link_elem.get_attribute('href')
                if not post_url:
                    continue

                if post_url in seen_post_urls:
                    continue
                seen_post_urls.add(post_url)

                post_data['post_url'] = post_url

                views_elem = container.locator('[data-e2e="video-views"]')
                if views_elem.count() > 0:
                    views_text = views_elem.inner_text().strip()
                    post_data['views'] = views_text if views_text else "0"
                else:
                    post_data['views'] = "0"

                img_elem = container.locator('img').first
                if img_elem.count() > 0:
                    post_data['media_url'] = img_elem.get_attribute('src') or ""
                else:
                    post_data['media_url'] = ""

                post_data['media_type'] = 'video'
                post_data['caption'] = ""
                post_data['likes'] = "0"
                post_data['comments'] = "0"

                collected_posts.append(post_data)
                print(f"\nProcessing video {len(collected_posts)}")
                print(f"  Post URL: {post_data['post_url']}")
                print(f"  Views: {post_data['views']}")

            except Exception as e:
                print(f"  Error parsing video: {e}")
                continue

        print(f"\nTotal videos collected: {len(collected_posts)}")

        for idx, post in enumerate(collected_posts, 1):
            card = social_model(
                m_username=username,
                m_real_name=real_name,
                m_bio=bio_text,
                m_total_posts="",
                m_total_followers=total_followers,
                m_total_following=total_following,
                m_weblink=[post.get('post_url', '')],
                m_content=post.get('caption', ''),
                m_content_type=[post.get('media_type', 'video')],
                m_platform="tiktok",
                m_post_comments="0",
                m_post_likes="0",
                m_retweets="0",
                m_post_views=post.get('views', '0'),
                m_channel_url=post.get('media_url', ''),
                m_network=self.seed_url
            )

            print(f"\n=== Video {idx} ===")
            print(f"Post URL: {post.get('post_url', '')}")
            print(f"Views: {post.get('views', '0')}")

            self.data.append(card.model_dump())
            cross_platform_mapper.add_card(card)