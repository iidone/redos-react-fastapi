from pydantic import BaseModel
from datetime import datetime
from typing import List, Union

class OrganizationCreate(BaseModel):
    name: str
    description: str
    created_by: int

class OrganizationResponse(BaseModel):
    id: int
    name: str
    description: str
    created_by: Union[int, str]
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
