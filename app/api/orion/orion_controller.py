import asyncio
from fastapi import HTTPException

from api.orion.request_manager.progress_controller import progress_controller
from api.social_manager.social_controller import social_controller


class orion_controller:
    def __init__(self, qmonitor):
        self.progress = progress_controller.get_instance()
        self.qmonitor = qmonitor

    async def _run_with_timeout(self, job_id, fn, *args, timeout=600):
        try:
            await asyncio.wait_for(asyncio.to_thread(fn, *args), timeout=timeout)
        except asyncio.TimeoutError:
            self.progress.error(job_id, "timeout")
        except Exception as exc:
            self.progress.error(job_id, str(exc))

    async def _run_job(self, job_id, command, data, timeout):
        async with self.qmonitor.track_job():
            controller = social_controller()
            await self._run_with_timeout(job_id, controller.invoke_trigger, command, data, timeout=timeout)

    async def social_trigger(self, job_id, command, data, timeout=600):
        try:
            state = self.progress.get(job_id)

            if state["status"] == "done":
                result = state.get("result") or {}
                return {"job_id": job_id, "result": result.get("data") if isinstance(result, dict) else result}

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
