from pydantic import BaseModel
import enum
from datetime import date
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
    is_active:bool
    created_At:date

    records:list[RecordSchema]=[]