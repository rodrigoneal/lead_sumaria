from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from sumula.api.config.db import get_session
from sumula.api.domain.repositories.auth_repository import AuthRepository


class UnauThorizedException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


api_key_header = APIKeyHeader(name="X-API-Key")


def auth_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthRepository:
    return AuthRepository(session)


async def check_api_key(
    auth_repository: Annotated[AuthRepository, Depends(auth_repository)],
    api_key_header: Annotated[str, Security(api_key_header)],
):
    result = await auth_repository.check_api_key(api_key_header)
    if result and result.status:
        return result
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou usuario não autorizado.",
    )
