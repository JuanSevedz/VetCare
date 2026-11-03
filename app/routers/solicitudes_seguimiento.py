from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.solicitud_seguimiento import (
    SolicitudSeguimientoCreate,
    SolicitudSeguimientoUpdate,
    SolicitudSeguimientoResponse,
)

from app.services.solicitud_seguimiento_service import (
    listar_solicitudes,
    buscar_solicitud,
    registrar_solicitud,
    modificar_solicitud,
)


router = APIRouter(tags=["Solicitudes de seguimiento"])


@router.get(
    "/mascotas/{mascota_id}/solicitudes-seguimiento",
    response_model=list[SolicitudSeguimientoResponse],
)
def obtener_solicitudes(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_solicitudes(
        db,
        mascota_id,
        usuario,
    )


@router.get(
    "/solicitudes-seguimiento/{solicitud_id}",
    response_model=SolicitudSeguimientoResponse,
)
def obtener_solicitud(
    solicitud_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return buscar_solicitud(
        db,
        solicitud_id,
        usuario,
    )


@router.post(
    "/mascotas/{mascota_id}/solicitudes-seguimiento",
    response_model=SolicitudSeguimientoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_solicitud_endpoint(
    mascota_id: str,
    datos: SolicitudSeguimientoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("PROPIETARIO")),
):
    return registrar_solicitud(
        db,
        mascota_id,
        datos,
        usuario,
    )


@router.patch(
    "/solicitudes-seguimiento/{solicitud_id}",
    response_model=SolicitudSeguimientoResponse,
)
def actualizar_solicitud_endpoint(
    solicitud_id: str,
    datos: SolicitudSeguimientoUpdate,
    db: Session = Depends(
        get_db
    ),
    usuario=Depends(
        require_role("VETERINARIO", "ADMIN")
    ),
):
    return modificar_solicitud(
        db,
        solicitud_id,
        datos,
        usuario,
    )