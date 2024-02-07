from fastapi import FastAPI
from sumula.api.domain.repositories.sumula import SumulaRepository



app = FastAPI()


# @app.get("/")
# async def root():
#     response = SumulaRepository().get_all()
#     return response

# @app.get("/")
# async def jogo(year: int, round: int):
#     response = SumulaRepository().get_by_year_and_round(year, round)
#     return response

@app.get("/")
async def jogo(year: int, game_num: int):
    response = SumulaRepository().get_by_year_game_num(year, game_num)
    return response