import sys
import os
import json

app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, app_dir)

SESSION_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright
from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.instagram import InstagramScraper
from api.social_manager.scrapers.facebook import FacebookScraper
from api.social_manager.scrapers.behance_scraper import BehanceScraper
from api.social_manager.scrapers.vimeo import VimeoScraper

SESSION_FILE_MAP = {
    "InstagramScraper": "instagram_session.json.gz",
    "FacebookScraper": "FacebookScraper_session.json.gz",
}


def run_scraper(scraper, page):
    from playwright.sync_api import sync_playwright
    print(f"\n{'='*50}")
    print(f">> Running scraper: {scraper.__class__.__name__}")
    print(f"{'='*50}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        if getattr(scraper, "requires_login", False):
            session_filename = SESSION_FILE_MAP.get(
                scraper.__class__.__name__, 
                f"{scraper.__class__.__name__}_session.json.gz"
            )
            session_file = os.path.join(SESSION_DIR, session_filename)
            print(f">> Session file: {session_file}")
            print(f">> Session exists: {os.path.exists(session_file)}")
            session = SessionManager(session_file)
            loaded = session.load(page)
            if loaded:
                print(">> Session loaded successfully! Applying cookies...")
                page.goto(scraper.seed_url, wait_until="domcontentloaded")
                session.apply_storage(page)
                page.reload(wait_until="domcontentloaded")
                page.wait_for_timeout(3000)
            else:
                print(">> No session found. Navigating to login page...")
                page.goto(scraper.base_url, wait_until="domcontentloaded")
                print(">> Login required. Please log in manually, then press ENTER...")
                input()
                session.save(page)
                print(f">> Session saved to {session_file}")
                page.goto(scraper.seed_url, wait_until="domcontentloaded")
        else:
            print(">> No login required, navigating directly...")
            page.goto(scraper.seed_url, wait_until="domcontentloaded")
        result = scraper.parse_page(page)
        print(f"\n>> Results for {scraper.__class__.__name__}:")
        print(f"{'='*50}")
        if result:
            if isinstance(result, dict):
                username = result.get('m_username', 'N/A')
                real_name = result.get('m_real_name', 'N/A')
                followers = result.get('m_followers', [])
                following = result.get('m_following', [])
                mutual = result.get('m_mutual_usernames', [])
                print(f"   Username: {username}")
                print(f"   Real Name: {real_name}")
                print(f"   Total Followers Count: {result.get('m_total_followers', 'N/A')}")
                print(f"   Total Following Count: {result.get('m_total_following', 'N/A')}")
                if followers:
                    print(f"\n   Collected Followers ({len(followers)}):")
                    for i, f in enumerate(followers, 1):
                        print(f"      {i}. {f}")
                if following:
                    print(f"\n   Collected Following ({len(following)}):")
                    for i, f in enumerate(following, 1):
                        print(f"      {i}. {f}")
                if mutual:
                    print(f"\n   Mutual Connections ({len(mutual)}):")
                    for i, m in enumerate(mutual, 1):
                        print(f"      {i}. {m}")
        print(f"\n>> Finished: {scraper.__class__.__name__}")
        browser.close()
        return result


def main():
    scrapers = [
        InstagramScraper(username="nazarali870", max_followers=30, max_following=30),
        #FacebookScraper(username="100081288807680", max_followers=30, max_following=10),
        #BehanceScraper(username="grapheine",max_followers=30,max_following=30),
    ]

    if not scrapers:
        print("No scrapers configured. Edit main.py and add scrapers to the list.")
        return

    import asyncio

    async def run_all_parallel(scrapers):
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, run_scraper, scraper, None) for scraper in scrapers]
        results = await asyncio.gather(*tasks)
        return results

    all_results = asyncio.run(run_all_parallel(scrapers))

    print(f"\n{'='*50}")
    print(">> SCRAPING COMPLETE - SUMMARY")
    print(f"{'='*50}")
    print(f"   Total scrapers run: {len(all_results)}")
    for r in all_results:
        platform = r.get('m_platform', 'Unknown') if r else 'Unknown'
        data = r or {}
        if data:
            followers = data.get('m_followers') or []
            following = data.get('m_following') or []
            print(f"   - {platform}: {data.get('m_username', 'N/A')} ({len(followers)} followers, {len(following)} following)")


if __name__ == "__main__":
    main()
