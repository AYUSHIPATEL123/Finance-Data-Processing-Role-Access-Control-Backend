from sqlalchemy.orm import Mapped,mapped_column,Relationship
from sqlalchemy import Date,String,Enum,ForeignKey
from database import Base
# from .users import User
import enum

class RecordType(enum.Enum):

    income = "income"
    expense = "expense"

class Record(Base):

    __tablename__ = "records"

    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True,index=True)
    amount:Mapped[int]=mapped_column(primary_key=True)
    # type:Mapped[RecordType]=mapped_column(Enum[RecordType],index=True)
    type:Mapped[str]=mapped_column(String(50),index=True)
    category:Mapped[str]=mapped_column(String(50))
    notes:Mapped[str]=mapped_column(String(500))

    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    user:Mapped["User"]=Relationship(back_populates="records")

