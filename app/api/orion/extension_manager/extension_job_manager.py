from __future__ import annotations

import asyncio
import time
from typing import Any

from api.orion.extension_manager.extension_models import ExtensionJob, ExtensionProgress, ExtensionResult
from api.orion.request_manager.progress_controller import progress_controller


class extension_job_manager:
    __instance = None

    @staticmethod
    def get_instance():
        if extension_job_manager.__instance is None:
            extension_job_manager()
        return extension_job_manager.__instance

    def __init__(self):
        if extension_job_manager.__instance is not None:
            return
        self._progress = progress_controller.get_instance()
        self._lock = asyncio.Lock()
        self._jobs: dict[str, dict[str, Any]] = {}
        extension_job_manager.__instance = self

    async def create_job(self, job: ExtensionJob) -> asyncio.Future:
        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()
        async with self._lock:
            self._jobs[job.job_id] = {
                "job": job,
                "future": future,
                "status": "queued",
                "assigned_extension_id": None,
                "created_at": time.time(),
                "updated_at": time.time(),
            }
        self._progress.update(job.job_id, 5, "queued")
        return future

    async def mark_assigned(self, job_id: str, extension_id: str) -> None:
        async with self._lock:
            state = self._jobs.get(job_id)
            if state:
                state["status"] = "assigned"
                state["assigned_extension_id"] = extension_id
                state["updated_at"] = time.time()
        self._progress.update(job_id, 15, "extension_assigned")

    async def mark_waiting(self, job_id: str) -> None:
        async with self._lock:
            state = self._jobs.get(job_id)
            if state:
                state["status"] = "waiting"
                state["updated_at"] = time.time()
        self._progress.update(job_id, 10, "extension_waiting")

    async def progress(self, progress: ExtensionProgress) -> None:
        self._progress.update(progress.job_id, progress.progress, progress.step)
        async with self._lock:
            state = self._jobs.get(progress.job_id)
            if state:
                state["status"] = progress.status
                state["updated_at"] = time.time()

    async def complete(self, result: ExtensionResult) -> None:
        payload = self._result_payload(result)
        if result.success:
            self._progress.done(result.job_id, payload)
        else:
            self._progress.error(result.job_id, result.message or result.error or "extension_job_failed")

        async with self._lock:
            state = self._jobs.get(result.job_id)
            if not state:
                return
            state["status"] = "done" if result.success else "error"
            state["updated_at"] = time.time()
            future: asyncio.Future = state["future"]
            if not future.done():
                future.set_result(payload)

    async def fail(self, job_id: str, message: str) -> None:
        result = ExtensionResult(job_id=job_id, status="error", success=False, error=message)
        await self.complete(result)

    async def remove(self, job_id: str) -> None:
        async with self._lock:
            self._jobs.pop(job_id, None)

    async def get(self, job_id: str) -> dict[str, Any] | None:
        async with self._lock:
            state = self._jobs.get(job_id)
            if not state:
                return None
            return {key: value for key, value in state.items() if key != "future"}

    async def assigned_job(self, job_id: str, extension_id: str) -> ExtensionJob | None:
        async with self._lock:
            state = self._jobs.get(job_id)
            if not state or state.get("assigned_extension_id") != extension_id:
                return None
            return state["job"]

    async def is_assigned_to(self, job_id: str, extension_id: str) -> bool:
        async with self._lock:
            state = self._jobs.get(job_id)
            return bool(state and state.get("assigned_extension_id") == extension_id)

    @staticmethod
    def _result_payload(result: ExtensionResult) -> dict[str, Any]:
        return {
            "status": "success" if result.success else "error",
            "platform": "extension",
            "executor": "extension",
            "source": "browser_extension",
            "trusted": False,
            "untrusted": True,
            "validation_status": "sanitized" if result.success else "failed",
            "data": result.data,
            "error": result.error,
            "message": result.message or result.error,
            "error_code": result.error_code,
            "login_url": result.login_url,
            "error_platform": result.platform,
        }
