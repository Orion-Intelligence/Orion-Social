from pydantic import BaseModel, Field

class SocialReconRequest(BaseModel):
    query: str = Field(..., min_length=1)
