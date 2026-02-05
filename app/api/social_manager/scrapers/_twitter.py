from playwright.sync_api import Page
from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.cross_platform_mapping import cross_platform_mapper


class twitter(BaseScraper):
    requires_login = True

    def __init__(self, username: str):
        super().__init__()
        self._username = username

    @property
    def base_url(self) -> str:
        return f"https://x.com/{self._username}/following"

    @property
    def seed_url(self) -> str:
        return f"https://x.com/{self._username}"

    @property
    def name(self) -> str:
        return "Twitter"

    def parse_page(self, page: Page):

        page.wait_for_selector('[data-testid="UserName"]', timeout=10000)

        loc = page.locator('[data-testid="UserName"] span').filter(has_text="@")
        username = loc.first.inner_text() if loc.count() > 0 else ""
        print("Username:", username)

        loc = page.locator('[data-testid="UserName"] span.css-1jxf684').first
        real_name = loc.inner_text() if loc.count() > 0 else ""
        print("Real name:", real_name)

        loc = page.locator('[data-testid="UserDescription"]')
        bio_text = loc.first.inner_text() if loc.count() > 0 else ""
        print("Bio:", bio_text)

        loc = page.locator('[data-testid="UserJoinDate"] span').last
        joined_date = loc.inner_text() if loc.count() > 0 else ""
        print("Joined:", joined_date)

        loc = page.locator('[data-testid="UserLocation"] span').last
        location = loc.inner_text() if loc.count() > 0 else ""
        print("Location:", location)

        loc = page.locator('a[href$="/verified_followers"] span.css-1jxf684').first
        total_followers = loc.inner_text() if loc.count() > 0 else ""
        print("Followers:", total_followers)

        loc = page.locator('a[href$="/following"] span.css-1jxf684').first
        total_following = loc.inner_text() if loc.count() > 0 else ""
        print("Following:", total_following)

        page.wait_for_selector('[data-testid="tweet"]', timeout=10000)
        page.wait_for_timeout(2000)

        MAX_POSTS = 5
        collected_posts = []
        seen_post_urls = set()

        while len(collected_posts) < MAX_POSTS:
            tweets = page.locator('[data-testid="tweet"]')
            count = tweets.count()

            for i in range(count):
                if len(collected_posts) >= MAX_POSTS:
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

                time_elem = tweet.locator('time')
                post_data["datetime"] = time_elem.get_attribute("datetime") if time_elem.count() else ""

                tweet_text_loc = tweet.locator('[data-testid="tweetText"]')
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

                print("\nCollected Post:")
                for k, v in post_data.items():
                    print(f"  {k}: {v}")

            if len(collected_posts) < MAX_POSTS:
                page.mouse.wheel(0, 900)
                page.wait_for_timeout(1500)

        print(f"\nTotal posts collected: {len(collected_posts)}")

        for idx, post in enumerate(collected_posts, 1):
            card = social_model(
                m_username=username,
                m_real_name=real_name,
                m_bio=bio_text,
                m_total_posts="",
                m_total_followers=total_followers,
                m_total_following=total_following,
                m_weblink=[post.get("post_url", "")],
                m_content=post.get("caption", ""),
                m_content_type=[post.get("media_type", "text")],
                m_platform="twitter",
                m_post_comments=post.get("comments", "0"),
                m_post_likes=post.get("likes", "0"),
                m_retweets=post.get("retweets", "0"),
                m_post_views=post.get("views", "0"),
                m_channel_url=post.get("media_url", ""),
                m_network=self.seed_url
            )

            self.data.append(card.model_dump())
            cross_platform_mapper.add_card(card)
