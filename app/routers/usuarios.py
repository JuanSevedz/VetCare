from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import (
    listar_usuarios,
    buscar_usuario,
    registrar_usuario,
)
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get(
    "/",
    response_model=list[UsuarioResponse]
)
def obtener_usuarios(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return listar_usuarios(db)


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse
)
def obtener_usuario(
    usuario_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    usuario_encontrado = buscar_usuario(db, usuario_id)

    if usuario_encontrado is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario_encontrado


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=201
)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    return registrar_usuario(db, usuario)