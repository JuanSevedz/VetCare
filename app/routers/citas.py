from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.cita import CitaCreate, CitaUpdate, CitaResponse
from app.services.cita_service import (
    listar_citas,
    buscar_cita,
    registrar_cita,
    modificar_cita,
)


router = APIRouter(
    prefix="/citas",
    tags=["Citas"],
)


@router.get(
    "/",
    response_model=list[CitaResponse],
)
def obtener_citas(
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_citas(db, usuario)


@router.get(
    "/{cita_id}",
    response_model=CitaResponse,
)
def obtener_cita(
    cita_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    cita = buscar_cita(db, cita_id, usuario)

    if cita is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada",
        )

    return cita


@router.post(
    "/",
    response_model=CitaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_cita(
    cita: CitaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO", "ADMIN")),
):
    return registrar_cita(db, cita, usuario)


@router.patch(
    "/{cita_id}",
    response_model=CitaResponse,
)
def actualizar_cita(
    cita_id: str,
    cita: CitaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return modificar_cita(
        db,
        cita_id,
        cita,
        usuario,
    )