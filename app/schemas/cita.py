from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


EstadoCita = Literal[
    "Pendiente",
    "Confirmada",
    "Atendida",
    "Cancelada",
]


class CitaCreate(BaseModel):
    id_mascota: str = Field(min_length=1, max_length=50)
    id_veterinario: str = Field(min_length=1, max_length=50)
    fecha: date
    hora: str = Field(min_length=1, max_length=20)
    motivo: str | None = Field(default=None, max_length=300)

    @field_validator("hora")
    @classmethod
    def validar_hora(cls, valor: str) -> str:
        valor = valor.strip()

        try:
            hora_validada = time.fromisoformat(valor)
        except ValueError:
            raise ValueError("La hora debe tener un formato válido HH:MM")

        if hora_validada.second != 0 or hora_validada.microsecond != 0:
            raise ValueError("La hora debe especificarse en formato HH:MM")

        return hora_validada.strftime("%H:%M")
    
    @model_validator(mode="after")
    def validar_fecha_futura(self):
        from datetime import date

        if self.fecha < date.today():
            raise ValueError("La fecha de la cita no puede estar en el pasado")

        return self


class CitaUpdate(BaseModel):
    fecha: date | None = None
    hora: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )
    motivo: str | None = Field(
        default=None,
        max_length=300,
    )
    estado: EstadoCita | None = None
    id_veterinario: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    @field_validator("hora")
    @classmethod
    def validar_hora(cls, valor: str | None) -> str | None:
        if valor is None:
            return None

        valor = valor.strip()

        try:
            hora_validada = time.fromisoformat(valor)
        except ValueError:
            raise ValueError("La hora debe tener un formato válido HH:MM")

        if hora_validada.second != 0 or hora_validada.microsecond != 0:
            raise ValueError("La hora debe especificarse en formato HH:MM")

        return hora_validada.strftime("%H:%M")


class CitaResponse(BaseModel):
    id: str
    id_mascota: str
    id_veterinario: str
    fecha: date
    hora: str
    motivo: str | None
    estado: EstadoCita

    model_config = ConfigDict(from_attributes=True)