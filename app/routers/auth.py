from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import autenticar_usuario


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    datos: LoginRequest,
    db: Session = Depends(get_db)
):
    return autenticar_usuario(
        db,
        datos.correo,
        datos.contrasena
    )
