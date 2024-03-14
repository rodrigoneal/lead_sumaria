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
    razao_social: Mapped[str] = mapped_column(nullable=True)
    nick_name: Mapped[str] = mapped_column(nullable=True)
    cnpj: Mapped[str] = mapped_column(nullable=True)
    tipo_empresa: Mapped[str] = mapped_column(nullable=True)
    uf: Mapped[str] = mapped_column(nullable=True)
    chave_api_1: Mapped[str] = mapped_column(nullable=True)
    chave_api_2: Mapped[str] = mapped_column(nullable=True)
    chave_api_3: Mapped[str] = mapped_column(nullable=True)
    codigo_generico_1: Mapped[str] = mapped_column(nullable=True)
    codigo_generico_2: Mapped[str] = mapped_column(nullable=True)
    modules: Mapped[dict | list] = mapped_column(JSON, nullable=True)
    subModules: Mapped[dict | list] = mapped_column(JSON, nullable=True)
    status: Mapped[bool] = mapped_column(nullable=False)
    created_by: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )


@reg.mapped_as_dataclass
class SumulaModel:
    __tablename__ = "sumula"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    competicao: Mapped[str] = mapped_column()
    rodada: Mapped[str] = mapped_column()
    data: Mapped[str] = mapped_column()
    horario: Mapped[str] = mapped_column()
    estadio: Mapped[str] = mapped_column()
    mandante: Mapped[str] = mapped_column()
    visitante: Mapped[str] = mapped_column()
    ano: Mapped[int] = mapped_column()
    jogo_num: Mapped[int] = mapped_column()
    jogo: Mapped[str] = mapped_column(JSON)
    arbitragem: Mapped[list[dict[str, str]]] = mapped_column(JSON)
    cronologia: Mapped[dict[str, dict[str, str]]] = mapped_column(JSON)
    escalacao: Mapped[dict] = mapped_column(JSON)
    gols: Mapped[list[dict[str, str]] | list] = mapped_column(JSON, nullable=True)
    cartoes_amarelo: Mapped[list[dict] | list] = mapped_column(JSON)
    cartoes_vermelho: Mapped[list[dict] | list] = mapped_column(JSON)
    comissao: Mapped[dict] = mapped_column(JSON)
    ocorrencias: Mapped[dict[str, str]] = mapped_column(JSON)
    acrescimos: Mapped[dict[str, str]] = mapped_column(JSON)
    observacao: Mapped[dict[str, str]] = mapped_column(JSON)
    assistente: Mapped[dict[str, str]] = mapped_column(JSON)
    substituicao: Mapped[list[dict[str, str]]] = mapped_column(JSON)
    url_pdf: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )

@reg.mapped_as_dataclass
class Logs:
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    id_client: Mapped[int] = mapped_column()
    dh_chamada: Mapped[datetime] = mapped_column()
    dh_retorno: Mapped[datetime] = mapped_column()
    url_chamada: Mapped[str] = mapped_column()
    st_sucesso: Mapped[bool] = mapped_column()
    dados_retorno: Mapped[dict] = mapped_column(JSON)
    cd_ocorrencia: Mapped[int] = mapped_column()
    ds_erro: Mapped[str] = mapped_column()
    