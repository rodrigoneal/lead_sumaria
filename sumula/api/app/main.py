from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import httpx
from sumula.api.controller.sumula_controle import download_sumula_jogo, download_sumulas, salvar_proximos_jogos
from sumula.api.domain.crud import read
from sumula.api.config import db 
from sumula.entities.entities import Sumula
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    await db.init()
    await db.create_tables()
    scheduler.add_job(salvar_proximos_jogos, CronTrigger(hour="1"))
    scheduler.add_job(download_sumulas, CronTrigger(hour="1", minute="15"))
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


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
