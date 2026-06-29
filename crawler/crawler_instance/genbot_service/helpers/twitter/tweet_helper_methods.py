import re
from playwright.sync_api import Page

from crawler.crawler_services.log_manager.log_controller import log


class TweetHelperMethods:
    def __init__(self):
        self.seen_ids = set()

    @staticmethod
    def extract_username(url: str) -> str:
        m = re.search(r'^(?:https?://)?(?:www\.)?(?:twitter\.com|x\.com|social\.com)/(?:@?)([A-Za-z0-9_]{1,15})(?:[/?#]|$)', url)
        if m:
            return m.group(1)
        raise ValueError(f"Invalid Twitter URL: {url}")

    @staticmethod
    def extract_weblinks(text: str) -> list:
        url_pattern = r'(https?://[^\s]+)'
        return re.findall(url_pattern, text)

    @staticmethod
    def _parse_count(count_text: str) -> int:
        if not count_text:
            return 0
        count_text = count_text.replace(",", "").strip().upper()
        match = re.search(r'([\d.]+)\s*([KMB]?)', count_text)
        if not match:
            return 0
        multiplier = {"K": 1000, "M": 1000000, "B": 1000000000}.get(match.group(2), 1)
        return int(float(match.group(1)) * multiplier)

    @staticmethod
    def _extract_status_href(article):
        tweet_id = article.get_attribute("data-tweet-id")
        anchors = article.query_selector_all('a[href*="/status/"]')
        if tweet_id:
            for anchor in anchors:
                href = anchor.get_attribute("href") or ""
                if f"/status/{tweet_id}" in href:
                    return href.split("?")[0]
        for anchor in anchors:
            href = anchor.get_attribute("href") or ""
            if re.search(r'/status/\d+', href) and anchor.query_selector("time"):
                return href.split("?")[0]
        for anchor in anchors:
            href = anchor.get_attribute("href") or ""
            if re.search(r'/status/\d+', href):
                return href.split("?")[0]
        return None

    @staticmethod
    def _extract_tweet_id(href: str):
        if not href:
            return None
        match = re.search(r'/status/(\d+)', href)
        return match.group(1) if match else None

    def _get_count(self, article, selectors) -> int:
        for selector in selectors:
            element = article.query_selector(selector)
            if not element:
                continue
            values = [
                element.get_attribute("aria-label") or "",
                element.inner_text().strip(),
            ]
            span = element.query_selector('span[data-testid="app-text-transition-container"] span')
            if span:
                values.insert(0, span.inner_text().strip())
            for value in values:
                count = self._parse_count(value)
                if count:
                    return count
        return 0

    @staticmethod
    def _get_tweet_articles(profile_page: Page) -> list:
        tweets = profile_page.query_selector_all('article[data-tweet-id], article[data-testid="tweet"]')
        if not tweets:
            tweets = profile_page.query_selector_all('article')
        if not tweets:
            tweets = profile_page.query_selector_all('div[data-testid="tweet"]')
        return tweets

    @staticmethod
    def _article_lines(article) -> list:
        return [line.strip() for line in article.inner_text().splitlines() if line.strip()]

    @staticmethod
    def _looks_like_tweet_date(text: str) -> bool:
        return bool(re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b|\b\d+[smhd]\b', text))

    def _extract_tweet_date(self, article, username: str) -> str:
        time_tag = article.query_selector('time')
        if time_tag:
            return time_tag.get_attribute("datetime") or ""

        lines = self._article_lines(article)
        username_line = f"@{username}".lower()
        for idx, line in enumerate(lines):
            if line.lower() == username_line and idx + 1 < len(lines) and self._looks_like_tweet_date(lines[idx + 1]):
                return lines[idx + 1]
        return ""

    def _extract_tweet_text(self, article, username: str) -> str:
        divs = article.query_selector_all('div[data-testid="tweetText"]') or article.query_selector_all('div[lang]')
        tweet_text = " ".join([div.inner_text().strip() for div in divs if div])
        if tweet_text:
            return tweet_text

        lines = self._article_lines(article)
        username_line = f"@{username}".lower()
        start = 0
        for idx, line in enumerate(lines):
            if line.lower() == username_line:
                start = idx + 1
                if start < len(lines) and self._looks_like_tweet_date(lines[start]):
                    start += 1
                break
        content_lines = [
            line for line in lines[start:]
            if line.lower() not in {"pinned", username_line}
        ]
        return " ".join(content_lines).strip()

    @staticmethod
    def _extract_tweets_from_dom(profile_page: Page, username: str) -> list[dict]:
        try:
            return profile_page.evaluate("""(username) => {
                const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
                const cleanUrl = value => {
                    if (!value) return '';
                    let url = String(value).trim().replace(/&amp;/g, '&').replace(/\\\\\\//g, '/');
                    if (!url || url.startsWith('data:')) return '';
                    if (url.startsWith('//')) url = `https:${url}`;
                    if (url.startsWith('/')) {
                        const origin = location.origin && location.origin !== 'null' ? location.origin : 'https://x.com';
                        url = `${origin}${url}`;
                    }
                    return url;
                };
                const srcFromImage = img => {
                    if (!img) return '';
                    const srcset = img.getAttribute('srcset') || '';
                    if (srcset) {
                        const candidates = srcset.split(',')
                            .map(item => cleanUrl(item.trim().split(/\\s+/)[0]))
                            .filter(Boolean);
                        if (candidates.length) return candidates[candidates.length - 1];
                    }
                    return cleanUrl(img.currentSrc || img.src || img.getAttribute('src'));
                };
                const statusIdFromHref = href => {
                    const match = String(href || '').match(/\\/status\\/(\\d+)/);
                    return match ? match[1] : '';
                };
                const normalizedStatusHref = href => {
                    try {
                        const url = new URL(cleanUrl(href), location.href);
                        const match = url.pathname.match(/^\\/([^/]+)\\/status\\/(\\d+)/);
                        if (match) return `https://x.com/${decodeURIComponent(match[1])}/status/${match[2]}`;
                    } catch {}
                    return cleanUrl(href);
                };
                const statusHref = link => normalizedStatusHref(link.getAttribute('href') || link.href || '');
                const usernameFromHref = href => {
                    try {
                        const url = new URL(href, location.href);
                        const parts = url.pathname.split('/').filter(Boolean);
                        if (parts.length >= 1 && /^[A-Za-z0-9_]{1,15}$/.test(parts[0])) return parts[0];
                    } catch {}
                    return username || '';
                };
                const containerForLink = link => {
                    const preferred = link.closest('article,[data-testid="tweet"],div.flex.flex-col.gap-3');
                    if (preferred) return preferred;
                    let node = link.parentElement;
                    for (let depth = 0; node && depth < 8; depth += 1, node = node.parentElement) {
                        const text = clean(node.innerText || node.textContent || '');
                        const hasMedia = Boolean(node.querySelector('img[src*="pbs.twimg.com/media"], img[src*="twimg.com/media"]'));
                        if (hasMedia || text.length > 40) return node;
                    }
                    return link.closest('div') || link.parentElement;
                };
                const textFromContainer = container => {
                    const direct = Array.from(container.querySelectorAll('div[data-testid="tweetText"], div[lang]'))
                        .map(node => clean(node.innerText || node.textContent || ''))
                        .filter(Boolean);
                    if (direct.length) return direct.join(' ').trim();
                    const candidates = Array.from(container.querySelectorAll('div[dir="auto"], span[dir="auto"]'))
                        .map(node => clean(node.innerText || node.textContent || ''))
                        .filter(text => {
                            if (text.length < 5) return false;
                            if (/^@?[A-Za-z0-9_]{1,15}$/.test(text)) return false;
                            if (/^\\d+(?:\\.\\d+)?[KMB]?\\s+Views$/i.test(text)) return false;
                            if (/^\\d{1,2}:\\d{2}\\s+[AP]M\\s*·/i.test(text)) return false;
                            return true;
                        })
                        .sort((a, b) => b.length - a.length);
                    return candidates[0] || '';
                };
                const mediaFromContainer = container => {
                    const media = [];
                    const push = value => {
                        const url = cleanUrl(value);
                        if (!url || !/twimg\\.com\\/media\\//i.test(url)) return;
                        if (/profile_images|profile_banners/i.test(url)) return;
                        if (!media.includes(url)) media.push(url);
                    };
                    for (const img of container.querySelectorAll('img')) push(srcFromImage(img));
                    const html = (container.innerHTML || '').replace(/\\\\\\//g, '/').replace(/&amp;/g, '&');
                    for (const match of html.matchAll(/https?:\\/\\/[^"'<>\\s)]+twimg\\.com\\/media\\/[^"'<>\\s)]+/ig)) {
                        push(match[0]);
                    }
                    return media;
                };
                const parseCount = text => {
                    const match = clean(text).replace(/,/g, '').match(/([\\d.]+)\\s*([KMB]?)\\s*Views/i);
                    if (!match) return '';
                    const multiplier = {K: 1000, M: 1000000, B: 1000000000}[match[2].toUpperCase()] || 1;
                    const parsed = parseFloat(match[1]);
                    return Number.isFinite(parsed) ? String(Math.round(parsed * multiplier)) : '';
                };
                const rows = [];
                const seen = new Set();
                for (const link of document.querySelectorAll('a[href*="/status/"]')) {
                    const href = statusHref(link);
                    const id = statusIdFromHref(href);
                    if (!id || seen.has(id)) continue;
                    const container = containerForLink(link);
                    if (!container) continue;
                    const content = textFromContainer(container);
                    const media = mediaFromContainer(container);
                    if (!content && media.length === 0) continue;
                    const time = container.querySelector('time')?.getAttribute('datetime') ||
                        Array.from(container.querySelectorAll(`a[href*="/status/${id}"]`))
                            .map(node => clean(node.innerText || node.textContent || ''))
                            .find(text => /\\b(?:AM|PM|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\b/i.test(text)) ||
                        '';
                    const bodyText = clean(container.innerText || container.textContent || '');
                    rows.push({
                        id,
                        date: time,
                        content,
                        url: href,
                        weblink: [],
                        media,
                        comment_count: '',
                        retweets: '',
                        likes: '',
                        views: parseCount(bodyText),
                        username: usernameFromHref(href),
                    });
                    seen.add(id);
                }
                return rows;
            }""", username)
        except Exception:
            return []

    def get_tweets_from_page(self, profile_page: Page, username: str) -> list:
        tweets = []
        tweet_articles = self._get_tweet_articles(profile_page)
        if not tweet_articles:
            log.g().w(f"Twitter parse found no tweet article tags for @{username}")

        for article in tweet_articles:
            try:
                href = self._extract_status_href(article)
                tweet_id = article.get_attribute("data-tweet-id") or self._extract_tweet_id(href)
                tweet_text = self._extract_tweet_text(article, username)
                tweet_time = self._extract_tweet_date(article, username)

                weblinks = self.extract_weblinks(tweet_text)
                media = []
                try:
                    for img in article.query_selector_all('img[src*="pbs.twimg.com/media"], img[src*="twimg.com/media"]'):
                        src = img.get_attribute("src")
                        if src and src not in media:
                            media.append(src)
                except Exception:
                    pass

                if tweet_id and tweet_text and tweet_id not in self.seen_ids:
                    tweet_url = href if href.startswith("http") else f"https://x.com{href}"
                    tweets.append({
                        "id": tweet_id,
                        "date": tweet_time,
                        "content": tweet_text,
                        "url": tweet_url,
                        "weblink": weblinks,
                        "media": media,
                        "comment_count": self._get_count(article, ['button[data-testid="reply"]']),
                        "retweets": self._get_count(article, ['button[data-testid="retweet"]']),
                        "likes": self._get_count(article, ['button[data-testid="like"]']),
                        "views": self._get_count(article, [
                            'a[href*="/analytics"]',
                            'a[aria-label*="views"]',
                            'a[aria-label*="Views"]'
                        ])
                    })
                    self.seen_ids.add(tweet_id)
            except Exception as ex:
                log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
                continue
        by_id = {tweet.get("id"): tweet for tweet in tweets if tweet.get("id")}
        for row in self._extract_tweets_from_dom(profile_page, username):
            tweet_id = row.get("id")
            if not tweet_id:
                continue
            if tweet_id in by_id:
                current = by_id[tweet_id]
                current_media = current.get("media") if isinstance(current.get("media"), list) else []
                for media_url in row.get("media") or []:
                    if media_url and media_url not in current_media:
                        current_media.append(media_url)
                current["media"] = current_media
                for key in ("content", "date", "url", "views"):
                    if not current.get(key) and row.get(key):
                        current[key] = row.get(key)
                continue
            if tweet_id in self.seen_ids:
                continue
            if not row.get("content") and not row.get("media"):
                continue
            tweets.append(row)
            by_id[tweet_id] = row
            self.seen_ids.add(tweet_id)
        log.g().i(f"Twitter parse extracted {len(tweets)} tweets from {len(tweet_articles)} articles for @{username}")
        return tweets

    def scroll_and_collect(self, profile_page: Page, username: str, existing_ids: set, desired_count: int, max_scrolls: int = 50) -> list:
        collected = []
        existing_ids = existing_ids or set()
        local_seen_ids = set()
        scrolls = 0
        empty_scrolls = 0
        empty_article_scrolls = 0
        while len(collected) < desired_count and scrolls < max_scrolls:
            prev_count = len(self._get_tweet_articles(profile_page))
            tweets = self.get_tweets_from_page(profile_page, username)
            new_found = False
            for tweet in tweets:
                tid = tweet.get("id")
                if tid is None:
                    continue
                if tid not in existing_ids and tid not in local_seen_ids:
                    collected.append(tweet)
                    local_seen_ids.add(tid)
                    new_found = True
                    if len(collected) >= desired_count:
                        break
            if new_found:
                empty_scrolls = 0
                empty_article_scrolls = 0
            else:
                empty_scrolls += 1
                if prev_count == 0 and not tweets:
                    empty_article_scrolls += 1
                else:
                    empty_article_scrolls = 0
                if empty_article_scrolls >= 5:
                    log.g().w(f"Twitter parse stopped after {empty_article_scrolls} zero-article scrolls for @{username}; collected={len(collected)} desired={desired_count}")
                    break
                if empty_scrolls >= 20:
                    log.g().w(f"Twitter parse stopped after {empty_scrolls} empty scrolls for @{username}; collected={len(collected)} desired={desired_count}")
                    break
            log.g().i(f"Twitter scroll {scrolls + 1}: articles={prev_count} page_tweets={len(tweets)} collected={len(collected)} desired={desired_count}")
            try:
                profile_page.mouse.wheel(0, 3000)
            except Exception:
                try:
                    profile_page.evaluate("window.scrollBy(0, 3000)")
                except Exception:
                    pass
            try:
                profile_page.wait_for_function(f"""() => document.querySelectorAll('article[data-tweet-id], article[data-testid="tweet"], article, div[data-testid="tweet"]').length > {prev_count}""", timeout=2000)
            except Exception:
                pass
            scrolls += 1
        if len(collected) < desired_count:
            log.g().w(f"Twitter parse collected fewer tweets than requested for @{username}: collected={len(collected)} desired={desired_count}")
        return collected
