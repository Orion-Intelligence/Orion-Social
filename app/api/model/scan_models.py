from pydantic import BaseModel
from typing import List, Dict

class Threat(BaseModel):
    header: str
    description: str
    confidence: str
    risk: str

class ScanMeta(BaseModel):
    URL: str
    Host: str
    Port: str
    Scanned_on_date: str
    Scanned_by: str

class ScanResult(BaseModel):
    meta: ScanMeta
    threats: Dict[str, List[Threat]]
