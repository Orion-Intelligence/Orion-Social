import asyncio
import concurrent.futures
from fastapi import FastAPI

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

        self.qmonitor = queue_monitor(self.MAX_CONCURRENT_REQUESTS)
        self.orion = orion_controller(self.qmonitor)

        routes = SocialRoutes(self.orion)
        self.app.include_router(routes.router)

        loop.create_task(self.qmonitor.run())


api_service = APIService()
app = api_service.app
