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

SESSION_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from api.social_manager.login_session.session_manager import SessionManager
from api.social_manager.scrapers.instagram import InstagramScraper
from api.social_manager.scrapers.facebook import FacebookScraper
from api.social_manager.scrapers.behance_scraper import BehanceScraper
from api.social_manager.scrapers.vimeo import VimeoScraper
from api.social_manager.scrapers._twitter import twitter
from api.social_manager.scrapers._tiktok import tiktok


SESSION_FILE_MAP = {
    "InstagramScraper": "instagram_session.json.gz",
    "FacebookScraper": "FacebookScraper_session.json.gz",
    "twitter": "twitter_session.json.gz",


}


def run_scraper(scraper):
    print(f"\n{'='*60}")
    print(f">> Running scraper: {scraper.__class__.__name__}")
    print(f"{'='*60}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        if getattr(scraper, "requires_login", False):

            session_filename = SESSION_FILE_MAP.get(
                scraper.__class__.__name__,
                f"{scraper.__class__.__name__}_session.json.gz"
            )

            session_file = os.path.join(SESSION_DIR, session_filename)
            print(f">> Using session file: {session_file}")

            session = SessionManager(session_file)
            loaded = session.load(page)

            if loaded:
                print(">> Session loaded successfully.")
                session.apply_storage(page)
            else:
                print(">> No session found.")
                page.goto(scraper.base_url, wait_until="domcontentloaded")
                input("Login manually, then press ENTER...")
                session.save(page)
                print(">> Session saved.")

        scraper.parse_page(page)

        browser.close()
        print(f">> Finished: {scraper.__class__.__name__}")


def main():
    scrapers = [
        # InstagramScraper(username="nazarali870", max_followers=30, max_following=30),
        FacebookScraper(username="saqibali.jaspal"),
        # BehanceScraper(username="grapheine", max_followers=30, max_following=30),
        # twitter("elonmusk"),
        # tiktok("jackyanimations_"),
        # VimeoScraper(username="example")
    ]

    if not scrapers:
        print("No scrapers configured.")
        return

    for scraper in scrapers:
        run_scraper(scraper)

    print(f"\n{'='*60}")
    print("SCRAPING COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
