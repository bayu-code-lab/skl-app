from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker
from backend.core.config import settings


engine = AsyncEngine(
    create_engine(
            settings.DATABASE_URI, 
            echo=True, 
            future=True,
        )
    )


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session