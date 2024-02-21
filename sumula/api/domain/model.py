from datetime import datetime

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Classe base para criar tabelas.

    Args:
        DeclarativeBase (DeclarativeBase): Classe base do SQLAlchemy
    """

    pass


class AuthenticationModel(Base):
    __tablename__ = "adm_clients"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_account = Column(Integer, nullable=False)
    codigo_cliente = Column(String(255))
    razao_social = Column(String(255))
    nick_name = Column(String(255))
    cnpj = Column(String(255))
    tipo_empresa = Column(String(255))
    uf = Column(String(255))
    chave_api_1 = Column(String(255))
    chave_api_2 = Column(String(255))
    chave_api_3 = Column(String(255))
    codigo_generico_1 = Column(String(255))
    codigo_generico_2 = Column(String(255))
    modules = Column(JSON)
    subModules = Column(JSON)
    status = Column(Boolean)
    created_by = Column(String(255))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
