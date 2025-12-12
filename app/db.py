from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./app.db"


# ASYNC ENGINE
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# ASYNC SESSION FACTORY
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# BASE MODEL
class Base(DeclarativeBase):
    pass


# DEPENDENCY FOR FASTAPI ROUTES
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session