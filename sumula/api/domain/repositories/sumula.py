from tinydb import Query

from sumula.entities.entities import Sumula as SumulaEntities


class SumulaRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, sumula: SumulaEntities):
        ano = sumula.primeira_pagina.jogo.ano
        jogo_num = sumula.primeira_pagina.jogo.jogo_num
        if self.db.search(
            (Query().primeira_pagina.jogo.ano == ano)
            & (Query().primeira_pagina.jogo.jogo_num == jogo_num)
        ):
            return
        print("Inserindo>>>")
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
            Query().primeira_pagina.jogo.ano
            == year & Query().primeira_pagina.jogo.rodada
            == round
        )

    def get_by_year_game_num(self, year, game_num):
        return self.db.get(
            (Query().primeira_pagina.jogo.ano == year)
            & (Query().primeira_pagina.jogo.jogo_num == game_num)
        )

    def get_by_team(self, team, year, rodada=0, jogo=0):
        team = team.capitalize()
        if rodada > 0:
            return self.db.search(
                (
                    Query().primeira_pagina.jogo.jogo.search(team)
                    & (Query().primeira_pagina.jogo.ano == year)
                    & (Query().primeira_pagina.jogo.rodada == rodada)
                )
            )
        if jogo > 0:
            return self.db.search(
                (Query().primeira_pagina.jogo.ano == year)
                & (Query().primeira_pagina.jogo.jogo_num == jogo)
            )
        return self.db.search(
            (
                Query().primeira_pagina.jogo.jogo.search(team)
                & (Query().primeira_pagina.jogo.ano == year)
            )
        )
