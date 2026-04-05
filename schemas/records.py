from pydantic import BaseModel
from typing import Optional
import enum


class RecordType(str,enum.Enum):
    income = "income"
    expense = "expense"


class RecordSchema(BaseModel):

    amount:int    
    type:RecordType
    category:str
    notes:Optional[str] = None

    user_id:int
   