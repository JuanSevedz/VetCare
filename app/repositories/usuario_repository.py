from sqlalchemy import text
from sqlalchemy.orm import Session


def obtener_usuarios(db: Session):
    query = text("""
        SELECT
            id,
            nombre,
            correo,
            telefono
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
            telefono
        FROM usuarios
        WHERE id = :usuario_id
    """)

    result = db.execute(query, {"usuario_id": usuario_id})
    row = result.first()

    if row is None:
        return None

    return dict(row._mapping)
def crear_usuario(db: Session, usuario: dict):
    query = text("""
        INSERT INTO usuarios (
            id,
            nombre,
            correo,
            contrasena,
            telefono
        )
        VALUES (
            :id,
            :nombre,
            :correo,
            :contrasena,
            :telefono
        )
        RETURNING
            id,
            nombre,
            correo,
            telefono
    """)

    result = db.execute(query, usuario)
    row = result.first()

    db.commit()

    return dict(row._mapping)

def obtener_usuario_por_correo(db: Session, correo: str):
    query = text("""
        SELECT
            id,
            nombre,
            correo,
            contrasena,
            telefono
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