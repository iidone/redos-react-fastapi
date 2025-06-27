from pydantic import BaseModel
from typing_extensions import List
from enum import Enum

class UsersSchema(BaseModel):
    role: str
    username: str
    full_name: str
    password: str
    email: str


class DeleteMasterRequest(BaseModel):
    ids: List[int]
    
class UserCreate(UsersSchema):
    pass

class UserResponce(UsersSchema):
    id: int
    
class UserRole(str, Enum):
    ORGANIZER = "organizer"
    ADMIN = "admin"
    
    
class UpdateUserRole(BaseModel):
    role: UserRole 

    class Config:
        json_schema_extra = {
            "example": {
                "role": "organizer"
            },
            "description": "Допустимые значения: 'organizer', 'admin'"
        }