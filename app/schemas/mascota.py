from datetime import date

from pydantic import BaseModel, Field


class MascotaCreate(BaseModel):
    id: str = Field(min_length=1, max_length=50)
    id_propietario: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=100)
    especie: str = Field(min_length=1, max_length=50)
    raza: str | None = Field(default=None, max_length=100)
    sexo: str | None = Field(default=None, max_length=30)
    fecha_nacimiento: date | None = None
    peso: float | None = Field(default=None, gt=0)
    microchip: str | None = Field(default=None, max_length=100)

class MascotaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    especie: str | None = Field(default=None, min_length=1, max_length=50)
    raza: str | None = Field(default=None, max_length=100)
    sexo: str | None = Field(default=None, max_length=30)
    fecha_nacimiento: date | None = None
    peso: float | None = Field(default=None, gt=0)
    microchip: str | None = Field(default=None, max_length=100)

class MascotaResponse(BaseModel):
    id: str
    id_propietario: str
    nombre: str
    especie: str
    raza: str | None = None
    sexo: str | None = None
    fecha_nacimiento: date | None = None
    peso: float | None = None
    microchip: str | None = None

    model_config = {
        "from_attributes": True
    }