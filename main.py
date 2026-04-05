from fastapi import FastAPI
from routers import records_route, users_route
from database import get_db,async_engine,Base
from models import records,users


app = FastAPI()


app.include_router(users_route.router)
app.include_router(records_route.router)

@app.on_event('startup')
async def create_tbl():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/')
async def home():
    return {"message":"HOME PAGE"}
