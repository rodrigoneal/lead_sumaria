from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sumula.api.domain.model import Logs


class LogsRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def save_logs(self, logs: Logs):
        async with self.session() as session:
            session.add(logs)
            await session.commit()
            await session.refresh(logs)

        return logs