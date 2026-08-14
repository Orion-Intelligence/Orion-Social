from typing import Any

from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.scrapers.live_search_handler import live_search_handler
from api.social_manager.social_recon.social_recon import social_recon
from api.social_manager.social_enums import SOCIAL_REQUEST_COMMANDS


class social_controller:
    def __init__(self) -> None:
        self._recon = social_recon()
        self._progress = progress_controller.get_instance()
        self._ddg = live_search_handler()
        self.job_id: str | None = None

    def init_job(self, job_id: str) -> None:
        self.job_id = job_id
        self._progress.init(job_id)
        self._progress.update(job_id, 0, "starting")

    @staticmethod
    def _clean_str(value: Any, default: str = "") -> str:
        if value is None:
            return default
        return str(value).strip()

    @staticmethod
    def _bytes_value(value: Any) -> bytes:
        if isinstance(value, bytes):
            return value
        if isinstance(value, bytearray):
            return bytes(value)
        return b""

    @staticmethod
    def _list_str_value(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]

    def invoke_trigger(self, command: int, data: Any = None) -> Any:
        data = data if isinstance(data, dict) else {}
        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_USER:
            self.init_job(self._clean_str(data.get("job_id")))
            try:
                username = self._clean_str(data.get("username"))
                mode = self._clean_str(data.get("mode"), "default")
                result = {"status": "success", "platform": "recon", "data": self._recon.parse(username, mode, job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_RECON_IMAGE:
            self.init_job(self._clean_str(data.get("job_id")))
            try:
                file_bytes = self._bytes_value(data.get("file_bytes"))
                filename = self._clean_str(data.get("filename"))
                if not file_bytes:
                    result = {"status": "error", "message": "image_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = {"status": "success", "platform": "recon_image", "data": self._recon.parse_image(file_bytes, filename=filename, job_id=self.job_id)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_USERNAMES:
            self.init_job(self._clean_str(data.get("job_id")))
            try:
                username = self._clean_str(data.get("username"))
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                platform = self._clean_str(data.get("platform"))
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.collect_social_handles(username, platform or None)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_IMAGES:
            self.init_job(self._clean_str(data.get("job_id")))
            try:
                username = self._clean_str(data.get("username"))
                platform = self._clean_str(data.get("platform"))
                max_images = max(1, min(int(data.get("max_images") or 10), 100))
                if not username:
                    result = {"status": "error", "message": "username_required", "data": None}
                    self._progress.done(self.job_id, result)
                    return result
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.scrape_images(username, platform, limit=max_images)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        if command == SOCIAL_REQUEST_COMMANDS.S_DDG_METADATA:
            self.init_job(self._clean_str(data.get("job_id")))
            try:
                tokens = self._list_str_value(data.get("tokens"))
                username = self._clean_str(data.get("username")) or None
                platform = self._clean_str(data.get("platform")) or None
                result = {"status": "success", "platform": "duckduckgo", "data": self._ddg.search_web(tokens, username, platform)}
                self._progress.done(self.job_id, result)
                return result
            except Exception as exc:
                self._progress.error(self.job_id, str(exc))
                raise

        return None
