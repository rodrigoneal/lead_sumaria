from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UniqueConstraint


class Base(DeclarativeBase):
    """
    Classe base para criar tabelas.

    Args:
        DeclarativeBase (DeclarativeBase): Classe base do SQLAlchemy
    """

    pass

class AgendamentoModel(Base):
    """
    Tabela de agendamento de partidas.

    Args:
        Base (DeclarativeBase): Classe base do SQLAlchemy
    """

    __tablename__ = "agendamento"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[datetime] = mapped_column(nullable=False)
    jogo: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default="pendente")

    __table_args__ = (
        UniqueConstraint('data', 'jogo', name='uq_data_jogo'),
    )