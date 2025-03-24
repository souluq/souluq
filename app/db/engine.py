from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import env

from .tables import Base

engine = create_async_engine(env.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine)


async def create_db_and_tables():
    print("Setting up database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
