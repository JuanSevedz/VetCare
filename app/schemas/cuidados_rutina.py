from pydantic import BaseModel, ConfigDict, Field


class CuidadoRutinaCreate(BaseModel):
    tipo: str = Field(min_length=1, max_length=100)
    frecuencia: str = Field(min_length=1, max_length=100)
    horario: str = Field(min_length=1, max_length=50)
    notas: str | None = Field(default=None, max_length=500)


class CuidadoRutinaUpdate(BaseModel):
    tipo: str | None = Field(default=None, min_length=1, max_length=100)
    frecuencia: str | None = Field(default=None, min_length=1, max_length=100)
    horario: str | None = Field(default=None, min_length=1, max_length=50)
    notas: str | None = Field(default=None, max_length=500)


class CuidadoRutinaResponse(BaseModel):
    id: str
    id_mascota: str
    tipo: str
    frecuencia: str
    horario: str
    notas: str | None = None

    model_config = ConfigDict(from_attributes=True)