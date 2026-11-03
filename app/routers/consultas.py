from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.auth import require_role

from app.schemas.consulta import (
    ConsultaCreate,
    ConsultaUpdate,
    ConsultaResponse,
)

from app.schemas.sintoma_consulta import (
    SintomaConsultaCreate,
    SintomaConsultaResponse,
)

from app.schemas.observacion_consulta import (
    ObservacionConsultaCreate,
    ObservacionConsultaResponse,
)

from app.services.consulta_service import (
    listar_consultas,
    buscar_consulta,
    registrar_consulta,
    modificar_consulta,
    listar_sintomas,
    registrar_sintoma,
    listar_observaciones,
    registrar_observacion,
)


router = APIRouter(
    prefix="/consultas",
    tags=["Consultas veterinarias"],
)


@router.get(
    "/",
    response_model=list[ConsultaResponse],
)
def obtener_consultas(
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_consultas(db, usuario)


@router.get(
    "/{consulta_id}",
    response_model=ConsultaResponse,
)
def obtener_consulta(
    consulta_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    consulta = buscar_consulta(
        db,
        consulta_id,
        usuario,
    )

    if consulta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta no encontrada",
        )

    return consulta


@router.post(
    "/",
    response_model=ConsultaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_consulta(
    datos: ConsultaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("VETERINARIO")
    ),
):
    return registrar_consulta(
        db,
        datos,
        usuario,
    )


@router.patch(
    "/{consulta_id}",
    response_model=ConsultaResponse,
)
def actualizar_consulta(
    consulta_id: str,
    datos: ConsultaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("VETERINARIO", "ADMIN")
    ),
):
    return modificar_consulta(
        db,
        consulta_id,
        datos,
        usuario,
    )


# ============================================================
# SÍNTOMAS
# ============================================================

@router.get(
    "/{consulta_id}/sintomas",
    response_model=list[SintomaConsultaResponse],
)
def obtener_sintomas(
    consulta_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_sintomas(
        db,
        consulta_id,
        usuario,
    )


@router.post(
    "/{consulta_id}/sintomas",
    response_model=SintomaConsultaResponse,
    status_code=status.HTTP_201_CREATED,
)
def agregar_sintoma(
    consulta_id: str,
    datos: SintomaConsultaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("VETERINARIO", "ADMIN")
    ),
):
    return registrar_sintoma(
        db,
        consulta_id,
        datos,
        usuario,
    )


# ============================================================
# OBSERVACIONES
# ============================================================

@router.get(
    "/{consulta_id}/observaciones",
    response_model=list[ObservacionConsultaResponse],
)
def obtener_observaciones(
    consulta_id: str,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("PROPIETARIO", "VETERINARIO", "ADMIN")
    ),
):
    return listar_observaciones(
        db,
        consulta_id,
        usuario,
    )


@router.post(
    "/{consulta_id}/observaciones",
    response_model=ObservacionConsultaResponse,
    status_code=status.HTTP_201_CREATED,
)
def agregar_observacion(
    consulta_id: str,
    datos: ObservacionConsultaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role("VETERINARIO", "ADMIN")
    ),
):
    return registrar_observacion(
        db,
        consulta_id,
        datos,
        usuario,
    )