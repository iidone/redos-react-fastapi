from pydantic import BaseModel
from datetime import datetime

class OrganizationCreate(BaseModel):
    name: str
    description: str
    created_by: int

class OrganizationResponce(BaseModel):
    id: int
    name: str
    description: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True  #
