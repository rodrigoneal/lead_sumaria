
import asyncio
import pathlib
from apagar import salvar_sumula
from sumula.extract_text.pdf_handler import Crawler
from sumula.proximas_partidas import atualizar_status, datas_dos_jogos, proximos_jogos
import tempfile


def deletar_temp():
    path = pathlib.Path(tempfile.gettempdir())
    for file in path.glob("*.pdf"):
        print(f"Deletando >>>> {file.name}")
        file.unlink(missing_ok=True)

crawler = Crawler()


asyncio.run(datas_dos_jogos())

results = asyncio.run(proximos_jogos())

async def jogos():
    tasks = []
    for result in results:
        ano = result.data.year
        jogo = result.jogo
        task = asyncio.create_task(crawler.pegar_todos_jogos(ano=ano, jogo=jogo))
        tasks.append(task)
        
        if len(tasks) >= 10:
            for task in asyncio.as_completed(tasks):
                sumula = await task
                ano = sumula.primeira_pagina.jogo.ano
                jogo = sumula.primeira_pagina.jogo.jogo_num
                await salvar_sumula(sumula)
                await atualizar_status(ano, jogo)
            tasks = []
            deletar_temp()
    
    # Lidar com tarefas restantes
    if tasks:
        for task in asyncio.as_completed(tasks):
            sumula = await task
            ano = sumula.primeira_pagina.jogo.ano
            jogo = sumula.primeira_pagina.jogo.jogo_num
            await salvar_sumula(sumula)
            await atualizar_status(ano, jogo)

results = asyncio.run(jogos())


# 1m 4,4s