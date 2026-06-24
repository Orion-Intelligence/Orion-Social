from abc import ABC, abstractmethod
from typing import List
from crawler.crawler_instance.local_interface_model.leak.model.leak_data_model import leak_data_model
from crawler.crawler_instance.local_shared_model.data_model.social_model import social_model
from crawler.crawler_services.redis_manager.redis_enums import CUSTOM_SCRIPT_REDIS_KEYS


class telegram_extractor_interface(ABC):
    def __init__(self):
        self.phone_number = None

    @abstractmethod
    def parse_leak_data(self) -> leak_data_model:
        """Parse leak data from the given Playwright page and return a leak_data_model."""
        pass

    @property
    @abstractmethod
    def card_data(self) -> List[social_model]:
        """Return the list of parsed leak models (card data)."""
        pass

    @abstractmethod
    def invoke_db(self, command: int, key: CUSTOM_SCRIPT_REDIS_KEYS, value):
        """Interact with Redis using the given command, key, and value."""
        pass

    @abstractmethod
    def append_leak_data(self, leak: social_model):
        """Append a single leak_model instance to the collected card data."""
        pass

    async def init_callback(self, callback):
        """pass callback model triggered on leak parsed"""
        pass

    async def check_phone_number(self, phone_number):
        pass
