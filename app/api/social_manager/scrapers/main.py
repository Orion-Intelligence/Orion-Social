import sys
import os
import asyncio
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
from api.social_manager.scrapers._duck_go_images import ImageScraper

from api.social_manager.scrapers.instagram import InstagramScraper
from api.social_manager.scrapers.facebook import FacebookScraper
from api.social_manager.scrapers.behance_scraper import BehanceScraper
from api.social_manager.scrapers.vimeo import VimeoScraper
from api.social_manager.scrapers._tiktok import TikTokScraper
from api.social_manager.scrapers._twitter import TwitterScraper
from api.social_manager.scrapers._duck_go import DuckDuckGoScraper




def run_scraper(scraper):

    print(f"\n{'='*50}")
    print(f">> Running scraper: {scraper.__class__.__name__}")
    print(f"{'='*50}")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        if getattr(scraper, "requires_login", False):

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

        else:
            page.goto(scraper.seed_url, wait_until="domcontentloaded")

        result = scraper.parse_page(page)

        browser.close()
        return result


def main():

    scrapers = [
        InstagramScraper(username="nazarali870", max_followers=10, max_following=10),
        #FacebookScraper(username="saqibali.jaspal", max_followers=30, max_following=10),
        # BehanceScraper(username="grapheine", max_followers=30, max_following=30),
        #tiktok(username="bilalshahid669"),
        #TwitterScraper(username="elonmusk", max_followers=10, max_following=10),
        #twitter(username="elonmusk"),
        #DuckDuckGoScraper("Usman Ali"),
        #ImageScraper(name="Elon Musk", limit=20)


    ]

    if not scrapers:
        print("No scrapers configured.")
        return

    async def run_all_parallel(scrapers):
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(None, run_scraper, scraper)
            for scraper in scrapers
        ]
        return await asyncio.gather(*tasks)

    all_results = asyncio.run(run_all_parallel(scrapers))

    print(f"\n{'='*50}")
    print(">> SCRAPING COMPLETE - SUMMARY")
    print(f"{'='*50}")
    print(f"Total scrapers run: {len(all_results)}")

    for result in all_results:
        if result:
            followers = result.get('m_followers') or []
            following = result.get('m_following') or []
            print(
                f"{result.get('m_platform', 'Unknown')}: "
                f"{result.get('m_username', 'N/A')} "
                f"({len(followers)} followers, {len(following)} following)"
            )


if __name__ == "__main__":
    main()
