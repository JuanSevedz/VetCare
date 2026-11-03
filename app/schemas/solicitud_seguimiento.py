from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EstadoSolicitud = Literal[
    "Pendiente",
    "En proceso",
    "Atendida",
    "Cancelada",
]


class SolicitudSeguimientoCreate(BaseModel):
    descripcion: str = Field(min_length=1, max_length=500)


class SolicitudSeguimientoUpdate(BaseModel):
    estado: EstadoSolicitud


class SolicitudSeguimientoResponse(BaseModel):
    id: str
    id_propietario: str
    id_mascota: str
    fecha: date
    descripcion: str
    estado: EstadoSolicitud

    model_config = ConfigDict(from_attributes=True)