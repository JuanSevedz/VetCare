from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.recordatorio import (
    RecordatorioCreate,
    RecordatorioUpdate,
    RecordatorioResponse,
)

from app.services.recordatorio_service import (
    listar_recordatorios,
    buscar_recordatorio,
    registrar_recordatorio,
    modificar_recordatorio,
)


router = APIRouter(tags=["Recordatorios"])


@router.get(
    "/mascotas/{mascota_id}/recordatorios",
    response_model=list[RecordatorioResponse],
)
def obtener_recordatorios(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_recordatorios(db, mascota_id, usuario)


@router.get(
    "/recordatorios/{recordatorio_id}",
    response_model=RecordatorioResponse,
)
def obtener_recordatorio(
    recordatorio_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return buscar_recordatorio(db, recordatorio_id, usuario)


@router.post(
    "/mascotas/{mascota_id}/recordatorios",
    response_model=RecordatorioResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_recordatorio_endpoint(
    mascota_id: str,
    datos: RecordatorioCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("VETERINARIO", "ADMIN")),
):
    return registrar_recordatorio(
        db,
        mascota_id,
        datos,
        usuario,
    )


@router.patch(
    "/recordatorios/{recordatorio_id}",
    response_model=RecordatorioResponse,
)
def actualizar_recordatorio_endpoint(
    recordatorio_id: str,
    datos: RecordatorioUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("VETERINARIO", "ADMIN")),
):
    return modificar_recordatorio(
        db,
        recordatorio_id,
        datos,
        usuario,
    )