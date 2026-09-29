from pydantic import BaseModel, ConfigDict, Field


class UsuarioCreate(BaseModel):
    id: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=100)
    correo: str = Field(min_length=3, max_length=150)
    contrasena: str = Field(min_length=8, max_length=72)
    telefono: str | None = Field(default=None, max_length=30)


class UsuarioResponse(BaseModel):
    id: str
    nombre: str
    correo: str
    telefono: str | None = None

    model_config = ConfigDict(from_attributes=True)