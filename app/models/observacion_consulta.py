from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ObservacionConsulta(Base):
    __tablename__ = "observaciones_consulta"

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    id_consulta: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("consultas.id"),
        nullable=False,
    )

    observacion: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )