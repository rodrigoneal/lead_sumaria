import asyncio
from os import PathLike
from tempfile import NamedTemporaryFile
from typing import Literal
import httpx


async def proximas_partidas(ano: str) -> httpx.Response:
    url = f"https://www.cbf.com.br/futebol-brasileiro/competicoes/copa-brasil-masculino/{ano}"
    return await requisicao(url)


async def requisicao(url) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        for _ in range(10):
            try:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
            except httpx.ReadTimeout:
                await asyncio.sleep(1)
                continue
        return response


async def download_pdf_sumula(
    ano: str, jogo: str, tipo: Literal["copa", "campeonato"] = "copa"
) -> PathLike:
    url_base = "https://conteudo.cbf.com.br/sumulas/{ano}/{num_competicao}{jogo}se.pdf"
    num_competicao = "424" if tipo == "copa" else "142"
    url = url_base.format(ano=ano, jogo=jogo, num_competicao=num_competicao)
    response = await requisicao(url)

    with NamedTemporaryFile(delete=False, suffix=".pdf") as file:
        print(f"Salvando >>>> {file.name}")
        file.write(response.content)
        return file.name
