from pydantic import BaseModel
import enum
from datetime import datetime
from .records import RecordSchema


class UserRoles(str,enum.Enum):
    admin = "admin"
    analyst="analyst"
    user ="user"


class UserSchema(BaseModel):

    username:str
    password:str
    email:str
    role:UserRoles
    

    records:list[RecordSchema]=[]


class UserOut(UserSchema):

    id:int
    is_active:bool
    created_At:datetime
    class Config:
        from_attributes=True    