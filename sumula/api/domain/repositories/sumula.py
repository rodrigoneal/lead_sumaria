from sumula.entities.entities import Sumula as SumulaEntities
from tinydb import TinyDB, Query


class SumulaRepository:

    def __init__(self):
        self.db = TinyDB("db.json")

    def insert(self, sumula: SumulaEntities):
        self.db.insert(sumula.model_dump())

    def get_all(self):
        return self.db.all()

    def get_by_id(self, id):
        return self.db.get(Query().id == id)

    def delete_by_id(self, id):
        self.db.remove(Query().id == id)

    def get_by_year(self, year):
        return self.db.search(Query().primeira_pagina.jogo.ano == year)

    def get_by_year_and_round(self, year, round):
        return self.db.search(
            Query().primeira_pagina.jogo.ano == year
            & Query().primeira_pagina.jogo.rodada == round
        )

    def get_by_year_game_num(self, year, game_num):
        return self.db.get(
          (  Query().primeira_pagina.jogo.ano == year)
            & (Query().primeira_pagina.jogo.jogo_num == game_num)
        )
    
    def get_by_team(self, team, year):
        team = team.capitalize()
        return self.db.search((Query().primeira_pagina.jogo.jogo.search(team) & (Query().primeira_pagina.jogo.ano == year)))