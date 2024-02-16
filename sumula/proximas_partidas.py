import asyncio
import re

import httpx
from bs4 import BeautifulSoup
from dateutil.parser import parse

from sumula.api.app.config.db import create_tables, get_session
from sumula.api.domain.repositories.agendamento import AgendamentoRepository


def pegar_link_partidas(html: str):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all(
        "a",
        class_="btn-link",
        href=lambda href: href and href.startswith("https://www.cbf.com.br"),
    )
    for link in links:
        yield link.get("href")

def pegar_data_jogo(html: str):
    soup = BeautifulSoup(html, "html.parser")
    partidas = soup.find_all('div', class_='text-1 m-b-10 text-center uppercase')
    padrao_data = r"(\d{2}\/)+(\d{4})\s*(\d{2}:\d{2})"
    padrao_jogo = r"Jogo:\s*(\d{1,3})"
    for partida in partidas:
        data = re.search(padrao_data, partida.text).group(0)
        jogo = re.search(padrao_jogo, partida.text).group(1)
        yield {"data": parse(data, dayfirst=True), "jogo": jogo} 


def proximas_partidas():
    with httpx.Client() as client:
        response = client.get(
            "https://www.cbf.com.br/futebol-brasileiro/competicoes/copa-brasil-masculino/2024"
        )
        return response
    
async def requisicao(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
        except httpx.ReadTimeout:
            await asyncio.sleep(1)
            response = await client.get(url)
        return response


async def datas_dos_jogos():
    await create_tables()
    session = await get_session()
    agendamento = AgendamentoRepository(session)
    tasks = []
    response = proximas_partidas()
    for link in pegar_link_partidas(response.text):
        task = asyncio.create_task(requisicao(link))
        tasks.append(task)
    for task in asyncio.as_completed(tasks):
        response = await task
        dados = pegar_data_jogo(response.text)
        for dado in dados:
            await agendamento.insert(
                dado
            )

