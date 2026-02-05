import time
import re
from playwright.sync_api import Page
from typing import List, Dict, Optional

from api.social_manager.scrapers.base_scraper import BaseScraper
from api.social_manager.models import social_model
from api.social_manager.cross_platform_mapping import cross_platform_mapper


class FacebookScraper(BaseScraper):
    requires_login = True

    def __init__(self, username: str):
        super().__init__()
        self._username = username

    @property
    def seed_url(self) -> str:
        return f"https://www.facebook.com/{self._username}"

    @property
    def base_url(self) -> str:
        return "https://www.facebook.com"

    @property
    def name(self) -> str:
        return "Facebook"

    def _extract_profile_info(self, page: Page) -> Dict:
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

            try:
                friends_elem = page.query_selector('a[href*="friends"] strong')
                if friends_elem:
                    profile_data["total_friends"] = friends_elem.inner_text().strip()
            except:
                pass

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

    def _extract_post_data(self, post_element) -> Optional[Dict]:
        try:
            post_data = {
                "caption": None,
                "image_url": None,
                "video_url": None,
                "likes": None,
                "comments_count": None,
                "shares": None,
                "commenters": []
            }

            try:
                caption_selectors = [
                    'div[data-ad-rendering-role="story_message"]',
                    'div[dir="auto"][style*="text-align"]',
                    'div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs'
                ]

                for selector in caption_selectors:
                    caption_elem = post_element.query_selector(selector)
                    if caption_elem:
                        post_data["caption"] = caption_elem.inner_text().strip()
                        break
            except:
                pass

            try:
                img_elem = post_element.query_selector('img[data-imgperflogname="feedImage"]')
                if img_elem:
                    post_data["image_url"] = img_elem.get_attribute("src")
            except:
                pass

            try:
                video_elem = post_element.query_selector('video')
                if video_elem:
                    post_data["video_url"] = video_elem.get_attribute("src")
            except:
                pass

            try:
                likes_selectors = [
                    'span[aria-label*="reaction"]',
                    'div.x9f619.x1ja2u2z.x78zum5.x2lah0s.x1n2onr6.x1qughib.x6s0dn4.xozqiw3.x1q0g3np span'
                ]

                for selector in likes_selectors:
                    likes_elem = post_element.query_selector(selector)
                    if likes_elem:
                        likes_text = likes_elem.inner_text().strip()
                        match = re.search(r'\d+', likes_text)
                        if match:
                            post_data["likes"] = match.group()
                        break
            except:
                pass

            try:
                comment_count_elem = post_element.query_selector('span:has-text("Comment")')
                if comment_count_elem:
                    parent = comment_count_elem.evaluate_handle('el => el.closest("div")')
                    if parent:
                        count_text = parent.inner_text()
                        match = re.search(r'\d+', count_text)
                        if match:
                            post_data["comments_count"] = match.group()
            except:
                pass

            post_data["commenters"] = self._extract_commenters(post_element)

            return post_data

        except Exception as e:
            print(f"[Facebook] Error extracting post data: {e}")
            return None

    def _extract_commenters(self, post_element) -> List[str]:
        commenters = []
        try:
            commenter_selectors = [
                'span[dir="auto"] a[role="link"]',
                'div.x1r8uery.x1iyjqo2 a.x1i10hfl'
            ]

            for selector in commenter_selectors:
                commenter_elems = post_element.query_selector_all(selector)
                for elem in commenter_elems:
                    try:
                        name = elem.inner_text().strip()
                        href = elem.get_attribute("href")

                        if href and ('profile.php' in href or '.com/' in href) and name:
                            if name not in commenters and len(name) > 0:
                                commenters.append(name)
                    except:
                        continue

            return list(set(commenters))[:20]

        except Exception as e:
            print(f"[Facebook] Error extracting commenters: {e}")
            return []

    def _collect_posts(self, page: Page, max_posts=10) -> List[Dict]:
        print(f"[Facebook] Collecting top {max_posts} posts...")

        posts = []
        seen_posts = set()
        scroll_attempts = 0
        max_scroll_attempts = 15

        while len(posts) < max_posts and scroll_attempts < max_scroll_attempts:
            try:
                post_containers = page.query_selector_all('div[role="article"]')

                for container in post_containers:
                    if len(posts) >= max_posts:
                        break

                    try:
                        post_text = container.inner_text()[:100]
                        post_id = hash(post_text)

                        if post_id in seen_posts:
                            continue

                        seen_posts.add(post_id)

                        post_data = self._extract_post_data(container)

                        if post_data and (post_data["caption"] or post_data["image_url"]):
                            posts.append(post_data)
                            print(f" → Post {len(posts)}/{max_posts} collected")
                            print(f"    Caption: {post_data['caption'][:50] if post_data['caption'] else 'N/A'}...")
                            print(f"    Image: {'Yes' if post_data['image_url'] else 'No'}")
                            print(f"    Commenters: {len(post_data['commenters'])}")

                    except Exception as e:
                        print(f"[Facebook] Error processing post container: {e}")
                        continue

                page.mouse.wheel(0, 2000)
                time.sleep(2)
                scroll_attempts += 1

            except Exception as e:
                print(f"[Facebook] Error in post collection loop: {e}")
                break

        return posts

    def _extract_friends_names(self, page: Page):
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

        except Exception as e:
            print(f"[Facebook] Error extracting friend names: {e}")
            return []

    def _collect_friends(self, page: Page, max_items=50):

        friends_url = f"{self.seed_url}/friends"
        page.goto(friends_url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(4000)

        collected = []
        seen = set()
        rounds_no_progress = 0

        while len(collected) < max_items and rounds_no_progress < 6:
            names = self._extract_friends_names(page)
            added = 0

            for name in names:
                if name not in seen:
                    seen.add(name)
                    collected.append(name)
                    print(f" → Friend: {name} ({len(collected)}/{max_items})")
                    added += 1

                if len(collected) >= max_items:
                    break

            rounds_no_progress = rounds_no_progress + 1 if added == 0 else 0
            page.mouse.wheel(0, 2500)
            time.sleep(2)

        return collected[:max_items]

    def parse_page(self, page: Page):
        print(f"[Facebook] Starting data collection for: {self._username}")

        page.goto(self.seed_url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(4000)

        profile_info = self._extract_profile_info(page)

        posts = self._collect_posts(page, max_posts=10)

        all_commenters = []
        for post in posts:
            all_commenters.extend(post.get("commenters", []))
        unique_commenters = list(set(all_commenters))

        friends = self._collect_friends(page, max_items=50)

        print("\n" + "=" * 60)
        print("COLLECTED DATA SUMMARY")
        print("=" * 60)
        print(f"Username: {self._username}")
        print(f"Real Name: {profile_info.get('real_name', 'N/A')}")
        print(f"Bio: {profile_info.get('bio', 'N/A')}")
        print(f"Location: {profile_info.get('location', 'N/A')}")
        print(f"Total Friends: {profile_info.get('total_friends', 'N/A')}")
        print(f"Friends Collected: {len(friends)}")
        print(f"Posts Collected: {len(posts)}")
        print(f"Unique Commenters: {len(unique_commenters)}")
        print("\n" + "-" * 60)
        print("POSTS DETAILS:")
        for i, post in enumerate(posts, 1):
            print(f"\nPost #{i}:")
            caption = post.get("caption") or "N/A"
            print(f"  Caption: {caption[:100]}...")

            image_url = post.get("image_url") or "N/A"
            print(f"  Image URL: {image_url[:80]}...")

            print(f"  Video URL: {post.get('video_url', 'N/A')}")
            print(f"  Likes: {post.get('likes', 'N/A')}")
            print(f"  Comments Count: {post.get('comments_count', 'N/A')}")
            print(f"  Commenters ({len(post.get('commenters', []))}): {', '.join(post.get('commenters', [])[:5])}")
        print("=" * 60 + "\n")

        card = social_model(
            m_weblink=[self.seed_url],
            m_username=self._username,
            m_real_name=profile_info.get("real_name"),
            m_bio=profile_info.get("bio"),
            m_location=profile_info.get("location"),
            m_total_followers=profile_info.get("total_friends"),  
            m_total_following=None,  
            m_followers=friends,
            m_following=friends,
            m_mutual_usernames=friends,
            m_content=f"Profile with {len(posts)} posts collected",
            m_content_type=["facebook_profile", "facebook_posts"],
            m_network="clearnet",
            m_platform="facebook",
            m_commenters=unique_commenters,
            m_posts_data=posts,  
            m_total_posts=str(len(posts))
        )

        self.data.append(card.model_dump())
        cross_platform_mapper.add_card(card)

        print(f"[Facebook] Data collection complete!")