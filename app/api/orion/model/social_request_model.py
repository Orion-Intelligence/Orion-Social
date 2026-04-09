from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class SocialReconRequest(BaseModel):
    query: str = Field(..., min_length=1)


class SocialPhoneReconRequest(BaseModel):
    query: str = Field(..., min_length=1)


class SocialProfileRequest(BaseModel):
    platform: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    @field_validator("platform", "username", mode="before")
    def to_lowercase(cls, value: str) -> str:
        if value is None:
            return None
        return value.lower()

class SocialFollowersRequest(BaseModel):
    platform: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    max_followers: int = Field(default=50, ge=1, le=5000)


class SocialFollowingRequest(BaseModel):
    platform: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    max_following: int = Field(default=50, ge=1, le=5000)


class SocialPostsRequest(BaseModel):
    platform: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    max_posts: int = Field(default=5, ge=1, le=100)

    @field_validator("platform", "username", mode="before")
    def sanitize(cls, value: str) -> str:
        if value is None:
            return None
        value = value.strip().lower()
        return value

class DuckDuckGoUsernamesRequest(BaseModel):
    username: str = Field(..., min_length=1)
    platform: Optional[str] = Field(default=None)


class DuckDuckGoImagesRequest(BaseModel):
    username: Optional[str] = Field(default=None)
    platform: Optional[str] = Field(default=None)


class DuckDuckGoMetadataRequest(BaseModel):
    tokens: List[str] = Field(..., min_length=1)
    username: Optional[str] = Field(default=None)
    platform: Optional[str] = Field(default=None)

    @field_validator("tokens")
    def validate_tokens(cls, value: List[str]) -> List[str]:
        cleaned = [token.strip() for token in value if isinstance(token, str) and token.strip()]
        if not cleaned:
            raise ValueError("Please enter at least one token.")
        return cleaned

    @field_validator("username", "platform", mode="before")
    def to_lowercase(cls, value: str) -> str:
        if value is None:
            return None
        return value.lower()


class SocialTarget(BaseModel):
    usernames: List[str] = Field(..., min_length=1)
    platform: str
    max_followers: int = Field(default=50, ge=1, le=5000)
    max_following: int = Field(default=50, ge=1, le=5000)


class SocialScrapeRequest(BaseModel):
    targets: List[SocialTarget]


class ProfileResponse(BaseModel):
    username: Optional[str] = None
    real_name: Optional[str] = None
    bio: Optional[str] = None
    total_posts: Optional[str] = None
    total_followers: Optional[str] = None
    total_following: Optional[str] = None
    platform: str
    profile_url: str
    status: str = "active"


class FollowersResponse(BaseModel):
    username: str
    platform: str
    followers: List[str]
    total_count: int


class FollowingResponse(BaseModel):
    username: str
    platform: str
    following: List[str]
    total_count: int


class PostData(BaseModel):
    post_url: str
    datetime: Optional[str] = None
    caption: Optional[str] = None
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    comments: Optional[str] = "0"
    likes: Optional[str] = "0"
    retweets: Optional[str] = None
    views: Optional[str] = None


class PostsResponse(BaseModel):
    username: str
    platform: str
    posts: List[PostData]
    total_count: int


class FullScrapeResponse(BaseModel):
    profile: Optional[ProfileResponse] = None
    followers: Optional[FollowersResponse] = None
    following: Optional[FollowingResponse] = None
    posts: Optional[PostsResponse] = None
    mutual: Optional[List[str]] = None
