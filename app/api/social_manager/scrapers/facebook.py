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

        while len(posts_data) < max_posts:
            all_articles = page.query_selector_all('div[role="article"]')

            post_elements = [
                el for el in all_articles
                if not (el.get_attribute("aria-label") or "").startswith("Comment by")
                   and el.query_selector('div[data-ad-preview="message"], div[data-ad-comet-preview="message"]')
            ]

            found_new = False

            for post in post_elements:
                if len(posts_data) >= max_posts:
                    break

                post_text_el = post.query_selector('div[data-ad-preview="message"]')
                if not post_text_el:
                    post_text_el = post.query_selector('div[data-ad-comet-preview="message"]')
                if not post_text_el:
                    continue

                caption = post_text_el.inner_text().strip()
                if not caption:
                    continue

                post_id = hash(caption[:100])
                if post_id in processed_post_ids:
                    continue

                processed_post_ids.add(post_id)
                found_new = True

                img_el = post.query_selector('img[data-imgperflogname="feedImage"]')
                media_url = img_el.get_attribute('src') if img_el else ""

                reaction_el = post.query_selector(
                    '[aria-label^="All reactions"] .x135b78x, .xt0b8zv.x1jx94hy .x135b78x')
                reaction_val = reaction_el.inner_text().strip() if reaction_el else "0"

                stats_spans = post.query_selector_all('span.xkrqix3.x1sur9pj')
                total_comments_feed = "0"
                total_shares_feed = "0"
                for span in stats_spans:
                    txt = span.inner_text().strip().lower()
                    if "comment" in txt:
                        total_comments_feed = txt.split()[0]
                    elif "share" in txt:
                        total_shares_feed = txt.split()[0]

                commenters = []

                try:
                    comment_btn = None
                    for span in stats_spans:
                        if "comment" in span.inner_text().lower():
                            comment_btn = span
                            break

                    if not comment_btn:
                        comment_btn = post.query_selector('[aria-label*="comment"], [aria-label*="Comment"]')

                    if comment_btn:
                        comment_btn.click()
                        page.wait_for_timeout(3000)

                        modal = None
                        for _ in range(10):
                            modal = page.query_selector('div[role="dialog"]')
                            if modal:
                                break
                            page.wait_for_timeout(500)

                        if modal:
                            seen_comment_keys = set()
                            no_progress_count = 0
                            prev_count = 0
                            scroll_attempts = 0

                            while len(commenters) < 20 and scroll_attempts < 25:
                                comment_articles = modal.query_selector_all(
                                    'div[role="article"][aria-label*="Comment by"]'
                                )

                                for article in comment_articles:
                                    if len(commenters) >= 20:
                                        break

                                    author_el = article.query_selector('a[role="link"] span[dir="auto"]')
                                    if not author_el:
                                        author_el = article.query_selector('a[role="link"] span.x3nfvp2 span')
                                    username = author_el.inner_text().strip() if author_el else ""

                                    if not username:
                                        continue

                                    text_el = article.query_selector('div[dir="auto"] > div[dir="auto"]')
                                    if not text_el:
                                        text_el = article.query_selector('div[dir="auto"]')
                                    comment_text = text_el.inner_text().strip() if text_el else ""

                                    if not comment_text:
                                        continue

                                    dedup_key = f"{username}::{comment_text[:80]}"
                                    if dedup_key in seen_comment_keys:
                                        continue
                                    seen_comment_keys.add(dedup_key)

                                    commenters.append({
                                        "username": username,
                                        "text": comment_text
                                    })

                                if len(commenters) == prev_count:
                                    no_progress_count += 1
                                else:
                                    no_progress_count = 0

                                prev_count = len(commenters)
                                scroll_attempts += 1

                                if no_progress_count >= 5:
                                    break

                                if len(commenters) < 20:
                                    page.evaluate('el => el.scrollBy(0, 1200)', modal)
                                    page.wait_for_timeout(2000)

                    page.keyboard.press("Escape")
                    for _ in range(10):
                        if not page.query_selector('div[role="dialog"]'):
                            break
                        page.wait_for_timeout(500)
                    page.wait_for_timeout(500)

                except Exception as e:
                    print(f"Error scraping comments: {e}")
                    try:
                        page.keyboard.press("Escape")
                        for _ in range(10):
                            if not page.query_selector('div[role="dialog"]'):
                                break
                            page.wait_for_timeout(500)
                    except Exception:
                        pass

                posts_data.append({
                    "status": "active",
                    "post_url": self.seed_url,
                    "datetime": "",
                    "caption": caption,
                    "media_url": media_url,
                    "media_type": "image" if media_url else "text",
                    "comments": total_comments_feed or "0",
                    "likes": reaction_val or "0",
                    "shares": total_shares_feed or "0",
                    "views": "0",
                    "top_commenters": [c["username"] for c in commenters],
                    "comments_text": [c["text"] for c in commenters],
                })

            if len(posts_data) < max_posts:
                page.mouse.wheel(0, 2500)
                page.wait_for_timeout(3000)
                if not found_new:
                    print("No new posts found after scroll, stopping.")
                    break

        return posts_data

    def _extract_profile_info(self, page: Page) -> Dict:
        """Extract basic profile information"""
        print("[Facebook] Extracting profile information...")
        profile_data = {
            "real_name": None,
            "bio": None,
            "location": None,
            "total_friends": None,
            "total_followers": None,
            "total_following": None
        }

        try:
            # Extract real name
            name_selectors = [
                'h1.html-h1',
                'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.xo1l8bm.xi81zsa.x1yc453h',
                'h2.html-h2'
            ]

            for selector in name_selectors:
                try:
                    name_elem = page.query_selector(selector)
                    if name_elem:
                        profile_data["real_name"] = name_elem.inner_text().strip()
                        break
                except:
                    continue

            # Extract friends count
            try:
                friends_elem = page.query_selector('a[href*="friends"] strong')
                if friends_elem:
                    profile_data["total_friends"] = friends_elem.inner_text().strip()
            except:
                pass

            # Extract bio/intro
            try:
                bio_selectors = [
                    'div[data-ad-rendering-role="story_message"]',
                    'div.x1iorvi4.x4uap5.x1g0dm76.xpdmqnj'
                ]

                for selector in bio_selectors:
                    bio_elem = page.query_selector(selector)
                    if bio_elem:
                        profile_data["bio"] = bio_elem.inner_text().strip()
                        break
            except:
                pass

            # Extract location
            try:
                location_elem = page.query_selector('a[href*="Sargodha"], span:has-text("Sargodha")')
                if location_elem:
                    profile_data["location"] = location_elem.inner_text().strip()
            except:
                pass

            print(f"[Facebook] Profile info collected: {profile_data}")
            return profile_data

        except Exception as e:
            print(f"[Facebook] Error extracting profile info: {e}")
            return profile_data

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        profile_data = {
            "real_name": None,
            "bio": None,
            "location": None,
            "total_friends": None,
            "total_followers": None,
            "total_following": None,
            "profile_url": self.seed_url,
        }

        try:
            for selector in ["h1", "h1.html-h1", "h2.html-h2"]:
                el = page.query_selector(selector)
                if el:
                    text = el.inner_text().strip()
                    if text:
                        profile_data["real_name"] = text
                        break

            followers_strong = page.query_selector('a[href*="followers"] strong')
            if followers_strong:
                profile_data["total_followers"] = followers_strong.inner_text().strip()
            else:
                followers_anchor = page.query_selector('a[href*="followers"]')
                if followers_anchor:
                    text = followers_anchor.inner_text().strip()
                    m = re.search(r"([\d.,]+\s*[KkMmBb]?)\s*followers", text, re.I)
                    if m:
                        profile_data["total_followers"] = m.group(1).strip()

            following_strong = page.query_selector('a[href*="following"] strong')
            if following_strong:
                profile_data["total_following"] = following_strong.inner_text().strip()

            friends_strong = page.query_selector('a[href*="friends"] strong')
            if friends_strong:
                profile_data["total_friends"] = friends_strong.inner_text().strip()



            bio_el = page.query_selector(
                "div.xz9dl7a.xp6pnuw.x160xiiu > span[dir='auto']"
            )
            if bio_el:
                profile_data["bio"] = bio_el.inner_text().strip()


            if not profile_data["bio"]:
                bio_text = page.evaluate("""
                    () => {
                        const div = document.querySelector(
                            'div.xz9dl7a.xp6pnuw.x160xiiu > span[dir="auto"]'
                        );
                        return div ? div.innerText.trim() : null;
                    }
                """)
                if bio_text:
                    profile_data["bio"] = bio_text

            for selector in [
                'a[href*="hometown"]',
                'a[href*="location"]',
                'a[href*="city"]',
                "li:has(svg) a",
            ]:
                el = page.query_selector(selector)
                if el:
                    text = el.inner_text().strip()
                    if text and not text.lower().startswith("http"):
                        profile_data["location"] = text
                        break

        except Exception:
            pass

        return profile_data
    def scrape_followers(self, page: Page) -> List[str]:
        return self._collect_friends(page, self._max_friends)

    def scrape_following(self, page: Page) -> List[str]:
        return self._collect_friends(page, self._max_friends)
