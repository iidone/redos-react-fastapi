from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrganizationCreate(BaseModel):
    name: str
    description: str
    created_by: int

class OrganizationResponce(BaseModel):
    id: int
    name: str
    description: str
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True 
        
        
class MemberResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str
        
        
        
class OrganizationWithMembersResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    members: List[MemberResponse]
