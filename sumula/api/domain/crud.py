from sumula.entities.entities import Sumula
from sumula.log import logger


async def insert(sumula: Sumula):
    logger.info("Sumula inserida")
    result = await Sumula.find_one(
        Sumula.primeira_pagina.jogo.ano == sumula.primeira_pagina.jogo.ano,
        Sumula.primeira_pagina.jogo.jogo_num == sumula.primeira_pagina.jogo.jogo_num,
    )
    if not result:
        await sumula.insert()


async def read(year, jogo):
    logger.info(f"Procurando sumula: {year} {jogo}")
    return await Sumula.find_one(
        Sumula.primeira_pagina.jogo.ano == year,
        Sumula.primeira_pagina.jogo.jogo_num == jogo,
    )
