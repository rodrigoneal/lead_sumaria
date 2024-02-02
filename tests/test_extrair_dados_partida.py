from sumula.extract_text.extract_text import extrair_dados_partida, extrair_dados_partida_e_limpar, limpar_dados_partida


def test_se_extrai_dados_partida_corretamente(primeira_pagina: str):
    dados_partida = extrair_dados_partida(primeira_pagina)
    assert dados_partida == '\n    Campeonato: Campeonato Brasileiro - Série A/2023 Rodada: 38 \n    Jogo: Coritiba S.a.f. / PR X Corinthians / SP\n    Data: 06/12/2023 Horário: 21:30 Estádio: Major Antônio Couto Pereira / Curitiba\n    '

def test_se_limpa_dados_partida():
    dados = '\n    Campeonato: Campeonato Brasileiro - Série A/2023 Rodada: 38 \n    Jogo: Coritiba S.a.f. / PR X Corinthians / SP\n    Data: 06/12/2023 Horário: 21:30 Estádio: Major Antônio Couto Pereira / Curitiba\n    '
    dados_partida = limpar_dados_partida(dados)
    assert dados_partida == ('06/12/2023', '21:30', 'Major Antônio Couto Pereira / Curitiba')

def test_se_traz_os_dados_limpo_e_estruturado(primeira_pagina: str):
    dados_partida = extrair_dados_partida_e_limpar(primeira_pagina)
    assert dados_partida == {'data': '06/12/2023', 'horario': '21:30', 'estadio': 'Major Antônio Couto Pereira / Curitiba'}