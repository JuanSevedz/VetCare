from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class SintomaConsulta(Base):
    __tablename__ = "sintomas_consulta"

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    id_consulta: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("consultas.id"),
        nullable=False,
    )

    sintoma: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )