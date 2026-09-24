from sqlalchemy import text


def obtener_mascotas(db):
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
        ORDER BY id
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]


def obtener_mascota_por_id(db, mascota_id):
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
    """)

    result = db.execute(
        query,
        {"mascota_id": mascota_id}
    )

    row = result.first()

    if row is None:
        return None

    return dict(row._mapping)
def crear_mascota(db, mascota):
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

    result = db.execute(
        query,
        mascota
    )

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    row = result.first()

    return dict(row._mapping)

def actualizar_mascota(db, mascota_id, datos):
    campos = []

    for campo in datos:
        campos.append(f"{campo} = :{campo}")

    query = text(f"""
        UPDATE mascotas
        SET {", ".join(campos)}
        WHERE id = :mascota_id
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

    result = db.execute(
        query,
        datos
    )

    row = result.first()

    if row is None:
        return None

    db.commit()

    return dict(row._mapping)

def eliminar_mascota(db, mascota_id):
    query = text("""
        DELETE FROM mascotas
        WHERE id = :mascota_id
        RETURNING id
    """)

    result = db.execute(
        query,
        {"mascota_id": mascota_id}
    )

    row = result.first()

    if row is None:
        return None

    db.commit()

    return row.id