from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from playwright.sync_api import Page
from api.social_manager.social_enums import SCRAPE_SCOPE


class BaseScraper(ABC):

    requires_login: bool = False

    def __init__(self, username: str, max_followers: int = 50, max_following: int = 50):
        self.data = []
        self._username = username
        self._max_followers = max_followers
        self._max_following = max_following
        self._scope = SCRAPE_SCOPE.FOLLOWERS_FOLLOWING

    def set_scope(self, scope: int):
        self._scope = scope

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
    def scrape_profile(self, page: Page) -> Dict[str, Any]:
        pass

    @abstractmethod
    def scrape_followers(self, page: Page) -> List[str]:
        pass

    @abstractmethod
    def scrape_following(self, page: Page) -> List[str]:
        pass

    def parse_page(self, page: Page) -> Dict[str, Any]:
        result = {}

        include_profile = self._scope in [
            SCRAPE_SCOPE.PROFILE_ONLY,
            SCRAPE_SCOPE.PROFILE_FOLLOWERS,
            SCRAPE_SCOPE.PROFILE_FOLLOWING
        ]

        include_followers = self._scope in [
            SCRAPE_SCOPE.FOLLOWERS_ONLY,
            SCRAPE_SCOPE.FOLLOWERS_FOLLOWING,
            SCRAPE_SCOPE.PROFILE_FOLLOWERS
        ]

        include_following = self._scope in [
            SCRAPE_SCOPE.FOLLOWING_ONLY,
            SCRAPE_SCOPE.FOLLOWERS_FOLLOWING,
            SCRAPE_SCOPE.PROFILE_FOLLOWING
        ]

        if include_profile:
            result["profile"] = self.scrape_profile(page)

        if include_followers:
            result["followers"] = self.scrape_followers(page)

        if include_following:
            result["following"] = self.scrape_following(page)

        if include_followers and include_following:
            followers_set = set(result.get("followers", []))
            following_set = set(result.get("following", []))
            result["mutual"] = list(followers_set & following_set)

        result["platform"] = self.name.lower()
        result["username"] = self._username

        return result
