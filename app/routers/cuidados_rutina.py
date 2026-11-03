from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.cuidados_rutina import (
    CuidadoRutinaCreate,
    CuidadoRutinaUpdate,
    CuidadoRutinaResponse,
)

from app.services.cuidados_rutina_service import (
    listar_cuidados,
    buscar_cuidado,
    registrar_cuidado,
    modificar_cuidado,
)


router = APIRouter(tags=["Cuidados y rutinas"])


@router.get(
    "/mascotas/{mascota_id}/cuidados",
    response_model=list[CuidadoRutinaResponse],
)
def obtener_cuidados(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_cuidados(db, mascota_id, usuario)


@router.get(
    "/cuidados/{cuidado_id}",
    response_model=CuidadoRutinaResponse,
)
def obtener_cuidado(
    cuidado_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return buscar_cuidado(db, cuidado_id, usuario)


@router.post(
    "/mascotas/{mascota_id}/cuidados",
    response_model=CuidadoRutinaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_cuidado_endpoint(
    mascota_id: str,
    datos: CuidadoRutinaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("VETERINARIO", "ADMIN")),
):
    return registrar_cuidado(
        db,
        mascota_id,
        datos,
        usuario,
    )


@router.patch(
    "/cuidados/{cuidado_id}",
    response_model=CuidadoRutinaResponse,
)
def actualizar_cuidado_endpoint(
    cuidado_id: str,
    datos: CuidadoRutinaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("VETERINARIO", "ADMIN")),
):
    return modificar_cuidado(
        db,
        cuidado_id,
        datos,
        usuario,
    )