import random
import re
from datetime import datetime, date, timedelta
from urllib.parse import urljoin, urlsplit, urlunsplit
from typing import Optional, List, Dict, Any
from playwright.sync_api import Page


class FacebookScraper:
    STARTUP_TIMEOUT_MS = 5 * 60 * 1000
    INITIAL_WAIT_MS = (3500, 6500)
    SHORT_WAIT_MS = (350, 1200)
    ACTION_WAIT_MS = (800, 2400)
    POST_WAIT_MS = (150, 650)
    SCROLL_WAIT_MS = (2200, 5200)
    SCROLL_DELTA = (900, 2600)

    POST_URL_SELECTORS = [
        'a[href*="/groups/"][href*="/posts/"]',
        'a[href*="/posts/"]',
        'a[href*="/permalink/"]',
        'a[href*="/reel/"]',
        'a[href*="/videos/"]',
        'a[href*="/watch/"]',
        'a[href*="/photo.php"]',
        'a[href*="/photos/"]',
        'a[href*="/events/"]',
        'a[href*="/marketplace/item/"]',
        'a[href*="story_fbid="]',
    ]

    POST_MARKER_SELECTORS = [
        '[aria-label="Actions for this post"]',
        '[data-ad-rendering-role="profile_name"]',
        '[data-ad-rendering-role="story_message"]',
        '[data-ad-rendering-role="like_button"]',
        '[data-ad-rendering-role="comment_button"]',
        '[data-ad-rendering-role="share_button"]',
        '[data-ad-rendering-role="meta"]',
        '[data-ad-rendering-role="title"]',
        '[data-ad-rendering-role="description"]',
        'img[data-imgperflogname="feedImage"]',
        'video',
        *POST_URL_SELECTORS,
    ]

    CONTENT_SELECTORS = [
        '[data-ad-rendering-role="story_message"]',
        '[data-ad-comet-preview="message"]',
        '[data-ad-preview="message"]',
        '[data-testid="post_message"]',
        'div[dir="auto"][style*="text-align"]',
    ]

    ATTACHMENT_TEXT_SELECTORS = [
        '[data-ad-rendering-role="title"]',
        '[data-ad-rendering-role="description"]',
        '[data-ad-rendering-role="meta"]',
    ]

    def __init__(self, seed_url: str, max_posts: int = 20):
        self.seed_url = seed_url.rstrip("/")
        self.max_posts = max_posts

    @staticmethod
    def _random_wait(page: Page, wait_range: tuple[int, int]):
        min_wait_ms, max_wait_ms = wait_range
        page.wait_for_timeout(random.randint(min_wait_ms, max_wait_ms))

    @staticmethod
    def _parse_post_date(raw_text: str) -> Optional[date]:
        if not raw_text:
            return None

        txt = re.sub(r"\s+", " ", raw_text.strip()).replace("·", " ").strip()
        txt = re.sub(r"\s+at\s+\d{1,2}:\d{2}\s*(?:AM|PM)?", "", txt, flags=re.I)
        low = txt.lower()
        today = date.today()

        if low.startswith("today"):
            return today
        if low.startswith("yesterday"):
            return today - timedelta(days=1)
        if re.match(r"^(\d+)\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes)\s*(ago)?$", low):
            return today

        m = re.match(r"^(\d+)\s*(d|day|days)\s*(ago)?$", low)
        if m:
            return today - timedelta(days=int(m.group(1)))

        m = re.match(r"^(\d+)\s*(w|week|weeks)\s*(ago)?$", low)
        if m:
            return today - timedelta(days=int(m.group(1)) * 7)

        for p in ["%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y", "%Y-%m-%d"]:
            try:
                return datetime.strptime(txt, p).date()
            except:
                pass

        for p in ["%B %d", "%b %d", "%d %B", "%d %b"]:
            try:
                d = datetime.strptime(txt, p).date().replace(year=today.year)
                if d > today:
                    d = d.replace(year=today.year - 1)
                return d
            except:
                pass

        return None

    @staticmethod
    def _visible_text(el) -> str:
        try:
            return (el.evaluate(
                """(node) => {
                    const rootRect = node.getBoundingClientRect();
                    const pieces = [];
                    const walker = document.createTreeWalker(
                        node,
                        NodeFilter.SHOW_TEXT,
                        {
                            acceptNode(textNode) {
                                const parent = textNode.parentElement;
                                if (!parent) return NodeFilter.FILTER_REJECT;
                                const style = window.getComputedStyle(parent);
                                if (
                                    style.display === "none" ||
                                    style.visibility === "hidden" ||
                                    style.opacity === "0"
                                ) {
                                    return NodeFilter.FILTER_REJECT;
                                }
                                const rect = parent.getBoundingClientRect();
                                if (
                                    rect.bottom <= rootRect.top ||
                                    rect.top >= rootRect.bottom ||
                                    rect.right <= rootRect.left ||
                                    rect.left >= rootRect.right
                                ) {
                                    return NodeFilter.FILTER_REJECT;
                                }
                                return NodeFilter.FILTER_ACCEPT;
                            }
                        }
                    );
                    while (walker.nextNode()) pieces.push(walker.currentNode.nodeValue);
                    return pieces.join("");
                }"""
            ) or "").strip()
        except:
            return ""

    @staticmethod
    def _clean_facebook_url(raw_url: str) -> Optional[str]:
        if not raw_url:
            return None
        url = urljoin("https://www.facebook.com", raw_url)
        split = urlsplit(url)
        if "facebook.com" not in split.netloc:
            return url
        return urlunsplit((split.scheme, split.netloc, split.path, "", ""))

    @staticmethod
    def _normalize_text(raw_text: str) -> str:
        if not raw_text:
            return ""
        lines = []
        for line in raw_text.replace("\r", "\n").splitlines():
            line = re.sub(r"\s+", " ", line).strip()
            if line:
                lines.append(line)
        return "\n".join(lines).strip()

    @staticmethod
    def _append_unique(parts: List[str], raw_text: str):
        text = FacebookScraper._normalize_text(raw_text)
        if not text:
            return
        for line in text.splitlines():
            if line and line not in parts:
                parts.append(line)

    def _is_noise_line(self, line: str) -> bool:
        low = line.strip().lower()
        if not low:
            return True

        skip_words = {
            "facebook",
            "like",
            "comment",
            "share",
            "reply",
            "send",
            "react",
            "follow",
            "all reactions:",
            "see more",
            "show more",
            "view more comments",
            "write a comment...",
            "write a comment…",
            "shared with public",
            "public",
            "m.me",
            "facebook.com",
            "www.facebook.com",
        }
        if low in skip_words:
            return True
        if "actions for this post" in low:
            return True
        if "write a comment" in low:
            return True
        if re.search(r"\b(like|comment|share|send|react)\b", low) and len(low.split()) <= 8:
            return True
        if re.search(r"\b\d+(?:\.\d+)?[km]?\s*(views?|shares?|comments?|reactions?|likes?)\b", low):
            return True
        if re.fullmatch(r"\d+(?:\.\d+)?[km]?", low):
            return True
        if low.endswith(".com") and " " not in low:
            return True
        if len(low) >= 40 and " " not in low and re.fullmatch(r"[a-z0-9_=-]+", low, re.I):
            return True
        if self._parse_post_date(line):
            return True
        return False

    def _clean_content_text(self, raw_text: str) -> str:
        cleaned = []
        for line in self._normalize_text(raw_text).splitlines():
            if self._is_noise_line(line):
                continue
            if line not in cleaned:
                cleaned.append(line)
        return "\n".join(cleaned).strip()

    @staticmethod
    def _to_int_count(s: str) -> Optional[int]:
        if not s:
            return None
        t = s.replace(",", "").strip().upper()
        m = re.search(r"(\d+(?:\.\d+)?)\s*([KM]?)", t)
        if not m:
            return None
        val = float(m.group(1))
        suf = m.group(2)
        if suf == "K":
            val *= 1000
        elif suf == "M":
            val *= 1000000
        return int(val)

    def extract_m_title(self, container) -> Optional[str]:
        try:
            el = container.query_selector('[data-ad-rendering-role="profile_name"]')
            if el:
                txt = (el.inner_text() or "").strip()
                if txt:
                    return txt
        except:
            pass

        try:
            a = container.query_selector("a[aria-label]")
            if a:
                aria = a.get_attribute("aria-label")
                if aria:
                    return aria.strip()
        except:
            pass

        try:
            raw = (container.inner_text() or "").strip()
            for line in raw.splitlines():
                line = line.strip()
                if self._parse_post_date(line):
                    return line
        except:
            pass

        return None

    def extract_post_url(self, container) -> Optional[str]:
        ignored_labels = {"enlarge", "comment", "like", "share", "react", "play", "mute"}

        try:
            for sel in self.POST_URL_SELECTORS:
                for link in container.query_selector_all(sel):
                    label = (link.get_attribute("aria-label") or "").strip().lower()
                    if label in ignored_labels:
                        continue
                    href = link.get_attribute("href")
                    clean = self._clean_facebook_url(href)
                    if clean:
                        return clean
        except:
            pass

        return None

    def extract_date(self, container, raw_text: str) -> Dict[str, Optional[str]]:
        candidates = []
        selectors = [
            "time",
            "abbr[title]",
            *self.POST_URL_SELECTORS,
        ]

        try:
            for sel in selectors:
                for el in container.query_selector_all(sel):
                    for attr in ["datetime", "title", "aria-label"]:
                        val = el.get_attribute(attr)
                        if val:
                            candidates.append(val)
                    visible = self._visible_text(el) or (el.inner_text() or "")
                    if visible:
                        candidates.append(visible)
        except:
            pass

        candidates.append(raw_text)
        for candidate in candidates:
            parsed = self.extract_date_from_caption(candidate)
            if parsed.get("date"):
                return parsed

        return {"m_title": None, "date": None}

    def extract_date_from_caption(self, caption: str) -> Dict[str, Optional[str]]:
        if not caption:
            return {"m_title": None, "date": None}

        text = re.sub(r"\s+", " ", caption.replace("·", " ")).strip()
        today = date.today()

        patterns = [
            (r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b", ["%d %B %Y", "%d %b %Y"]),
            (r"\b[A-Za-z]{3,9}\s+\d{1,2},\s*\d{4}\b", ["%B %d, %Y", "%b %d, %Y"]),
            (r"\b\d{4}-\d{2}-\d{2}\b", ["%Y-%m-%d"]),
        ]

        for rx, fmts in patterns:
            m = re.search(rx, text)
            if m:
                raw = m.group(0).strip()
                for f in fmts:
                    try:
                        d = datetime.strptime(raw, f).date()
                        return {"m_title": raw, "date": d.isoformat()}
                    except:
                        pass
                return {"m_title": raw, "date": None}

        m = re.search(r"\b(today|yesterday)\b", text, re.I)
        if m:
            raw = m.group(1)
            d = today if raw.lower() == "today" else today - timedelta(days=1)
            return {"m_title": raw, "date": d.isoformat()}

        m = re.search(r"\b(\d+)\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes)\b", text, re.I)
        if m:
            return {"m_title": m.group(0), "date": today.isoformat()}

        m = re.search(r"\b(\d+)\s*(d|day|days)\b", text, re.I)
        if m:
            d = today - timedelta(days=int(m.group(1)))
            return {"m_title": m.group(0), "date": d.isoformat()}

        m = re.search(r"\b(\d+)\s*(w|week|weeks)\b", text, re.I)
        if m:
            d = today - timedelta(days=int(m.group(1)) * 7)
            return {"m_title": m.group(0), "date": d.isoformat()}

        m = re.search(r"\b\d{1,2}\s+[A-Za-z]{3,9}\b", text)
        if m:
            raw = m.group(0).strip()
            for f in ["%d %B", "%d %b"]:
                try:
                    d = datetime.strptime(raw, f).date().replace(year=today.year)
                    if d > today:
                        d = d.replace(year=today.year - 1)
                    return {"m_title": raw, "date": d.isoformat()}
                except:
                    pass

        m = re.search(r"\b[A-Za-z]{3,9}\s+\d{1,2}\b", text)
        if m:
            raw = m.group(0).strip()
            for f in ["%B %d", "%b %d"]:
                try:
                    d = datetime.strptime(raw, f).date().replace(year=today.year)
                    if d > today:
                        d = d.replace(year=today.year - 1)
                    return {"m_title": raw, "date": d.isoformat()}
                except:
                    pass

        return {"m_title": None, "date": None}

    def extract_likes(self, container) -> Optional[int]:
        try:
            raw = (container.inner_text() or "").strip()
            text = re.sub(r"\s+", " ", raw)

            m = re.search(r"all reactions:\s*([0-9.,kKmM]+)", text, re.I)
            if m:
                return self._to_int_count(m.group(1))

            matches = re.findall(r"(?:like|love|care|haha|wow|sad|angry):\s*([0-9.,kKmM]+)\s*people", text, re.I)
            if matches:
                total = 0
                for val in matches:
                    n = self._to_int_count(val)
                    if n:
                        total += n
                return total or None

            m = re.search(r"([0-9.,kKmM]+)\s*(reactions?|likes?)", text, re.I)
            if m:
                return self._to_int_count(m.group(1))
        except:
            pass

        try:
            total = 0
            for el in container.query_selector_all('[aria-label*=" people"]'):
                label = (el.get_attribute("aria-label") or "").strip()
                if not re.match(r"^(like|love|care|haha|wow|sad|angry):", label, re.I):
                    continue
                n = self._to_int_count(label)
                if n:
                    total += n
            if total:
                return total
        except:
            pass

        for sel in ['[aria-label^="All reactions"]', 'span[aria-label*="reaction"]', 'span[aria-label*="Reactions"]']:
            try:
                el = container.query_selector(sel)
                if el:
                    txt = (el.get_attribute("aria-label") or el.inner_text() or "").strip()
                    if txt:
                        n = self._to_int_count(txt)
                        if n is not None:
                            return n
            except:
                pass

        return None

    def extract_content(self, container, raw_text: str) -> str:
        content_parts = []
        try:
            for selector in self.CONTENT_SELECTORS:
                for el in container.query_selector_all(selector):
                    txt = self._visible_text(el) or (el.inner_text() or "")
                    txt = self._clean_content_text(txt)
                    self._append_unique(content_parts, txt)
            if content_parts:
                return "\n".join(content_parts).strip()
        except:
            pass

        attachment_parts = []
        try:
            for selector in self.ATTACHMENT_TEXT_SELECTORS:
                for el in container.query_selector_all(selector):
                    txt = self._visible_text(el) or (el.inner_text() or "")
                    txt = self._clean_content_text(txt)
                    self._append_unique(attachment_parts, txt)
            if attachment_parts:
                return "\n".join(attachment_parts).strip()
        except:
            pass

        cleaned = self._clean_content_text(raw_text).splitlines()
        if len(cleaned) > 1 and len(cleaned[0].split()) <= 5:
            cleaned = cleaned[1:]

        return "\n".join(cleaned).strip()

    def extract_media(self, container) -> Dict[str, Any]:
        media = {
            "images": [],
            "videos": [],
            "video_blobs": 0,
            "attachment_urls": [],
        }

        try:
            for img in container.query_selector_all('img[data-imgperflogname="feedImage"], img[src*="scontent"]'):
                src = img.get_attribute("src")
                if not src or src.startswith("data:") or "static.xx.fbcdn.net" in src:
                    continue
                if re.search(r"_s(?:32|40|48|56|64|80)x(?:32|40|48|56|64|80)", src):
                    continue
                if src not in media["images"]:
                    media["images"].append(src)
        except:
            pass

        try:
            for video in container.query_selector_all("video"):
                src = video.get_attribute("src")
                if not src:
                    continue
                if src.startswith("blob:"):
                    media["video_blobs"] += 1
                    continue
                if src not in media["videos"]:
                    media["videos"].append(src)
        except:
            pass

        try:
            for link in container.query_selector_all("a[href]"):
                href = link.get_attribute("href")
                clean = self._clean_facebook_url(href)
                if not clean:
                    continue
                if "facebook.com" in urlsplit(clean).netloc:
                    continue
                if clean not in media["attachment_urls"]:
                    media["attachment_urls"].append(clean)
        except:
            pass

        return media

    def detect_post_type(self, container, post_url: Optional[str], media: Dict[str, Any]) -> str:
        url = post_url or ""
        try:
            raw = (container.inner_text() or "").lower()
        except:
            raw = ""

        if "/marketplace/item/" in url:
            return "marketplace"
        if "/events/" in url:
            return "event"
        if "/reel/" in url:
            return "reel"
        if "/watch/" in url or "/videos/" in url or media.get("videos") or media.get("video_blobs"):
            return "video"
        if "/photo" in url or media.get("images"):
            return "photo"
        if " was live" in raw or " live " in raw:
            return "live"
        try:
            if media.get("attachment_urls") or container.query_selector('[data-ad-rendering-role="title"], [data-ad-rendering-role="description"]'):
                return "link_or_share"
            if container.query_selector('[data-ad-rendering-role="story_message"], [data-ad-comet-preview="message"], [data-ad-preview="message"]'):
                return "text"
        except:
            pass
        return "post"

    def extract_comments(self, raw_text: str) -> Dict[str, Optional[int]]:
        text = re.sub(r"\s+", " ", raw_text)
        comments = None

        mc = re.search(r"([0-9.,kKmM]+)\s*comments?", text, re.I)
        if mc:
            comments = self._to_int_count(mc.group(1))

        return {"comments": comments}

    def is_post_container(self, container) -> bool:
        try:
            aria = (container.get_attribute("aria-label") or "").lower()
            if aria.startswith("comment by"):
                return False
        except:
            pass

        try:
            if container.evaluate("(el) => !!el.closest('[data-commentid]')"):
                return False
        except:
            pass

        try:
            return bool(container.evaluate(
                """(el) => {
                    const markers = [
                        '[aria-label="Actions for this post"]',
                        '[data-ad-rendering-role="profile_name"]',
                        '[data-ad-rendering-role="story_message"]',
                        '[data-ad-comet-preview="message"]',
                        '[data-ad-preview="message"]',
                        'a[href*="/posts/"]',
                        'a[href*="/groups/"][href*="/posts/"]',
                        'a[href*="/permalink/"]',
                        'a[href*="/reel/"]',
                        'a[href*="/videos/"]',
                        'a[href*="/watch/"]',
                        'a[href*="/photo.php"]',
                        'a[href*="/photos/"]',
                        'a[href*="/events/"]',
                        'a[href*="/marketplace/item/"]',
                        'a[href*="story_fbid="]',
                        'img[data-imgperflogname="feedImage"]',
                        'video',
                        '[data-ad-rendering-role="like_button"]',
                        '[data-ad-rendering-role="comment_button"]',
                        '[data-ad-rendering-role="share_button"]',
                        '[data-ad-rendering-role="title"]',
                        '[data-ad-rendering-role="description"]'
                    ];
                    for (let node = el; node && node !== document.body; node = node.parentElement) {
                        if (markers.some((selector) => node.querySelector(selector))) {
                            return true;
                        }
                    }
                    return false;
                }"""
            ))
        except:
            pass

        try:
            if container.query_selector('[aria-label="Actions for this post"]'):
                return True
            if container.query_selector('[data-ad-rendering-role="profile_name"]'):
                return True
            if container.query_selector('[data-ad-rendering-role="story_message"]'):
                return True
            if container.query_selector(", ".join(self.POST_MARKER_SELECTORS)):
                return True
        except:
            pass
        return False

    def _expand_visible_truncations(self, page: Page):
        try:
            page.evaluate(
                """() => {
                    const labels = new Set(["See more", "Show more"]);
                    const candidates = Array.from(document.querySelectorAll('div[role="button"], span[role="button"], a[role="link"], span'));
                    let clicked = 0;
                    for (const el of candidates) {
                        const text = (el.innerText || el.textContent || "").trim();
                        if (!labels.has(text)) continue;
                        const rect = el.getBoundingClientRect();
                        if (rect.width === 0 || rect.height === 0) continue;
                        try {
                            el.click();
                            clicked += 1;
                        } catch (_) {}
                        if (clicked >= 25) break;
                    }
                }"""
            )
        except:
            pass

    def _get_post_containers(self, page: Page):
        try:
            page.evaluate(
                """() => {
                    let idx = Number(document.documentElement.dataset.fbScraperPostSeq || "0");
                    const markers = document.querySelectorAll([
                        '[aria-label="Actions for this post"]',
                        '[data-ad-rendering-role="profile_name"]',
                        '[data-ad-rendering-role="story_message"]',
                        '[data-ad-rendering-role="like_button"]',
                        '[data-ad-rendering-role="comment_button"]',
                        '[data-ad-rendering-role="share_button"]',
                        '[data-ad-rendering-role="title"]',
                        '[data-ad-rendering-role="description"]',
                        '[data-ad-comet-preview="message"]',
                        '[data-ad-preview="message"]',
                        'a[href*="/groups/"][href*="/posts/"]',
                        'a[href*="/posts/"]',
                        'a[href*="/permalink/"]',
                        'a[href*="/reel/"]',
                        'a[href*="/videos/"]',
                        'a[href*="/watch/"]',
                        'a[href*="/photo.php"]',
                        'a[href*="/photos/"]',
                        'a[href*="/events/"]',
                        'a[href*="/marketplace/item/"]',
                        'a[href*="story_fbid="]'
                    ].join(','));

                    for (const marker of markers) {
                        let root = marker.closest('div[role="article"]');
                        if (!root) {
                            root = marker;
                            for (let depth = 0; depth < 12 && root.parentElement; depth++) {
                                root = root.parentElement;
                                const hasProfile = !!root.querySelector('[data-ad-rendering-role="profile_name"]');
                                const hasBody = !!root.querySelector(
                                    '[data-ad-rendering-role="story_message"], [data-ad-comet-preview="message"], [data-ad-preview="message"], [data-ad-rendering-role="like_button"], [data-ad-rendering-role="comment_button"], [data-ad-rendering-role="share_button"], [data-ad-rendering-role="title"], [data-ad-rendering-role="description"], video, img[data-imgperflogname="feedImage"], a[href*="/groups/"][href*="/posts/"], a[href*="/posts/"], a[href*="/permalink/"], a[href*="/reel/"], a[href*="/videos/"], a[href*="/watch/"], a[href*="/photo.php"], a[href*="/photos/"], a[href*="/events/"], a[href*="/marketplace/item/"], a[href*="story_fbid="]'
                                );
                                if (hasProfile && hasBody) break;
                            }
                        }

                        if (root && !root.dataset.fbScraperPostRoot) {
                            root.dataset.fbScraperPostRoot = String(++idx);
                        }
                    }
                    document.documentElement.dataset.fbScraperPostSeq = String(idx);
                }"""
            )
        except:
            pass

        containers = []
        seen = set()
        for selector in ['[data-fb-scraper-post-root]', 'div[role="article"]']:
            try:
                for container in page.query_selector_all(selector):
                    try:
                        marker = container.get_attribute("data-fb-scraper-post-root") or str(id(container))
                    except:
                        marker = str(id(container))
                    if marker in seen:
                        continue
                    seen.add(marker)
                    containers.append(container)
            except:
                pass
        return containers

    def _close_login_popup(self, page):
        try:
            close_btn = page.locator('div[aria-label="Close"][role="button"]').first
            if close_btn.count() > 0:
                close_btn.click(timeout=3000)
                self._random_wait(page, self.ACTION_WAIT_MS)
        except:
            pass

    def scrape_posts(self, page: Page) -> List[Dict[str, Any]]:
        results = []
        seen = set()

        page.goto(self.seed_url, wait_until="domcontentloaded", timeout=self.STARTUP_TIMEOUT_MS)
        self._random_wait(page, self.INITIAL_WAIT_MS)
        self._close_login_popup(page)
        self._random_wait(page, self.SHORT_WAIT_MS)
        self._expand_visible_truncations(page)
        self._random_wait(page, self.SHORT_WAIT_MS)

        max_scrolls = 20
        scrolls = 0

        while len(results) < self.max_posts and scrolls < max_scrolls:
            try:
                page.wait_for_load_state("domcontentloaded")
                self._random_wait(page, self.SHORT_WAIT_MS)
                self._expand_visible_truncations(page)
                self._random_wait(page, self.SHORT_WAIT_MS)
                containers = self._get_post_containers(page)

                for container in containers:
                    if len(results) >= self.max_posts:
                        break

                    try:
                        raw_text = (container.inner_text() or "").strip()
                        if not raw_text:
                            continue
                        if not self.is_post_container(container):
                            continue

                        m_title = self.extract_m_title(container)
                        post_url = self.extract_post_url(container)
                        post_key = post_url or hash(raw_text[:1000])
                        if post_key in seen:
                            continue
                        seen.add(post_key)

                        date_info = self.extract_date(container, raw_text)
                        date_iso = date_info.get("date")

                        likes = self.extract_likes(container)
                        content = self.extract_content(container, raw_text)
                        cs = self.extract_comments(raw_text)
                        media = self.extract_media(container)
                        post_type = self.detect_post_type(container, post_url, media)

                        post = {
                            "m_title": m_title,
                            "date": date_iso,
                            "url": post_url,
                            "type": post_type,
                            "content": content if content else None,
                            "likes": likes,
                            "comments": cs["comments"],
                            "images": media["images"],
                            "videos": media["videos"],
                            "video_blobs": media["video_blobs"],
                            "attachment_urls": media["attachment_urls"],
                        }

                        has_payload = any([
                            m_title,
                            date_iso,
                            post_url,
                            content,
                            likes is not None,
                            cs["comments"] is not None,
                            media["images"],
                            media["videos"],
                            media["video_blobs"],
                            media["attachment_urls"],
                        ])
                        if has_payload:
                            results.append(post)
                            self._random_wait(page, self.POST_WAIT_MS)

                    except:
                        continue

            except Exception as e:
                print(f"[!] Loop error: {e}")

            page.mouse.wheel(0, random.randint(*self.SCROLL_DELTA))
            self._random_wait(page, self.SCROLL_WAIT_MS)
            scrolls += 1

        return results
