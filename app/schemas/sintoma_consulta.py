from pydantic import BaseModel, ConfigDict, Field


class SintomaConsultaCreate(BaseModel):
    sintoma: str = Field(min_length=1, max_length=200)


class SintomaConsultaResponse(BaseModel):
    id: str
    id_consulta: str
    sintoma: str

    model_config = ConfigDict(from_attributes=True)