import re

from bs4 import BeautifulSoup
from dateutil.parser import parse

from sumula.logger import logger



def extrair_link_partidas(html: str):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all(
        "a",
        class_="btn-link",
        href=lambda href: href and href.startswith("https://www.cbf.com.br"),
    )
    for link in links:
        logger.info(f"Link: {link.get('href')}")
        yield link.get("href")

def extrair_data_jogo(html: str):
    soup = BeautifulSoup(html, "html.parser")
    partidas = soup.find_all('div', class_='text-1 m-b-10 text-center uppercase')
    padrao_data = r"(\d{2}\/)+(\d{4})\s*(\d{2}:\d{2})"
    padrao_jogo = r"Jogo:\s*(\d{1,3})"
    for partida in partidas:
        data = re.search(padrao_data, partida.text).group(0)
        jogo = re.search(padrao_jogo, partida.text).group(1)
        logger.info(f"Data: {data} Jogo: {jogo}")
        yield {"data": parse(data, dayfirst=True), "jogo": jogo} 

# async def agendamento_repository():
#     session = await get_session()
#     return AgendamentoRepository(session)



# async def proximos_jogos():
#     now = datetime.now()
#     agendamento = await agendamento_repository()
#     return await agendamento.next_players(now)


# async def atualizar_status(ano, jogo):
#     agendamento = await agendamento_repository()
#     return await agendamento.update(ano, jogo)

# async def salvar_jogo(ano, jogo):
#     agendamento = await agendamento_repository()
#     return await agendamento.next_players(ano, jogo)
