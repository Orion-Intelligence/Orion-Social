import re
from playwright.sync_api import Page


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



    def get_tweets_from_page(self, profile_page: Page, username: str) -> list:
        tweets = []
        tweet_articles = profile_page.query_selector_all('article')
        pass

        for article in tweet_articles:
            try:
                anchor = article.query_selector('a[href*="/status/"]')
                tweet_id = None
                if anchor:
                    href = anchor.get_attribute("href")
                    tweet_id = href.split('/status/')[1].split('?')[0]

                divs = article.query_selector_all('div[data-testid="tweetText"]') or article.query_selector_all(
                    'div[lang]')
                tweet_text = " ".join([div.inner_text().strip() for div in divs if div])

                time_tag = article.query_selector('time')
                tweet_time = time_tag.get_attribute("datetime") if time_tag else ""

                weblinks = self.extract_weblinks(tweet_text)

                def get_count(element):
                    if not element:
                        return 0
                    span = element.query_selector('span[data-testid="app-text-transition-container"] span')
                    count_text = span.inner_text().strip() if span else '0'
                    if 'K' in count_text:
                        return int(float(count_text.replace('K', '')) * 1000)
                    elif 'M' in count_text:
                        return int(float(count_text.replace('M', '')) * 1000000)
                    return int(count_text or 0)

                if tweet_id and tweet_text and tweet_id not in self.seen_ids:
                    tweets.append({
                        "id": tweet_id,
                        "date": tweet_time,
                        "content": tweet_text,
                        "url": f"https://x.com/{username}/status/{tweet_id}",
                        "weblink": weblinks,
                        "comment_count": get_count(article.query_selector('button[data-testid="reply"]')),
                        "retweets": get_count(article.query_selector('button[data-testid="retweet"]')),
                        "likes": get_count(article.query_selector('button[data-testid="like"]')),
                        "views": get_count(article.query_selector('a[href*="analytics"]'))
                    })
                    self.seen_ids.add(tweet_id)
            except Exception as ex:
                log.g().e(f"SCRIPT ERROR {ex} " + str(self.__class__.__name__))
                continue
        return tweets

    def scroll_and_collect(self, profile_page: Page, username: str, existing_ids: set, desired_count: int, max_scrolls: int = 50) -> list:
        collected = []
        local_seen_ids = set()
        scrolls = 0
        empty_scrolls = 0
        while len(collected) < desired_count and scrolls < max_scrolls:
            prev_count = len(profile_page.query_selector_all("article"))
            profile_page.evaluate("window.scrollBy(0, 3000)")
            try:
                profile_page.wait_for_function(f"() => document.querySelectorAll('article').length > {prev_count}", timeout=1000)
            except Exception as _:
                pass
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
            else:
                empty_scrolls += 1
                if empty_scrolls >= 20:
                    break
            scrolls += 1
        return collected

