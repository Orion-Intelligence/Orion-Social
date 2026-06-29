from typing import List, Optional
from pydantic import Field

from crawler.crawler_instance.local_interface_model.app.base_model import base_model


class apt_model(base_model):
    m_entity_type: Optional[str] = None
    m_entity_id: Optional[str] = None
    m_source_url: Optional[str] = None
    m_family: List[str] = Field(default_factory=list)
    m_family_ids: List[str] = Field(default_factory=list)
    m_aliases: List[str] = Field(default_factory=list)
    m_references: List[str] = Field(default_factory=list)
    m_platform: str
    m_country: Optional[str] = None
    m_actor: Optional[str] = None
    m_os: Optional[str] = None
    m_status: List[str] = Field(default_factory=list)
