from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class SocialReconRequest(BaseModel):
    query: str = Field(..., min_length=1)

    @field_validator("query", mode="before")
    @classmethod
    def strip_query(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if isinstance(value, str) else value


class HateSpeechRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)

    @field_validator("text", mode="before")
    @classmethod
    def strip_text(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if isinstance(value, str) else value


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
    @classmethod
    def validate_tokens(cls, value: List[str]) -> List[str]:
        cleaned = [token.strip() for token in value if isinstance(token, str) and token.strip()]
        if not cleaned:
            raise ValueError("Please enter at least one token.")
        return cleaned

    @field_validator("username", "platform", mode="before")
    @classmethod
    def to_lowercase(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.lower()
