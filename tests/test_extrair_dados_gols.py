from sumula.extract_text.extract_text import extrair_dados_gols, limpar_dados_gols


def test_se_extrai_dados_dos_gols(segunda_pagina):
    dados_gols = extrair_dados_gols(segunda_pagina)
    assert len(dados_gols) == 5


def test_se_limpa_dados_gols():
    gols = [
        "23:00 1T89NRCleber Bomfim de Jesus Ceará/CE",
        "+1 1T34CTVitor Mendes Alves Juventude/RS",
        "06:00 2T77NRGuilherme Parede Pinheiro Juventude/RS",
        "24:00 2T8NRFernando Pereira do Nascimento Ceará/CE",
        "43:00 2T11PNErick de Arruda Serafim Ceará/CE",
    ]
    dados_gols = limpar_dados_gols(gols)
    assert len(dados_gols) == len(gols)
