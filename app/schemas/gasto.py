from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class GastoCreate(BaseModel):
    fecha: date
    categoria: str = Field(min_length=1, max_length=100)
    descripcion: str = Field(min_length=1, max_length=300)
    valor: float = Field(gt=0)


class GastoUpdate(BaseModel):
    fecha: date | None = None
    categoria: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    descripcion: str | None = Field(
        default=None,
        min_length=1,
        max_length=300,
    )
    valor: float | None = Field(default=None, gt=0)


class GastoResponse(BaseModel):
    id: str
    id_mascota: str
    fecha: date
    categoria: str
    descripcion: str
    valor: float

    model_config = ConfigDict(from_attributes=True)