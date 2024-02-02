from sumula.extract_text.extract_text import extrair_relacao_jogadores


def test_se_pega_a_relacao_jogadores():
    dados_jogadores = extrair_relacao_jogadores("142317se.pdf")
    assert len(dados_jogadores) == 2
    assert dados_jogadores[0]["time"] == 'Ceará / CE'
    assert dados_jogadores[1]["time"] == 'Cuiabá Saf / MT'