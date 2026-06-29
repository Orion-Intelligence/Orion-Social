from typing import List, Literal, Optional
from pydantic import Field, model_validator

from crawler.crawler_instance.local_interface_model.app.base_model import base_model

NetworkType = Literal["clearnet", "i2p", "onion", "invalid"]
LeakContentType = Literal[
    "general",
    "forums",
    "cve",
    "tracking",
    "news",
    "stolen",
    "drugs",
    "hacking",
    "marketplaces",
    "cryptocurrency",
    "leak",
    "leaks",
    "adult",
    "carding",
    "scams",
    "ransomware",
    "databases",
    "money_laundering",
    "counterfeit",
    "malware",
    "botnets",
    "exploit_collector",
    "spam",
    "chemicals",
    "weapons",
    "human_trafficking",
    "csam",
    "doxing",
    "extortion",
    "espionage",
    "propaganda",
    "terrorism",
    "government_leaks",
    "c2_panels",
    "ddos",
    "apt",
    "cracking",
    "social_collector",
    "twitter",
    "reddit",
]


class leak_model(base_model):
    m_ref_html: Optional[str] = None
    m_html: Optional[str] = None
    m_reference_html: Optional[str] = None
    m_important_content: str
    m_network: NetworkType
    m_section: Optional[List[str]] = Field(default_factory=list)
    m_content_type: List[LeakContentType]
    m_screenshot: Optional[str] = None
    m_dumplink: List[str] = Field(default_factory=list)
    m_websites: List[str] = Field(default_factory=list)
    m_logo_or_images: List[str] = Field(default_factory=list)
    m_data_size: Optional[str] = None
    m_revenue: Optional[str] = None
    m_employee_count: Optional[str] = None
    m_confidence: List[str] = Field(default_factory=list)
    m_tags: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_screenshot_for_leak(self):
        content_types = [str(x).strip().lower() for x in self.m_content_type]

        if any(ct in ["leak", "leaks"] for ct in content_types) and not self.m_screenshot:
            raise ValueError("m_screenshot is required when m_content_type contains 'leak'")

        return self
