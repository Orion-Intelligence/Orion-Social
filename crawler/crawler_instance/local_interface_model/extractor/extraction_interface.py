from abc import ABC, abstractmethod
from typing import Callable, Dict, List

from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_interface_model.extractor.model.leak_data_model import leak_data_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel
from crawler.crawler_services.redis_manager.redis_enums import REDIS_COMMANDS, REDIS_CONNECTIONS


class extraction_interface(ABC):
    def __init__(self):
        self.callback: Callable[[], bool | None] | None = None
        self._card_data: List = []
        self._entity_data: List[entity_model] = []
        self._latest_data_points: Dict[str, str] = {}

    @abstractmethod
    def parse_leak_data(self, page) -> leak_data_model:
        """Parse data from the given page and return the extracted data model."""
        pass

    @property
    @abstractmethod
    def is_crawled(self) -> bool:
        """Return if script has been crawled."""
        pass

    @property
    def latest_data_points(self) -> Dict[str, str]:
        """Return latest data point values collected during parsing."""
        if not hasattr(self, "_latest_data_points"):
            self._latest_data_points = {}
        return self._latest_data_points

    def _latest_data_point_key(self, key: str) -> str:
        scope = getattr(self, "m_latest_data_point_scope", None) or getattr(self, "m_seed_url", "")
        scope = "".join(ch.lower() if ch.isalnum() else "_" for ch in str(scope)).strip("_")
        scoped_key = f"{scope}_{key}" if scope else key
        return f"_script_latest_datapoints_{REDIS_CONNECTIONS._redis_key_version}_{scoped_key}"

    def _has_latest_data_point(self, key: str) -> bool:
        return bool(self.invoke_db(REDIS_COMMANDS.S_GET_STRING, self._latest_data_point_key(key), "", None))

    def _is_requested_hash_id(self, card) -> bool:
        requested_hash_id = str(getattr(self, "m_hash_id", "") or "").strip()
        return bool(requested_hash_id and getattr(card, "m_hash_id", None) == requested_hash_id)

    def _is_latest_data_point(self, key: str, value: str) -> bool:
        """Return if the given value matches the stored latest data point."""
        if not value:
            return False
        stored_value = self.invoke_db(REDIS_COMMANDS.S_GET_STRING, self._latest_data_point_key(key), "", None)
        if self.is_crawled and stored_value == value:
            return True
        self.latest_data_points.setdefault(key, value)
        return False

    def _set_latest_data_point(self):
        """Persist collected latest data points."""
        for key, value in self.latest_data_points.items():
            if value:
                self.invoke_db(REDIS_COMMANDS.S_SET_STRING, self._latest_data_point_key(key), value, None)

    @property
    @abstractmethod
    def seed_url(self) -> str:
        """Return the seed URL to start crawling from."""
        pass

    @property
    @abstractmethod
    def developer_signature(self) -> str:
        """Return developer signature."""
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        """Return the base domain URL of the source."""
        pass

    @property
    @abstractmethod
    def rule_config(self) -> RuleModel:
        """Return the crawling rule configuration."""
        pass

    @property
    @abstractmethod
    def card_data(self) -> List:
        """Return the list of parsed card data models."""
        pass

    @property
    @abstractmethod
    def entity_data(self) -> List[entity_model]:
        """Return the list of parsed entity data."""
        pass

    @abstractmethod
    def contact_page(self) -> str:
        """Return the contact page URL of the data source."""
        pass

    @abstractmethod
    def invoke_db(self, command: int, key: str, value, expiry: int | None = 60):
        """
        Interact with Redis using the given command, key, value, and optional expiry.

        Parameters:
            command (int): The Redis command enum.
            key: The Redis key to operate on.
            value: The value to set or use in the operation.
            expiry (int, optional): Expiration time in seconds. Default is 60.
        """
        pass

    def append_leak_data(self, leak, entity: entity_model):
        """Append a single parsed card model to the collected card data."""
        self._card_data.append(leak)
        self._entity_data.append(entity)
        if callable(self.callback):
            if self.callback():
                self._card_data.clear()
                self._entity_data.clear()

    def init_callback(self, callback):
        """Pass callback model triggered when data is parsed."""
        pass
