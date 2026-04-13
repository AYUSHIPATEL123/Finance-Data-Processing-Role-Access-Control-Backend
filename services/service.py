from fastapi import HTTPException,Depends,Request,status
from fastapi.security import OAuth2PasswordBearer
import hashlib
from typing import Annotated
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from datetime import datetime,timedelta
import jwt
from jwt.exceptions import PyJWTError
import os
from database import get_db
from models.users import User

pwd_content = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password:str) -> str:
    
    hashed = hashlib.sha256(password.encode()).hexdigest()
    
    return pwd_content.hash(hashed)


def verify_password(plan_password:str,stored_password:str) -> bool:
    
    hashed = hashlib.sha256(plan_password.encode()).hexdigest()
    
    return pwd_content.verify(hashed,stored_password)


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

async def get_jwt_token(email:str,role:str):

    exp = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    
    # exp = datetime.utcnow() + timedelta(seconds=15)

    token = jwt.encode({"email":email,"role":role,"exp":exp},os.getenv('SECRET_KEY'),algorithm=os.getenv('ALGORITHM'))
    
    return token


async def decode_jwt_token(token:str):
    
    try:

        print("=====",token)
        
        user_data = jwt.decode(token,os.getenv('SECRET_KEY'),algorithms=[os.getenv('ALGORITHM')])
    
        email = user_data.get('email')

        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
        return email
    
    except PyJWTError as e:

        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        detail=f'{e}')


async def get_current_user(token:Annotated[str,Depends(oauth2_schema)],db:AsyncSession = Depends(get_db)):
    
    try:

        # token = request.headers.get("Authorization")
        
        # if not token:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token is missing")
        
        # token = token.split(" ")[-1]

        print("+++++",token)

        email = await decode_jwt_token(token)

        query = select(User).where(User.email == email)

        user = await db.execute(query)
        
        user = user.scalar_one_or_none()

        return user
    
    except TypeError as e:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Unauthorized User,{e}')


def require_role(*roles):

    async def check_role(current_user=Depends(get_current_user)):
    
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")
        
        return current_user
    
    return check_role
        
