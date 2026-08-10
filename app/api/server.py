import asyncio
import concurrent.futures
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.orion.services.extension_manager.extension_connection_manager import extension_connection_manager
from api.orion.orion_controller import orion_controller
from api.orion.request_manager.queue_monitor import queue_monitor
from api.routes import SocialRoutes


class APIService:
    MAX_CONCURRENT_REQUESTS = 60

    def __init__(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT_REQUESTS)
        loop = asyncio.get_event_loop()
        loop.set_default_executor(executor)

        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["Authorization", "Content-Type"],
        )

        self.qmonitor = queue_monitor(self.MAX_CONCURRENT_REQUESTS)
        self.orion = orion_controller(self.qmonitor)

        routes = SocialRoutes(self.orion)
        self.app.include_router(routes.router)
        self.app.include_router(extension_connection_manager.get_instance().router)
        
        @self.app.on_event("startup")
        async def startup_event():
            import asyncio
            from api.orion.services.shared.hate_speech_classifier import hate_speech_classifier
            # Load the model in a background thread so it doesn't block FastAPI startup
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, hate_speech_classifier.load)
            
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

        loop.create_task(self.qmonitor.run())


api_service = APIService()
app = api_service.app
