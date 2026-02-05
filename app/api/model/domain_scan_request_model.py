from pydantic import BaseModel
from typing import Optional

class domain_scan_request(BaseModel):
    scanType: str
    domain: str
    checkLive: Optional[bool] = False
