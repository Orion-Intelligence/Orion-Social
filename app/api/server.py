import asyncio
import logging
import concurrent.futures
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from .model.social_request_model import SocialReconRequest
from .progress_controller import progress_controller
from .social_manager.social_controller import social_controller
from .social_manager.social_enums import SOCIAL_REQUEST_COMMANDS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class APIService:
    MAX_CONCURRENT_REQUESTS = 60

    def __init__(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT_REQUESTS)
        loop = asyncio.get_event_loop()
        loop.set_default_executor(executor)

        self.app = FastAPI()
        self.semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_REQUESTS)
        self.waiting_requests = 0
        self.active_requests = 0
        self.waiting_lock = asyncio.Lock()

        self.progress = progress_controller.get_instance()
        self.social_instance = social_controller()

        self.app.add_api_route("/social/recon", self.social_recon, methods=["POST"])

        loop.create_task(self.log_queue_size())

    @asynccontextmanager
    async def track_waiting(self, _: str):
        async with self.waiting_lock:
            self.waiting_requests += 1
        try:
            async with self.semaphore:
                async with self.waiting_lock:
                    self.waiting_requests -= 1
                    self.active_requests += 1
                yield
        finally:
            async with self.waiting_lock:
                self.active_requests -= 1

    async def log_queue_size(self):
        while True:
            await asyncio.sleep(5)

    async def _run_with_timeout(self, job_id: str, fn, *args, timeout: int = 600):
        try:
            await asyncio.wait_for(asyncio.to_thread(fn, *args), timeout=timeout)
        except asyncio.TimeoutError:
            self.progress.error(job_id, "timeout")
        except Exception as exc:
            self.progress.error(job_id, str(exc))

    async def social_recon(self, params: SocialReconRequest):
        try:
            mode = getattr(params, "mode", "default")
            job_id = str(hash(f"recon:{params.username}:{mode}"))

            state = self.progress.get(job_id)

            if state["status"] == "done":
                return {"job_id": job_id, "result": state.get("result")}

            if state["status"] == "pending":
                return {
                    "job_id": job_id,
                    "status": "pending",
                    "progress": state.get("progress", 0),
                    "step": state.get("step", "")
                }

            if state["status"] == "error":
                return {
                    "job_id": job_id,
                    "status": "error",
                    "message": state.get("error", "error")
                }

            self.progress.init(job_id)
            self.progress.update(job_id, 0, "queued")

            data = {"job_id": job_id, "username": params.username, "mode": mode}

            asyncio.create_task(
                self._run_with_timeout(
                    job_id,
                    self.social_instance.invoke_trigger,
                    SOCIAL_REQUEST_COMMANDS.S_RECON_USER,
                    data,
                    timeout=600
                )
            )

            return {"job_id": job_id, "status": "pending", "progress": 0, "step": "queued"}

        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail="Error running recon") from exc


api_service = APIService()
app = api_service.app
