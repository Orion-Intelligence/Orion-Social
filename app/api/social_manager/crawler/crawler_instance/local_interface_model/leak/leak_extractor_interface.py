from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
import inspect
import re

from crawler.crawler_instance.local_shared_model.data_model.entity_model import entity_model
from crawler.crawler_instance.local_shared_model.data_model.leak_model import leak_model
from crawler.crawler_instance.local_interface_model.leak.model.leak_data_model import leak_data_model
from crawler.crawler_instance.local_shared_model.rule_model import RuleModel, ThreatType, RuleType
from crawler.crawler_services.redis_manager.redis_enums import CUSTOM_SCRIPT_REDIS_KEYS


class leak_extractor_interface(ABC):
    _RULE_TYPE_RULES = {
        RuleType.DEFACEMENT: {"rule_type": "unique", "path": "defacement_collector"},
        RuleType.EXPLOIT: {"rule_type": "unique", "path": "exploit_collector"},
        RuleType.FORUM: {"rule_type": "unique", "path": "social/forum"},
        RuleType.GENERIC: {
            "rule_type": "generic",
            "path": None,
            "value_regex": r"^https?://[a-z2-7]{16,56}\.onion(?:/.*)?$",
        },
        RuleType.LEAK: {"rule_type": "unique", "path": "leak_collector/leak"},
        RuleType.MASTODON: {
            "rule_type": "shared",
            "path": "scrapers",
            "value_regex": r"^https?://(?:[^/]+\.)?mastodon\.social(?:/.*)?$",
        },
        RuleType.NEWS: {"rule_type": "unique", "path": "news_collector"},
        RuleType.PASTEBIN: {
            "rule_type": "shared",
            "path": "scrapers",
            "value_regex": r"^https?://(?:[^/]+\.)?pastebin\.com(?:/.*)?$",
        },
        RuleType.REDDIT: {
            "rule_type": "shared",
            "path": "scrapers",
            "value_regex": r"^https?://(?:[^/]+\.)?reddit\.com(?:/.*)?$",
        },
        RuleType.YOUTUBE: {
            "rule_type": "shared",
            "path": "scrapers",
            "value_regex": r"^https?://(?:www\.)?youtube\.com(?:/.*)?$",
        },
        RuleType.TRACKING: {"rule_type": "unique", "path": "leak_collector/tracking"},
        RuleType.TWITTER: {
            "rule_type": "shared",
            "path": "scrapers",
            "value_regex": r"^https?://(?:www\.)?x\.com(?:/.*)?$",
        },
        RuleType.FACEBOOK: {
            "rule_type": "shared",
            "path": "scrapers",
            "value_regex": r"^https?://(?:www\.)?facebook\.com(?:/.*)?$",
        },
        RuleType.TIKTOK: {
            "rule_type": "shared",
            "path": "scrapers",
            "value_regex": r"^https?://(?:www\.)?tiktok\.com(?:/.*)?$",
        },
        RuleType.INSTAGRAM: {
            "rule_type": "shared",
            "path": "scrapers",
            "value_regex": r"^https?://(?:www\.)?instagram\.com(?:/.*)?$",
        },
    }

    @staticmethod
    def _normalize_rule_path(class_path: str) -> str:
        normalized = class_path.replace("\\", "/").lower()
        replacements = [
            ("social_collector/scripts/forums", "social/forum"),
            ("social_collector/scripts/platform", "social/platform"),
            ("leak_collector/scripts/leak", "leak_collector/leak"),
            ("leak_collector/scripts/tracking", "leak_collector/tracking"),
            ("news_collector/scripts", "news_collector"),
            ("exploit_collector/scripts", "exploit_collector"),
            ("defacement_collector/scripts", "defacement_collector"),
        ]
        for source, target in replacements:
            normalized = normalized.replace(source, target)
        return normalized

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        orig_init = getattr(cls, "__init__", lambda self, *a, **k: None)

        def __init__(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)

            cfg = self.rule_config
            actual_type = getattr(cfg, "m_threat_type", None)

            if not isinstance(actual_type, ThreatType):
                raise ValueError(
                    f"{self.__class__.__name__}.rule_config.m_threat_type must be a ThreatType, "
                    f"got {actual_type!r}"
                )

            class_file = Path(inspect.getfile(self.__class__)).resolve()
            class_path = self._normalize_rule_path(str(class_file))
            actual_rule_type = getattr(cfg, "m_rule_type", None)

            if not isinstance(actual_rule_type, RuleType):
                raise ValueError(
                    f"{self.__class__.__name__}.rule_config.m_rule_type must be a RuleType, "
                    f"got {actual_rule_type!r}"
                )

            rule_definition = self._RULE_TYPE_RULES.get(actual_rule_type)
            if not rule_definition:
                raise ValueError(f"Unsupported rule type: {actual_rule_type!r}")

            expected_path = rule_definition["path"]
            if expected_path and expected_path not in class_path:
                raise ValueError(
                    f"{self.__class__.__name__} is inside '{class_path}' "
                    f"but rule_config.m_rule_type expects path '{expected_path}'."
                )

            value_regex = rule_definition.get("value_regex")
            if value_regex:
                candidates = [getattr(self, "seed_url", "") or "", getattr(self, "base_url", "") or ""]
                if not any(re.match(value_regex, candidate) for candidate in candidates if candidate):
                    raise ValueError(
                        f"{self.__class__.__name__}.rule_config.m_rule_type='{actual_rule_type.value}' "
                        f"requires seed_url/base_url to match '{value_regex}'."
                    )

        cls.__init__ = __init__

    @abstractmethod
    def parse_leak_data(self, page) -> leak_data_model:
        """Parse leak data from the given Playwright page and return a leak_data_model."""
        pass

    @property
    @abstractmethod
    def is_crawled(self) -> bool:
        """Return if script has been crawled."""
        pass

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
    def card_data(self) -> List[leak_model]:
        """Return the list of parsed leak models (card data)."""
        pass

    @property
    @abstractmethod
    def entity_data(self) -> List[entity_model]:
        """Return the list of parsed leak models (entity data)."""
        pass

    @abstractmethod
    def contact_page(self) -> str:
        """Return the contact page URL of the data source."""
        pass

    @abstractmethod
    def invoke_db(self, command: int, key: str, value, expiry: int = 60):
        """
        Interact with Redis using the given command, key, value, and optional expiry.

        Parameters:
            command (int): The Redis command enum.
            key (CUSTOM_SCRIPT_REDIS_KEYS): The Redis key to operate on.
            value: The value to set or use in the operation.
            expiry (int, optional): Expiration time in seconds. Default is 60.
        """
        pass

    @abstractmethod
    def append_leak_data(self, leak: leak_model, entity: entity_model):
        """Append a single leak_model instance to the collected card data."""
        pass

    def init_callback(self, callback):
        """pass callback model triggered on leak parsed"""
        pass
