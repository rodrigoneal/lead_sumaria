from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sumula.api.domain.model import AuthenticationModel


class AuthRepository:
    def __init__(self, session: AsyncSession = None):
        self.session = session

    async def check_api_key(self, api_key: str):
        stmt = select(AuthenticationModel).where(
            AuthenticationModel.chave_api_2 == api_key
        )
        async with self.session() as session:
            result = await session.execute(stmt)
            return result.scalars().first()

    async def create_token(self, token: str, is_active: bool):
        model = AuthenticationModel(chave=token, st_ativo=is_active)
        async with self.session as session:
            session.add(model)
            await session.commit()
