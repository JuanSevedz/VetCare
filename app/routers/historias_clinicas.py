from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.historia_clinica import (
    HistoriaClinicaCreate,
    HistoriaClinicaResponse,
)

from app.services.historia_clinica_service import (
    listar_historias_clinicas,
    buscar_historia_clinica,
    registrar_historia_clinica,
)


router = APIRouter(
    prefix="/historias-clinicas",
    tags=["Historias clínicas"],
)


@router.get(
    "/",
    response_model=list[HistoriaClinicaResponse],
)
def obtener_historias_clinicas(
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_historias_clinicas(db, usuario)


@router.get(
    "/{historia_id}",
    response_model=HistoriaClinicaResponse,
)
def obtener_historia_clinica(
    historia_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    historia = buscar_historia_clinica(
        db,
        historia_id,
        usuario,
    )

    if historia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historia clínica no encontrada",
        )

    return historia


@router.post(
    "/",
    response_model=HistoriaClinicaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_historia_clinica(
    datos: HistoriaClinicaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "ADMIN")
    ),
):
    return registrar_historia_clinica(
        db,
        datos,
        usuario,
    )