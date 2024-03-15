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
# Conversão da Súmula do Campeonato Brasileiro e da Copa do Brasil para JSON 🚀

Para autenticação, é necessário passar o Token no cabeçalho da requisição. Por exemplo: `X-API-Key: 1234`.

A URL base é [https://www.leadtax-api.lead.tax/sumula/](https://www.leadtax-api.lead.tax/sumula/).

O segundo path é o ano, por exemplo: `2023`.

O terceiro path é o número do jogo, por exemplo: `10`.

Na query `competicao`, pode-se escolher entre `copa do brasil` e `campeonato brasileiro`.

Por exemplo: [https://www.leadtax-api.lead.tax/sumula/2023/10?competicao=copa%20do%20brasil](https://www.leadtax-api.lead.tax/sumula/2023/10?competicao=copa%20do%20brasil).

```python
import requests

headers = {
    'accept': 'application/json',
    'X-API-Key': '1234',
}

response = requests.get('https://www.leadtax-api.lead.tax/sumula/2023/10?competicao=copa%20do%20brasil', headers=headers)

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
    return RedirectResponse("/sumula/docs")


add_routers(app)
