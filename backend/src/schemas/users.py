from pydantic import BaseModel
from typing_extensions import List

class UsersSchema(BaseModel):
    role: str
    username: str
    first_name: str
    last_name: str
    password: str
    email: str


class DeleteMasterRequest(BaseModel):
    ids: List[int]
    
class UserCreate(UsersSchema):
    pass

class UserResponce(UsersSchema):
    id: int