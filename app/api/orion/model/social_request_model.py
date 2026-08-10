from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class SocialReconRequest(BaseModel):
    query: str = Field(..., min_length=1)


class SocialPhoneReconRequest(BaseModel):
    query: str = Field(..., min_length=1)


class SocialProfileRequest(BaseModel):
    platform: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    social_data_type: Optional[str] = None
    use_extension: bool = False
    max_posts: int = Field(default=10, ge=1, le=100)
    max_shorts: int = Field(default=20, ge=1, le=100)
    max_comments: int = Field(default=25, ge=1, le=100)
    max_followers: int = Field(default=1000, ge=1, le=5000)
    max_following: int = Field(default=1000, ge=1, le=5000)
    target_type: Optional[str] = None


    @field_validator("platform", "target_type", mode="before")
    def platform_to_lowercase(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip().lower()

    @field_validator("username", mode="before")
    def strip_username(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()

class SocialFollowersRequest(BaseModel):
    platform: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    max_followers: int = Field(default=50, ge=1, le=5000)
    social_data_type: Optional[str] = None
    target_type: Optional[str] = None

    @field_validator("platform", "target_type", mode="before")
    def sanitize_platform(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip().lower()

    @field_validator("username", mode="before")
    def sanitize_username(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()


class SocialFollowingRequest(BaseModel):
    platform: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    max_following: int = Field(default=50, ge=1, le=5000)
    social_data_type: Optional[str] = None
    target_type: Optional[str] = None

    @field_validator("platform", "target_type", mode="before")
    def sanitize_platform(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip().lower()

    @field_validator("username", mode="before")
    def sanitize_username(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()


class SocialPostsRequest(BaseModel):
    platform: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    max_posts: int = Field(default=10, ge=1, le=100)
    max_comments: int = Field(default=10, ge=1, le=100)
    post_offset: int = Field(default=0, ge=0, le=1000)
    existing_posts_count: int = Field(default=0, ge=0, le=1000)
    existing_post_urls: List[str] = Field(default_factory=list)
    comment_offset: int = Field(default=0, ge=0, le=1000)
    social_data_type: Optional[str] = None
    hash_id: Optional[str] = None
    use_extension: bool = False
    target_type: Optional[str] = None

    @field_validator("platform", "target_type", mode="before")
    def sanitize_platform(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip().lower()

    @field_validator("username", mode="before")
    def sanitize_username(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()


class SocialVideosRequest(BaseModel):
    platform: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    max_videos: int = Field(default=10, ge=1, le=100)
    max_comments: int = Field(default=10, ge=1, le=100)
    comment_offset: int = Field(default=0, ge=0, le=1000)
    social_data_type: Optional[str] = None
    hash_id: Optional[str] = None
    target_type: Optional[str] = None

    @field_validator("platform", "target_type", mode="before")
    def sanitize_platform(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip().lower()

    @field_validator("username", mode="before")
    def sanitize_username(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()


class SocialShortsRequest(BaseModel):
    platform: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    max_shorts: int = Field(default=10, ge=1, le=100)
    max_comments: int = Field(default=10, ge=1, le=100)
    post_offset: int = Field(default=0, ge=0, le=1000)
    existing_posts_count: int = Field(default=0, ge=0, le=1000)
    existing_post_urls: List[str] = Field(default_factory=list)
    comment_offset: int = Field(default=0, ge=0, le=1000)
    social_data_type: Optional[str] = None
    hash_id: Optional[str] = None
    target_type: Optional[str] = None

    @field_validator("platform", "target_type", mode="before")
    def sanitize_platform(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip().lower()

    @field_validator("username", mode="before")
    def sanitize_username(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()

class DuckDuckGoUsernamesRequest(BaseModel):
    username: str = Field(..., min_length=1)
    platform: Optional[str] = Field(default=None)


class DuckDuckGoImagesRequest(BaseModel):
    username: Optional[str] = Field(default=None)
    platform: Optional[str] = Field(default=None)
    max_images: int = Field(default=10, ge=1, le=100)
    hash_id: Optional[str] = None


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
    def to_lowercase(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.lower()


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
