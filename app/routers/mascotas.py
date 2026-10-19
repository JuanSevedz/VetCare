from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

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


router = APIRouter(
    prefix="/mascotas",
    tags=["Mascotas"]
)


@router.get("/", response_model=list[MascotaResponse])
def obtener_mascotas(
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO", "ADMIN"))
):
    propietario_id = (
        None if usuario["rol"] == "ADMIN"
        else usuario["id"]
    )

    return listar_mascotas(db, propietario_id)


@router.get("/{mascota_id}", response_model=MascotaResponse)
def obtener_mascota(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO", "ADMIN"))
):
    propietario_id = (
        None if usuario["rol"] == "ADMIN"
        else usuario["id"]
    )

    mascota = buscar_mascota(
        db,
        mascota_id,
        propietario_id
    )

    if mascota is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada"
        )

    return mascota


@router.post(
    "/",
    response_model=MascotaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_mascota(
    mascota: MascotaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO"))
):
    return registrar_mascota(
        db,
        mascota,
        usuario["id"]
    )


@router.put("/{mascota_id}", response_model=MascotaResponse)
def modificar_mascota(
    mascota_id: str,
    mascota: MascotaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO", "ADMIN"))
):
    propietario_id = (
        None if usuario["rol"] == "ADMIN"
        else usuario["id"]
    )

    resultado = actualizar_mascota(
        db,
        mascota_id,
        mascota,
        propietario_id
    )

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Mascota no encontrada o no se enviaron "
                "datos para actualizar"
            )
        )

    return resultado


@router.delete(
    "/{mascota_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def borrar_mascota(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO", "ADMIN"))
):
    propietario_id = (
        None if usuario["rol"] == "ADMIN"
        else usuario["id"]
    )

    resultado = eliminar_mascota(
        db,
        mascota_id,
        propietario_id
    )

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada"
        )

    return None