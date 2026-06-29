import asyncio
from contextlib import asynccontextmanager


class queue_monitor:
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.waiting_requests = 0
        self.active_requests = 0
        self.lock = asyncio.Lock()

    @asynccontextmanager
    async def track_job(self):
        async with self.lock:
            self.waiting_requests += 1
        try:
            async with self.semaphore:
                async with self.lock:
                    self.waiting_requests -= 1
                    self.active_requests += 1
                yield
        finally:
            async with self.lock:
                self.active_requests -= 1

    async def run(self):
        while True:
            await asyncio.sleep(5)
            async with self.lock:
                waiting = self.waiting_requests
                active = self.active_requests
            available = self.max_concurrent - active
            print(f"[Queue Monitor] Waiting: {waiting}, In Use: {active}, Available: {available}", flush=True)
