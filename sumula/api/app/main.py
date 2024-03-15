import warnings
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from sumula.api.app.routers import add_routers
from sumula.api.app.routers.middleware_logs import CustomHeaderMiddleware
from sumula.api.config import db

warnings.simplefilter(action="ignore", category=FutureWarning)


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    docs_url="/docs",
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
app.add_middleware(CustomHeaderMiddleware)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/sumula/documentation")


add_routers(app)
