"""
Request models for IOC extraction endpoint
"""

from pydantic import BaseModel
from typing import Optional


class IOCExtractRequest(BaseModel):
    """
    Request model for IOC extraction
    Supports both file upload and direct text input
    """
    text: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Optional:  Malicious IP:  192.168.1.1, Hash: d41d8cd98f00b204e9800998ecf8427e"
            }
        }