from database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Enum,DateTime,func
import enum
# from .records import Record

class Roles(enum.Enum):
    admin = "admin"
    analyst="analyst"
    user ="user"

class User(Base):

    __tablename__ = "users"

    id:Mapped[int]=mapped_column(autoincrement=True,primary_key=True,index=True)
    username:Mapped[str]=mapped_column(String(50),index=True)
    password:Mapped[str]=mapped_column(String(255))
    email:Mapped[str]=mapped_column(String(50),unique=True,index=True)
    # role:Mapped[Roles]=mapped_column(Enum(Roles),index=True)
    role:Mapped[str]=mapped_column(String(20),index=True)
    is_active:Mapped[bool]=mapped_column(default=True)
    created_At:Mapped[DateTime]=mapped_column(DateTime(timezone=True),server_default=func.now())

    records:Mapped[list["Record"]]=relationship(back_populates="user",lazy="selectin")
    