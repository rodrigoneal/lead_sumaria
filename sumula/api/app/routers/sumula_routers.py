from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sumula.api.config.config import Campeonatos
from sumula.api.config.db import get_session
from sumula.api.controller.sumula_controle import download_sumula_jogo
from sumula.api.domain.model import AuthenticationModel, SumulaModel
from sumula.api.domain.repositories.sumula_repository import SumulaRepository
from sumula.api.providers.auth import check_api_key
from sumula.entities.entities import SumulaResponse

sumula_routers = APIRouter(tags=["Sumula"])






@sumula_routers.get("/{ano}/{jogo}", response_model=SumulaResponse)
async def sumula_to_pdf(
    user: Annotated[AuthenticationModel, Depends(check_api_key)],
    ano: Annotated[int, Path(example=2023, title="Ano da partida")],
    jogo: Annotated[int, Path(example=10, title="Numero da partida")],
    session: Annotated[AsyncSession, Depends(get_session)],
    competicao: Annotated[Campeonatos, Query(example=Campeonatos.COPA)],
):
    sumula_repository = SumulaRepository(session)
    if result := await sumula_repository.read_sumula_by_competicao(
        competicao.value, ano, jogo
    ):
        return result
    result = await download_sumula_jogo(ano, jogo, competicao.name.lower())
    sumula = SumulaModel(**result.to_database())
    result = await sumula_repository.insert_sumula(sumula)
    return result