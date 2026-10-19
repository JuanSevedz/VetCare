from sqlalchemy import text
from sqlalchemy.orm import Session


def obtener_usuarios(db: Session):
    query = text("""
        SELECT
            id,
            nombre,
            correo,
            telefono,
            rol
        FROM usuarios
        ORDER BY id
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]


def obtener_usuario_por_id(db: Session, usuario_id: str):
    query = text("""
        SELECT
            id,
            nombre,
            correo,
            telefono,
            rol
        FROM usuarios
        WHERE id = :usuario_id
    """)

    result = db.execute(
        query,
        {"usuario_id": usuario_id}
    )

    row = result.first()

    if row is None:
        return None

    return dict(row._mapping)


def crear_usuario(db: Session, usuario: dict):
    query_usuario = text("""
        INSERT INTO usuarios (
            id,
            nombre,
            correo,
            contrasena,
            telefono,
            rol
        )
        VALUES (
            :id,
            :nombre,
            :correo,
            :contrasena,
            :telefono,
            'PROPIETARIO'
        )
        RETURNING
            id,
            nombre,
            correo,
            telefono,
            rol
    """)

    query_propietario = text("""
        INSERT INTO propietarios (
            id_usuario,
            direccion
        )
        VALUES (
            :id_usuario,
            NULL
        )
    """)

    try:
        result = db.execute(query_usuario, usuario)
        nuevo_usuario = dict(result.first()._mapping)

        db.execute(
            query_propietario,
            {"id_usuario": usuario["id"]}
        )

        db.commit()

        return nuevo_usuario

    except Exception:
        db.rollback()
        raise


def obtener_usuario_por_correo(db: Session, correo: str):
    query = text("""
        SELECT
            id,
            nombre,
            correo,
            contrasena,
            telefono,
            rol
        FROM usuarios
        WHERE correo = :correo
    """)

    result = db.execute(
        query,
        {"correo": correo}
    )

    row = result.first()

    if row is None:
        return None

    return dict(row._mapping)