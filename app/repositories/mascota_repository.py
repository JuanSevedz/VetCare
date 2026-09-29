from sqlalchemy import text
from sqlalchemy.orm import Session


def obtener_mascotas(db: Session, propietario_id: str):
    query = text("""
        SELECT
            id,
            id_propietario,
            nombre,
            especie,
            raza,
            sexo,
            fecha_nacimiento,
            peso,
            microchip
        FROM mascotas
        WHERE id_propietario = :propietario_id
        ORDER BY id
    """)

    result = db.execute(
        query,
        {"propietario_id": propietario_id}
    )

    return [dict(row._mapping) for row in result]


def obtener_mascota_por_id(
    db: Session,
    mascota_id: str,
    propietario_id: str
):
    query = text("""
        SELECT
            id,
            id_propietario,
            nombre,
            especie,
            raza,
            sexo,
            fecha_nacimiento,
            peso,
            microchip
        FROM mascotas
        WHERE id = :mascota_id
          AND id_propietario = :propietario_id
    """)

    result = db.execute(
        query,
        {
            "mascota_id": mascota_id,
            "propietario_id": propietario_id
        }
    )

    row = result.first()

    if row is None:
        return None

    return dict(row._mapping)


def crear_mascota(
    db: Session,
    mascota,
    propietario_id: str
):
    query = text("""
        INSERT INTO mascotas (
            id,
            id_propietario,
            nombre,
            especie,
            raza,
            sexo,
            fecha_nacimiento,
            peso,
            microchip
        )
        VALUES (
            :id,
            :id_propietario,
            :nombre,
            :especie,
            :raza,
            :sexo,
            :fecha_nacimiento,
            :peso,
            :microchip
        )
        RETURNING
            id,
            id_propietario,
            nombre,
            especie,
            raza,
            sexo,
            fecha_nacimiento,
            peso,
            microchip
    """)

    datos = mascota.model_dump()
    datos["id_propietario"] = propietario_id

    try:
        result = db.execute(query, datos)
        db.commit()
    except Exception:
        db.rollback()
        raise

    row = result.first()

    return dict(row._mapping)


def actualizar_mascota(
    db: Session,
    mascota_id: str,
    propietario_id: str,
    datos: dict
):
    campos = []

    for campo in datos:
        campos.append(f"{campo} = :{campo}")

    query = text(f"""
        UPDATE mascotas
        SET {", ".join(campos)}
        WHERE id = :mascota_id
          AND id_propietario = :propietario_id
        RETURNING
            id,
            id_propietario,
            nombre,
            especie,
            raza,
            sexo,
            fecha_nacimiento,
            peso,
            microchip
    """)

    datos["mascota_id"] = mascota_id
    datos["propietario_id"] = propietario_id

    result = db.execute(
        query,
        datos
    )

    row = result.first()

    if row is None:
        return None

    db.commit()

    return dict(row._mapping)


def eliminar_mascota(
    db: Session,
    mascota_id: str,
    propietario_id: str
):
    query = text("""
        DELETE FROM mascotas
        WHERE id = :mascota_id
          AND id_propietario = :propietario_id
        RETURNING id
    """)

    result = db.execute(
        query,
        {
            "mascota_id": mascota_id,
            "propietario_id": propietario_id
        }
    )

    row = result.first()

    if row is None:
        return None

    db.commit()

    return row.id