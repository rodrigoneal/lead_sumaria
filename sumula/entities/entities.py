from beanie import Document
from pydantic import BaseModel


class Jogo(BaseModel):
    campeonato: str
    rodada: int | str
    jogo: str
    data: str
    horario: str
    estadio: str
    mandante: str
    visitante: str
    ano: int
    jogo_num: int


class Arbitragem(BaseModel):
    funcao: str
    nome: str


class Cronologia1T(BaseModel):
    entrada_mandante: str
    atraso_mandante: str
    entrada_visitante: str
    atraso_visitante: str
    inicio: str
    atraso_inicio: str
    termino: str
    acrescimo: str
    resultado: str


class Cronologia2T(BaseModel):
    entrada_mandante: str
    atraso_mandante: str
    entrada_visitante: str
    atraso_visitante: str
    inicio: str
    atraso_inicio: str
    termino: str
    acrescimo: str
    resultado: str


class CronologiaPenalti(BaseModel):
    resultado: str | None = None


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
    penalti: CronologiaPenalti


class PrimeiraPagina(BaseModel):
    jogo: Jogo
    arbitragem: list[Arbitragem]
    cronologia: Cronologia
    escalacao: Escalacao


# Segunda Pagina


class ComissaoTecnica(BaseModel):
    cargo: str
    nome: str


class EquipeComissao(BaseModel):
    time: str
    comissao: list[ComissaoTecnica]


class Comissao(BaseModel):
    mandante: EquipeComissao
    visitante: EquipeComissao


class Gols(BaseModel):
    hora_gol: str
    tempo_jogo: str
    numero_jogador: str
    tipo_gol: str
    nome_jogador: str
    time: str


class CartoesAmarelo(BaseModel):
    hora_cartao: str
    tempo_jogo: str
    numero_jogador: str
    motivo: str
    nome_jogador: str
    time: str


class CartaoVermelho(BaseModel):
    hora_cartao: str
    tempo_jogo: str
    numero_jogador: str
    motivo: str
    nome_jogador: str
    time: str
    aplicado: str


class SegundaPagina(BaseModel):
    gols: list[Gols]
    cartoes_amarelo: list[CartoesAmarelo]
    cartoes_vermelho: list[CartaoVermelho]
    comissao: Comissao


# Terceira Pagina


class Ocorrencias(BaseModel):
    mensagem: str | None


class Acrescimo(BaseModel):
    mensagem: str


class Observacoes(BaseModel):
    mensagem: str


class Assistente(BaseModel):
    mensagem: str


class Substituicoes(BaseModel):
    hora_substituicao: str
    time: str
    tempo: str
    num_entrou: str
    num_saiu: str
    entrou: str
    saiu: str


class TerceiraPagina(BaseModel):
    ocorrencias: Ocorrencias
    acrescimos: Acrescimo
    observacao: Observacoes
    assistente: Assistente
    substituicao: list[Substituicoes]


class Sumula(Document):
    primeira_pagina: PrimeiraPagina
    segunda_pagina: SegundaPagina
    terceira_pagina: TerceiraPagina
    url_pdf: str

    def to_database(self):
        return {
            "ano": self.primeira_pagina.jogo.ano,
            "jogo": self.primeira_pagina.jogo.jogo_num,
        }
