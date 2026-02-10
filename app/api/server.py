import asyncio
import logging
import concurrent.futures
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from .model.social_request_model import (
    SocialReconRequest,
    SocialScrapeRequest,
    SocialProfileRequest,
    SocialFollowersRequest,
    SocialFollowingRequest, SocialPostsRequest
)
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
        self.social_controller_instance = social_controller()

        self.app.add_api_route("/social/recon", self.social_recon, methods=["POST"])
        self.app.add_api_route("/social/scrape", self.social_scrape, methods=["POST"])
        self.app.add_api_route("/social/profile", self.social_profile, methods=["POST"])
        self.app.add_api_route("/social/followers", self.social_followers, methods=["POST"])
        self.app.add_api_route("/social/following", self.social_following, methods=["POST"])
        self.app.add_api_route("/social/posts", self.social_posts, methods=["POST"])

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
            job_id = str(hash(f"recon:{params.query}:{mode}"))

            state = self.progress.get(job_id)

            if state["status"] == "done":
                return {"job_id": job_id, "result": state.get("result").get("data")}

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

            data = {"job_id": job_id, "username": params.query, "mode": mode}

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


    async def social_scrape(self, request: SocialScrapeRequest):
        logger.info("Received request at /social/scrape")

        targets = [
            {
                "platform": t.platform,
                "usernames": t.usernames,
                "max_followers": t.max_followers,
                "max_following": t.max_following
            }
            for t in request.targets
        ]

        if not targets:
            raise HTTPException(status_code=400, detail="Targets are required")

        scrape_key = str(hash(str(targets)))
        state = self.social_controller_instance.get_scrape_status(scrape_key)

        if state["status"] == "done":
            return state["data"]

        if state["status"] == "pending":
            return {
                "status": "pending",
                "progress": state.get("progress", 0),
                "step": state.get("step", "")
            }

        data = {
            "scrape_key": scrape_key,
            "targets": targets,
            "compare_results": True,
            "similarity_threshold": 70
        }

        async def run():
            await asyncio.to_thread(
                self.social_controller_instance.invoke_trigger,
                SOCIAL_REQUEST_COMMANDS.S_SCRAPE_MULTIPLE,
                data
            )

        asyncio.create_task(run())

        return {
            "status": "pending",
            "progress": 0,
            "step": "queued"
        }

    async def social_profile(self, request: SocialProfileRequest):
        logger.info("Received request at /social/profile")

        scrape_key = str(hash(f"profile:{request.platform}:{request.username}"))
        state = self.social_controller_instance.get_scrape_status(scrape_key)

        if state["status"] == "done":
            return state["data"]

        if state["status"] == "pending":
            return {
                "status": "pending",
                "progress": state.get("progress", 0),
                "step": state.get("step", "")
            }

        async def run():
            await asyncio.to_thread(
                self.social_controller_instance.scrape_profile,
                scrape_key,
                request.platform,
                request.username
            )

        asyncio.create_task(run())

        return {
            "status": "pending",
            "progress": 0,
            "step": "queued"
        }

    async def social_followers(self, request: SocialFollowersRequest):
        logger.info("Received request at /social/followers")

        scrape_key = str(hash(f"followers:{request.platform}:{request.username}:{request.max_followers}"))
        state = self.social_controller_instance.get_scrape_status(scrape_key)

        if state["status"] == "done":
            return state["data"]

        if state["status"] == "pending":
            return {
                "status": "pending",
                "progress": state.get("progress", 0),
                "step": state.get("step", "")
            }

        async def run():
            await asyncio.to_thread(
                self.social_controller_instance.scrape_followers,
                scrape_key,
                request.platform,
                request.username,
                request.max_followers
            )

        asyncio.create_task(run())

        return {
            "status": "pending",
            "progress": 0,
            "step": "queued"
        }

    async def social_following(self, request: SocialFollowingRequest):
        logger.info("Received request at /social/following")

        scrape_key = str(hash(f"following:{request.platform}:{request.username}:{request.max_following}"))
        state = self.social_controller_instance.get_scrape_status(scrape_key)

        if state["status"] == "done":
            return state["data"]

        if state["status"] == "pending":
            return {
                "status": "pending",
                "progress": state.get("progress", 0),
                "step": state.get("step", "")
            }

        async def run():
            await asyncio.to_thread(
                self.social_controller_instance.scrape_following,
                scrape_key,
                request.platform,
                request.username,
                request.max_following
            )

        asyncio.create_task(run())

        return {
            "status": "pending",
            "progress": 0,
            "step": "queued"
        }

    async def social_posts(self, request: SocialPostsRequest):
        logger.info("Received request at /social/posts")

        scrape_key = str(hash(f"posts:{request.platform}:{request.username}:{request.max_posts}"))
        state = self.social_controller_instance.get_scrape_status(scrape_key)

        if state["status"] == "done":
            return state["data"]

        if state["status"] == "pending":
            return {
                "status": "pending",
                "progress": state.get("progress", 0),
                "step": state.get("step", "")
            }

        async def run():
            await asyncio.to_thread(
                self.social_controller_instance.scrape_posts,
                scrape_key,
                request.platform,
                request.username,
                request.max_posts
            )

        asyncio.create_task(run())

        return {
            "status": "pending",
            "progress": 0,
            "step": "queued"
        }


api_service = APIService()
app = api_service.app
