


import asyncio

from sumula.api.controller.sumula_controle import salvar_proximos_jogos, download_sumulas

asyncio.run(salvar_proximos_jogos())

asyncio.run(download_sumulas())


