from fastapi import FastAPI
from routers import records_route, users_route,auth_route
from database import get_db,async_engine,Base
from models import records,users
from contextlib import asynccontextmanager

count =0 
@asynccontextmanager
async def lifespan(app:FastAPI):
   
    print("👋 started the app ... ")

    yield
    global count
    
    print(f"🌅 sutting down the app...{count}")


app = FastAPI(lifespan=lifespan)


app.include_router(users_route.router)
app.include_router(records_route.router)
app.include_router(auth_route.router)


@app.on_event('startup')
async def create_tbl():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/')
async def home():
    global count
    count += 1 
    return {"message":"HOME PAGE"}

