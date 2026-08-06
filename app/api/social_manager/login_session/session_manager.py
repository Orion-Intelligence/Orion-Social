import os
import gzip
import json
import traceback
from playwright.sync_api import Page


class SessionManager:
    @staticmethod
    def _log_exception(context: str, exc: Exception) -> None:
        print(f"[SessionManager] {context}: {exc}", flush=True)
        traceback.print_exc()

    def __init__(self, scraper_name: str):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.session_dir = os.getenv("ORION_SESSION_ROOT") or os.path.join(base_dir, "sessions")
        os.makedirs(self.session_dir, exist_ok=True)

        s = str(scraper_name)
        filename = os.path.basename(s)
        if not filename.lower().endswith("_session.json.gz"):
            filename = f"{filename.lower()}_session.json.gz"
        self.session_file = os.path.join(self.session_dir, filename.lower())

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
        except Exception as exc:
            self._log_exception(f"save session_file={self.session_file!r}", exc)
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
        except Exception as exc:
            self._log_exception(f"load session_file={self.session_file!r}", exc)
            return False

    def apply_storage(self, page: Page) -> bool:
        try:
            for k, v in self._pending_local.items():
                page.evaluate("([k, v]) => localStorage.setItem(k, v)", [k, v])

            for k, v in self._pending_session.items():
                page.evaluate("([k, v]) => sessionStorage.setItem(k, v)", [k, v])

            return True
        except Exception as exc:
            self._log_exception("apply_storage", exc)
            return False
