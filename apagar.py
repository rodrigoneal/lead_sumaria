import asyncio
from sumula.extract_text.pdf_handler import Crawler, PDFHandler
from aiotinydb import AIOTinyDB



# pdf_handler = PDFHandler("defeito_6.pdf")
# pdf_handler.sumula()


crawler = Crawler()

competicao = "copa"

num_jogos = 381 if competicao == "campeaonato" else 123


async def pegar_dados(ano, jogo):
    result = await crawler.pegar_todos_jogos(ano, jogo)
    async with AIOTinyDB('db.json') as db:
        db.insert(result.model_dump())

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



asyncio.run(pegar_todos_jogos())