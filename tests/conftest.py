import pytest


@pytest.fixture
def primeira_pagina():
    return """     
    Jogo: 378 CBF - CONFEDERAÇÃO BRASILEIRA DE FUTEBOL
    SÚMULA ON-LINE
    Campeonato: Campeonato Brasileiro - Série A/2023 Rodada: 38 
    Jogo: Coritiba S.a.f. / PR X Corinthians / SP
    Data: 06/12/2023 Horário: 21:30 Estádio: Major Antônio Couto Pereira / Curitiba
    Arbitragem
    Arbitro: Jonathan Benkenstein Pinheiro (CD / RS)
    Arbitro Assistente 1: Tiago Augusto Kappes Diel (AB / RS)
    Arbitro Assistente 2: Maira Mastella Moreira (AB / RS)
    Quarto Arbitro: Ivan da Silva Guimaraes Junior (AB / AM)
    Assessor: Ana Karina Marques Valentin (CBF / PE)
    Quinto Arbitro: Ivan Carlos Bohn (MTR / PR)
    Delegado Local: Eduardo Senna (CBF / PR)
    VAR: Daniel Nobre Bins (VAR-FIFA / RS)
    AVAR2: Bruno Arleu de Araujo (FIFA / RJ)
    Observador de VAR: Hilton Moutinho Rodrigues (CBF / RJ)
    AVAR: Andre da Silva Bitencourt (AB / RS)
    Cronologia
    1º Tempo
    Entrada do mandante: 21:20     Atraso: Não Houve
    Entrada do visitante: 21:20     Atraso: Não Houve
    Início 1º Tempo: 21:32     Atraso: 2 min
    Término do 1º Tempo: 22:20     Acréscimo: 3 min2º Tempo
    Entrada do mandante: 22:33     Atraso: Não Houve
    Entrada do visitante: 22:33     Atraso: Não Houve
    Início do 2º Tempo: 22:40     Atraso: 5 min
    Término do 2º Tempo: 23:28     Acréscimo: 3 min
    Resultado do 1º Tempo: 0 X 2     Resultado Final: 0 X 2     
    Relação de Jogadores
    Coritiba S.a.f. / PR
    NºApelido Nome Completo T/RP/A CBF
    72Pedro Morisco Pedro Luccas Morisco ... T(g)P613263
    7Andrey Andrey Ramos do Nasc ... TP404816
    8Willian Fa ... Willian Roberto de Farias TP180083
    14Thalisson  ... Thalisson Gabriel Pe ... TP552216
    16Natanael M ... Natanael Moreira Milouski TP559812
    19Sebastian  ... Sebastian Gomez Londono TP820851
    20Gabriel Silva Gabriel Silva Azeved ... TP590905
    37Kaio Lima Kaio Cesar Andrade Lima TP628499
    55Thiago Dom ... Thiago Dombroski Moreira TP519381
    83Jamerson Jamerson Santos de Jesus TP528144
    99Edu Eduardo Nascimento d ... TP307405
    27Luan Polli Luan Polli Gomes R(g)P338625
    2Hayner Hayner Willian Monja ... RP402405
    4Reynaldo Reynaldo Cesar Moraes RP352000
    5Mauricio Mauricio de Carvalho ... RP292608
    10Marcelino  ... Damian Marcelino Moreno RP793722
    12Marcão Marco Antonio Amorim ... RP525004
    17Matheus Matheus Henrique Bianqui RP581520
    25Jorge Vini ... Jorge Vinicius Ribei ... RP606028
    29Diogo Batista Diogo Batista de Souza RP613494
    47Jean Jean Henrique Carnei ... RP610578
    77Eberth Eberth Araujo Nogueira RP609955
    98LUCAS RONIER Lucas Ronier Vieira Pires RP645961Corinthians / SP
    NºApelido Nome Completo T/RP/A CBF
    22Carlos Carlos Miguel dos Sa ... T(g)P534596
    4Gil Carlos Gilberto do N ... TP178854
    5Fausto Fausto Mariano Vera TP776923
    9Yuri Alberto Yuri Alberto Monteir ... TP436395
    11Angel Romero Angel Rodrigo Romero ... TP507462
    14Caetano Joao Victor Andrade  ... TP310842
    21Matheus Bidu Matheus Lima Beltrao ... TP502230
    23Fagner Fagner Conserva Lemos TP177050
    24Cantillo Victor Danilo Cantil ... TP691641
    26Guilherme  ... Guilherme Sucigan Ma ... TP629792
    30Matheus Ar ... Matheus de Araujo Andrade TP545392
    32Matheus Do ... Matheus Planelles Donelli R(g)P541820
    2Rafael Ramos Rafael Antonio Figue ... RP757386
    13Léo Mana Leonardo Mana Hernandes RP620577
    17Giovane Na ... Giovane Santana do N ... RP582628
    25Bruno Mendez Bruno Mendez Cittadini RP648335
    27Pedrinho Pedro Henrique Silva ... RP697315
    33RUAN Ruan de Oliveira Ferreira RP626986
    36Wesley Wesley Gassova Ribei ... RP686457
    41Felipe Aug ... Felipe Augusto da Silva RP529019
    47Joao Pedro Joao Pedro de Sousa  ... RP615235
    T = Titular | R = Reserva | P = Profissional | A = Amador | (g) = Goleiro 
    Confederação Brasileira de Futebol Publicação da Súmula: 07/12/2023 00:52 Emissão desta via: 07/12/2023 00:52 Página 1/3
                                1 / 3
    """

@pytest.fixture
def segunda_pagina():
    return """
 Comissão Técnica
Ceará / CE
Assistente Técnico: Juliano Roberto Antonello
Assistente Técnico: Alcino Rodrigues Lima
Médico: Pedro Guilme Teixeira De Sousa Filho
Treinador De Goleiros: Everaldo Goncalves Santana
Preparador Físico: Edy Carlos Toporowicz Soares
Fisioterapeuta: Joao Paulo Cavalcante FrotaJuventude / RS
Técnico: Celso Juarez Roth
Assistente Técnico: Humberto Gomes Ferreira
Médico: Alexandre Schio Fay
Treinador De Goleiros: Marcio Rodrigo Angonese
Preparador Físico: Marcos Galgaro
Massagista: Cleber Willian Fernandes
Gols
Tempo 1T/2T NºTipoNome do Jogador Equipe
23:00 1T89NRCleber Bomfim de Jesus Ceará/CE
+1 1T34CTVitor Mendes Alves Juventude/RS
06:00 2T77NRGuilherme Parede Pinheiro Juventude/RS
24:00 2T8NRFernando Pereira do Nascimento Ceará/CE
43:00 2T11PNErick de Arruda Serafim Ceará/CE
NR = Normal | PN = Pênalti | CT = Contra | FT = Falta
Cartões Amarelos
Tempo 1T/2TNºNome do Jogador Equipe
24:00 1T26Luis Felipe Rebelo Costa Juventude/RS
Motivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Ao calçar o adversario
28:00 2T20Onitlasi Junior de Moraes Rodrigues Juventude/RS
Motivo: A2.  Desaprovar com palavras ou gestos as decisões da arbitragem  - Por reclamacao contra arbitragem.
29:00 2T77Guilherme Parede Pinheiro Juventude/RS
Motivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Ao entrar de carrinho no adversario
42:00 2T25Lucas Pereira Ramires Constante Juventude/RS
Motivo: A1.24.  Outro motivo (somente neste caso, abriria um campo livre para o árbitro digitar o que quiser) - Por tocar a mao na bola
intencionalmente dentro da area penal, impedindo um chute a sua meta.
11:00 2T89Cleber Bomfim de Jesus Ceará/CE
Motivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Ao calçar o adversario.
26:00 1T7Richardson Fernandes dos Santos Ceará/CE
Motivo: A1.3.  Cometer uma falta tática para impedir um ataque promissor - Ao calçar o adversario.
27:00 1T44Marcos Victor Ferreira da Silva Ceará/CE
Motivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Ao calçar o adversario
37:00 2T11Erick de Arruda Serafim Ceará/CE
Motivo: A1.13.  Dar uma entrada contra um adversário de maneira temerária na disputa da bola - Dar uma entrada de carrinho no
adversario.
Cartões Vermelhos
NÃO HOUVE EXPULSÕES
Confederação Brasileira de Futebol Publicação da Súmula: 13/11/2022 19:18 Emissão desta via: 13/11/2022 19:18 Página 2/3
                               2 / 3
    """
