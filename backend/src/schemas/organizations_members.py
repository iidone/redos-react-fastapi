from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrganizationMemberBase(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    organization_id: int = Field(..., description="ID организации")
    assigned_by: int = Field(..., description="ID пользователя, добавившего в организацию")

class OrganizationMemberCreate(OrganizationMemberBase):
    pass

class OrganizationMemberResponce(OrganizationMemberBase):
    assigned_at: datetime

    class Config:
        from_attributes = True