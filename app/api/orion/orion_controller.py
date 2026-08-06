import asyncio
from fastapi import HTTPException

from api.orion.services.extension_manager.extension_executor import extension_executor
from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.social_controller import social_controller


class orion_controller:
    def __init__(self, qmonitor):
        self.progress = progress_controller.get_instance()
        self.qmonitor = qmonitor
        self.extension_executor = extension_executor.get_instance()

    async def _run_with_timeout(self, job_id, fn, *args, timeout=600):
        try:
            await asyncio.wait_for(asyncio.to_thread(fn, *args), timeout=timeout)
        except asyncio.TimeoutError:
            self.progress.error(job_id, "timeout")
        except Exception as exc:
            self.progress.error(job_id, str(exc))

    async def _run_job(self, job_id, command, data, timeout):
        async with self.qmonitor.track_job():
            if data.get("use_extension"):
                extension_result = await self.extension_executor.dispatch_and_wait(command, data, timeout=timeout)
                if extension_result is not None:
                    return
                self.progress.error(job_id, "extension_unavailable")
                return
            controller = social_controller()
            await self._run_with_timeout(job_id, controller.invoke_trigger, command, data, timeout=timeout)

    async def social_trigger(self, job_id, command, data, timeout=600):
        try:
            state = self.progress.get(job_id)

            if state["status"] == "done":
                result = state.get("result") or {}
                if isinstance(result, dict) and "data" in result and result.get("status") != "error":
                    result = result.get("data")
                return {"job_id": job_id, "result": result}

            if state["status"] == "pending":
                return {"job_id": job_id, "status": "pending", "progress": state.get("progress", 5), "step": state.get("step", "")}

            if state["status"] == "error":
                return {"job_id": job_id, "status": "error", "message": state.get("error", "error")}

            self.progress.init(job_id)
            self.progress.update(job_id, 0, "queued")

            asyncio.create_task(self._run_job(job_id, command, data, timeout))
            return {"job_id": job_id, "status": "pending", "progress": 5, "step": "queued"}

        except HTTPException:
            self.progress.error(job_id, "timeout")
            raise
        except Exception as exc:
            self.progress.error(job_id, "timeout")
            raise HTTPException(status_code=500, detail="Error running job") from exc
