import re

from pydantic import BaseModel, field_validator
from typing import List, Optional


class entity_model(BaseModel):
    m_email: Optional[List[str]] = None
    m_phone_numbers: Optional[List[str]] = None
    m_location: Optional[List[str]] = None
    m_social_media_profiles: Optional[List[str]] = None
    m_username: Optional[List[str]] = None
    m_industry: Optional[str] = None
    m_company_name: Optional[str] = None
    m_country: Optional[List[str]] = None
    m_ip: Optional[List[str]] = None
    m_credit_cards: Optional[List[str]] = None
    m_crypto_addresses: Optional[List[str]] = None
    m_in_passport_numbers: Optional[List[str]] = None
    m_persons: Optional[List[str]] = None
    m_domain: Optional[List[str]] = None
    m_ans: Optional[List[str]] = None

    m_us_bank_numbers: Optional[List[str]] = None
    m_us_driver_licenses: Optional[List[str]] = None
    m_us_passport_numbers: Optional[List[str]] = None
    m_us_ssn_numbers: Optional[List[str]] = None

    m_team: Optional[str] = None
    m_attacker: Optional[List[str]] = None
    m_family: Optional[List[str]] = None
    m_family_ids: Optional[List[str]] = None
    m_cve: Optional[List[str]] = None
    m_cwe: Optional[List[str]] = None
    m_author: Optional[List[str]] = None
    m_hashtags: Optional[List[str]] = None
    m_product: Optional[List[str]] = None
    m_isp: Optional[List[str]] = None

    @field_validator("m_cve", mode="before")
    @classmethod
    def normalize_cve(cls, value):
        if value is None:
            return None

        values = value if isinstance(value, list) else [value]
        normalized = []
        for item in values:
            text = item.strip() if isinstance(item, str) else str(item).strip() if isinstance(item, (int, float, bool)) else ""
            match = re.fullmatch(r"(?:CVE[-_ ]*)?(\d{4})[-_ ]+(\d{4,})", text, re.IGNORECASE)
            normalized.append(f"CVE-{match.group(1)}-{match.group(2)}" if match else text)

        return normalized

    @field_validator("m_cwe", mode="before")
    @classmethod
    def normalize_cwe(cls, value):
        if value is None:
            return None

        values = value if isinstance(value, list) else [value]
        normalized = []
        for item in values:
            text = item.strip() if isinstance(item, str) else str(item).strip() if isinstance(item, (int, float, bool)) else ""
            match = re.fullmatch(r"(?:CWE[-_ ]*)?(\d{1,6})", text, re.IGNORECASE)
            normalized.append(f"CWE-{match.group(1)}" if match else text)

        return normalized

    model_config = {
        "extra": "allow"
    }
