from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.repositories.usuario_repository import (
    obtener_usuarios,
    obtener_usuario_por_id,
    crear_usuario,
)


def listar_usuarios(db: Session):
    return obtener_usuarios(db)


def buscar_usuario(db: Session, usuario_id: str):
    return obtener_usuario_por_id(db, usuario_id)
def registrar_usuario(db: Session, usuario):
    usuario_data = usuario.model_dump()

    usuario_data["contrasena"] = hash_password(
        usuario_data["contrasena"]
    )

    return crear_usuario(db, usuario_data)