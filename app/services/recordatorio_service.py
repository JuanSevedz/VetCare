from fastapi import HTTPException

from app.repositories.mascota_repository import (
    obtener_mascota_por_id,
)

from app.repositories.recordatorio_repository import (
    listar_recordatorios_mascota,
    obtener_recordatorio_por_id,
    crear_recordatorio,
    actualizar_recordatorio,
)


def listar_recordatorios(db, mascota_id, usuario):
    mascota = obtener_mascota_por_id(db, mascota_id, None)

    if not mascota:
        raise HTTPException(404, "Mascota no encontrada.")

    if (
        usuario["rol"] == "PROPIETARIO"
        and mascota["id_propietario"] != usuario["id"]
    ):
        raise HTTPException(404, "Mascota no encontrada.")

    return listar_recordatorios_mascota(
        db,
        mascota_id,
        usuario["rol"],
        usuario["id"],
    )


def buscar_recordatorio(db, recordatorio_id, usuario):
    recordatorio = obtener_recordatorio_por_id(
        db,
        recordatorio_id,
        usuario["rol"],
        usuario["id"],
    )

    if not recordatorio:
        raise HTTPException(404, "Recordatorio no encontrado.")

    return recordatorio


def registrar_recordatorio(db, mascota_id, datos, usuario):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(
            403,
            "No tiene permisos para registrar recordatorios.",
        )

    mascota = obtener_mascota_por_id(db, mascota_id, None)

    if not mascota:
        raise HTTPException(404, "Mascota no encontrada.")

    datos = datos.model_dump()

    for campo in ("categoria", "descripcion"):
        datos[campo] = datos[campo].strip()

        if not datos[campo]:
            raise HTTPException(
                422,
                f"El campo {campo} no puede estar vacío.",
            )

    return crear_recordatorio(
        db,
        mascota_id,
        datos,
    )


def modificar_recordatorio(db, recordatorio_id, datos, usuario):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(
            403,
            "No tiene permisos para modificar recordatorios.",
        )

    buscar_recordatorio(db, recordatorio_id, usuario)

    cambios = datos.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(
            422,
            "Debe enviar al menos un campo para actualizar.",
        )

    for campo, valor in cambios.items():
        if valor is None:
            raise HTTPException(
                422,
                f"El campo {campo} no puede ser nulo.",
            )

        if isinstance(valor, str):
            cambios[campo] = valor.strip()

            if not cambios[campo]:
                raise HTTPException(
                    422,
                    f"El campo {campo} no puede estar vacío.",
                )

    resultado = actualizar_recordatorio(
        db,
        recordatorio_id,
        cambios,
    )

    if not resultado:
        raise HTTPException(
            404,
            "No fue posible actualizar el recordatorio.",
        )

    return resultado