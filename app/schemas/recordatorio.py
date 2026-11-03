from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EstadoRecordatorio = Literal[
    "Pendiente",
    "Completado",
    "Cancelado",
]


class RecordatorioCreate(BaseModel):
    categoria: str = Field(
        min_length=1,
        max_length=100,
    )
    fecha: date
    descripcion: str = Field(
        min_length=1,
        max_length=300,
    )
    estado: EstadoRecordatorio = "Pendiente"


class RecordatorioUpdate(BaseModel):
    categoria: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    fecha: date | None = None
    descripcion: str | None = Field(
        default=None,
        min_length=1,
        max_length=300,
    )
    estado: EstadoRecordatorio | None = None


class RecordatorioResponse(BaseModel):
    id: str
    id_mascota: str
    categoria: str
    fecha: date
    descripcion: str
    estado: EstadoRecordatorio

    model_config = ConfigDict(from_attributes=True)