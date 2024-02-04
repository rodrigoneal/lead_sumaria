from sumula.extract_text.extract_text import extrair_dados_cartao_amarelos, limpar_dados_cartao_amarelos


def test_se_extrai_dados_cartao_amarelo(segunda_pagina):
    dados_cartao_amarelo = extrair_dados_cartao_amarelos(segunda_pagina)
    assert "Luis Felipe Rebelo Costa" in dados_cartao_amarelo


def test_se_limpa_dados_cartao_amarelo():
    text = "\nTempo 1T/2TNºNome do Jogador Equipe\n24:00 1T26Luis Felipe Rebelo Costa Juventude/RS\nMotivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Ao calçar o adversario\n28:00 2T20Onitlasi Junior de Moraes Rodrigues Juventude/RS\nMotivo: A2.  Desaprovar com palavras ou gestos as decisões da arbitragem  - Por reclamacao contra arbitragem.\n29:00 2T77Guilherme Parede Pinheiro Juventude/RS\nMotivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Ao entrar de carrinho no adversario\n42:00 2T25Lucas Pereira Ramires Constante Juventude/RS\nMotivo: A1.24.  Outro motivo (somente neste caso, abriria um campo livre para o árbitro digitar o que quiser) - Por tocar a mao na bola\nintencionalmente dentro da area penal, impedindo um chute a sua meta.\n11:00 2T89Cleber Bomfim de Jesus Ceará/CE\nMotivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Ao calçar o adversario.\n26:00 1T7Richardson Fernandes dos Santos Ceará/CE\nMotivo: A1.3.  Cometer uma falta tática para impedir um ataque promissor - Ao calçar o adversario.\n27:00 1T44Marcos Victor Ferreira da Silva Ceará/CE\nMotivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Ao calçar o adversario\n37:00 2T11Erick de Arruda Serafim Ceará/CE\nMotivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Dar uma entrada de carrinho no\nadversario.\n"
    dados_cartao_amarelo = limpar_dados_cartao_amarelos(text)
    assert len(dados_cartao_amarelo) == 8
