from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EstadoVacuna = Literal["Aplicada", "Pendiente"]


class VacunaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    fecha_aplicacion: date
    fecha_proxima: date | None = None
    lote: str | None = Field(default=None, max_length=100)
    estado: EstadoVacuna = "Aplicada"
    id_veterinario: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )


class VacunaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    fecha_aplicacion: date | None = None
    fecha_proxima: date | None = None
    lote: str | None = Field(default=None, max_length=100)
    estado: EstadoVacuna | None = None


class VacunaResponse(BaseModel):
    id: str
    id_mascota: str
    id_veterinario: str
    nombre: str
    fecha_aplicacion: date
    fecha_proxima: date | None = None
    lote: str | None = None
    estado: EstadoVacuna

    model_config = ConfigDict(from_attributes=True)