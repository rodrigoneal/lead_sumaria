import asyncio
from tempfile import NamedTemporaryFile
from typing import Literal
import httpx


def proximas_partidas():
    with httpx.Client() as client:
        response = client.get(
            "https://www.cbf.com.br/futebol-brasileiro/competicoes/copa-brasil-masculino/2023"
        )
        return response
    
async def requisicao(url):
    async with httpx.AsyncClient() as client:
        for _ in range(10):
            try:
                response = await client.get(url, timeout=10)
                break
            except httpx.ReadTimeout:
                await asyncio.sleep(1)
                continue
        return response


async def download_pdf_sumula(ano: str, jogo: str, tipo: Literal["copa", "campeonato"] = "copa"):
    url_base = "https://conteudo.cbf.com.br/sumulas/{ano}/{num_competicao}{jogo}se.pdf"
    num_competicao = "424" if tipo == "copa" else "142"
    url = url_base.format(ano=ano, jogo=jogo, num_competicao=num_competicao)
    response = await requisicao(url)

    with NamedTemporaryFile(delete=False, suffix=".pdf") as file:
        print(f"Salvando >>>> {file.name}")
        file.write(response.content)
        return file.name


