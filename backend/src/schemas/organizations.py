from pydantic import BaseModel
from datetime import datetime

class OrganizationCreate(BaseModel):
    name: str
    description: str
    created_by: int

class OrganizationResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True  #
