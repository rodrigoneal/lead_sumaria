import asyncio
from sumula.api.domain.model import AgendamentoModel
from sumula.api.domain.repositories.sumula import SumulaRepository
from sumula.entities.entities import Sumula
from sumula.extract_text.pdf_handler import Crawler
from aiotinydb import AIOTinyDB

crawler = Crawler()

competicao = "copa"

num_jogos = 381 if competicao == "campeaonato" else 123



async def salvar_sumula(model: Sumula):
    async with AIOTinyDB('db.json') as db:
        sumula_repository = SumulaRepository(db)
        sumula_repository.insert(model)
async def pegar_dados(ano, jogo):
    result = await crawler.pegar_todos_jogos(ano, jogo)
    async with AIOTinyDB('db.json') as db:
        sumula_repository = SumulaRepository(db)
        sumula_repository.insert(result)

async def pegar_todos_jogos():
    anos = ["2022", "2023"]
    jogos = range(1, num_jogos)
    tasks = []
    for ano in anos:
        for jogo in jogos:
            tasks.append(asyncio.create_task(pegar_dados(ano, jogo)))
            if len(tasks) >= 10:
                for task in asyncio.as_completed(tasks):
                    await task
                tasks = []


# asyncio.run(pegar_todos_jogos())