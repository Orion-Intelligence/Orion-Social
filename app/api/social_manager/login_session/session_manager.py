import os
import gzip
import json
from playwright.sync_api import Page


class SessionManager:

    def __init__(self, session_file: str = "session_data.json.gz"):
        self.session_file = session_file
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
                f.write(json.dumps(state))

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

            self._pending_local = state.get("local_storage", {})
            self._pending_session = state.get("session_storage", {})

            return True
        except Exception:
            return False

    def apply_storage(self, page: Page) -> bool:
        try:
            for k, v in self._pending_local.items():
                page.evaluate(f"() => localStorage.setItem('{k}', '{v}')")

            for k, v in self._pending_session.items():
                page.evaluate(f"() => sessionStorage.setItem('{k}', '{v}')")

            return True
        except Exception:
            return False
