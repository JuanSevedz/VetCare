from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    correo: str = Field(min_length=3, max_length=150)
    contrasena: str = Field(min_length=1, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
