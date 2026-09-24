from app.repositories.mascota_repository import (
    obtener_mascotas,
    obtener_mascota_por_id,
    crear_mascota,
    actualizar_mascota as actualizar_mascota_repository,
    eliminar_mascota as eliminar_mascota_repository
)


def listar_mascotas(db):
    return obtener_mascotas(db)


def buscar_mascota(db, mascota_id):
    return obtener_mascota_por_id(db, mascota_id)


def registrar_mascota(db, mascota):
    return crear_mascota(
        db,
        mascota.model_dump()
    )


def actualizar_mascota(db, mascota_id, mascota):
    datos = mascota.model_dump(exclude_unset=True)

    if not datos:
        return None

    return actualizar_mascota_repository(
        db,
        mascota_id,
        datos
    )

def eliminar_mascota(db, mascota_id):
    return eliminar_mascota_repository(
        db,
        mascota_id
    )