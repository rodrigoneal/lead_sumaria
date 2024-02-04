from pydantic import BaseModel


class Jogo(BaseModel):
    campeonato: str
    rodada: int
    jogo: str
    data: str
    horario: str
    estadio: str
    mandante: str
    visitante: str

class Arbitragem(BaseModel):
    funcao: str
    nome: str

class Cronologia1T(BaseModel):
    entrada_mandante: str
    atraso_mandante: str
    entrada_visitante: str
    atraso_visitante: str
    inicio:str
    atraso_inicio: str
    termino: str
    acrescimo: str
    resultado: str

class Cronologia2T(BaseModel):
    entrada_mandante: str
    atraso_mandante: str
    entrada_visitante: str
    atraso_visitante: str
    inicio:str
    atraso_inicio: str
    termino: str
    acrescimo: str
    resultado: str

class RelacaoJogadores(BaseModel):
    numero: int
    apelido: str
    nome: str
    t_r: str
    p_a: str
    cbf: str

class Equipe(BaseModel):
    time: str
    escalao: list[RelacaoJogadores]


class Escalacao(BaseModel):
    mandante: Equipe
    visitante: Equipe

class Cronologia(BaseModel):
    primeiro_tempo: Cronologia1T
    segundo_tempo: Cronologia2T

class PrimeiraPagina(BaseModel):
    jogo: Jogo
    arbitragem: list[Arbitragem]
    cronologia: Cronologia
    escalacao: Escalacao


class Sumula(BaseModel):
    campeonato: str
    rodada: str
    jogo: str
    data: str
    horario: str
    estadio: str
    mandante: str
    visitante: str
    arbitragem: list
    cronologia: list