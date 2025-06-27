from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrganizationMemberBase(BaseModel):
    member_id: int = Field(..., description="ID пользователя")
    organization_id: int = Field(..., description="ID организации")
    organizer_id: int = Field(..., description="ID организации")


class OrganizationMemberCreate(OrganizationMemberBase):
    pass    

class OrganizationMemberResponse(BaseModel):
    id: int
    member_id: int
    member_name: str
    organization_id: int
    organization_name: str
    organizer_id: int
    organizer_name: str
    assigned_at: datetime

    class Config:
        from_attributes = True
        
        
        
        
        