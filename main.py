import warnings
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from sumula.api.app.routers import add_routers
from sumula.api.config import db

warnings.simplefilter(action="ignore", category=FutureWarning)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables()
    yield


description = """
# Conversão da Súmula do Campeonato Brasileiro e da Copa do Brasil para JSON 🚀

O segundo path é o ano, por exemplo: `2023`.

O terceiro path é o número do jogo, por exemplo: `10`.

Na query `competicao`, pode-se escolher entre `copa do brasil` e `campeonato brasileiro`.

```python
import requests

headers = {
    'accept': 'application/json',
}

response = requests.get('https://127.0.0.1/sumula/2023/10?competicao=copa%20do%20brasil', headers=headers)

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
        "name": "Rodrigo Castro",
        "email": "rodrigho2006@gmail.com",
    },
    description=description,
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/sumula/docs")


add_routers(app)
