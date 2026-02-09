from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class social_model(BaseModel):
    m_weblink: List[str] = Field(default_factory=list)

    m_username: Optional[str] = None
    m_network: Optional[str] = None
    m_real_name: Optional[str] = None
    m_total_posts: Optional[str] = None

    m_followers: Optional[List[str]] = None
    m_following: Optional[List[str]] = None

    m_total_followers: Optional[str] = None
    m_total_following: Optional[str] = None

    m_bio: Optional[str] = None
    m_location: Optional[str] = None

    m_content: Optional[str] = None
    m_content_type: List[str] = Field(default_factory=list)

    m_channel_url: Optional[str] = None
    m_platform: str

    m_post_comments: Optional[str] = None
    m_post_likes: Optional[str] = None
    m_post_shares: Optional[str] = None
    m_post_comments_count: Optional[str] = None
    m_post_views: Optional[str] = None
    m_views: Optional[str] = None
    m_comment_count: Optional[str] = None
    m_likes: Optional[str] = None
    m_retweets: Optional[str] = None

    m_commenters: List[str] = Field(default_factory=list)
    m_mutual_usernames: List[str] = Field(default_factory=list)

    m_posts_data: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
