import sys
import os
from playwright.sync_api import sync_playwright

app_dir = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)
sys.path.insert(0, app_dir)

from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.instagram import InstagramScraper


def run_instagram_scraper(username: str, max_followers: int = 40, max_following: int = 40, max_posts: int = 5):
    scraper = InstagramScraper(
        username=username,
        max_followers=max_followers,
        max_following=max_following
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # ---- login/session flow ----
        session = SessionManager(scraper.__class__.__name__)
        print(f">> Session file: {session.session_file}")
        print(f">> Session exists: {os.path.exists(session.session_file)}")

        loaded = session.load(page)

        if loaded:
            print(">> Session loaded successfully!")
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            session.apply_storage(page)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
        else:
            print(">> No session found. Login manually...")
            page.goto(scraper.base_url, wait_until="domcontentloaded")
            input("Press ENTER after login...")
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            session.save(page)
            print(">> Session saved successfully!")

        # ---- instagram scraping ----
        result = {
            "platform": "instagram",
            "username": username,
            "status": "active",
            "profile": {},
            "followers": [],
            "following": [],
            "posts": [],
            "total_posts": 0
        }

        try:
            print("\n>> Scraping profile...")
            result["profile"] = scraper.scrape_profile(page)
        except Exception as e:
            print(f"[ERROR] scrape_profile: {e}")

        try:
            print("\n>> Scraping followers...")
            result["followers"] = scraper.scrape_followers(page)
            print(f">> Followers collected: {len(result['followers'])}")
        except Exception as e:
            print(f"[ERROR] scrape_followers: {e}")

        try:
            print("\n>> Scraping following...")
            result["following"] = scraper.scrape_following(page)
            print(f">> Following collected: {len(result['following'])}")
        except Exception as e:
            print(f"[ERROR] scrape_following: {e}")

        try:
            print("\n>> Scraping posts...")
            result["posts"] = scraper.scrape_posts(page, max_posts=max_posts)
            result["total_posts"] = len(result["posts"])
            print(f">> Posts collected: {result['total_posts']}")
        except Exception as e:
            print(f"[ERROR] scrape_posts: {e}")

        browser.close()
        return result


def main():
    username = "dawn.today"   # change here
    max_followers = 40
    max_following = 40
    max_posts = 5

    print(f"\n{'='*60}")
    print("RUNNING INSTAGRAM SCRAPER")
    print(f"{'='*60}")
    print(f"Username: {username}")

    result = run_instagram_scraper(
        username=username,
        max_followers=max_followers,
        max_following=max_following,
        max_posts=max_posts
    )

    print(f"\n{'='*60}")
    print("SCRAPING COMPLETE - SUMMARY")
    print(f"{'='*60}")
    print(f"Platform : {result.get('platform')}")
    print(f"Username : {result.get('username')}")
    print(f"Status   : {result.get('status')}")

    print("\nPROFILE")
    for k, v in result.get("profile", {}).items():
        print(f"  {k}: {v}")

    print(f"\nFollowers ({len(result.get('followers', []))}):")
    print(result.get("followers", []))

    print(f"\nFollowing ({len(result.get('following', []))}):")
    print(result.get("following", []))

    print(f"\nPosts ({result.get('total_posts', 0)}):")
    for i, post in enumerate(result.get("posts", []), 1):
        print(f"\n  POST {i}")
        print(f"    URL      : {post.get('post_url', '')}")
        print(f"    Caption  : {post.get('caption', '')[:80]}")
        print(f"    Likes    : {post.get('likes', '')}")
        print(f"    Comments : {post.get('comments', '')}")
        print(f"    Datetime : {post.get('datetime', '')}")
        print(f"    Media    : {post.get('media_type', '')}")

if __name__ == "__main__":
    main()