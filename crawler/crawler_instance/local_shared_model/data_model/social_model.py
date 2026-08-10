import hashlib
from typing import Literal, List, Optional

from pydantic import BaseModel, Field, model_serializer, model_validator

from crawler.crawler_instance.local_interface_model.app.base_model import base_model
from crawler.crawler_services.shared.russian_translator import russian_translator

NetworkType = Literal["clearnet", "i2p", "onion", "invalid", "tor"]
PlatformType = List[str]

class social_comment_model(BaseModel):
    m_username: Optional[str] = None
    m_time: Optional[str] = None
    m_likes: Optional[str] = None
    m_text: Optional[str] = None
    m_hash: Optional[str] = None

    @model_validator(mode="after")
    def build_comment_hash(self):
        raw_hash = "|".join([
            self.m_username or "",
            self.m_time or "",
            self.m_likes or "",
            self.m_text or "",
        ])
        self.m_hash = hashlib.sha256(raw_hash.encode("utf-8")).hexdigest()
        return self

    @model_serializer
    def serialize_comment(self):
        return {
            "commenter": self.m_username,
            "time": self.m_time,
            "likes": self.m_likes,
            "text": self.m_text,
            "hash": self.m_hash,
        }

class social_model(base_model):
    m_sender_name: Optional[str] = None
    m_network: NetworkType
    m_viral: Optional[bool] = None
    m_hash_id: Optional[str] = None
    m_content_type: List[str] = Field(default_factory=list)
    m_channel_url: Optional[str] = None
    m_message_sharable_link: Optional[str] = None
    m_message_id: Optional[str] = None
    m_platform: PlatformType
    m_group_name: Optional[str] = None
    m_group_info: Optional[str] = None
    m_post_comments: Optional[str] = None
    m_post_comments_list: List[str] = Field(default_factory=list)
    m_comments: List[social_comment_model] = Field(default_factory=list)
    m_post_likes: Optional[str] = None
    m_post_shares: Optional[str] = None
    m_post_tags: List[str] = Field(default_factory=list)
    m_post_views: Optional[str] = None
    m_post_expiry: Optional[str] = None
    m_views: Optional[str] = None
    m_comment_count: Optional[str] = None
    m_likes: Optional[str] = None
    m_retweets: Optional[str] = None
    m_commenters: List[str] = Field(default_factory=list)
    m_img_src: Optional[str] = None
    m_coverpage: Optional[str] = None
    m_code_snippet: List[str] = Field(default_factory=list)
    m_hate_speech: Optional[dict] = None

    @staticmethod
    def unique_identifier(*values) -> str:
        raw_hash = "|".join(str(value or "") for value in values)
        return hashlib.sha256(raw_hash.encode("utf-8")).hexdigest()

    @model_validator(mode="after")
    def translate_forum_text(self):
        content_types = [str(content_type).strip().lower() for content_type in self.m_content_type]
        platforms = [str(platform).strip().lower() for platform in self.m_platform]
        if "forum" in platforms or "forum" in content_types:
            self.m_title = russian_translator.forum_title(self.m_title)
            self.m_content = russian_translator.forum_content(self.m_content)
        return self

    @model_serializer(mode="wrap")
    def serialize_social_model(self, handler):
        data = handler(self)
        data.pop("m_post_comments", None)
        data.pop("m_post_comments_list", None)
        data.pop("m_commenters", None)
        data["m_message_sharable_link"] = str(
            data.get("m_message_sharable_link") or data.get("m_url") or data.get("m_channel_url") or ""
        )
        data["m_comments"] = data.get("m_comments") or []
        return data

    @model_validator(mode="after")
    def build_hash_id(self):
        if self.m_hash_id:
            return self
        stable_id = self.m_url or self.m_message_sharable_link or self.m_message_id
        self.m_hash_id = self.unique_identifier(
            ",".join(self.m_platform),
            stable_id,
            "" if stable_id else self.m_title,
            "" if stable_id else self.m_content,
            "" if stable_id else self.m_date,
        )
        return self
