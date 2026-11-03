from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.historia_clinica_repository import (
    obtener_historia_clinica_por_id,
)

from app.repositories.consulta_repository import (
    obtener_consultas,
    obtener_consulta_por_id,
    obtener_cita_para_consulta,
    existe_consulta_por_cita,
    crear_consulta,
    actualizar_consulta as actualizar_consulta_repository,
    obtener_sintomas,
    obtener_observaciones,
    crear_sintoma,
    crear_observacion,
)


def listar_consultas(
    db: Session,
    usuario: dict,
):
    return obtener_consultas(
        db,
        usuario["rol"],
        usuario["id"],
    )


def buscar_consulta(
    db: Session,
    consulta_id: str,
    usuario: dict,
):
    return obtener_consulta_por_id(
        db,
        consulta_id,
        usuario["rol"],
        usuario["id"],
    )


def registrar_consulta(
    db: Session,
    datos,
    usuario: dict,
):
    if usuario["rol"] != "VETERINARIO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un veterinario puede registrar consultas",
        )

    datos_consulta = datos.model_dump()

    if datos_consulta["fecha"] > date.today():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="La fecha de la consulta no puede estar en el futuro",
        )

    historia = obtener_historia_clinica_por_id(
        db,
        datos_consulta["id_historia_clinica"],
        "ADMIN",
        usuario["id"],
    )

    if historia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historia clínica no encontrada",
        )

    cita = obtener_cita_para_consulta(
        db,
        datos_consulta["id_cita"],
        datos_consulta["id_historia_clinica"],
    )

    if cita is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La cita no existe o no corresponde a esta historia clínica",
        )

    if cita["id_veterinario"] != usuario["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes registrar consultas para citas asignadas a otro veterinario",
        )

    if cita["estado"] != "Confirmada":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La cita debe estar confirmada para registrar la consulta",
        )

    if cita["fecha"] != datos_consulta["fecha"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="La fecha de la consulta debe coincidir con la fecha de la cita",
        )

    if existe_consulta_por_cita(
        db,
        datos_consulta["id_cita"],
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta cita ya tiene una consulta registrada",
        )

    datos_consulta["id_veterinario"] = usuario["id"]

    try:
        resultado = crear_consulta(
            db,
            datos_consulta,
        )

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se pudo registrar la consulta por un conflicto con los datos",
        ) from error

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La cita dejó de estar disponible para registrar la consulta",
        )

    return resultado


def modificar_consulta(
    db: Session,
    consulta_id: str,
    datos,
    usuario: dict,
):
    consulta_actual = buscar_consulta(
        db,
        consulta_id,
        usuario,
    )

    if consulta_actual is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta no encontrada",
        )

    cambios = datos.model_dump(exclude_unset=True)

    if not cambios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar",
        )

    if any(valor is None for valor in cambios.values()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="El diagnóstico y el tratamiento no pueden quedar vacíos",
        )

    resultado = actualizar_consulta_repository(
        db,
        consulta_id,
        cambios,
    )

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo actualizar la consulta",
        )

    return resultado


def listar_sintomas(
    db: Session,
    consulta_id: str,
    usuario: dict,
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

    return obtener_sintomas(db, consulta_id)


def registrar_sintoma(
    db: Session,
    consulta_id: str,
    datos,
    usuario: dict,
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

    return crear_sintoma(
        db,
        consulta_id,
        datos.sintoma.strip(),
    )


def listar_observaciones(
    db: Session,
    consulta_id: str,
    usuario: dict,
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

    return obtener_observaciones(db, consulta_id)


def registrar_observacion(
    db: Session,
    consulta_id: str,
    datos,
    usuario: dict,
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

    return crear_observacion(
        db,
        consulta_id,
        datos.observacion.strip(),
    )