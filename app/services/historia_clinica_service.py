from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.historia_clinica_repository import (
    obtener_historias_clinicas,
    obtener_historia_clinica_por_id,
    obtener_historia_por_mascota,
    mascota_existe,
    mascota_pertenece_a_propietario,
    crear_historia_clinica,
)


def listar_historias_clinicas(
    db: Session,
    usuario: dict,
):
    return obtener_historias_clinicas(
        db,
        usuario["rol"],
        usuario["id"],
    )


def buscar_historia_clinica(
    db: Session,
    historia_id: str,
    usuario: dict,
):
    return obtener_historia_clinica_por_id(
        db,
        historia_id,
        usuario["rol"],
        usuario["id"],
    )


def registrar_historia_clinica(
    db: Session,
    datos,
    usuario: dict,
):
    mascota_id = datos.id_mascota

    if not mascota_existe(db, mascota_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada",
        )

    if usuario["rol"] == "PROPIETARIO":
        pertenece = mascota_pertenece_a_propietario(
            db,
            mascota_id,
            usuario["id"],
        )

        if not pertenece:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes crear historias clínicas para tus mascotas",
            )

    historia_existente = obtener_historia_por_mascota(
        db,
        mascota_id,
    )

    if historia_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La mascota ya tiene una historia clínica registrada",
        )

    try:
        return crear_historia_clinica(
            db,
            mascota_id,
        )

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La mascota ya tiene una historia clínica registrada",
        ) from error