from pydantic import Field
from typing import Literal, Optional, List

from crawler.crawler_instance.local_interface_model.app.base_model import base_model

NetworkType = Literal["clearnet", "i2p", "onion", "invalid"]
IocType = Literal[
    "brand_impersonation",
    "c2_server",
    "crypto_drain",
    "crypto_phishing",
    "hacked",
    "malicious_redirect",
    "malware_url",
    "open_directory",
    "phishing",
    "phishing_domain",
    "scam",
    "spam_url",
    "typosquatting",
]


class defacement_model(base_model):
    m_web_server: Optional[List[str]] = Field(default_factory=list)
    m_source_url: Optional[List[str]] = Field(default_factory=list)
    m_network: NetworkType
    m_ioc_type: List[IocType]
    m_mirror_links: List[str] = Field(default_factory=list)
    m_platform: List[str] = Field(default_factory=list)
    m_vulnerability: Optional[str] = None
    m_external_scanners: List[str] = Field(default_factory=list)
    m_tags: List[str] = Field(default_factory=list)
    m_total_report: Optional[str] = None
