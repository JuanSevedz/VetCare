from datetime import date

from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Mascota(Base):
    __tablename__ = "mascotas"

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    id_propietario: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("propietarios.id_usuario"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    especie: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    raza: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    sexo: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    fecha_nacimiento: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    peso: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    microchip: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
