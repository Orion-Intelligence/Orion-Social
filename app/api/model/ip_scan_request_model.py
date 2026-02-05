from pydantic import BaseModel

class IPScanRequest(BaseModel):
    ip: str


