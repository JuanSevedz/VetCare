from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


COLUMNAS = """
    r.id,
    r.id_mascota,
    r.categoria,
    r.fecha,
    r.descripcion,
    r.estado
"""


def listar_recordatorios_mascota(
    db: Session,
    mascota_id: str,
    rol: str,
    usuario_id: str,
):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM recordatorios r
        JOIN mascotas m ON m.id = r.id_mascota
        WHERE r.id_mascota = :mascota_id
          AND (
              :rol IN ('ADMIN', 'VETERINARIO')
              OR (
                  :rol = 'PROPIETARIO'
                  AND m.id_propietario = :usuario_id
              )
          )
        ORDER BY r.fecha DESC
    """)

    result = db.execute(
        query,
        {
            "mascota_id": mascota_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    )

    return [dict(row._mapping) for row in result]


def obtener_recordatorio_por_id(
    db: Session,
    recordatorio_id: str,
    rol: str,
    usuario_id: str,
):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM recordatorios r
        JOIN mascotas m ON m.id = r.id_mascota
        WHERE r.id = :recordatorio_id
          AND (
              :rol IN ('ADMIN', 'VETERINARIO')
              OR (
                  :rol = 'PROPIETARIO'
                  AND m.id_propietario = :usuario_id
              )
          )
    """)

    row = db.execute(
        query,
        {
            "recordatorio_id": recordatorio_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    ).first()

    return dict(row._mapping) if row else None


def crear_recordatorio(
    db: Session,
    mascota_id: str,
    datos: dict,
):
    query = text("""
        INSERT INTO recordatorios (
            id,
            id_mascota,
            categoria,
            fecha,
            descripcion,
            estado
        )
        VALUES (
            :id,
            :id_mascota,
            :categoria,
            :fecha,
            :descripcion,
            :estado
        )
        RETURNING
            id,
            id_mascota,
            categoria,
            fecha,
            descripcion,
            estado
    """)

    parametros = {
        **datos,
        "id": f"REC-{uuid4().hex}",
        "id_mascota": mascota_id,
    }

    try:
        row = db.execute(query, parametros).first()
        db.commit()

        return dict(row._mapping) if row else None

    except Exception:
        db.rollback()
        raise


def actualizar_recordatorio(
    db: Session,
    recordatorio_id: str,
    datos: dict,
):
    campos_permitidos = {
        "categoria",
        "fecha",
        "descripcion",
        "estado",
    }

    if not datos or not set(datos).issubset(campos_permitidos):
        return None

    asignaciones = ", ".join(
        f"{campo} = :{campo}"
        for campo in datos
    )

    query = text(f"""
        UPDATE recordatorios
        SET {asignaciones}
        WHERE id = :recordatorio_id
        RETURNING
            id,
            id_mascota,
            categoria,
            fecha,
            descripcion,
            estado
    """)

    try:
        row = db.execute(
            query,
            {
                **datos,
                "recordatorio_id": recordatorio_id,
            },
        ).first()

        if not row:
            db.rollback()
            return None

        resultado = dict(row._mapping)
        db.commit()

        return resultado

    except Exception:
        db.rollback()
        raise