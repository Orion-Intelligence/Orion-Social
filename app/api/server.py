import asyncio
import concurrent.futures
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.orion.orion_controller import orion_controller
from api.orion.request_manager.queue_monitor import queue_monitor
from api.routes import SocialRoutes


class APIService:
    MAX_CONCURRENT_REQUESTS = 60

    def __init__(self):
        self.qmonitor = queue_monitor(self.MAX_CONCURRENT_REQUESTS)
        self.orion = orion_controller(self.qmonitor)

        self.app = FastAPI(lifespan=self.lifespan)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["Authorization", "Content-Type"],
        )

        routes = SocialRoutes(self.orion)
        self.app.include_router(routes.router)

        @self.app.get("/health")
        async def health_check():
            try:
                from api.orion.services.shared.hate_speech_classifier import hate_speech_classifier
                hate_speech_status = {
                    "initialized": getattr(hate_speech_classifier, "_initialized", False),
                    "model": getattr(hate_speech_classifier, "model_name", "unknown"),
                    "classifier_loaded": getattr(hate_speech_classifier, "classifier", None) is not None,
                    "hate_threshold": getattr(hate_speech_classifier, "hate_threshold", 0.5),
                    "offensive_threshold": getattr(hate_speech_classifier, "offensive_threshold", 0.5)
                }
            except Exception as e:
                hate_speech_status = {"status": "error", "message": str(e)}
                
            return {
                "status": "healthy",
                "hate_speech_classifier": hate_speech_status
            }

    @asynccontextmanager
    async def lifespan(self, _: FastAPI):
        from api.orion.services.shared.hate_speech_classifier import hate_speech_classifier

        model_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        running_loop = asyncio.get_running_loop()
        monitor_task = asyncio.create_task(self.qmonitor.run())
        model_future = running_loop.run_in_executor(model_executor, hate_speech_classifier.load)

        try:
            yield
        finally:
            monitor_task.cancel()
            model_future.cancel()
            await asyncio.gather(monitor_task, model_future, return_exceptions=True)
            model_executor.shutdown(wait=False, cancel_futures=True)


api_service = APIService()
app = api_service.app
