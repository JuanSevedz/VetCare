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
    eliminar_mascota
)


router = APIRouter(
    prefix="/mascotas",
    tags=["Mascotas"]
)


@router.get(
    "/",
    response_model=list[MascotaResponse]
)
def obtener_mascotas(db: Session = Depends(get_db)):
    return listar_mascotas(db)


@router.get(
    "/{mascota_id}",
    response_model=MascotaResponse
)
def obtener_mascota(
    mascota_id: str,
    db: Session = Depends(get_db)
):
    mascota = buscar_mascota(db, mascota_id)

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
    db: Session = Depends(get_db)
):
    return registrar_mascota(db, mascota)

@router.put(
    "/{mascota_id}",
    response_model=MascotaResponse
)
def modificar_mascota(
    mascota_id: str,
    mascota: MascotaUpdate,
    db: Session = Depends(get_db)
):
    resultado = actualizar_mascota(
        db,
        mascota_id,
        mascota
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
    db: Session = Depends(get_db)
):
    resultado = eliminar_mascota(
        db,
        mascota_id
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Mascota no encontrada"
        )