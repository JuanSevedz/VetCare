import logging

logger = logging.getLogger(__name__)

from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.cita_repository import (
    obtener_citas,
    obtener_cita_por_id,
    mascota_pertenece_a_propietario,
    veterinario_existe,
    existe_conflicto_cita,
    crear_cita,
    actualizar_cita as actualizar_cita_repository,
)

TRANSICIONES_CITA = {
    "Pendiente": {"Confirmada", "Cancelada"},
    "Confirmada": {"Atendida", "Cancelada"},
    "Atendida": set(),
    "Cancelada": set(),
}

def listar_citas(db: Session, usuario: dict):
    return obtener_citas(
        db,
        usuario["rol"],
        usuario["id"],
    )


def buscar_cita(
    db: Session,
    cita_id: str,
    usuario: dict,
):
    return obtener_cita_por_id(
        db,
        cita_id,
        usuario["rol"],
        usuario["id"],
    )


def registrar_cita(
    db: Session,
    datos,
    usuario: dict,
):
    datos_cita = datos.model_dump()

    if usuario["rol"] == "PROPIETARIO":
        pertenece = mascota_pertenece_a_propietario(
            db,
            datos_cita["id_mascota"],
            usuario["id"],
        )

        if not pertenece:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes solicitar citas para tus propias mascotas",
            )

    if not veterinario_existe(db, datos_cita["id_veterinario"]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El veterinario seleccionado no tiene un perfil válido",
        )
    if existe_conflicto_cita(
        db=db,
        id_mascota=datos_cita["id_mascota"],
        id_veterinario=datos_cita["id_veterinario"],
        fecha=datos_cita["fecha"],
        hora=datos_cita["hora"],
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La mascota o el veterinario ya tiene una cita activa en esa fecha y hora",
        )

    try:
        return crear_cita(db, datos_cita)

    except IntegrityError as error:
        logger.exception(
            "Error de integridad al registrar una cita"
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo registrar la cita por un conflicto con los datos",
        ) from error


def modificar_cita(
    db: Session,
    cita_id: str,
    datos,
    usuario: dict,
):
    cita_actual = buscar_cita(db, cita_id, usuario)

    if cita_actual is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada",
        )

    cambios = datos.model_dump(exclude_unset=True)
    if "fecha" in cambios and cambios["fecha"] is not None:
        if cambios["fecha"] < date.today():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La fecha de la cita no puede estar en el pasado",
            )
    if not cambios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar",
        )

    rol = usuario["rol"]
    if "estado" in cambios:
        estado_actual = cita_actual["estado"]
        estado_nuevo = cambios["estado"]

        if estado_nuevo != estado_actual:
            estados_permitidos = TRANSICIONES_CITA.get(
                estado_actual,
                set(),
            )

            if estado_nuevo not in estados_permitidos:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"No se permite cambiar el estado "
                        f"de '{estado_actual}' a '{estado_nuevo}'"
                    ),
                )

    if rol == "PROPIETARIO":
        campos_permitidos = {"fecha", "hora", "motivo", "estado"}

        if not set(cambios).issubset(campos_permitidos):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes cambiar el veterinario asignado",
            )

        if "estado" in cambios and cambios["estado"] != "Cancelada":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El propietario solo puede cancelar una cita",
            )

        if cita_actual["estado"] not in {"Pendiente", "Confirmada"}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta cita ya no puede modificarse",
            )

    elif rol == "VETERINARIO":
        if set(cambios) != {"estado"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El veterinario solo puede actualizar el estado de la cita",
            )

        if cambios["estado"] not in {"Confirmada", "Atendida", "Cancelada"}:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Estado no permitido para el veterinario",
            )

    if "id_veterinario" in cambios:
        if not veterinario_existe(db, cambios["id_veterinario"]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El veterinario seleccionado no tiene un perfil válido",
            )
    if {"fecha", "hora", "id_veterinario"} & set(cambios):
        conflicto = existe_conflicto_cita(
            db=db,
            id_mascota=cita_actual["id_mascota"],
            id_veterinario=cambios.get(
                "id_veterinario",
                cita_actual["id_veterinario"],
            ),
            fecha=cambios.get("fecha", cita_actual["fecha"]),
            hora=cambios.get("hora", cita_actual["hora"]),
            excluir_cita_id=cita_id,
        )

        if conflicto:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La mascota o el veterinario ya tiene otra cita activa en esa fecha y hora",
            )
    try:
        resultado = actualizar_cita_repository(
            db,
            cita_id,
            rol,
            usuario["id"],
            cambios,
        )
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo actualizar la cita por un conflicto con los datos",
        ) from error

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo actualizar la cita",
        )

    return resultado