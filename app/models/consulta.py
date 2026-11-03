from datetime import date

from sqlalchemy import Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Consulta(Base):
    __tablename__ = "consultas"

    __table_args__ = (
        UniqueConstraint(
            "id_cita",
            name="uq_consultas_cita",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    id_historia_clinica: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("historias_clinicas.id"),
        nullable=False,
    )

    id_veterinario: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("personal_veterinario.id_usuario"),
        nullable=False,
    )

    id_cita: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("citas.id"),
        nullable=False,
    )

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    motivo: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    diagnostico: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    tratamiento: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )