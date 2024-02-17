import asyncio
from datetime import datetime
from sumula.api.domain.crud import insert
from sumula.download.pdf_downloader import download_pdf_sumula, proximas_partidas, requisicao
from sumula.extract_text.pdf_handler import PDFHandler
from sumula.proximas_partidas import agendamento_repository, extrair_data_jogo, extrair_link_partidas


async def download_sumula_jogo(ano, jogo):
    pdf_sumula = await download_pdf_sumula(ano, jogo)
    return PDFHandler(pdf_sumula).sumula()

async def salvar_proximos_jogos():
    agendamento = await agendamento_repository()
    tasks = []
    ano = 2023
    response = await proximas_partidas(ano)
    for link in extrair_link_partidas(response.text):
        task = asyncio.create_task(requisicao(link))
        tasks.append(task)
    for task in asyncio.as_completed(tasks):
        response = await task
        dados = extrair_data_jogo(response.text)
        for dado in dados:
            await agendamento.insert(
                dado
            )
    


async def download_sumulas():
    agendamento = await agendamento_repository()
    now = datetime.now()
    results = await agendamento.next_players(now)
    tasks = []
    for result in results:
        task = asyncio.create_task(download_sumula_jogo(result.data.year, result.jogo))
        tasks.append(task)
        if len(tasks) >= 10:
            for task in asyncio.as_completed(tasks):
                sumula = await task
                await insert(sumula)
                await agendamento.update(**sumula.to_database())
            tasks = []
    if tasks:
        for task in asyncio.as_completed(tasks):
            sumula = await task
            await insert(sumula)
            await agendamento.update(**sumula.to_database())
    
