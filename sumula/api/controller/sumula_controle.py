from sumula.download.pdf_downloader import download_pdf_sumula
from sumula.etc.file_handler import deletar_temp
from sumula.extract_text.pdf_handler import PDFHandler
from sumula.logger import logger

# from sumula.proximas_partidas import agendamento_repository, extrair_data_jogo, extrair_link_partidas


async def download_sumula_jogo(ano, jogo, campeonato):
    logger.info(f"Baixando sumula {ano}/{jogo} para o {campeonato}")
    pdf_sumula = await download_pdf_sumula(ano, jogo, campeonato)
    sumula = PDFHandler(**pdf_sumula).sumula()
    deletar_temp()
    return sumula
