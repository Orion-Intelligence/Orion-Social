import re
from urllib.parse import urljoin
from playwright.sync_api import Page

class MastodonHelperMethods:
    def __init__(self):
        self.seen_ids = set()

    @staticmethod
    def get_profile_info(page: Page) -> dict:
        info = {}
        try:
            username_elem = page.query_selector('.account__header__tabs__name h1 small span')
            username = username_elem.inner_text().strip() if username_elem else ""
            info = {
                "username": username
            }
        except Exception:
            pass
        return info

    @staticmethod
    def extract_weblinks(text: str) -> list:
        url_pattern = r'(https?://[^\s]+)'
        return re.findall(url_pattern, text)

    def get_posts_from_page(self, page: Page, username: str) -> list:
        posts = []
        articles = page.query_selector_all('article[data-id]')
        for article in articles:
            try:
                post_id = article.get_attribute("data-id")
                if not post_id or post_id in {"pinned-view-all"}:
                    continue
                if not article.query_selector('a.status__relative-time time, a.status__relative-time'):
                    continue
                media_elems = article.query_selector_all('.media-gallery__item-thumbnail img')
                media = []
                for m in media_elems:
                    src = m.get_attribute("src")
                    if src:
                        media.append(src)
                if post_id not in self.seen_ids:
                    posts.append(post_id)
                    self.seen_ids.add(post_id)
            except Exception:
                continue
        return posts

    @staticmethod
    def extract_post_details(page: Page, post_id: str, seed_url: str):
        article = page.query_selector(f'article[data-id="{post_id}"]')
        if not article:
            return {}

        date_elem = article.query_selector('a.status__relative-time time, time')
        date_str = date_elem.get_attribute("datetime") if date_elem else ""

        wrapper = article.query_selector("div.status__wrapper")
        data_boosted_by = wrapper.get_attribute("data-boosted_by") if wrapper else ""

        username_elem = article.query_selector(".display-name__account")
        username = username_elem.inner_text().strip() if username_elem else ""

        content_elem = article.query_selector("div.status__content__text, div.status__content")
        content = content_elem.inner_text().strip() if content_elem else ""

        url_elem = article.query_selector("a.status__relative-time")
        url = urljoin(seed_url, url_elem.get_attribute("href") if url_elem else "")

        media_elems = article.query_selector_all('.media-gallery__item-thumbnail img')
        media = [m.get_attribute("src") for m in media_elems if m.get_attribute("src")]

        card_title_elem = article.query_selector(".status-card__title")
        card_title = card_title_elem.inner_text().strip() if card_title_elem else ""

        boosts = None
        favourites = None
        comments = []

        result = {
            "id": post_id,
            "boosted_by": data_boosted_by,
            "username": username,
            "content": content,
            "date": date_str,
            "url": url,
            "media": media,
            "card_title": card_title
        }
        if boosts is not None:
            result["boosts"] = boosts
        if favourites is not None:
            result["favourites"] = favourites
        if comments:
            result["comments"] = comments

        return result

    def scroll_and_collect(self, page: Page, username: str, existing_ids: set, desired_count: int, max_scrolls: int = 1050) -> list:
        collected = []
        local_seen_ids = set()
        scrolls = 0
        while len(collected) < desired_count and scrolls < max_scrolls:
            try:
                page.wait_for_selector('article[data-id]', timeout=10000)
            except Exception:
                break
            posts = self.get_posts_from_page(page, username)
            new_found = False
            for post in posts:
                if post not in existing_ids and post not in local_seen_ids:
                    collected.append(post)
                    local_seen_ids.add(post)
                    new_found = True
                    if len(collected) >= desired_count:
                        break
            if not new_found and scrolls > 5:
                break
            scrolls += 1
            page.evaluate("""() => {
                const items = document.querySelectorAll('article[data-id]');
                if (items.length) items[items.length - 1].scrollIntoView();
            }""")
        return collected[:desired_count]
