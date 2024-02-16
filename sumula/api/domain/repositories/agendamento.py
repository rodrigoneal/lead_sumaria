from sqlalchemy.ext.asyncio import AsyncSession

from sumula.api.domain.model import AgendamentoModel
from sqlalchemy.exc import IntegrityError


class AgendamentoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, agendamento):
        model = AgendamentoModel(**agendamento)
        async with self.session() as session:
            session.add(model)
            try:
                await session.commit()
            except IntegrityError as e:
                print("Erro de integridade: ", e)
                await session.rollback()
                return 
            print("Salvando Data >>>")
            await session.refresh(model)
            return model