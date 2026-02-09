from pydantic import BaseModel, Field
from typing import List

class SocialReconRequest(BaseModel):
    query: str = Field(..., min_length=1)
class SocialTarget(BaseModel):
    usernames: List[str] = Field(..., min_length=1)
    platform: str
    max_followers: int = Field(default=50, ge=1, le=5000)
    max_following: int = Field(default=50, ge=1, le=5000)

class SocialScrapeRequest(BaseModel):
    targets: List[SocialTarget]