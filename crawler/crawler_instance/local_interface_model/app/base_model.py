from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class base_model(BaseModel):
    m_scrap_file: Optional[str] = None
    m_title: Optional[str] = None
    m_url: Optional[str] = None
    m_base_url: Optional[str] = None
    m_content: Optional[str] = None
    m_weblink: List[str] = Field(default_factory=list)
    m_date: Optional[date] = None
