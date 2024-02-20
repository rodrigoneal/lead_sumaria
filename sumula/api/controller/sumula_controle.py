import asyncio
from datetime import datetime
from sumula.api.config.db import init
from sumula.api.domain.crud import insert
from sumula.download.pdf_downloader import download_pdf_sumula, proximas_partidas, requisicao
from sumula.etc.file_handler import deletar_temp
from sumula.extract_text.pdf_handler import PDFHandler
from sumula.logger import logger
# from sumula.proximas_partidas import agendamento_repository, extrair_data_jogo, extrair_link_partidas


async def download_sumula_jogo(ano, jogo):
    logger.info(f"Baixando sumula {ano}/{jogo}")
    pdf_sumula = await download_pdf_sumula(ano, jogo)
    sumula = PDFHandler(**pdf_sumula).sumula()
    deletar_temp()
    return sumula
    

# async def salvar_proximos_jogos():
#     logger.info("Salvando proximos jogos")
#     agendamento = await agendamento_repository()
#     tasks = []
#     ano = datetime.now().year
#     response = await proximas_partidas(ano)
#     for link in extrair_link_partidas(response.text):
#         task = asyncio.create_task(requisicao(link))
#         tasks.append(task)
#     for task in asyncio.as_completed(tasks):
#         response = await task
#         dados = extrair_data_jogo(response.text)
#         for dado in dados:
#             await agendamento.insert(
#                 dado
#             )
#     logger.success("Proximos jogos salvos")
    


# async def download_sumulas():
#     logger.info("Baixando sumulas")
#     agendamento = await agendamento_repository()
#     await init()
#     now = datetime.now()
#     results = await agendamento.next_players(now)
#     tasks = []
#     logger.info(f"Proximos jogos: {results}")
#     for result in results:
#         task = asyncio.create_task(download_sumula_jogo(result.data.year, result.jogo))
#         tasks.append(task)
#         if len(tasks) >= 10:
#             for task in asyncio.as_completed(tasks):
#                 sumula = await task
#                 await insert(sumula)
#                 await agendamento.update(**sumula.to_database())
#             tasks = []
#     if tasks:
#         for task in asyncio.as_completed(tasks):
#             sumula = await task
#             await insert(sumula)
#             await agendamento.update(**sumula.to_database())
#     deletar_temp()
#     logger.success("Sumulas baixadas")
    
