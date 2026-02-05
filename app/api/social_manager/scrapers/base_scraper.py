from abc import ABC, abstractmethod
from typing import Dict, Any
from playwright.sync_api import Page


class BaseScraper(ABC):

    requires_login: bool = False

    def __init__(self):
        self.data = []

    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    @property
    @abstractmethod
    def seed_url(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def parse_page(self, page: Page) -> Dict[str, Any]:
        pass
