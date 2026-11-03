from sqlalchemy import text
from sqlalchemy.orm import Session


CAMPOS_ACTUALIZABLES = {
    "nombre",
    "especie",
    "raza",
    "sexo",
    "fecha_nacimiento",
    "peso",
    "microchip",
}


def obtener_mascotas(
    db: Session,
    propietario_id: str | None
):
    if propietario_id is None:
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

    else:
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
    propietario_id: str | None
):
    if propietario_id is None:
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

        parametros = {"mascota_id": mascota_id}

    else:
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

        parametros = {
            "mascota_id": mascota_id,
            "propietario_id": propietario_id
        }

    result = db.execute(query, parametros)
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
        row = result.first()
        db.commit()

        return dict(row._mapping)

    except Exception:
        db.rollback()
        raise


def actualizar_mascota(
    db: Session,
    mascota_id: str,
    propietario_id: str | None,
    datos: dict
):
    # Impedir actualizaciones de campos no autorizados.
    campos_invalidos = set(datos) - CAMPOS_ACTUALIZABLES

    if campos_invalidos:
        raise ValueError(
            f"Campos no permitidos: {', '.join(sorted(campos_invalidos))}"
        )

    if not datos:
        return None

    # Los nombres de columna se construyen exclusivamente
    # a partir de la lista de campos permitidos.
    asignaciones = ", ".join(
        f"{campo} = :{campo}"
        for campo in datos
    )

    if propietario_id is None:
        condicion = "id = :mascota_id"
        parametros = {
            **datos,
            "mascota_id": mascota_id
        }
    else:
        condicion = """
            id = :mascota_id
            AND id_propietario = :propietario_id
        """
        parametros = {
            **datos,
            "mascota_id": mascota_id,
            "propietario_id": propietario_id
        }

    query = text(f"""
        UPDATE mascotas
        SET {asignaciones}
        WHERE {condicion}
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

    try:
        result = db.execute(query, parametros)
        row = result.first()

        if row is None:
            db.rollback()
            return None

        mascota_actualizada = dict(row._mapping)
        db.commit()

        return mascota_actualizada

    except Exception:
        db.rollback()
        raise


def eliminar_mascota(
    db: Session,
    mascota_id: str,
    propietario_id: str | None
):
    if propietario_id is None:
        query = text("""
            DELETE FROM mascotas
            WHERE id = :mascota_id
            RETURNING id
        """)

        parametros = {"mascota_id": mascota_id}

    else:
        query = text("""
            DELETE FROM mascotas
            WHERE id = :mascota_id
              AND id_propietario = :propietario_id
            RETURNING id
        """)

        parametros = {
            "mascota_id": mascota_id,
            "propietario_id": propietario_id
        }

    try:
        result = db.execute(query, parametros)
        row = result.first()

        if row is None:
            db.rollback()
            return None

        mascota_id_eliminada = row.id
        db.commit()

        return mascota_id_eliminada

    except Exception:
        db.rollback()
        raise