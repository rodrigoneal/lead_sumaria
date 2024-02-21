from sumula.extract_text.extract_text import (
    extrair_dados_arbitragem,
    limpar_dados_arbitragem,
)


def test_se_extrai_dados_arbitragem(primeira_pagina: str):
    dados_arbitragem = extrair_dados_arbitragem(primeira_pagina)
    assert (
        dados_arbitragem
        == "\n    Arbitro: Jonathan Benkenstein Pinheiro (CD / RS)\n    Arbitro Assistente 1: Tiago Augusto Kappes Diel (AB / RS)\n    Arbitro Assistente 2: Maira Mastella Moreira (AB / RS)\n    Quarto Arbitro: Ivan da Silva Guimaraes Junior (AB / AM)\n    Assessor: Ana Karina Marques Valentin (CBF / PE)\n    Quinto Arbitro: Ivan Carlos Bohn (MTR / PR)\n    Delegado Local: Eduardo Senna (CBF / PR)\n    VAR: Daniel Nobre Bins (VAR-FIFA / RS)\n    AVAR2: Bruno Arleu de Araujo (FIFA / RJ)\n    Observador de VAR: Hilton Moutinho Rodrigues (CBF / RJ)\n    AVAR: Andre da Silva Bitencourt (AB / RS)\n    "
    )


def test_se_limpa_dados_arbitragem():
    texto = "\n    Arbitro: Jonathan Benkenstein Pinheiro (CD / RS)\n    Arbitro Assistente 1: Tiago Augusto Kappes Diel (AB / RS)\n    Arbitro Assistente 2: Maira Mastella Moreira (AB / RS)\n    Quarto Arbitro: Ivan da Silva Guimaraes Junior (AB / AM)\n    Assessor: Ana Karina Marques Valentin (CBF / PE)\n    Quinto Arbitro: Ivan Carlos Bohn (MTR / PR)\n    Delegado Local: Eduardo Senna (CBF / PR)\n    VAR: Daniel Nobre Bins (VAR-FIFA / RS)\n    AVAR2: Bruno Arleu de Araujo (FIFA / RJ)\n    Observador de VAR: Hilton Moutinho Rodrigues (CBF / RJ)\n    AVAR: Andre da Silva Bitencourt (AB / RS)\n    "
    dados_arbitragem = limpar_dados_arbitragem(texto)
    assert len(dados_arbitragem) == 11
