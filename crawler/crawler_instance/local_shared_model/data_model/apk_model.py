from pydantic import Field
from typing import Literal, Optional, List

from crawler.crawler_instance.local_interface_model.app.base_model import base_model

NetworkType = Literal["clearnet", "i2p", "onion", "invalid"]
ApkContentType = Literal["apk", "pc_game"]


class apk_model(base_model):
    m_package_id: str
    m_network: NetworkType
    m_version: Optional[str] = None
    m_content_type: List[ApkContentType] = Field(default_factory=list)
    m_download_link: List[str] = Field(default_factory=list)
    m_mod_features: str
