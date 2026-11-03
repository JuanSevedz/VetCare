from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.vacuna import (
    VacunaCreate,
    VacunaUpdate,
    VacunaResponse,
)

from app.services.vacuna_service import (
    listar_vacunas,
    buscar_vacuna,
    registrar_vacuna,
    modificar_vacuna,
)


router = APIRouter(tags=["Vacunas"])


@router.get(
    "/mascotas/{mascota_id}/vacunas",
    response_model=list[VacunaResponse],
)
def obtener_vacunas(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO", "VETERINARIO", "ADMIN")),
):
    return listar_vacunas(db, mascota_id, usuario)


@router.get(
    "/vacunas/{vacuna_id}",
    response_model=VacunaResponse,
)
def obtener_vacuna(
    vacuna_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO", "VETERINARIO", "ADMIN")),
):
    return buscar_vacuna(db, vacuna_id, usuario)


@router.post(
    "/mascotas/{mascota_id}/vacunas",
    response_model=VacunaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_vacuna(
    mascota_id: str,
    datos: VacunaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("VETERINARIO", "ADMIN")),
):
    return registrar_vacuna(db, mascota_id, datos, usuario)


@router.patch(
    "/vacunas/{vacuna_id}",
    response_model=VacunaResponse,
)
def actualizar_vacuna(
    vacuna_id: str,
    datos: VacunaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("VETERINARIO", "ADMIN")),
):
    return modificar_vacuna(db, vacuna_id, datos, usuario)