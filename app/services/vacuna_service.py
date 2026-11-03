from fastapi import HTTPException

from app.repositories.mascota_repository import obtener_mascota_por_id

from app.repositories.vacuna_repository import (
    listar_vacunas_mascota,
    obtener_vacuna_por_id,
    crear_vacuna,
    actualizar_vacuna,
)


def listar_vacunas(db, mascota_id, usuario):
    mascota = obtener_mascota_por_id(db, mascota_id, None)

    if not mascota:
        raise HTTPException(404, "Mascota no encontrada.")

    if (
        usuario["rol"] == "PROPIETARIO"
        and mascota["id_propietario"] != usuario["id"]
    ):
        raise HTTPException(404, "Mascota no encontrada.")

    return listar_vacunas_mascota(
        db, mascota_id, usuario["rol"], usuario["id"]
    )


def buscar_vacuna(db, vacuna_id, usuario):
    vacuna = obtener_vacuna_por_id(
        db, vacuna_id, usuario["rol"], usuario["id"]
    )

    if not vacuna:
        raise HTTPException(404, "Vacuna no encontrada.")

    return vacuna


def registrar_vacuna(db, mascota_id, datos, usuario):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(
            403,
            "No tiene permisos para registrar vacunas."
        )

    mascota = obtener_mascota_por_id(db, mascota_id, None)

    if not mascota:
        raise HTTPException(404, "Mascota no encontrada.")

    datos = datos.model_dump()

    if usuario["rol"] == "VETERINARIO":
        veterinario_id = usuario["id"]
    else:
        veterinario_id = datos.pop("id_veterinario", None)

        if not veterinario_id:
            raise HTTPException(
                422,
                "El administrador debe indicar el veterinario responsable."
            )

        from sqlalchemy import text

        veterinario = db.execute(
            text("""
                SELECT id_usuario
                FROM personal_veterinario
                WHERE id_usuario = :id
            """),
            {"id": veterinario_id},
        ).first()

        if not veterinario:
            raise HTTPException(
                422,
                "El veterinario indicado no existe."
            )

    if (
        datos["fecha_proxima"]
        and datos["fecha_proxima"] < datos["fecha_aplicacion"]
    ):
        raise HTTPException(
            422,
            "La próxima fecha de vacunación no puede ser anterior a la aplicación."
        )

    for campo in ("nombre", "lote"):
        if isinstance(datos.get(campo), str):
            datos[campo] = datos[campo].strip()

            if campo == "nombre" and not datos[campo]:
                raise HTTPException(
                    422,
                    "El nombre de la vacuna no puede estar vacío."
                )

    return crear_vacuna(
        db,
        mascota_id,
        veterinario_id,
        datos,
    )

def modificar_vacuna(db, vacuna_id, datos, usuario):
    if usuario["rol"] not in {"VETERINARIO", "ADMIN"}:
        raise HTTPException(403, "No tiene permisos para modificar vacunas.")

    actual = buscar_vacuna(db, vacuna_id, usuario)
    cambios = datos.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(422, "Debe enviar al menos un campo para actualizar.")

    for campo, valor in cambios.items():
        if valor is None and campo != "fecha_proxima":
            raise HTTPException(422, f"El campo {campo} no puede ser nulo.")

        if isinstance(valor, str):
            cambios[campo] = valor.strip()
            if campo == "nombre" and not cambios[campo]:
                raise HTTPException(422, "El nombre no puede estar vacío.")

    fecha_aplicacion = cambios.get(
        "fecha_aplicacion", actual["fecha_aplicacion"]
    )
    fecha_proxima = cambios.get(
        "fecha_proxima", actual["fecha_proxima"]
    )

    if fecha_proxima and fecha_proxima < fecha_aplicacion:
        raise HTTPException(
            422,
            "La próxima fecha de vacunación no puede ser anterior a la aplicación.",
        )

    resultado = actualizar_vacuna(db, vacuna_id, cambios)

    if not resultado:
        raise HTTPException(404, "No fue posible actualizar la vacuna.")

    return resultado