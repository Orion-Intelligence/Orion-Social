import re
from typing import Dict, Any, List, Tuple
from playwright.sync_api import Page, ElementHandle
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
    def followers_url(self) -> str:
        if self._username.isdigit():
            return f"https://www.facebook.com/profile.php?id={self._username}&sk=followers"
        return f"https://www.facebook.com/{self._username}/followers"

    @property
    def following_url(self) -> str:
        if self._username.isdigit():
            return f"https://www.facebook.com/profile.php?id={self._username}&sk=following"
        return f"https://www.facebook.com/{self._username}/following"

    @property
    def base_url(self) -> str:
        return "https://www.facebook.com"

    @property
    def name(self) -> str:
        return "Facebook"



    @staticmethod
    def _author_from_aria(article: ElementHandle) -> str:
        label = article.get_attribute("aria-label") or ""
        if not label.startswith("Comment by "):
            return ""
        rest = label[len("Comment by "):]
        rest = re.sub(
            r'\s+(?:about\s+)?(?:'
            r'a\s+few\s+seconds?\s+ago|just\s+now'
            r'|(?:a|an|\d+)\s+(?:second|minute|hour|day|week|month|year)s?(?:\s+ago)?'
            r'|yesterday(?:\s+at\s+[\d:]+(?::\d+)?\s*(?:AM|PM)?)?'
            r'|(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)(?:\s+at\s+[\d:]+(?::\d+)?\s*(?:AM|PM)?)?'
            r'|(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?'
            r'|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)'
            r'\s+\d{1,2}(?:,?\s+\d{4})?(?:\s+at\s+[\d:]+(?::\d+)?\s*(?:AM|PM)?)?)\s*$',
            '', rest, flags=re.I
        ).strip()
        return rest

    @staticmethod
    def _text_from_article(article: ElementHandle) -> str:
        el = article.query_selector('div[dir="auto"][style*="text-align"]')
        if el:
            return el.inner_text().strip()
        el = article.query_selector('div[dir="auto"] div[dir="auto"]')
        if el:
            return el.inner_text().strip()
        el = article.query_selector('div[dir="auto"]')
        if el:
            return el.inner_text().strip()
        return ""

    def _extract_post_stats(self, page: Page, post: ElementHandle) -> Tuple[str, str, str]:
        likes = "0"
        comments = "0"
        shares = "0"
        try:
            el = post.query_selector('[aria-label*="reaction" i], [aria-label*="like" i][role="button"]')
            if el:
                m = re.search(r'([\d,]+)', el.get_attribute("aria-label") or "")
                if m:
                    likes = m.group(1).replace(",", "")
        except Exception:
            pass
        try:
            stats = page.evaluate(
                r"""(el) => {
                    const out = { comments: "0", shares: "0" };
                    const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
                    let n;
                    while ((n = walk.nextNode())) {
                        const t = n.textContent.trim();
                        if (/^[\d,]+\s+comment/i.test(t))
                            out.comments = t.match(/^([\d,]+)/)[1].replace(/,/g,'');
                        else if (/^[\d,]+\s+share/i.test(t))
                            out.shares = t.match(/^([\d,]+)/)[1].replace(/,/g,'');
                    }
                    return out;
                }""", post
            )
            comments = stats.get("comments", "0")
            shares = stats.get("shares", "0")
        except Exception:
            pass
        return likes, comments, shares



    _PERMALINK_PATTERNS = ("/posts/", "/permalink/", "/reel/", "/reels/", "/videos/", "story_fbid")

    @classmethod
    def _get_post_permalink(cls, post: ElementHandle) -> str:
        def clean(href: str) -> str:
            if href.startswith("/"):
                href = "https://www.facebook.com" + href
            return href.split("?")[0]

        def valid(href: str) -> bool:
            return bool(href) and not href.startswith("?") and "comment_id" not in href \
                   and any(p in href for p in cls._PERMALINK_PATTERNS)

        el = post.query_selector("a:has(abbr)")
        if el:
            h = clean(el.get_attribute("href") or "")
            if valid(h):
                return h

        for sel in ['a[href*="/posts/"]', 'a[href*="/permalink/"]', 'a[href*="/reel/"]',
                    'a[href*="/reels/"]', 'a[href*="/videos/"]', 'a[href*="story_fbid"]']:
            for link in post.query_selector_all(sel):
                h = clean(link.get_attribute("href") or "")
                if valid(h):
                    return h

        result = post.evaluate(
            """(el) => {
                const PATS = ['/posts/','/permalink/','/reel/','/reels/','/videos/','story_fbid'];
                let best = null;
                for (const a of el.querySelectorAll('a[href]')) {
                    const h = a.getAttribute('href') || '';
                    if (h.startsWith('?') || h.includes('comment_id')) continue;
                    if (PATS.some(p => h.includes(p))) {
                        if (!best || h.length < best.length) best = h;
                    }
                }
                if (best && best.startsWith('/')) best = 'https://www.facebook.com' + best;
                return best;
            }"""
        )
        if result and valid(result):
            return result.split("?")[0]
        return ""


    @staticmethod
    def _get_comment_labels(page: Page) -> set:
        return {
            a.get_attribute("aria-label") or ""
            for a in page.query_selector_all('div[role="article"][aria-label^="Comment by"]')
        }

    def _scrape_comments(self, page: Page, baseline: set) -> list:

        commenters = []
        seen_keys = set()

        def get_new_articles():
            all_arts = page.query_selector_all(
                'div[role="article"][aria-label^="Comment by"]'
            )
            return [a for a in all_arts if (a.get_attribute("aria-label") or "") not in baseline]

        print("[FB]   Waiting for comments to load...")
        for _ in range(20):
            if get_new_articles():
                break
            page.wait_for_timeout(500)
        else:
            print("[FB]   No comments appeared — skipping")
            return commenters

        no_progress = 0
        scroll_count = 0

        while len(commenters) < 20:
            new_articles = get_new_articles()
            print(f"[FB]   {len(new_articles)} comment articles visible (scroll {scroll_count})")

            added = 0
            for article in new_articles:
                if len(commenters) >= 20:
                    break
                username = self._author_from_aria(article)
                comment_text = self._text_from_article(article)
                if not username or not comment_text:
                    continue
                key = f"{username}::{comment_text[:80]}"
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                commenters.append({"username": username, "text": comment_text})
                print(f"[FB]     + {username!r}: {comment_text[:60]!r}")
                added += 1

            if len(commenters) >= 20:
                break

            if added == 0:
                no_progress += 1
                if no_progress >= 4:
                    print("[FB]   No new comments after 4 scrolls — done")
                    break
            else:
                no_progress = 0

            try:
                last = new_articles[-1]
                box = last.bounding_box()
                if box:
                    page.mouse.move(
                        box["x"] + box["width"] / 2,
                        box["y"] + box["height"] / 2
                    )
                page.mouse.wheel(0, 1200)
            except Exception:
                page.mouse.wheel(0, 1200)

            page.wait_for_timeout(2500)
            scroll_count += 1

        return commenters

    def _click_comments_button(self, page: Page, post: ElementHandle) -> bool:
        try:
            for btn in post.query_selector_all('div[role="button"], span[role="button"]'):
                if re.search(r'\d+\s*comment', (btn.inner_text() or "").lower()):
                    btn.scroll_into_view_if_needed()
                    btn.click()
                    return True
            btn = post.query_selector('[aria-label*="comment" i][role="button"]')
            if btn:
                btn.scroll_into_view_if_needed()
                btn.click()
                return True
        except Exception as e:
            print(f"[FB]   Click failed: {e}")
        return False

    def _close_comments(self, page: Page, baseline: set):
        try:
            page.keyboard.press("Escape")
            for _ in range(14):  # up to 7s
                remaining = page.query_selector_all(
                    'div[role="article"][aria-label^="Comment by"]'
                )
                still_open = [
                    a for a in remaining
                    if (a.get_attribute("aria-label") or "") not in baseline
                ]
                if not still_open:
                    print("[FB]   Panel closed")
                    return
                page.wait_for_timeout(500)
        except Exception:
            pass
        page.wait_for_timeout(1000)



    def scrape_posts(self, page: Page, max_posts: int = 5) -> List[Dict[str, Any]]:

        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        posts_data: List[Dict[str, Any]] = []
        processed_ids: set = set()
        no_new_rounds = 0

        while len(posts_data) < max_posts and no_new_rounds < 8:
            found_new = False

            pending = []
            for post in page.query_selector_all('div[role="article"]'):
                if (post.get_attribute("aria-label") or "").startswith("Comment by"):
                    continue
                text_el = post.query_selector(
                    'div[data-ad-preview="message"], div[data-ad-comet-preview="message"]'
                )
                if not text_el:
                    continue
                caption = text_el.inner_text().strip()
                if not caption:
                    continue
                post_id = hash(caption[:100])
                if post_id in processed_ids:
                    continue

                permalink = self._get_post_permalink(post)

                media_url, media_type = "", "text"
                for sel, mtype in [
                    ('img[data-imgperflogname="feedImage"]', "image"),
                    ("video[poster]", "video"),
                ]:
                    el = post.query_selector(sel)
                    if el:
                        src = el.get_attribute("src") or el.get_attribute("poster") or ""
                        if src:
                            media_url, media_type = src, mtype
                            break
                if not media_url:
                    for sel in ['a[role="link"] img[src*="t15.5256"]', 'a[role="link"] img[src]']:
                        el = post.query_selector(sel)
                        if el:
                            src = el.get_attribute("src") or ""
                            if src.startswith("http"):
                                media_url = src
                                media_type = "video" if "t15.5256" in sel else "image"
                                break

                likes, comments, shares = self._extract_post_stats(page, post)

                pending.append({
                    "post_id":    post_id,
                    "caption":    caption,
                    "permalink":  permalink,
                    "media_url":  media_url,
                    "media_type": media_type,
                    "likes":      likes,
                    "comments":   comments,
                    "shares":     shares,
                })

            for meta in pending:
                if len(posts_data) >= max_posts:
                    break
                if meta["post_id"] in processed_ids:
                    continue
                processed_ids.add(meta["post_id"])
                found_new = True



                baseline = self._get_comment_labels(page)

                fresh_post = None
                for el in page.query_selector_all('div[role="article"]'):
                    if (el.get_attribute("aria-label") or "").startswith("Comment by"):
                        continue
                    text_el = el.query_selector(
                        'div[data-ad-preview="message"], div[data-ad-comet-preview="message"]'
                    )
                    if text_el and hash(text_el.inner_text().strip()[:100]) == meta["post_id"]:
                        fresh_post = el
                        break

                commenters = []
                if fresh_post and self._click_comments_button(page, fresh_post):
                    page.wait_for_timeout(2000)  # let panel animate in
                    commenters = self._scrape_comments(page, baseline)
                    self._close_comments(page, baseline)
                else:
                    print("[FB]   Could not click comments — skipping")

                posts_data.append({
                    "status":        "active",
                    "post_url":      meta["permalink"] or self.seed_url,
                    "datetime":      "",
                    "caption":       meta["caption"],
                    "media_url":     meta["media_url"],
                    "media_type":    meta["media_type"],
                    "comments":      meta["comments"],
                    "likes":         meta["likes"],
                    "shares":        meta["shares"],
                    "views":         "0",
                    "connections":   [c["username"] for c in commenters],
                    "comments_text": [c["text"]     for c in commenters],
                })
                print(f"[FB] ✓ {len(commenters)} comments collected | likes={meta['likes']} shares={meta['shares']}")

            no_new_rounds = 0 if found_new else no_new_rounds + 1

            if len(posts_data) < max_posts:
                page.mouse.wheel(0, 2500)
                page.wait_for_timeout(3000)

        return posts_data



    def _extract_names(self, page: Page):
        try:
            names = []
            for span in page.query_selector_all(
                'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1lkfr7t.x1lbecb7.x1s688f.xzsf02u[dir="auto"]'
            ):
                name = span.inner_text().strip()
                if not name:
                    continue
                anchor = span.evaluate_handle('el => el.closest("a")')
                if not anchor:
                    continue
                href = anchor.evaluate('el => el.href')
                if 'profile.php?id=' in href or (href.count('/') >= 3 and '?' not in href.split('/')[-1]):
                    names.append(name)
            return names
        except Exception:
            return []

    def _resolve_list_url(self, page: Page, mode: str) -> str:
        page.goto(self.seed_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)
        hrefs = [
            (a.get_attribute("href") or "").lower()
            for a in page.query_selector_all('a[href]')
        ]
        has_followers = any("/followers" in h or "sk=followers" in h for h in hrefs)
        has_following = any("/following" in h or "sk=following" in h for h in hrefs)
        has_friends   = any("/friends"   in h or "sk=friends"   in h for h in hrefs)

        if mode == "followers":
            return self.followers_url if has_followers else (self.friends_url if has_friends else self.followers_url)
        if mode == "following":
            return self.following_url if has_following else (self.friends_url if has_friends else self.following_url)
        return self.friends_url

    def _collect_people(self, page: Page, max_items: int, mode: str) -> List[str]:
        page.goto(self._resolve_list_url(page, mode), wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        collected, seen, no_progress = [], set(), 0

        while len(collected) < max_items and no_progress < 12:
            added = 0
            for name in self._extract_names(page):
                if name not in seen:
                    seen.add(name)
                    collected.append(name)
                    added += 1
                if len(collected) >= max_items:
                    break
            no_progress = 0 if added else no_progress + 1
            if not added:
                page.wait_for_timeout(1500)
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(2000)

        return collected[:max_items]


    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        data: Dict[str, Any] = {
            "real_name": None, "bio": None, "location": None,
            "total_friends": None, "total_followers": None,
            "total_following": None, "profile_url": self.seed_url,
        }

        try:
            for sel in ["h1", "h1.html-h1", "h2.html-h2"]:
                el = page.query_selector(sel)
                if el:
                    text = el.inner_text().strip()
                    if text:
                        data["real_name"] = text
                        break

            for key, pattern in [("total_followers", "followers"),
                                  ("total_following", "following"),
                                  ("total_friends",   "friends")]:
                el = page.query_selector(f'a[href*="{pattern}"] strong')
                if el:
                    data[key] = el.inner_text().strip()
                elif pattern == "followers":
                    el = page.query_selector(f'a[href*="{pattern}"]')
                    if el:
                        m = re.search(r"([\d.,]+\s*[KkMmBb]?)\s*followers", el.inner_text(), re.I)
                        if m:
                            data[key] = m.group(1).strip()

            bio_el = page.query_selector("div.xz9dl7a.xp6pnuw.x160xiiu > span[dir='auto']")
            if bio_el:
                data["bio"] = bio_el.inner_text().strip()
            if not data["bio"]:
                data["bio"] = page.evaluate(
                    """() => {
                        const d = document.querySelector('div.xz9dl7a.xp6pnuw.x160xiiu > span[dir="auto"]');
                        return d ? d.innerText.trim() : null;
                    }"""
                )

            for sel in ['a[href*="hometown"]', 'a[href*="location"]', 'a[href*="city"]', "li:has(svg) a"]:
                el = page.query_selector(sel)
                if el:
                    text = el.inner_text().strip()
                    if text and not text.lower().startswith("http"):
                        data["location"] = text
                        break

        except Exception as e:
            print(f"[Facebook] Profile error: {e}")

        return data

    def scrape_followers(self, page: Page) -> List[str]:
        return self._collect_people(page, self._max_friends, mode="followers")

    def scrape_following(self, page: Page) -> List[str]:
        return self._collect_people(page, self._max_friends, mode="following")