from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse
import httpx
from sumula.api.controller.sumula_controle import download_sumula_jogo
from sumula.api.domain.crud import read
from sumula.api.config import db
from sumula.api.domain.model import AuthenticationModel
from sumula.api.providers.auth import check_api_key 
from sumula.entities.entities import Sumula


import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    await db.create_tables()
    yield


app = FastAPI(lifespan=lifespan,docs_url="/sumula/documentation", redoc_url=None)

@app.get("/sumula/", include_in_schema=False)
async def root():
    return RedirectResponse("/sumula/documentation")

@app.get("/sumula", response_model=Sumula)
async def search(user: Annotated[AuthenticationModel, Depends(check_api_key)], ano: Annotated[int, Query(example=2023)], jogo: Annotated[int, Query(example=10, title="Numero da partida")]):
    result = await read(ano, jogo)
    if not result:
        try:
            result = await download_sumula_jogo(ano, jogo)
            await result.insert()
        except httpx.HTTPStatusError:
            raise  HTTPException(status_code=404, detail="Jogo não encontrado")
    return result
