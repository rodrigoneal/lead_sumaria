import json
import warnings
from contextlib import asynccontextmanager
from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from sumula.api.config import db
from sumula.api.controller.sumula_controle import download_sumula_jogo
from sumula.api.domain.crud import read
from sumula.api.domain.model import AuthenticationModel, SumulaModel
from sumula.api.providers.auth import check_api_key
from sumula.entities.entities import Sumula

warnings.simplefilter(action="ignore", category=FutureWarning)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await db.init()
    await db.create_tables()
    yield


description = """
Converte a Sumula da Campeonato Brasileiro e Copa do Brasil para Json. 🚀

Para autenticacão é necessario passar o Token no cabecalho da requisição. Por exemplo: `X-API-Key: 1234`

a URL base é <https://www.leadtax-api.lead.tax/sumula/>

O primeiro path é o tipo de  campeonato que pode ser `copa` ou `campeonato`.

O segundo path é o ano exemplo: `2023`.

O terceiro path é o numero do jogo exemplo: `10`.

Por exemplo: `https://www.leadtax-api.lead.tax/sumula/copa/2023/10`

```
import requests

headers = {
    'accept': 'application/json',
    'X-API-Key': '1234',
}

response = requests.get('https://www.leadtax-api.lead.tax/sumula/copa/2023/10', headers=headers)

```

O response vai retornar um json com os dados da sumula, que pode ser vista no swagger na parte de schemas com o nome `Sumula`.

Para verificar o swagger, acesse [Swagger](https://www.leadtax-api.lead.tax/sumula/documentation "Documentação da API") ou o [Redoc](https://www.leadtax-api.lead.tax/sumula/redoc "Redoc")

"""

app = FastAPI(
    title="Sumula API",
    version="0.0.1",
    lifespan=lifespan,
    docs_url="/documentation",
    redoc_url="/redoc",
    root_path="/sumula",
    openapi_url="/openapi.json",
    contact={
        "name": "Edilson Barros",
        "url": "https://www.portal.lead.tax/",
        "email": "ediilson.barros@leadtax.com.br",
    },
    description=description,
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/sumula/documentation")


@app.get("/copa/{ano}/{jogo}", response_model=Sumula)
async def copa_brasil(
    # user: Annotated[AuthenticationModel, Depends(check_api_key)],
    ano: Annotated[int, Path(example=2023)],
    jogo: Annotated[int, Path(example=10, title="Numero da partida")],
    session: Annotated[AsyncSession, Depends(db.get_session)]
):
    campeonato = "Copa do Brasil"
    result = await read(ano, jogo, campeonato)
    if not result:
        try:
            result = await download_sumula_jogo(ano, jogo, "copa")
            try:
                await result.insert()
            except Exception:
                pass
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return result


@app.get("/campeonato/{ano}/{jogo}", response_model=SumulaModel)
async def campeonato_brasileiro(
    # user: Annotated[AuthenticationModel, Depends(check_api_key)],
    ano: Annotated[int, Path(example=2023)],
    jogo: Annotated[int, Path(example=10, title="Numero da partida")],
    session: Annotated[AsyncSession, Depends(db.get_session)],
):
    campeonato = "Campeonato Brasileiro"
    result = await download_sumula_jogo(ano, jogo, "campeonato")

    sumula = SumulaModel(**result.to_database())
    async with session() as session:
        session.add(sumula)
        await session.commit()
        await session.refresh(sumula)
    return sumula
    # async with session() as session:
    #     session.add(result)
    #     await session.commit()
    #     await session.refresh(result)


    # result = await read(ano, jogo, campeonato)
    # if not result:
    #     try:
    #         
    #         try:
    #             await result.insert()
    #         except Exception:
    # #             pass
    #     except httpx.HTTPStatusError:
    #         raise HTTPException(status_code=404, detail="Jogo não encontrado")
    # return result
