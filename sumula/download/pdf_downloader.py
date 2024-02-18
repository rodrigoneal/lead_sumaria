import asyncio
from os import PathLike
from tempfile import NamedTemporaryFile
from typing import Literal
import httpx

from sumula.log import logger



async def proximas_partidas(ano: str) -> httpx.Response:
    logger.info(f"Requisitando proximas partidas para o ano: {ano}")
    url = f"https://www.cbf.com.br/futebol-brasileiro/competicoes/copa-brasil-masculino/{ano}"
    return await requisicao(url)


async def requisicao(url) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        
        for _ in range(10):
            try:
                logger.info(f"Requisitando: {url}")
                response = await client.get(url, timeout=10)
                if response.status_code == 200:
                    break
                response.raise_for_status()
            except httpx.ReadTimeout:
                logger.info(f"Timeout na requisição: {url}")
                await asyncio.sleep(1)
                continue
            except httpx.HTTPStatusError as e:
                logger.info(f"Erro de requisição: {url} status: {e.response.status_code}")
                raise e
        return response


async def download_pdf_sumula(
    ano: str, jogo: str, tipo: Literal["copa", "campeonato"] = "copa"
) -> PathLike:
    logger.info(f"Baixando PDF para o ano: {ano} e jogo: {jogo} e tipo: {tipo}")
    url_base = "https://conteudo.cbf.com.br/sumulas/{ano}/{num_competicao}{jogo}se.pdf"
    num_competicao = "424" if tipo == "copa" else "142"
    url = url_base.format(ano=ano, jogo=jogo, num_competicao=num_competicao)
    response = await requisicao(url)

    with NamedTemporaryFile(delete=False, suffix=".pdf") as file:
        file.write(response.content)
        logger.info(f"Salvando PDF no arquivo: {file.name}")
        return file.name
