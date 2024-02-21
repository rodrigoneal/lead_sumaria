import warnings
from contextlib import asynccontextmanager
from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.responses import RedirectResponse

from sumula.api.config import db
from sumula.api.controller.sumula_controle import download_sumula_jogo
from sumula.api.domain.crud import read
from sumula.api.domain.model import AuthenticationModel
from sumula.api.providers.auth import check_api_key
from sumula.entities.entities import Sumula

warnings.simplefilter(action="ignore", category=FutureWarning)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    await db.create_tables()
    yield


app = FastAPI(lifespan=lifespan, docs_url="/documentation", root_path="/sumula", openapi_url="/openapi.json")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/documentation")


@app.get("/copa/{ano}/{jogo}", response_model=Sumula)
async def copa_brasil(
    user: Annotated[AuthenticationModel, Depends(check_api_key)],
    ano: Annotated[int, Path(example=2023)],
    jogo: Annotated[int, Path(example=10, title="Numero da partida")],
):
    campeonato = "Copa do Brasil"
    result = await read(ano, jogo, campeonato)
    if not result:
        try:
            result = await download_sumula_jogo(ano, jogo, "copa")
            try:
                await result.insert()
            except Exception:
                pass
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return result


@app.get("campeaonato/{ano}/{jogo}", response_model=Sumula)
async def campeonato_brasileiro(
    user: Annotated[AuthenticationModel, Depends(check_api_key)],
    ano: Annotated[int, Path(example=2023)],
    jogo: Annotated[int, Path(example=10, title="Numero da partida")],
):
    campeonato = "Campeonato Brasileiro"
    result = await read(ano, jogo, campeonato)
    if not result:
        try:
            result = await download_sumula_jogo(ano, jogo, "campeonato")
            try:
                await result.insert()
            except Exception:
                pass
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return result
