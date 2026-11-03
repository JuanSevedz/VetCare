from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Cita(Base):
    __tablename__ = "citas"

    __table_args__ = (
        CheckConstraint(
            "estado IN ('Pendiente', 'Confirmada', 'Atendida', 'Cancelada')",
            name="chk_citas_estado",
        ),
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)

    id_mascota: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("mascotas.id", name="fk_citas_mascota"),
        nullable=False,
    )

    id_veterinario: Mapped[str] = mapped_column(
        String(50),
        ForeignKey(
            "personal_veterinario.id_usuario",
            name="fk_citas_veterinario",
        ),
        nullable=False,
    )

    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    hora: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[str | None] = mapped_column(String(300), nullable=True)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)