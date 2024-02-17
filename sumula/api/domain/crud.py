from sumula.entities.entities import Sumula


async def insert(sumula: Sumula):
    result = await Sumula.find_one(
        Sumula.primeira_pagina.jogo.ano == sumula.primeira_pagina.jogo.ano,
        Sumula.primeira_pagina.jogo.jogo_num == sumula.primeira_pagina.jogo.jogo_num,
    )
    if not result:
        await sumula.insert()


async def read(year, jogo):
    return await Sumula.find_one(
        Sumula.primeira_pagina.jogo.ano == year,
        Sumula.primeira_pagina.jogo.jogo_num == jogo,
    )
