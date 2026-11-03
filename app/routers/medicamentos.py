from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.medicamento import (
    MedicamentoCreate,
    MedicamentoUpdate,
    MedicamentoResponse,
)

from app.services.medicamento_service import (
    listar_medicamentos_consulta,
    obtener_medicamento,
    registrar_medicamento,
    modificar_medicamento,
)


router = APIRouter(
    tags=["Medicamentos formulados"],
)


# ============================================================
# MEDICAMENTOS POR CONSULTA
# ============================================================

@router.get(
    "/consultas/{consulta_id}/medicamentos",
    response_model=list[MedicamentoResponse],
)
def obtener_medicamentos_consulta(
    consulta_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_medicamentos_consulta(
        db,
        consulta_id,
        usuario,
    )


@router.post(
    "/consultas/{consulta_id}/medicamentos",
    response_model=MedicamentoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_medicamento_consulta(
    consulta_id: str,
    datos: MedicamentoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("VETERINARIO", "ADMIN")
    ),
):
    return registrar_medicamento(
        db,
        consulta_id,
        datos.model_dump(),
        usuario,
    )


# ============================================================
# MEDICAMENTO INDIVIDUAL
# ============================================================

@router.get(
    "/medicamentos/{medicamento_id}",
    response_model=MedicamentoResponse,
)
def obtener_medicamento_id(
    medicamento_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return obtener_medicamento(
        db,
        medicamento_id,
        usuario,
    )


@router.patch(
    "/medicamentos/{medicamento_id}",
    response_model=MedicamentoResponse,
)
def actualizar_medicamento_id(
    medicamento_id: str,
    datos: MedicamentoUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("VETERINARIO", "ADMIN")
    ),
):
    return modificar_medicamento(
        db,
        medicamento_id,
        datos.model_dump(exclude_unset=True),
        usuario,
    )