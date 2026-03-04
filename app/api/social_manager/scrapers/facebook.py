import re
from typing import Dict, Any, List, Tuple, Optional
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

    # -------------------------------------------------------------------------
    # STABLE COMMENT AUTHOR EXTRACTION
    # aria-label="Comment by Nayab Zoey RedBird 4 hours ago"  ← always present
    # -------------------------------------------------------------------------
    @staticmethod
    def _author_from_aria(article: ElementHandle) -> str:
        """
        Extract commenter name from the article's aria-label.
        Format: "Comment by <Name> <N> <unit> ago"
        This attribute is required for accessibility and never changes.
        """
        label = article.get_attribute("aria-label") or ""
        # Strip leading prefix
        if not label.startswith("Comment by "):
            return ""
        rest = label[len("Comment by "):]
        # Strip trailing time expression e.g. "4 hours ago", "just now", "Yesterday at 3:00 PM"
        rest = re.sub(
            r'\s+\d+\s+(?:second|minute|hour|day|week|month|year)s?\s+ago\s*$',
            '', rest, flags=re.I
        ).strip()
        rest = re.sub(r'\s+just\s+now\s*$', '', rest, flags=re.I).strip()
        rest = re.sub(r'\s+Yesterday\s+at\s+[\d:]+\s*(?:AM|PM)?\s*$', '', rest, flags=re.I).strip()
        return rest.strip()

    # -------------------------------------------------------------------------
    # STABLE COMMENT TEXT EXTRACTION
    # div[dir="auto"][style="text-align: start;"]  ← inline style, always set
    # -------------------------------------------------------------------------
    @staticmethod
    def _text_from_article(article: ElementHandle) -> str:
        """
        Extract comment body using the inline style attribute which Facebook
        sets consistently on comment text containers.
        Falls back to the deepest dir="auto" div if the style isn't present.
        """
        # Primary: inline style is stable, not a generated class
        el = article.query_selector('div[dir="auto"][style*="text-align"]')
        if el:
            return el.inner_text().strip()

        # Fallback: nested dir=auto (text container is always the deepest one)
        el = article.query_selector('div[dir="auto"] div[dir="auto"]')
        if el:
            return el.inner_text().strip()

        el = article.query_selector('div[dir="auto"]')
        if el:
            return el.inner_text().strip()

        return ""

    # -------------------------------------------------------------------------
    # STABLE STATS EXTRACTION  (no CSS class selectors)
    # -------------------------------------------------------------------------
    def _extract_post_stats(self, page: Page, post: ElementHandle) -> Tuple[str, str, str]:
        """
        Returns (reaction_val, total_comments, total_shares).

        Uses:
          - aria-label on the reactions summary button  (stable ARIA)
          - JS text-node walker to find "X comments" / "X shares"  (stable text)
        """
        reaction_val = "0"
        total_comments = "0"
        total_shares = "0"

        try:
            # Reactions: Facebook always puts aria-label="X reactions" or
            # "Like: X" on the reaction summary element.
            reaction_el = post.query_selector(
                '[aria-label*="reaction" i], [aria-label*="like" i][role="button"]'
            )
            if reaction_el:
                lbl = reaction_el.get_attribute("aria-label") or ""
                m = re.search(r'([\d,]+)', lbl)
                if m:
                    reaction_val = m.group(1).replace(",", "")
        except Exception:
            pass

        try:
            # Walk text nodes to find "N comment(s)" and "N share(s)".
            # Text nodes are independent of class names.
            stats = page.evaluate(
                """(postEl) => {
                    const out = { comments: "0", shares: "0" };
                    const walk = document.createTreeWalker(
                        postEl, NodeFilter.SHOW_TEXT, null
                    );
                    let node;
                    while ((node = walk.nextNode())) {
                        const t = node.textContent.trim();
                        if (/^[\d,]+\s+comment/i.test(t)) {
                            const m = t.match(/^([\d,]+)/);
                            if (m) out.comments = m[1].replace(/,/g, '');
                        } else if (/^[\d,]+\s+share/i.test(t)) {
                            const m = t.match(/^([\d,]+)/);
                            if (m) out.shares = m[1].replace(/,/g, '');
                        }
                    }
                    return out;
                }""",
                post,
            )
            total_comments = stats.get("comments", "0")
            total_shares = stats.get("shares", "0")
        except Exception:
            pass

        return reaction_val, total_comments, total_shares

    # -------------------------------------------------------------------------
    # STABLE COMMENT TRIGGER
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # FIND POST PERMALINK FROM FEED ARTICLE
    # -------------------------------------------------------------------------
    @staticmethod
    def _get_post_permalink(post: ElementHandle) -> str:
        """Extract the permanent URL of a post from its feed article element."""
        # Strategy 1: anchor wrapping a timestamp abbreviation
        el = post.query_selector("a:has(abbr)")
        if el:
            href = el.get_attribute("href") or ""
            if "/posts/" in href or "/permalink/" in href or "story_fbid" in href:
                if href.startswith("/"):
                    href = "https://www.facebook.com" + href
                return href

        # Strategy 2: any a[href*="/posts/"] inside the article
        links = post.query_selector_all('a[href*="/posts/"], a[href*="/permalink/"]')
        for link in links:
            href = link.get_attribute("href") or ""
            if href.startswith("/"):
                href = "https://www.facebook.com" + href
            if "comment_id" not in href:
                return href

        # Strategy 3: JS - find shortest /posts/ href
        result = post.evaluate(
            """(el) => {
                const anchors = el.querySelectorAll('a[href]');
                let best = null;
                for (const a of anchors) {
                    const h = a.getAttribute('href') || '';
                    if ((h.includes('/posts/') || h.includes('/permalink/')) &&
                        !h.includes('comment_id')) {
                        if (!best || h.length < best.length) best = h;
                    }
                }
                if (best && best.startsWith('/'))
                    best = 'https://www.facebook.com' + best;
                return best;
            }"""
        )
        return result or ""

    # -------------------------------------------------------------------------
    # CORE COMMENT SCRAPER  (navigate to permalink, read comments there)
    # -------------------------------------------------------------------------
    def _scrape_post_comments(self, page: Page, permalink: str) -> list:
        """
        Navigate to permalink and collect comments.
        Accepts a plain string URL — no ElementHandle — so it is never stale.
        """
        commenters = []
        seen_keys = set()

        if not permalink:
            print("[FB] No permalink provided — skipping comments")
            return commenters

        print(f"[FB] Fetching comments from: {permalink}")
        origin_url = page.url

        try:
            page.goto(permalink, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(4000)

            scroll_attempts = 0
            no_progress_streak = 0
            prev_count = 0

            while len(commenters) < 20 and scroll_attempts < 20:
                articles = page.query_selector_all(
                    'div[role="article"][aria-label^="Comment by"]'
                )
                print(f"[FB]   {len(articles)} comment articles found (scroll {scroll_attempts + 1})")

                for article in articles:
                    if len(commenters) >= 20:
                        break
                    username = self._author_from_aria(article)
                    if not username:
                        continue
                    comment_text = self._text_from_article(article)
                    if not comment_text:
                        continue
                    key = f"{username}::{comment_text[:80]}"
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    commenters.append({"username": username, "text": comment_text})
                    print(f"[FB]     + {username!r}: {comment_text[:50]!r}")

                if len(commenters) == prev_count:
                    no_progress_streak += 1
                else:
                    no_progress_streak = 0
                prev_count = len(commenters)
                scroll_attempts += 1

                if no_progress_streak >= 4:
                    break
                if len(commenters) < 20:
                    page.mouse.wheel(0, 1500)
                    page.wait_for_timeout(2000)

        except Exception as e:
            print(f"[FB] Error scraping comments: {e}")
        finally:
            try:
                page.goto(origin_url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3000)
            except Exception:
                pass

        return commenters

    def scrape_posts(self, page: Page, max_posts: int = 5) -> List[Dict[str, Any]]:
        """
        Two-phase approach to avoid stale ElementHandle errors:

        PHASE 1  (on the feed page)
          - Scroll and collect raw post metadata entirely as plain Python dicts.
            No ElementHandles are kept — everything extracted to strings immediately.

        PHASE 2  (navigate to each permalink)
          - For each collected permalink, navigate and scrape comments.
          - The feed page is never revisited with stale handles.
        """
        page.goto(self.seed_url, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        # ── Phase 1: collect post metadata (plain data only, no ElementHandles) ─────
        raw_posts = []           # list of dicts with plain string values
        processed_ids: set = set()
        no_new_rounds = 0

        while len(raw_posts) < max_posts and no_new_rounds < 8:
            found_new = False

            all_articles = page.query_selector_all('div[role="article"]')
            post_elements = [
                el for el in all_articles
                if not (el.get_attribute("aria-label") or "").startswith("Comment by")
                and el.query_selector(
                    'div[data-ad-preview="message"], div[data-ad-comet-preview="message"]'
                )
            ]

            for post in post_elements:
                if len(raw_posts) >= max_posts:
                    break

                # Caption
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
                processed_ids.add(post_id)
                found_new = True

                # Permalink — extract to plain string NOW before any navigation
                permalink = self._get_post_permalink(post)
                print(f"[FB] Post permalink: {permalink!r}")

                # Media
                img_el = post.query_selector('img[data-imgperflogname="feedImage"]')
                media_url = img_el.get_attribute("src") if img_el else ""

                # Stats (reactions / comments / shares)
                reaction_val, total_comments, total_shares = self._extract_post_stats(page, post)

                raw_posts.append({
                    "caption":    caption,
                    "permalink":  permalink,
                    "media_url":  media_url,
                    "likes":      reaction_val,
                    "comments":   total_comments,
                    "shares":     total_shares,
                })

            no_new_rounds = 0 if found_new else no_new_rounds + 1

            if len(raw_posts) < max_posts:
                page.mouse.wheel(0, 2500)
                page.wait_for_timeout(3000)

        print(f"[FB] Phase 1 complete: {len(raw_posts)} posts collected")

        # ── Phase 2: visit each permalink and scrape comments ────────────────────────
        posts_data: List[Dict[str, Any]] = []

        for raw in raw_posts:
            commenters = self._scrape_post_comments(page, raw["permalink"])
            posts_data.append({
                "status":        "active",
                "post_url":      raw["permalink"] or self.seed_url,
                "datetime":      "",
                "caption":       raw["caption"],
                "media_url":     raw["media_url"],
                "media_type":    "image" if raw["media_url"] else "text",
                "comments":      raw["comments"],
                "likes":         raw["likes"],
                "shares":        raw["shares"],
                "views":         "0",
                "connections":   [c["username"] for c in commenters],
                "comments_text": [c["text"]     for c in commenters],
            })

        return posts_data


    # -------------------------------------------------------------------------
    # REMAINING METHODS (unchanged)
    # -------------------------------------------------------------------------

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

    def _resolve_list_url(self, page: Page, mode: str) -> str:
        page.goto(self.seed_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)
        anchors = page.query_selector_all('a[href]')
        hrefs = [a.get_attribute("href").lower() for a in anchors if a.get_attribute("href")]

        def has_followers(): return any("/followers" in h or "sk=followers" in h for h in hrefs)
        def has_following(): return any("/following" in h or "sk=following" in h for h in hrefs)
        def has_friends():   return any("/friends" in h or "sk=friends" in h for h in hrefs)

        if mode == "followers":
            return self.followers_url if has_followers() else (self.friends_url if has_friends() else self.followers_url)
        if mode == "following":
            return self.following_url if has_following() else (self.friends_url if has_friends() else self.following_url)
        return self.friends_url

    def _collect_people(self, page: Page, max_items: int, mode: str):
        target_url = self._resolve_list_url(page, mode)
        page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        collected, seen = [], set()
        no_progress_rounds = 0

        while len(collected) < max_items and no_progress_rounds < 12:
            names = self._extract_names(page)
            added = 0
            for name in names:
                if name not in seen:
                    seen.add(name)
                    collected.append(name)
                    added += 1
                if len(collected) >= max_items:
                    break

            no_progress_rounds = 0 if added else no_progress_rounds + 1
            if added == 0:
                page.wait_for_timeout(1500)
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(2000)

        return collected[:max_items]

    def _extract_profile_info(self, page: Page) -> Dict:
        print("[Facebook] Extracting profile information...")
        profile_data = {
            "real_name": None, "bio": None, "location": None,
            "total_friends": None, "total_followers": None, "total_following": None,
        }
        try:
            for selector in ['h1.html-h1', 'span[dir="auto"]', 'h2.html-h2']:
                try:
                    el = page.query_selector(selector)
                    if el:
                        profile_data["real_name"] = el.inner_text().strip()
                        break
                except Exception:
                    continue

            for key, pattern in [
                ("total_friends", "friends"),
                ("total_followers", "followers"),
                ("total_following", "following"),
            ]:
                try:
                    el = page.query_selector(f'a[href*="{pattern}"] strong')
                    if el:
                        profile_data[key] = el.inner_text().strip()
                except Exception:
                    pass

            for selector in ['div[data-ad-rendering-role="story_message"]']:
                bio_el = page.query_selector(selector)
                if bio_el:
                    profile_data["bio"] = bio_el.inner_text().strip()
                    break

            print(f"[Facebook] Profile info collected: {profile_data}")
        except Exception as e:
            print(f"[Facebook] Error extracting profile info: {e}")
        return profile_data

    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        page.goto(self.seed_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        profile_data = {
            "real_name": None, "bio": None, "location": None,
            "total_friends": None, "total_followers": None, "total_following": None,
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

            bio_el = page.query_selector("div.xz9dl7a.xp6pnuw.x160xiiu > span[dir='auto']")
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

            for selector in ['a[href*="hometown"]', 'a[href*="location"]', 'a[href*="city"]', "li:has(svg) a"]:
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
        return self._collect_people(page, self._max_friends, mode="followers")

    def scrape_following(self, page: Page) -> List[str]:
        return self._collect_people(page, self._max_friends, mode="following")