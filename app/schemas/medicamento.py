from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class MedicamentoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    dosis: str = Field(min_length=1, max_length=100)
    frecuencia: str = Field(min_length=1, max_length=100)
    duracion: str = Field(min_length=1, max_length=100)
    fecha_inicio: date
    fecha_fin: date
    estado: str = "Activo"


class MedicamentoUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    dosis: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    frecuencia: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    duracion: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    estado: str | None = None


class MedicamentoResponse(BaseModel):
    id: str
    id_consulta: str
    nombre: str
    dosis: str
    frecuencia: str
    duracion: str
    fecha_inicio: date
    fecha_fin: date
    estado: str

    model_config = ConfigDict(from_attributes=True)
