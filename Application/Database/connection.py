from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
Base = declarative_base()

engine = create_async_engine(
    url=DATABASE_URL,
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database connected successfully")
    except Exception as e:
        print(f"Database connection failed {e}")


async def get_db():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
