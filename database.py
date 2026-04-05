from sqlalchemy.ext.asyncio import AsyncSession , async_sessionmaker,create_async_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DB_URL = "mysql+aiomysql://root:root@localhost:3306/data_pro_db"

async_engine = create_async_engine(url=SQLALCHEMY_DB_URL,echo=True)

AsyncSessionLocal = async_sessionmaker(bind=async_engine,class_= AsyncSession,expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
