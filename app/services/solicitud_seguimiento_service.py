from fastapi import HTTPException

from app.repositories.mascota_repository import (
    obtener_mascota_por_id,
)

from app.repositories.solicitud_seguimiento_repository import (
    listar_solicitudes_mascota,
    obtener_solicitud_por_id,
    crear_solicitud,
    actualizar_estado_solicitud,
)


def listar_solicitudes(db, mascota_id, usuario):
    mascota = obtener_mascota_por_id(
        db,
        mascota_id,
        None,
    )

    if not mascota:
        raise HTTPException(
            404,
            "Mascota no encontrada.",
        )

    if (
        usuario["rol"] == "PROPIETARIO"
        and mascota["id_propietario"] != usuario["id"]
    ):
        raise HTTPException(
            404,
            "Mascota no encontrada.",
        )

    return listar_solicitudes_mascota(
        db,
        mascota_id,
    )


def buscar_solicitud(db, solicitud_id, usuario):
    solicitud = obtener_solicitud_por_id(
        db,
        solicitud_id,
        usuario["rol"],
        usuario["id"],
    )

    if not solicitud:
        raise HTTPException(
            404,
            "Solicitud de seguimiento no encontrada.",
        )

    return solicitud


def registrar_solicitud(
    db,
    mascota_id,
    datos,
    usuario,
):
    if usuario["rol"] != "PROPIETARIO":
        raise HTTPException(
            403,
            "Solo los propietarios pueden crear solicitudes de seguimiento.",
        )

    mascota = obtener_mascota_por_id(
        db,
        mascota_id,
        None,
    )

    if not mascota:
        raise HTTPException(
            404,
            "Mascota no encontrada.",
        )

    if mascota["id_propietario"] != usuario["id"]:
        raise HTTPException(
            404,
            "Mascota no encontrada.",
        )

    descripcion = datos.descripcion.strip()

    if not descripcion:
        raise HTTPException(
            422,
            "La descripción no puede estar vacía.",
        )

    return crear_solicitud(
        db,
        usuario["id"],
        mascota_id,
        descripcion,
    )


def modificar_solicitud(
    db,
    solicitud_id,
    datos,
    usuario,
):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(
            403,
            "No tiene permisos para modificar solicitudes de seguimiento.",
        )

    buscar_solicitud(
        db,
        solicitud_id,
        usuario,
    )

    cambios = datos.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(
            422,
            "Debe enviar al menos un campo para actualizar.",
        )

    resultado = actualizar_estado_solicitud(
        db,
        solicitud_id,
        cambios["estado"],
    )

    if not resultado:
        raise HTTPException(
            404,
            "No fue posible actualizar la solicitud.",
        )

    return resultado