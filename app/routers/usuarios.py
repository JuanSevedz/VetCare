from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import get_current_user, require_role
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import (
    listar_usuarios,
    buscar_usuario,
    registrar_usuario,
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


# Consultar el perfil del usuario autenticado
@router.get("/me", response_model=UsuarioResponse)
def obtener_perfil_propio(
    usuario=Depends(get_current_user),
):
    return usuario


# Listar usuarios: solamente ADMIN
@router.get("/", response_model=list[UsuarioResponse])
def obtener_usuarios(
    db: Session = Depends(get_db),
    usuario=Depends(require_role("ADMIN")),
):
    return listar_usuarios(db)


# Consultar un usuario por ID: el propio usuario o ADMIN
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    if usuario["id"] != usuario_id and usuario["rol"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para consultar este usuario",
        )

    resultado = buscar_usuario(db, usuario_id)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return resultado


# Registro público: siempre crea un PROPIETARIO
@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
):
    return registrar_usuario(db, usuario)