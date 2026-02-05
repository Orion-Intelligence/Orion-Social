from pydantic import BaseModel, Field, model_validator
from datetime import date
from typing import Optional, List

from crawler.constants.enums import VALID_NETWORK_TYPES


class apk_model(BaseModel):
    m_app_name: str
    m_package_id: str
    m_app_url: str
    m_network: Optional[str] = None
    m_version: Optional[str] = None
    m_content_type: List[str] = Field(default_factory=list)
    m_download_link: List[str] = Field(default_factory=list)
    m_apk_size: Optional[str] = None
    m_latest_date: Optional[str] = None
    m_mod_features: str

    @model_validator(mode='after')
    def check_required_fields_and_enums(self):
        required_fields = ["m_app_name"]
        for field_name in required_fields:
            if getattr(self, field_name) is None:
                raise ValueError(f"The field '{field_name}' is required and cannot be None.")

        if self.m_network not in VALID_NETWORK_TYPES:
            raise ValueError(f"Invalid network type provided: {self.m_network}. Must be one of {', '.join(VALID_NETWORK_TYPES)}.")

        if not isinstance(self.m_content_type, list):
            raise ValueError("m_content_type must be a list of valid content types.")

        return self

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            date: lambda v: v.strftime("%Y-%m-%d") if v else None
        }
    }
