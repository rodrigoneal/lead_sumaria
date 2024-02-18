from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, extract

from sumula.api.domain.model import AgendamentoModel
from sqlalchemy.exc import IntegrityError

from sumula.log import logger


class AgendamentoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, agendamento):
        model = AgendamentoModel(**agendamento)
        async with self.session() as session:
            session.add(model)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                logger.info(f"Agendamento ja existe: {model}")
                return
            logger.info(f"Agendamento inserido: {model}")
            await session.refresh(model)
            return model

    async def next_players(self, data: datetime):
        logger.info(f"Proximos jogos: {data}")
        query = select(AgendamentoModel).where(
            (AgendamentoModel.data <= data) & (AgendamentoModel.status == "pendente")
        )
        async with self.session() as session:
            result = await session.execute(query)
            return result.scalars()

    async def update(self, ano, jogo):
        logger.info(f"Atualizando agendamento: {ano} {jogo}")
        query = (
            update(AgendamentoModel)
            .where((extract('year', AgendamentoModel.data) == ano) & (AgendamentoModel.jogo == jogo))
            .values(status="realizado")
        )
        async with self.session() as session:
            await session.execute(query)
            await session.commit()
