import re
from playwright.sync_api import Page
from typing import List, Dict, Any
from datetime import datetime

from crawler.crawler_services.log_manager.log_controller import log
from crawler.crawler_services.shared.helper_method import helper_method


class RedditHelperMethod:

    @staticmethod
    def extract_subreddit_name(url: str) -> str:
        match = re.search(r"reddit\.com/r/([A-Za-z0-9_]+)", url)
        if match:
            return match.group(1)
        raise ValueError(f"Invalid Reddit URL: {url}")

    @staticmethod
    def extract_weblinks(text: str) -> List[str]:
        return re.findall(r'(https?://[^\s]+)', text)

    @staticmethod
    def get_subreddit_metadata(page: Page, subreddit_name: str) -> Dict[str, Any]:
        metadata = {
            'name': subreddit_name,
            'bio': '',
            'created_date': '',
            'visibility': 'public',
            'members': 0
        }
        try:
            title_el = page.query_selector('div#title.i18n-subreddit-title')
            desc_el = page.query_selector('div#description.i18n-subreddit-description')
            if title_el and desc_el:
                metadata['bio'] = f"{title_el.inner_text().strip()}: {desc_el.inner_text().strip()}"
            elif title_el:
                metadata['bio'] = title_el.inner_text().strip()
            elif desc_el:
                metadata['bio'] = desc_el.inner_text().strip()

            created_time = page.query_selector('faceplate-timeago > time')
            if created_time:
                metadata['created_date'] = created_time.get_attribute("datetime")

            visibility_el = page.query_selector('svg[icon-name="world-outline"] + *')
            if visibility_el:
                metadata['visibility'] = visibility_el.inner_text().strip()

            member_el = page.query_selector('strong#subscribers')
            if member_el:
                text = member_el.inner_text().strip()
                num_match = re.search(r'([\d.,]+)([km]?)', text.lower())
                if num_match:
                    num = float(num_match.group(1).replace(',', ''))
                    mult = num_match.group(2)
                    if mult == 'k':
                        num *= 1_000
                    elif mult == 'm':
                        num *= 1_000_000
                    metadata['members'] = int(num)
        except Exception as ex:
            log.g().e(f"SCRIPT ERROR {ex}")
        return metadata

    @staticmethod
    def get_posts_from_page(page: Page, _: str) -> List[Dict[str, Any]]:
        posts = []
        seen_ids = set()
        post_containers = page.query_selector_all('shreddit-post, article, div.grid')
        for container in post_containers:
            try:
                username = ""
                try:
                    username = container.get_attribute("author") or ""
                    username_el = container.query_selector('span.whitespace-nowrap, a[href*="/user/"], a[href*="/u/"]')
                    if username_el:
                        username = (username or username_el.inner_text().strip()).replace("u/", "")
                except Exception:
                    pass

                timestamp = ""
                try:
                    time_el = container.query_selector('faceplate-timeago time[datetime], time[datetime]')
                    if time_el:
                        timestamp = time_el.get_attribute("datetime")
                except Exception:
                    pass

                title = ""
                post_id = None
                post_url = ""
                try:
                    title_el = container.query_selector('a[id^="post-title-"], a[slot="title"], h3 a')
                    if title_el:
                        title = title_el.inner_text().strip()
                        post_url = title_el.get_attribute('href')
                        if post_url and post_url.startswith('/'):
                            post_url = "https://old.reddit.com" + post_url
                        id_match = re.search(r'post-title-(t3_[a-zA-Z0-9]+)', title_el.get_attribute('id') or '')
                        if id_match:
                            post_id = id_match.group(1)
                    post_id = post_id or container.get_attribute("thingid") or container.get_attribute("id")
                    post_url = post_url or container.get_attribute("permalink") or ""
                    if post_url and post_url.startswith('/'):
                        post_url = "https://old.reddit.com" + post_url
                except Exception:
                    pass

                if not post_id or post_id in seen_ids:
                    continue
                seen_ids.add(post_id)

                weblinks = []
                try:
                    website_links = container.query_selector_all('a.post-link')
                    for ext_link in website_links:
                        ext_href = ext_link.get_attribute('href')
                        if ext_href and ext_href.startswith('http') and ext_href not in weblinks:
                            weblinks.append(ext_href)
                except Exception:
                    pass

                content = ""
                try:
                    content_el = container.query_selector('div[slot="text-body"], div[data-click-id="text"]')
                    if content_el:
                        content = content_el.inner_text().strip()
                except Exception:
                    pass

                media = []
                try:
                    for img in container.query_selector_all('img'):
                        src = img.get_attribute("src")
                        if src and src.startswith("http") and src not in media:
                            media.append(src)
                except Exception:
                    pass

                score = ""
                try:
                    score_el = container.query_selector('[id^="score-"], faceplate-number, shreddit-post')
                    if score_el:
                        score = score_el.get_attribute("score") or score_el.inner_text().strip()
                except Exception:
                    pass

                comment_count = ""
                try:
                    count_el = container.query_selector('a[href*="/comments/"] faceplate-number, [id^="comment-count"]')
                    if count_el:
                        comment_count = count_el.get_attribute("number") or count_el.inner_text().strip()
                except Exception:
                    pass

                posts.append({
                    'id': post_id,
                    'url': post_url,
                    'title': title,
                    'username': username,
                    'content': content,
                    'timestamp': timestamp,
                    'weblinks': weblinks,
                    'media': media,
                    'score': score,
                    'comment_count': comment_count,
                })
            except Exception:
                continue

        return posts

    @staticmethod
    def get_comments_from_post(page: Page, post_url: str, max_comments: int = 5, comment_offset: int = 0) -> List[Dict[str, Any]]:
        comments = []
        seen = set()
        max_comments = max(1, min(int(max_comments or 5), 10))
        comment_offset = max(0, int(comment_offset or 0))
        target_count = comment_offset + max_comments
        try:
            page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
            idle_scrolls = 0
            for _ in range(30):
                comment_elements = page.query_selector_all('shreddit-comment')
                before_count = len(comments)
                for comment in comment_elements:
                    if len(comments) >= target_count:
                        return comments[comment_offset:target_count]
                    try:
                        comment_data = {}

                        timestamp_el = comment.query_selector('time[datetime]')
                        content_el = comment.query_selector('div[id*="comment"] p, p')
                        author = comment.get_attribute("author") or ""
                        likes = comment.get_attribute("score") or ""
                        if not author:
                            author_el = comment.query_selector('a[href*="/user/"], a[href*="/u/"]')
                            if author_el:
                                author = author_el.inner_text().strip().replace("u/", "")

                        if author:
                            comment_data['username'] = author
                        if likes:
                            comment_data['likes'] = likes
                        if timestamp_el:
                            comment_data['timestamp'] = timestamp_el.get_attribute('datetime')
                        if content_el:
                            comment_data['content'] = helper_method.filter_comments(content_el.inner_text().strip())

                        key = "|".join([
                            comment_data.get("username", ""),
                            comment_data.get("timestamp", ""),
                            comment_data.get("content", ""),
                        ])
                        if comment_data.get('content') and key not in seen:
                            seen.add(key)
                            comments.append(comment_data)
                    except Exception:
                        continue
                idle_scrolls = idle_scrolls + 1 if len(comments) == before_count else 0
                if len(comments) >= target_count or idle_scrolls >= 5:
                    break
                try:
                    page.evaluate("""() => {
                        for (const button of document.querySelectorAll('button')) {
                            const text = (button.innerText || '').toLowerCase();
                            if (text.includes('more comments') || text.includes('view more') || text.includes('load more')) {
                                try { button.click(); } catch (e) {}
                            }
                        }
                        window.scrollBy(0, 4000);
                    }""")
                    page.wait_for_timeout(750)
                except Exception:
                    break

        except Exception:
            pass

        return comments[comment_offset:target_count]

    @staticmethod
    def scroll_and_collect_posts(page: Page, subreddit_name: str, desired_count: int, max_scrolls: int = 100, filter_date: datetime = None) -> List[Dict[str, Any]]:
        collected: List[Dict[str, Any]] = []
        seen_ids = set()
        scrolls = 0

        while len(collected) < desired_count and scrolls < max_scrolls:
            posts = RedditHelperMethod.get_posts_from_page(page, subreddit_name)
            if not posts:
                return []
            new_found = False

            for post in posts:
                if filter_date and post.get('timestamp'):
                    try:
                        post_time = datetime.fromisoformat(post['timestamp'].replace('Z', '+00:00'))
                    except Exception:
                        post_time = None
                    if post_time and post_time < filter_date:
                        return collected

                if post['id'] not in seen_ids:
                    collected.append(post)
                    seen_ids.add(post['id'])
                    new_found = True
                    if len(collected) >= desired_count:
                        break

            try:
                page.evaluate("window.scrollBy(0, 12000)")
            except Exception as ex:
                log.g().e(f"SCRIPT ERROR {ex} ")
                try:
                    page.evaluate("window.scrollBy(0, 12000)")
                except Exception as ex:
                    log.g().e(f"SCRIPT ERROR {ex} ")

            try:
                page.wait_for_function(
                    "prev => document.querySelectorAll('a[id^=\"post-title-\"]').length > prev",
                    timeout=6000
                )
            except Exception:
                try:
                    page.wait_for_load_state("domcontentloaded", timeout=2000)
                except Exception as ex:
                    log.g().e(f"SCRIPT ERROR {ex} ")

            if not new_found and scrolls >= max_scrolls:
                break

            scrolls += 1

        return collected
