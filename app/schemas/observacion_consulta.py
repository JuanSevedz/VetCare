from pydantic import BaseModel, ConfigDict, Field


class ObservacionConsultaCreate(BaseModel):
    observacion: str = Field(min_length=1, max_length=500)


class ObservacionConsultaResponse(BaseModel):
    id: str
    id_consulta: str
    observacion: str

    model_config = ConfigDict(from_attributes=True)