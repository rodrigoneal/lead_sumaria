from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from sumula.api.domain.model import SumulaModel


class SumulaRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def read_sumula_by_competicao(
        self, competicao: str, ano: int, jogo_num: int
    ) -> List[SumulaModel]:
        stmt = select(SumulaModel).where(
            SumulaModel.competicao.contains(competicao), SumulaModel.ano == ano, SumulaModel.jogo_num == jogo_num
        )
        async with self.session() as session:
            return (await session.scalars(stmt)).first()
    async def insert_sumula(self, sumula: SumulaModel):
        async with self.session() as session:
            session.add(sumula)
            await session.commit()
            await session.refresh(sumula)

        return sumula