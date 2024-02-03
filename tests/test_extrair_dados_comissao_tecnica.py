from sumula.extract_text.extract_text import (
    extrair_comissao_tecnica,
    limpar_comissao_tecnica,
)


def test_se_extrai_comissao_tecnica(segunda_pagina):
    dados_comissao = extrair_comissao_tecnica(segunda_pagina)
    assert len(dados_comissao) == 12


def test_se_limpa_dados_comissao_tecnica(segunda_pagina):
    comissao = [
        "Assistente Técnico: Juliano Roberto Antonello",
        "Assistente Técnico: Alcino Rodrigues Lima",
        "Médico: Pedro Guilme Teixeira De Sousa Filho",
        "Treinador De Goleiros: Everaldo Goncalves Santana",
        "Preparador Físico: Edy Carlos Toporowicz Soares",
        "Fisioterapeuta: Joao Paulo Cavalcante FrotaJuventude / RS",
        "Técnico: Celso Juarez Roth",
        "Assistente Técnico: Humberto Gomes Ferreira",
        "Médico: Alexandre Schio Fay",
        "Treinador De Goleiros: Marcio Rodrigo Angonese",
        "Preparador Físico: Marcos Galgaro",
        "Massagista: Cleber Willian Fernandes",
    ]


    dados_comissao = limpar_comissao_tecnica(comissao, "Ceará / CE", "Juventude / RS")
    assert len(dados_comissao["Ceará / CE"]) == 6 
    assert len(dados_comissao["Juventude / RS"]) == 6


# (\+(\d+)|\d+:\d+) tempo do gol
# tempo de jogo (\d+[Tt])
# numero jogador T(\d+)
# tipo (NR|PN|CT|FT)
# Nome (NR|PN|CT|FT)(.*)