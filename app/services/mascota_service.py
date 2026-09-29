from app.repositories.mascota_repository import (
    obtener_mascotas,
    obtener_mascota_por_id,
    crear_mascota,
    actualizar_mascota as actualizar_mascota_repository,
    eliminar_mascota as eliminar_mascota_repository,
)


def listar_mascotas(db, propietario_id: str):
    return obtener_mascotas(
        db,
        propietario_id
    )


def buscar_mascota(
    db,
    mascota_id: str,
    propietario_id: str
):
    return obtener_mascota_por_id(
        db,
        mascota_id,
        propietario_id
    )


def registrar_mascota(
    db,
    mascota,
    propietario_id: str
):
    return crear_mascota(
        db,
        mascota,
        propietario_id
    )


def actualizar_mascota(
    db,
    mascota_id: str,
    mascota,
    propietario_id: str
):
    datos = mascota.model_dump(
        exclude_unset=True
    )

    if not datos:
        return None

    return actualizar_mascota_repository(
        db,
        mascota_id,
        propietario_id,
        datos
    )


def eliminar_mascota(
    db,
    mascota_id: str,
    propietario_id: str
):
    return eliminar_mascota_repository(
        db,
        mascota_id,
        propietario_id
    )