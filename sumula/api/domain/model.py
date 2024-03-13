from datetime import datetime

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_column, registry


reg = registry()


@reg.mapped_as_dataclass
class AuthenticationModel:
    __tablename__ = "adm_clients"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    id_account: Mapped[int] = mapped_column(nullable=False)
    codigo_cliente: Mapped[int] = mapped_column(nullable=False)
    razao_social: Mapped[str] = mapped_column()
    nick_name: Mapped[str] = mapped_column()
    cnpj: Mapped[str] = mapped_column()
    tipo_empresa: Mapped[str] = mapped_column()
    uf: Mapped[str] = mapped_column()
    chave_api_1: Mapped[str] = mapped_column()
    chave_api_2: Mapped[str] = mapped_column()
    chave_api_3: Mapped[str] = mapped_column()
    codigo_generico_1: Mapped[str] = mapped_column()
    codigo_generico_2: Mapped[str] = mapped_column()
    modules: Mapped[dict | list] = mapped_column(JSON)
    subModules: Mapped[dict | list] = mapped_column(JSON)
    status: Mapped[bool] = mapped_column(nullable=False)
    created_by: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(init=False)
    updated_at: Mapped[datetime] = mapped_column(init=False)


@reg.mapped_as_dataclass
class SumulaModel:
    __tablename__ = "sumula"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    competicao: Mapped[str] = mapped_column()
    rodada: Mapped[int] = mapped_column()
    data: Mapped[str] = mapped_column()
    horario: Mapped[str] = mapped_column()
    estadio: Mapped[str] = mapped_column()
    mandante: Mapped[str] = mapped_column()
    visitante: Mapped[str] = mapped_column()
    ano: Mapped[int] = mapped_column()
    jogo_num: Mapped[int] = mapped_column()
    jogo: Mapped[dict] = mapped_column(JSON)
    arbitragem: Mapped[dict | list] = mapped_column(JSON)
    cronologia: Mapped[dict | list] = mapped_column(JSON)
    escalacao: Mapped[dict | list] = mapped_column(JSON)
    gols: Mapped[dict | list] = mapped_column(
        JSON, nullable=True
    )
    cartoes_amarelo: Mapped[dict | list] = mapped_column(JSON)
    cartoes_vermelho: Mapped[dict | list] = mapped_column(JSON)
    comissao: Mapped[dict | list] = mapped_column(JSON)
    ocorrencias: Mapped[dict | list] = mapped_column(JSON)
    acrescimos: Mapped[dict | list] = mapped_column(JSON)
    observacao: Mapped[dict | list] = mapped_column(JSON)
    assistente: Mapped[dict | list] = mapped_column(JSON)
    substituicao: Mapped[dict | list] = mapped_column(JSON)
    url_pdf: Mapped[str] = mapped_column()
   


    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, onupdate=func.now(), nullable=True)
