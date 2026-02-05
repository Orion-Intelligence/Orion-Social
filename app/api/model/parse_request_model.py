from typing import List, Dict

from pydantic import BaseModel

class parse_cti_model(BaseModel):
    text: str

class parse_request_model(BaseModel):
    data: List[str]

class parse_semantic(BaseModel):
    data: List[str]

class embed_index_model(BaseModel):
    data: List[str]
    normalize: bool = True

class parse_translation_model(BaseModel):
    text: str

class RuntimeParsePayload(BaseModel):
    text: Dict[str, str]