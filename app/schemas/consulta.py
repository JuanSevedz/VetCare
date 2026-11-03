from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ConsultaCreate(BaseModel):
    id_historia_clinica: str = Field(
        min_length=1,
        max_length=50,
    )

    id_cita: str = Field(
        min_length=1,
        max_length=50,
    )

    fecha: date

    motivo: str = Field(
        min_length=1,
        max_length=300,
    )

    diagnostico: str = Field(
        min_length=1,
        max_length=500,
    )

    tratamiento: str = Field(
        min_length=1,
        max_length=500,
    )


class ConsultaUpdate(BaseModel):
    diagnostico: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )

    tratamiento: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )


class ConsultaResponse(BaseModel):
    id: str
    id_historia_clinica: str
    id_veterinario: str
    id_cita: str
    fecha: date
    motivo: str
    diagnostico: str
    tratamiento: str

    model_config = ConfigDict(from_attributes=True)