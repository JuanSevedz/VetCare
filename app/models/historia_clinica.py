from datetime import date

from sqlalchemy import Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class HistoriaClinica(Base):
    __tablename__ = "historias_clinicas"

    __table_args__ = (
        UniqueConstraint(
            "id_mascota",
            name="uq_historias_clinicas_mascota",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    id_mascota: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("mascotas.id"),
        nullable=False,
    )

    fecha_creacion: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )