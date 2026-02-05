from pydantic import BaseModel, Field

class SocialReconRequest(BaseModel):
    username: str = Field(..., min_length=1)
