from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrganizationsBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class OrganizationCreate(OrganizationsBase):
    pass

class OrganizationResponce(OrganizationsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
