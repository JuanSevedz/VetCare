from datetime import date

from fastapi import HTTPException

from app.repositories.medicamento_repository import (
    obtener_medicamentos_por_consulta,
    obtener_medicamento_por_id,
    crear_medicamento,
    actualizar_medicamento,
)

from app.services.consulta_service import buscar_consulta


ESTADOS_MEDICAMENTO = {"Activo", "Finalizado", "Suspendido"}

ROLES_AUTORIZADOS = {"VETERINARIO", "ADMIN"}


def _validar_rol(rol):
    if rol not in ROLES_AUTORIZADOS:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para gestionar medicamentos.",
        )


def _limpiar_datos(datos):
    datos_limpios = {}

    for campo, valor in datos.items():
        if isinstance(valor, str):
            valor = valor.strip()

            if not valor:
                raise HTTPException(
                    status_code=422,
                    detail=f"El campo '{campo}' no puede estar vacío.",
                )

        if valor is None:
            raise HTTPException(
                status_code=422,
                detail=f"El campo '{campo}' no puede ser nulo.",
            )

        datos_limpios[campo] = valor

    return datos_limpios

def _validar_consulta_accesible(db, consulta_id, usuario):
    consulta = buscar_consulta(db, consulta_id, usuario)

    if consulta is None:
        raise HTTPException(
            status_code=404,
            detail="Consulta no encontrada.",
        )

    return consulta

def listar_medicamentos_consulta(db, consulta_id, usuario):
    # Verificar que el usuario pueda acceder a la consulta.
    _validar_consulta_accesible(db, consulta_id, usuario)

    return obtener_medicamentos_por_consulta(db, consulta_id)


def obtener_medicamento(db, medicamento_id, usuario):
    medicamento = obtener_medicamento_por_id(
        db,
        medicamento_id,
        usuario["rol"],
        usuario["id"],
    )

    if not medicamento:
        raise HTTPException(
            status_code=404,
            detail="Medicamento no encontrado.",
        )

    return medicamento


def registrar_medicamento(db, consulta_id, datos, usuario):
    _validar_rol(usuario["rol"])

    # Verificar que la consulta exista y sea accesible.
    _validar_consulta_accesible(db, consulta_id, usuario)
    datos_limpios = _limpiar_datos(datos)

    if datos_limpios["estado"] not in ESTADOS_MEDICAMENTO:
        raise HTTPException(
            status_code=422,
            detail="El estado del medicamento no es válido.",
        )

    if datos_limpios["fecha_fin"] < datos_limpios["fecha_inicio"]:
        raise HTTPException(
            status_code=422,
            detail="La fecha de finalización no puede ser anterior a la fecha de inicio.",
        )

    return crear_medicamento(db, consulta_id, datos_limpios)


def modificar_medicamento(db, medicamento_id, datos, usuario):
    _validar_rol(usuario["rol"])

    # Verificar existencia y permisos sobre el medicamento.
    medicamento_actual = obtener_medicamento(
        db,
        medicamento_id,
        usuario,
    )

    datos_limpios = _limpiar_datos(datos)

    if not datos_limpios:
        raise HTTPException(
            status_code=422,
            detail="Debe proporcionar al menos un campo para actualizar.",
        )

    if "estado" in datos_limpios:
        if datos_limpios["estado"] not in ESTADOS_MEDICAMENTO:
            raise HTTPException(
                status_code=422,
                detail="El estado del medicamento no es válido.",
            )

    fecha_inicio = datos_limpios.get(
        "fecha_inicio",
        medicamento_actual["fecha_inicio"],
    )

    fecha_fin = datos_limpios.get(
        "fecha_fin",
        medicamento_actual["fecha_fin"],
    )

    if fecha_fin < fecha_inicio:
        raise HTTPException(
            status_code=422,
            detail="La fecha de finalización no puede ser anterior a la fecha de inicio.",
        )

    actualizado = actualizar_medicamento(
        db,
        medicamento_id,
        datos_limpios,
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="No fue posible actualizar el medicamento.",
        )

    return actualizado