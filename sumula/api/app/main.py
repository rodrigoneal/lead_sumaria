from datetime import datetime
import json
from starlette.middleware.base import BaseHTTPMiddleware
import warnings
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Path, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from sumula.api.config import db
from sumula.api.config.config import Campeonatos
from sumula.api.controller.sumula_controle import download_sumula_jogo
from sumula.api.domain.model import AuthenticationModel, Logs, SumulaModel
from sumula.api.domain.repositories.auth_repository import AuthRepository
from sumula.api.domain.repositories.logs_repository import LogsRepository
from sumula.api.providers.auth import  check_api_key
from sumula.api.domain.repositories.sumula_repository import SumulaRepository
from sumula.entities.entities import SumulaResponse
from sumula.etc.file_handler import async_iterator_wrapper as aiwrap

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

O segundo path é o ano exemplo: `2023`.

O terceiro path é o numero do jogo exemplo: `10`.

Atravez da query `competicao` pode-se escolher entre `copa do brasil` e `campeonato brasileiro`. 

Por exemplo: `https://www.leadtax-api.lead.tax/sumula/2023/10?competicao=copa do brasil`

```
import requests

headers = {
    'accept': 'application/json',
    'X-API-Key': '1234',
}

response = requests.get('https://www.leadtax-api.lead.tax/sumula/2023/10?competicao=copa do brasil', headers=headers)

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


@app.middleware(BaseHTTPMiddleware)
async def log_requests(request: Request, call_next):
    session = await db.get_session()
    if request.url.query:
        try:
            st_sucesso = False
            auth_repository = AuthRepository(session)
            api_key = request.headers.get("X-API-Key")
            id_usuario = 0
            if user := await auth_repository.check_api_key(api_key):
                id_usuario = user.id
            chamada = str(request.url)
            start = datetime.now()
            response = await call_next(request)
            if response.status_code == 200:
                st_sucesso = True
            resp_body = [
                section async for section in response.__dict__["body_iterator"]
            ]
            response.__setattr__("body_iterator", aiwrap(resp_body))
            response_body = json.loads(resp_body[0].decode())
            logs = Logs(
                id_client=id_usuario,
                dh_chamada=start,
                dh_retorno=datetime.now(),
                url_chamada=chamada,
                st_sucesso=st_sucesso,
                dados_retorno=response_body,
                cd_ocorrencia=0,
                ds_erro="",
            )
            logs_repository = LogsRepository(session)
            await logs_repository.save_logs(logs)
            return response
        except Exception as e:
            raise e

    response = await call_next(request)
    return response


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/sumula/documentation")


@app.get("/{ano}/{jogo}", response_model=SumulaResponse)
async def sumula_to_pdf(
    user: Annotated[AuthenticationModel, Depends(check_api_key)],
    ano: Annotated[int, Path(example=2023, title="Ano da partida")],
    jogo: Annotated[int, Path(example=10, title="Numero da partida")],
    session: Annotated[AsyncSession, Depends(db.get_session)],
    competicao: Annotated[Campeonatos, Query(example=Campeonatos.COPA)],
):
    sumula_repository = SumulaRepository(session)
    if result := await sumula_repository.read_sumula_by_competicao(
        competicao.value, ano, jogo
    ):
        return result
    result = await download_sumula_jogo(ano, jogo, competicao.name.lower())
    sumula = SumulaModel(**result.to_database())
    result = await sumula_repository.insert_sumula(sumula)
    return result
