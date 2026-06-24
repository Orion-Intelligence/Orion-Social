from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional, List

class defacement_model(BaseModel):
    m_leak_date: Optional[date] = None
    m_web_server: Optional[List[str]] = Field(default_factory=list)
    m_source_url: Optional[List[str]] = Field(default_factory=list)
    m_base_url: str
    m_url: str
    m_content: str | None
    m_network: str
    m_ioc_type: List[str]
    m_mirror_links: List[str] = Field(default_factory=list)

    @field_validator('m_leak_date', mode='before')
    def parse_date_of_leak(cls, value):
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format for m_leak_date: {value}. Expected format: YYYY-MM-DD.")
        return value

    model_config = {
        "arbitrary_types_allowed": True
    }
