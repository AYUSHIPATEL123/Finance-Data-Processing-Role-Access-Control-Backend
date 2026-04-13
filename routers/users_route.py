from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import select
from schemas.users import UserSchema,UserOut
from models.users import User
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from services.service import oauth2_schema,hash_password,get_current_user,require_role


router = APIRouter()


@router.get('/users/',response_model=list[UserOut])
async def users(db:Annotated[AsyncSession,Depends(get_db)],access:Annotated[UserOut,Depends(require_role("admin","analyst","user"))]):
    
    query = select(User)
    
    if access.role == "user":
        query = select(User).where(User.id==access.id)

    users = await db.execute(query)
    
    users = users.scalars().all()
    
    return users


@router.put('/update-user/{id}',response_model=UserOut)
async def update_user(id:int,new_data:UserSchema,access:Annotated[UserOut,Depends(require_role("admin"))],db:AsyncSession=Depends(get_db)):
    
    user = await db.get(User,id)
    
    if new_data:
        user.username = new_data.username
        user.password = hash_password(new_data.password)
        user.email = new_data.email
        user.role = new_data.role
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found") 

    await db.commit()
    
    await db.refresh(user)
    
    return user


@router.delete('/del-user/{id}')
async def del_user(id:int,access:Annotated[UserOut,Depends(require_role("admin"))],db:AsyncSession=Depends(get_db)):
    
    user = await db.get(User,id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found") 
    
    await db.delete(user)
    
    await db.commit()
   
    raise HTTPException(status_code=status.HTTP_200_OK,detail="done") 
