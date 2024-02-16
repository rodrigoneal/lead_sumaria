import os
from functools import cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from sumula.api.domain.model import Base

num_cpu = os.cpu_count()

connection_pool_size = min(32, num_cpu + 4) if num_cpu else 4


class Settings:
    asyncpg_url: str = os.getenv("SQL_URL") or "sqlite+aiosqlite:///agendamento.db"


@cache
def get_settings():
    """Retorna as configurações do projeto.

    Returns:
        Settings: configurações do projeto.
    """
    return Settings()


settings = get_settings()


engine = create_async_engine(
    settings.asyncpg_url
)


# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    return async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    """Cria as tabelas no banco de dados."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)