import time
import threading
from typing import Dict, Any


class progress_controller:
    __instance = None

    @staticmethod
    def get_instance():
        if progress_controller.__instance is None:
            progress_controller()
        return progress_controller.__instance

    def __init__(self):
        if progress_controller.__instance is not None:
            return

        self._lock = threading.Lock()
        self._store: Dict[str, Dict[str, Any]] = {}

        progress_controller.__instance = self

    def init(self, job_id: str, ttl: int = 3600):
        with self._lock:
            if job_id in self._store:
                return
            self._store[job_id] = {
                "status": "pending",
                "progress": 5,
                "step": "starting",
                "expires_at": time.time() + ttl
            }

    def update(self, job_id: str, progress: int, step: str):
        if progress<5:
            progress = 5
        with self._lock:
            st = self._store.get(job_id)
            if not st:
                return
            st["status"] = "pending"
            if step == "queued":
                progress = 5
            st["progress"] = int(max(5, min(100, progress)))
            st["step"] = step

    def done(self, job_id: str, result: Any):
        with self._lock:
            st = self._store.get(job_id)
            if not st:
                return
            st["status"] = "done"
            st["progress"] = 100
            st["step"] = "complete"
            st["result"] = result
            st["expires_at"] = time.time() + 300

    def error(self, job_id: str, message: str):
        with self._lock:
            st = self._store.get(job_id)
            if not st:
                return
            st["status"] = "error"
            st["step"] = "error"
            st["error"] = message
            st["expires_at"] = time.time() + 300

    def get(self, job_id: str) -> Dict[str, Any]:
        self.cleanup()
        with self._lock:
            return self._store.get(job_id, {"status": "new"})

    def cleanup(self):
        now = time.time()
        with self._lock:
            expired = [k for k, v in self._store.items() if (v.get("expires_at") or 0) < now]
            for k in expired:
                self._store.pop(k, None)
