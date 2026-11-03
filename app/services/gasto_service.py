from fastapi import HTTPException

from app.repositories.mascota_repository import (
    obtener_mascota_por_id,
)

from app.repositories.gasto_repository import (
    listar_gastos_mascota,
    obtener_gasto_por_id,
    crear_gasto,
    actualizar_gasto,
)


def listar_gastos(db, mascota_id, usuario):
    mascota = obtener_mascota_por_id(db, mascota_id, None)

    if not mascota:
        raise HTTPException(404, "Mascota no encontrada.")

    if (
        usuario["rol"] == "PROPIETARIO"
        and mascota["id_propietario"] != usuario["id"]
    ):
        raise HTTPException(404, "Mascota no encontrada.")

    return listar_gastos_mascota(
        db,
        mascota_id,
        usuario["rol"],
        usuario["id"],
    )


def buscar_gasto(db, gasto_id, usuario):
    gasto = obtener_gasto_por_id(
        db,
        gasto_id,
        usuario["rol"],
        usuario["id"],
    )

    if not gasto:
        raise HTTPException(404, "Gasto no encontrado.")

    return gasto


def registrar_gasto(db, mascota_id, datos, usuario):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(
            403,
            "No tiene permisos para registrar gastos.",
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

    if datos["valor"] <= 0:
        raise HTTPException(
            422,
            "El valor del gasto debe ser mayor que cero.",
        )

    return crear_gasto(db, mascota_id, datos)


def modificar_gasto(db, gasto_id, datos, usuario):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(
            403,
            "No tiene permisos para modificar gastos.",
        )

    buscar_gasto(db, gasto_id, usuario)

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

    if "valor" in cambios and cambios["valor"] <= 0:
        raise HTTPException(
            422,
            "El valor del gasto debe ser mayor que cero.",
        )

    resultado = actualizar_gasto(db, gasto_id, cambios)

    if not resultado:
        raise HTTPException(
            404,
            "No fue posible actualizar el gasto.",
        )

    return resultado