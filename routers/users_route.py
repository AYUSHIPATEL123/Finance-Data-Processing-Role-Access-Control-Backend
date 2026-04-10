from fastapi import APIRouter,Depends
from sqlalchemy import select
from passlib.context import CryptContext
from schemas.users import UserSchema,UserOut
from models.users import User
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from services.service import oauth2_schema
import hashlib


router = APIRouter()


pwd_content = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password:str) -> str:
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return pwd_content.hash(hashed)

def verify_password(plan_password:str,stored_password:str) -> bool:
    hashed = hashlib.sha256(plan_password.encode()).hexdigest()
    return pwd_content.verify(hashed,stored_password)


@router.get('/users/',response_model=list[UserOut])
async def users(db:Annotated[AsyncSession,Depends(get_db)],token:Annotated[str,Depends(oauth2_schema)]):
    query = select(User)
    users = await db.execute(query)
    users = users.scalars().all()
    print(token)
    return users


@router.put('/update-user/{id}',response_model=UserOut)
async def update_user(id:int,new_data:UserSchema,db:AsyncSession=Depends(get_db)):
    user = await db.get(User,id)
    if new_data:
        user.username = new_data.username
        user.password = hash_password(new_data.password)
        user.email = new_data.email
        user.role = new_data.role
    else:
        return {"error":"new data not reached"}

    await db.commit()
    await db.refresh(user)
    return user


@router.delete('/del-user/{id}')
async def del_user(id:int,db:AsyncSession=Depends(get_db)):
    user = await db.get(User,id)
    if not user:
        return {"message": "user not found"}
    await db.delete(user)
    await db.commit()
   
    return {"message":"user deleted successfully"}
