from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.mascota import (
    MascotaCreate,
    MascotaUpdate,
    MascotaResponse,
)
from app.services.mascota_service import (
    listar_mascotas,
    buscar_mascota,
    registrar_mascota,
    actualizar_mascota,
    eliminar_mascota,
)
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/mascotas",
    tags=["Mascotas"]
)


@router.get(
    "/",
    response_model=list[MascotaResponse]
)
def obtener_mascotas(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return listar_mascotas(
        db,
        usuario["id"]
    )


@router.get(
    "/{mascota_id}",
    response_model=MascotaResponse
)
def obtener_mascota(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    mascota = buscar_mascota(
        db,
        mascota_id,
        usuario["id"]
    )

    if mascota is None:
        raise HTTPException(
            status_code=404,
            detail="Mascota no encontrada"
        )

    return mascota


@router.post(
    "/",
    response_model=MascotaResponse,
    status_code=201
)
def crear_mascota(
    mascota: MascotaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return registrar_mascota(
        db,
        mascota,
        usuario["id"]
    )


@router.put(
    "/{mascota_id}",
    response_model=MascotaResponse
)
def modificar_mascota(
    mascota_id: str,
    mascota: MascotaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    resultado = actualizar_mascota(
        db,
        mascota_id,
        mascota,
        usuario["id"]
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Mascota no encontrada o no se enviaron datos para actualizar"
        )

    return resultado


@router.delete(
    "/{mascota_id}",
    status_code=204
)
def borrar_mascota(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    resultado = eliminar_mascota(
        db,
        mascota_id,
        usuario["id"]
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Mascota no encontrada"
        )