from sumula.extract_text.extract_text import (
    extrair_dados_cronologia,
    limpar_dados_cronologia,
)


def test_se_extrai_dados_cronologia(primeira_pagina: str):
    dados_cronologia = extrair_dados_cronologia(primeira_pagina)
    assert (
        dados_cronologia
        == "\n    1º Tempo\n    Entrada do mandante: 21:20     Atraso: Não Houve\n    Entrada do visitante: 21:20     Atraso: Não Houve\n    Início 1º Tempo: 21:32     Atraso: 2 min\n    Término do 1º Tempo: 22:20     Acréscimo: 3 min2º Tempo\n    Entrada do mandante: 22:33     Atraso: Não Houve\n    Entrada do visitante: 22:33     Atraso: Não Houve\n    Início do 2º Tempo: 22:40     Atraso: 5 min\n    Término do 2º Tempo: 23:28     Acréscimo: 3 min\n    Resultado do 1º Tempo: 0 X 2     Resultado Final: 0 X 2     \n    "
    )


def test_se_limpa_dados_cronologia():
    dados = "\n    1º Tempo\n    Entrada do mandante: 21:20     Atraso: Não Houve\n    Entrada do visitante: 21:20     Atraso: Não Houve\n    Início 1º Tempo: 21:32     Atraso: 2 min\n    Término do 1º Tempo: 22:20     Acréscimo: 3 min2º Tempo\n    Entrada do mandante: 22:33     Atraso: Não Houve\n    Entrada do visitante: 22:33     Atraso: Não Houve\n    Início do 2º Tempo: 22:40     Atraso: 5 min\n    Término do 2º Tempo: 23:28     Acréscimo: 3 min\n    Resultado do 1º Tempo: 0 X 2     Resultado Final: 0 X 2     \n    "
    dados_cronologia = limpar_dados_cronologia(dados)
    assert len(dados_cronologia) == 9
