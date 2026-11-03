from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.gasto import (
    GastoCreate,
    GastoUpdate,
    GastoResponse,
)

from app.services.gasto_service import (
    listar_gastos,
    buscar_gasto,
    registrar_gasto,
    modificar_gasto,
)


router = APIRouter(tags=["Gastos"])


@router.get(
    "/mascotas/{mascota_id}/gastos",
    response_model=list[GastoResponse],
)
def obtener_gastos(
    mascota_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_gastos(db, mascota_id, usuario)


@router.get(
    "/gastos/{gasto_id}",
    response_model=GastoResponse,
)
def obtener_gasto(
    gasto_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return buscar_gasto(db, gasto_id, usuario)


@router.post(
    "/mascotas/{mascota_id}/gastos",
    response_model=GastoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_gasto_endpoint(
    mascota_id: str,
    datos: GastoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("VETERINARIO", "ADMIN")),
):
    return registrar_gasto(
        db,
        mascota_id,
        datos,
        usuario,
    )


@router.patch(
    "/gastos/{gasto_id}",
    response_model=GastoResponse,
)
def actualizar_gasto_endpoint(
    gasto_id: str,
    datos: GastoUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_role("VETERINARIO", "ADMIN")),
):
    return modificar_gasto(
        db,
        gasto_id,
        datos,
        usuario,
    )