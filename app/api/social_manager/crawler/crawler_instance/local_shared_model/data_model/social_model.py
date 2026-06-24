from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, date

class social_model(BaseModel):
    m_title: Optional[str] = None
    m_sender_name: Optional[str] = None
    m_message_sharable_link: str
    m_weblink: List[str] = Field(default_factory=list)
    m_network: str
    m_content: Optional[str] = None
    m_bio: Optional[str] = None
    m_profile_pic: Optional[str] = None
    m_cover_pic: Optional[str] = None
    m_followers: Optional[str] = None
    m_following: Optional[str] = None
    m_viral: Optional[bool] = None
    m_total_posts: Optional[str] = None
    m_content_type: List[str] = Field(default_factory=list)
    m_message_date: Optional[date]
    m_channel_url: Optional[str] = None
    m_message_id: Optional[str] = None
    m_platform: str
    m_group_name: Optional[str] = None
    m_group_info: Optional[str] = None
    m_post_comments: Optional[str] = None
    m_post_likes: Optional[str] = None
    m_post_shares: Optional[str] = None
    m_post_comments_count: Optional[str] = None
    m_post_tags:List[str] = Field(default_factory=list)
    m_post_views: Optional[str] = None
    m_post_expiry:Optional[str] = None
    m_views: Optional[str] = None
    m_comment_count: Optional[str] = None
    m_likes: Optional[str] = None
    m_retweets: Optional[str] = None
    m_commenters: List[str] = Field(default_factory=list)
    m_profile_views: Optional[str] = None
    m_total_views: Optional[str] = None
    m_rating: Optional[str] = None
    m_joined_relative: Optional[str] = None
    m_joined_exact: Optional[str] = None


    @field_validator('m_message_date', mode='before')
    def parse_message_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format for m_message_date: {value}. Expected format: YYYY-MM-DD.")
        return value

    @model_validator(mode='after')
    def validate_model(self):
        required_fields = [
            "m_message_sharable_link"
        ]
        for field_name in required_fields:
            if not getattr(self, field_name):
                raise ValueError(f"The field '{field_name}' is required and cannot be None or empty.")

        if not isinstance(self.m_content_type, list):
            raise ValueError("m_content_type must be a list.")

        return self

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            date: lambda v: v.strftime("%Y-%m-%d") if v else None
        }
    }
