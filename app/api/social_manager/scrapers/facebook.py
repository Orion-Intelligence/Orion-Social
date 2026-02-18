import re
from typing import Dict, Any, List
from playwright.sync_api import Page
from api.social_manager.scrapers.base_scraper import BaseScraper


class FacebookScraper(BaseScraper):

    requires_login = True

    def __init__(self, username: str, max_followers: int = 50, max_following: int = 50):
        super().__init__(username, max_followers, max_following)
        self._max_friends = max(max_followers, max_following)

    @property
    def seed_url(self) -> str:
        if self._username.isdigit():
            return f"https://www.facebook.com/profile.php?id={self._username}"
        return f"https://www.facebook.com/{self._username}"

    @property
    def friends_url(self) -> str:
        if self._username.isdigit():
            return f"https://www.facebook.com/profile.php?id={self._username}&sk=friends"
        return f"https://www.facebook.com/{self._username}/friends"

    @property
    def base_url(self) -> str:
        return "https://www.facebook.com"

    @property
    def name(self) -> str:
        return "Facebook"

    def _extract_names(self, page: Page):
        try:
            name_spans = page.query_selector_all(
                'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1lkfr7t.x1lbecb7.x1s688f.xzsf02u[dir="auto"]'
            )

            names = []
            for span in name_spans:
                name_text = span.inner_text().strip()
                if not name_text:
                    continue

                parent_anchor = span.evaluate_handle('el => el.closest("a")')
                if not parent_anchor:
                    continue

                href = parent_anchor.evaluate('el => el.href')
                is_profile = (
                    'profile.php?id=' in href or
                    (href.count('/') >= 3 and '?' not in href.split('/')[-1])
                )

                if is_profile:
                    names.append(name_text)

            return names

        except Exception:
            return []

    def _collect_friends(self, page: Page, max_items: int):
        page.goto(self.friends_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        collected = []
        seen = set()
        no_progress_rounds = 0
        max_no_progress = 12

        while len(collected) < max_items and no_progress_rounds < max_no_progress:
            names = self._extract_names(page)
            added = 0

            for name in names:
                if name not in seen:
                    seen.add(name)
                    collected.append(name)
                    added += 1

                if len(collected) >= max_items:
                    break

            if added == 0:
                no_progress_rounds += 1
                page.wait_for_timeout(1500)
            else:
                no_progress_rounds = 0

            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(2000)

        return collected[:max_items]

    def scrape_posts(self, page: Page, max_posts: int = 5) -> List[Dict[str, Any]]:

        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        posts_data = []
        processed_post_ids = set()

        POST_CONTAINER = 'div[data-ad-preview="message"]'
        COMMENT_BUTTON = 'div[aria-label="Leave a comment"]'

        REACTION_COUNT_SELECTOR = '.xt0b8zv.x1jx94hy.xj87blo.x1lbueug span .x135b78x'
        STATS_SELECTOR = 'span.xdmh292.x15dsfln.x140p0ai span.html-span'

        while len(posts_data) < max_posts:
            post_elements = page.query_selector_all('div[role="article"]')

            for post in post_elements:
                if len(posts_data) >= max_posts:
                    break

                post_text_el = post.query_selector(POST_CONTAINER)
                caption = post_text_el.inner_text().strip() if post_text_el else "No text"

                post_id = hash(caption[:100])
                if post_id in processed_post_ids:
                    continue
                processed_post_ids.add(post_id)

                img_el = post.query_selector('img[data-imgperflogname="feedImage"]')
                media_url = img_el.get_attribute('src') if img_el else ""

                total_reactions = post.query_selector(REACTION_COUNT_SELECTOR)
                reaction_val = total_reactions.inner_text() if total_reactions else "0"

                stats_elements = post.query_selector_all(STATS_SELECTOR)
                total_comments_on_feed = stats_elements[0].inner_text() if len(stats_elements) > 0 else "0"
                total_shares_on_feed = stats_elements[1].inner_text() if len(stats_elements) > 1 else "0"

                commenters = []
                comment_btn = post.query_selector(COMMENT_BUTTON)

                if comment_btn:
                    try:
                        comment_btn.click()
                        page.wait_for_timeout(2500)


                        rows = page.query_selector_all('div[role="article"]')

                        for row in rows:
                            author_el = row.query_selector('a[role="link"] span[dir="auto"]')
                            text_el = row.query_selector('div[dir="auto"]')

                            if author_el and text_el:
                                username = author_el.inner_text().strip()
                                comment_text = text_el.inner_text().strip()

                                if username and comment_text and username not in ["Like", "Reply"]:
                                    commenters.append({
                                        "username": username,
                                        "text": comment_text
                                    })

                        page.keyboard.press("Escape")
                        page.wait_for_timeout(1000)
                    except Exception as e:
                        print(f"Error opening comments: {e}")

                posts_data.append({
                    "caption": caption,
                    "media_url": media_url,
                    "total_reactions": reaction_val,
                    "total_comments": total_comments_on_feed,
                    "total_shares": total_shares_on_feed,
                    "comment_details": commenters,
                    "profile_url": self.seed_url
                })

            page.mouse.wheel(0, 2500)
            page.wait_for_timeout(3000)

        return posts_data

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        name_el = page.query_selector('h1')
        name = name_el.inner_text().strip() if name_el else ""

        bio_el = page.query_selector('div[data-pagelet="ProfileTilesFeed_0"] span')
        bio = bio_el.inner_text().strip() if bio_el else ""

        return {
            "real_name": name,
            "bio": bio,
            "location": "",
            "total_posts": "",
            "total_followers": "",
            "total_following": "",
            "profile_url": self.seed_url
        }

    def scrape_followers(self, page: Page) -> List[str]:
        return self._collect_friends(page, self._max_friends)

    def scrape_following(self, page: Page) -> List[str]:
        return self._collect_friends(page, self._max_friends)
