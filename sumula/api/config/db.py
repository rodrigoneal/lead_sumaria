import os
from functools import cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from sumula.api.domain.model import Base
from dotenv import load_dotenv


import motor.motor_asyncio
from beanie import init_beanie

from sumula.entities.entities import Sumula


num_cpu = os.cpu_count()

connection_pool_size = min(32, num_cpu + 4) if num_cpu else 4

load_dotenv()

class Settings:
    asyncpg_url: str = os.getenv("SQL_URL") or "sqlite+aiosqlite:///agendamento.db"
    MONGO_URI: str = os.getenv("MONGO_URI") or "mongodb://localhost:27017"


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



async def init():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(database=client.sumula, document_models=[Sumula])