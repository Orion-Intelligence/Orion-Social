from typing import List, Optional
from pydantic import BaseModel, Field


class SocialTarget(BaseModel):
    """Single target definition for scraping"""
    usernames: List[str] = Field(..., min_length=1)
    platform: str = Field(...)
    max_followers: int = Field(default=100, ge=1, le=5000)
    max_following: int = Field(default=100, ge=1, le=5000)


class SocialScrapeRequest(BaseModel):
    """
    Unified scrape request model.
    - For single platform: provide usernames, platform directly
    - For multiple platforms: provide targets list
    """
    # Single platform scrape fields
    usernames: Optional[List[str]] = Field(default=None, min_length=1)
    platform: Optional[str] = Field(default=None)
    max_followers: int = Field(default=100, ge=1, le=5000)
    max_following: int = Field(default=100, ge=1, le=5000)

    # Multiple platform scrape fields
    targets: Optional[List[SocialTarget]] = Field(default=None)
