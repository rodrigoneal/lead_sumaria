from typing import Annotated, Literal
from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field


class DadosTime(BaseModel):
    nome: str
    uf: str


class Jogo(BaseModel):
    competicao: str
    rodada: int | str
    jogo: str
    data: str
    horario: str
    estadio: str
    mandante: DadosTime
    visitante: DadosTime
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
    nome: Annotated[str, AfterValidator(lambda v: v.replace("...", "").strip())]
    t_r: Annotated[str, Field(alias="T/R", description="T=Titular, R=Reserva")]
    p_a: Annotated[str, Field(alias="P/A", description="P=Profissional, A=Amador")]
    cbf: str

    model_config = ConfigDict(populate_by_name=True)


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
    num_entrou: Annotated[int, BeforeValidator(lambda v: int(v))]
    num_saiu: Annotated[int, BeforeValidator(lambda v: int(v))]
    entrou: Annotated[str, BeforeValidator(lambda v: v.replace("...", "").strip())]
    saiu: Annotated[str, BeforeValidator(lambda v: v.replace("...", "").strip())]


class TerceiraPagina(BaseModel):
    ocorrencias: Ocorrencias
    acrescimos: Acrescimo
    observacao: Observacoes
    assistente: Assistente
    substituicao: list[Substituicoes]


class EventoBase(BaseModel):
    tipo: str
    tempo_jogo: str | None = None
    time: str | None = None

    model_config = ConfigDict(extra="allow")


class EventoGol(EventoBase):
    tipo: Literal["gol"] = "gol"
    hora: str = Field(alias="hora_gol")
    numero_jogador: Annotated[int, BeforeValidator(lambda v: int(v))]
    nome: str
    tipo_gol: str


def parser_numero_jogador(v: str) -> int | str:
    try:
        return int(v)
    except ValueError:
        return v


# Cartão Amarelo
class EventoCartaoAmarelo(EventoBase):
    tipo: Literal["cartao_amarelo"] = "cartao_amarelo"
    hora: str = Field(alias="hora_cartao")
    numero_jogador: Annotated[int | str, BeforeValidator(parser_numero_jogador)]
    nome: str
    motivo: str


# Cartão Vermelho
class EventoCartaoVermelho(EventoBase):
    tipo: Literal["cartao_vermelho"] = "cartao_vermelho"
    hora: str = Field(alias="hora_cartao")
    numero_jogador: Annotated[int | str, BeforeValidator(parser_numero_jogador)]
    nome: str
    motivo: str
    aplicado: str


# Substituição
class EventoSubstituicao(EventoBase):
    tipo: Literal["substituicao"] = "substituicao"
    hora: str = Field(alias="hora_substituicao")
    entrou: str
    saiu: str
    num_entrou: Annotated[int, BeforeValidator(lambda v: int(v))]
    num_saiu: Annotated[int, BeforeValidator(lambda v: int(v))]


class SumulaResponse(BaseModel):
    competicao: str
    rodada: int | str
    jogo: str
    data: str
    horario: str
    estadio: str
    mandante: DadosTime
    visitante: DadosTime
    ano: int
    jogo_num: int

    arbitragem: list[Arbitragem]
    cronologia: Cronologia
    escalacao: Escalacao

    # eventos unificados
    eventos: list[EventoBase]

    comissao: Comissao
    ocorrencias: Ocorrencias
    acrescimos: Acrescimo
    observacao: Observacoes
    assistente: Assistente
    url_pdf: str


class Sumula(BaseModel):
    primeira_pagina: PrimeiraPagina
    segunda_pagina: SegundaPagina
    terceira_pagina: TerceiraPagina
    url_pdf: str

    def get_eventos(self) -> list[EventoBase]:
        eventos = []

        # ======================
        # GOLS
        # ======================
        for g in self.segunda_pagina.gols:
            eventos.append(
                EventoGol(
                    hora_gol=g.hora_gol,
                    tempo_jogo=g.tempo_jogo,
                    numero_jogador=g.numero_jogador,
                    nome=g.nome_jogador,
                    tipo_gol=g.tipo_gol,
                    time=g.time,
                )
            )

        # ======================
        # CARTÕES AMARELOS
        # ======================
        for c in self.segunda_pagina.cartoes_amarelo:
            eventos.append(
                EventoCartaoAmarelo(
                    hora_cartao=c.hora_cartao,
                    tempo_jogo=c.tempo_jogo,
                    numero_jogador=c.numero_jogador,
                    nome=c.nome_jogador,
                    motivo=c.motivo,
                    time=c.time,
                )
            )

        # ======================
        # CARTÕES VERMELHOS
        # ======================
        for c in self.segunda_pagina.cartoes_vermelho:
            eventos.append(
                EventoCartaoVermelho(
                    hora_cartao=c.hora_cartao,
                    tempo_jogo=c.tempo_jogo,
                    numero_jogador=c.numero_jogador,
                    nome=c.nome_jogador,
                    motivo=c.motivo,
                    aplicado=c.aplicado,
                    time=c.time,
                )
            )

        # ======================
        # SUBSTITUIÇÕES
        # ======================
        for s in self.terceira_pagina.substituicao:
            eventos.append(
                EventoSubstituicao(
                    hora_substituicao=s.hora_substituicao,
                    tempo_jogo=s.tempo,
                    num_entrou=s.num_entrou,
                    num_saiu=s.num_saiu,
                    entrou=s.entrou,
                    saiu=s.saiu,
                    time=s.time,
                )
            )

        return eventos

    def to_database(self):
        database = self.primeira_pagina.model_dump()
        database.update(self.segunda_pagina.model_dump())
        database.update(self.terceira_pagina.model_dump())
        database.update(self.primeira_pagina.model_dump()["jogo"])
        database["url_pdf"] = self.url_pdf
        database["eventos"] = [e.model_dump() for e in self.get_eventos()]
        return database
