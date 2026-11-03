from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class HistoriaClinicaCreate(BaseModel):
    id_mascota: str = Field(min_length=1, max_length=50)


class HistoriaClinicaResponse(BaseModel):
    id: str
    id_mascota: str
    fecha_creacion: date

    model_config = ConfigDict(from_attributes=True)