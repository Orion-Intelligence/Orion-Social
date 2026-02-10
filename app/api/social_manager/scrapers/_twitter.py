from typing import Dict, Any, List
from playwright.sync_api import Page
from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.helper_methods.cross_platform_mapping import cross_platform_mapper


class TwitterScraper(BaseScraper):
    requires_login = True

    def __init__(self, username: str, max_followers: int = 50, max_following: int = 50):
        super().__init__(username, max_followers, max_following)

    @property
    def base_url(self) -> str:
        return "https://x.com/"

    @property
    def seed_url(self) -> str:
        return f"https://x.com/{self._username}"

    @property
    def name(self) -> str:
        return "Twitter"

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_selector('[data-testid="UserName"]', timeout=10000)

        loc = page.locator('[data-testid="UserName"] span').filter(has_text="@")
        username = loc.first.inner_text() if loc.count() > 0 else ""

        loc = page.locator('[data-testid="UserName"] span.css-1jxf684').first
        real_name = loc.inner_text() if loc.count() > 0 else ""

        loc = page.locator('[data-testid="UserDescription"]')
        bio_text = loc.first.inner_text() if loc.count() > 0 else ""

        loc = page.locator('[data-testid="UserJoinDate"] span').last
        joined_date = loc.inner_text() if loc.count() > 0 else ""

        loc = page.locator('[data-testid="UserLocation"] span').last
        location = loc.inner_text() if loc.count() > 0 else ""

        loc = page.locator('a[href$="/verified_followers"] span.css-1jxf684').first
        total_followers = loc.inner_text() if loc.count() > 0 else ""

        loc = page.locator('a[href$="/following"] span.css-1jxf684').first
        total_following = loc.inner_text() if loc.count() > 0 else ""

        return {
            "username": username,
            "real_name": real_name,
            "bio": bio_text,
            "joined_date": joined_date,
            "location": location,
            "total_followers": total_followers,
            "total_following": total_following,
            "profile_url": self.seed_url
        }

    def scrape_posts(self, page: Page, max_posts: int = 5) -> List[Dict[str, Any]]:
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_selector('[data-testid="tweet"]', timeout=10000)
        page.wait_for_timeout(2000)

        collected_posts = []
        seen_post_urls = set()

        while len(collected_posts) < max_posts:
            tweets = page.locator('[data-testid="tweet"]')
            count = tweets.count()

            for i in range(count):
                if len(collected_posts) >= max_posts:
                    break

                tweet = tweets.nth(i)

                post_link_loc = tweet.locator('a[href*="/status/"]').first
                if post_link_loc.count() == 0:
                    continue

                post_url = post_link_loc.get_attribute('href')
                if not post_url:
                    continue

                full_url = f"https://x.com{post_url}"
                if full_url in seen_post_urls:
                    continue

                seen_post_urls.add(full_url)
                post_data = {"post_url": full_url}

                time_elem = tweet.locator('time').first
                post_data["datetime"] = (
                    time_elem.get_attribute("datetime")
                    if time_elem.count() > 0
                    else ""
                )

                tweet_text_loc = tweet.locator('[data-testid="tweetText"]').first
                post_data["caption"] = tweet_text_loc.inner_text() if tweet_text_loc.count() else ""

                image_loc = tweet.locator('[data-testid="tweetPhoto"]')
                if image_loc.count():
                    img = image_loc.locator("img").first
                    post_data["media_url"] = img.get_attribute("src") if img.count() else ""
                    post_data["media_type"] = "image"
                else:
                    video_loc = tweet.locator('[data-testid="videoComponent"]')
                    if video_loc.count():
                        video = video_loc.locator("video").first
                        post_data["media_url"] = video.get_attribute("poster") if video.count() else ""
                        post_data["media_type"] = "video"
                    else:
                        post_data["media_url"] = ""
                        post_data["media_type"] = "text"

                reply_loc = tweet.locator('[data-testid="reply"]')
                post_data["comments"] = reply_loc.inner_text().strip() if reply_loc.count() else "0"

                retweet_loc = tweet.locator('[data-testid="retweet"]')
                post_data["retweets"] = retweet_loc.inner_text().strip() if retweet_loc.count() else "0"

                like_loc = tweet.locator('[data-testid="like"]')
                post_data["likes"] = like_loc.inner_text().strip() if like_loc.count() else "0"

                views_loc = tweet.locator('a[href*="/analytics"]')
                post_data["views"] = views_loc.inner_text().strip() if views_loc.count() else "0"

                collected_posts.append(post_data)

            if len(collected_posts) < max_posts:
                page.mouse.wheel(0, 900)
                page.wait_for_timeout(1500)

        return collected_posts

    def scrape_posts_with_profile(self, page: Page, max_posts: int = 5) -> Dict[str, Any]:
        profile_data = self.scrape_profile(page)
        posts_data = self.scrape_posts(page, max_posts)

        for post in posts_data:
            card = social_model(
                m_username=profile_data.get("username", ""),
                m_real_name=profile_data.get("real_name", ""),
                m_bio=profile_data.get("bio", ""),
                m_location=profile_data.get("location", ""),
                m_total_followers=profile_data.get("total_followers", ""),
                m_total_following=profile_data.get("total_following", ""),
                m_weblink=[post.get("post_url", "")],
                m_content=post.get("caption", ""),
                m_content_type=[post.get("media_type", "text")],
                m_platform="twitter",
                m_post_datetime=post.get("datetime", ""),
                m_post_comments=post.get("comments", "0"),
                m_post_likes=post.get("likes", "0"),
                m_retweets=post.get("retweets", "0"),
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

    def _scroll_and_collect_users(self, page: Page, max_users: int) -> List[Dict[str, str]]:
        page.wait_for_timeout(3000)

        try:
            page.wait_for_selector('[data-testid="UserCell"]', timeout=10000)
        except:
            return []

        collected_users = []
        seen_usernames = set()
        prev_count = 0
        no_progress_rounds = 0
        max_no_progress = 5

        while len(collected_users) < max_users and no_progress_rounds < max_no_progress:
            user_cells = page.locator('[data-testid="UserCell"]')
            count = user_cells.count()

            for i in range(count):
                if len(collected_users) >= max_users:
                    break

                cell = user_cells.nth(i)

                username_loc = cell.locator('div[dir="ltr"] span').filter(has_text="@")
                username = username_loc.first.inner_text() if username_loc.count() > 0 else ""

                if not username or username in seen_usernames:
                    continue

                seen_usernames.add(username)

                real_name_loc = cell.locator('span.css-1jxf684').filter(has_not_text="@").first
                real_name = real_name_loc.inner_text() if real_name_loc.count() > 0 else ""

                bio_loc = cell.locator('div[dir="auto"]').last
                bio = bio_loc.inner_text() if bio_loc.count() > 0 else ""

                user_data = {
                    "username": username,
                    "real_name": real_name,
                    "bio": bio
                }

                collected_users.append(user_data)

            if len(collected_users) == prev_count:
                no_progress_rounds += 1
            else:
                no_progress_rounds = 0

            prev_count = len(collected_users)

            if len(collected_users) < max_users:
                page.mouse.wheel(0, 1500)
                page.wait_for_timeout(2000)

        return collected_users

    def scrape_followers(self, page: Page) -> List[Dict[str, str]]:
        followers_url = f"{self.seed_url}/verified_followers"
        page.goto(followers_url, wait_until="domcontentloaded")
        return self._scroll_and_collect_users(page, self._max_followers)

    def scrape_following(self, page: Page) -> List[Dict[str, str]]:
        following_url = f"{self.seed_url}/following"
        page.goto(following_url, wait_until="domcontentloaded")
        return self._scroll_and_collect_users(page, self._max_following)