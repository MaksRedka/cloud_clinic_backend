"""Database settings."""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from dotenv import load_dotenv

from typing import AsyncGenerator

from src.configs import postgres_settings

load_dotenv()


# Postgres database connect config
engine = create_async_engine(postgres_settings.DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base: DeclarativeMeta = declarative_base()


async def initialize_postgres() -> None:
    """Initialize connection to postgres database """
    async with engine.begin() as connection:
        Base.metadata.bind = engine
        await connection.run_sync(Base.metadata.create_all)


async def get_postgres() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
