from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    correo: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    contrasena: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    telefono: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )
