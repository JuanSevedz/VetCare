from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.auth import crear_access_token
from app.core.security import verify_password
from app.repositories.usuario_repository import (
    obtener_usuario_por_correo,
)


def autenticar_usuario(
    db: Session,
    correo: str,
    contrasena: str
):
    usuario = obtener_usuario_por_correo(db, correo)

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    if not verify_password(
        contrasena,
        usuario["contrasena"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    token = crear_access_token(usuario["id"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }
