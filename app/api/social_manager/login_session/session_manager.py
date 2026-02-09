import os
import gzip
import json
from playwright.sync_api import Page


class SessionManager:

    def __init__(self, scraper_name: str):
        # Base directory = social_manager/
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        # sessions directory
        self.session_dir = os.path.join(base_dir, "sessions")
        os.makedirs(self.session_dir, exist_ok=True)

        # dynamic session filename
        filename = f"{scraper_name.lower()}_session.json.gz"
        self.session_file = os.path.join(self.session_dir, filename)

        self._pending_local = {}
        self._pending_session = {}

    def safe_get_storage(self, page: Page, storage_type: str):
        script = f"""
        () => {{
            try {{
                return Object.assign({{}}, window.{storage_type});
            }} catch (e) {{
                return null;
            }}
        }}
        """
        return page.evaluate(script)

    def save(self, page: Page) -> bool:
        try:
            state = {
                "cookies": page.context.cookies(),
                "local_storage": self.safe_get_storage(page, "localStorage"),
                "session_storage": self.safe_get_storage(page, "sessionStorage"),
            }

            with gzip.open(self.session_file, "wt", encoding="utf-8") as f:
                json.dump(state, f)

            return True
        except Exception:
            return False

    def load(self, page: Page) -> bool:
        if not os.path.exists(self.session_file):
            return False

        try:
            with gzip.open(self.session_file, "rt", encoding="utf-8") as f:
                state = json.load(f)

            if state.get("cookies"):
                page.context.add_cookies(state["cookies"])

            self._pending_local = state.get("local_storage", {}) or {}
            self._pending_session = state.get("session_storage", {}) or {}

            return True
        except Exception:
            return False

    def apply_storage(self, page: Page) -> bool:
        try:
            for k, v in self._pending_local.items():
                page.evaluate("([k, v]) => localStorage.setItem(k, v)", [k, v])

            for k, v in self._pending_session.items():
                page.evaluate("([k, v]) => sessionStorage.setItem(k, v)", [k, v])

            return True
        except Exception:
            return False
