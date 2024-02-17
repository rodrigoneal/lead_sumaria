from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import httpx
from sumula.api.controller.sumula_controle import download_sumula_jogo
from sumula.api.domain.crud import read
from sumula.api.config import db 
from sumula.entities.entities import Sumula


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    await db.create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", response_model=Sumula)
async def search(ano: int, jogo: int):
    result = await read(ano, jogo)
    if not result:
        try:
            result = await download_sumula_jogo(ano, jogo)
            await result.insert()
        except httpx.HTTPStatusError:
            raise  HTTPException(status_code=404, detail="Jogo não encontrado")
    return result
