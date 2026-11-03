from fastapi import HTTPException

from app.repositories.mascota_repository import (
    obtener_mascota_por_id,
)

from app.repositories.cuidados_rutina_repository import (
    listar_cuidados_mascota,
    obtener_cuidado_por_id,
    crear_cuidado,
    actualizar_cuidado,
)


def listar_cuidados(db, mascota_id, usuario):
    mascota = obtener_mascota_por_id(db, mascota_id, None)

    if not mascota:
        raise HTTPException(404, "Mascota no encontrada.")

    if (
        usuario["rol"] == "PROPIETARIO"
        and mascota["id_propietario"] != usuario["id"]
    ):
        raise HTTPException(404, "Mascota no encontrada.")

    return listar_cuidados_mascota(
        db,
        mascota_id,
        usuario["rol"],
        usuario["id"],
    )


def buscar_cuidado(db, cuidado_id, usuario):
    cuidado = obtener_cuidado_por_id(
        db,
        cuidado_id,
        usuario["rol"],
        usuario["id"],
    )

    if not cuidado:
        raise HTTPException(404, "Cuidado o rutina no encontrado.")

    return cuidado


def registrar_cuidado(db, mascota_id, datos, usuario):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(
            403,
            "No tiene permisos para registrar cuidados o rutinas.",
        )

    mascota = obtener_mascota_por_id(db, mascota_id, None)

    if not mascota:
        raise HTTPException(404, "Mascota no encontrada.")

    datos = datos.model_dump()

    for campo in ("tipo", "frecuencia", "horario"):
        datos[campo] = datos[campo].strip()

        if not datos[campo]:
            raise HTTPException(
                422,
                f"El campo {campo} no puede estar vacío.",
            )

    if datos["notas"] is not None:
        datos["notas"] = datos["notas"].strip() or None

    return crear_cuidado(db, mascota_id, datos)


def modificar_cuidado(db, cuidado_id, datos, usuario):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(
            403,
            "No tiene permisos para modificar cuidados o rutinas.",
        )

    buscar_cuidado(db, cuidado_id, usuario)

    cambios = datos.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(
            422,
            "Debe enviar al menos un campo para actualizar.",
        )

    for campo, valor in cambios.items():
        if valor is None:
            if campo == "notas":
                continue

            raise HTTPException(
                422,
                f"El campo {campo} no puede ser nulo.",
            )

        if isinstance(valor, str):
            cambios[campo] = valor.strip()

            if campo == "notas":
                cambios[campo] = cambios[campo] or None
            elif not cambios[campo]:
                raise HTTPException(
                    422,
                    f"El campo {campo} no puede estar vacío.",
                )

    resultado = actualizar_cuidado(db, cuidado_id, cambios)

    if not resultado:
        raise HTTPException(
            404,
            "No fue posible actualizar el cuidado o rutina.",
        )

    return resultado