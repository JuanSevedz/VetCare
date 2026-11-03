from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


COLUMNAS = """
    v.id,
    v.id_mascota,
    v.id_veterinario,
    v.nombre,
    v.fecha_aplicacion,
    v.fecha_proxima,
    v.lote,
    v.estado
"""


def listar_vacunas_mascota(db: Session, mascota_id: str, rol: str, usuario_id: str):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM vacunas v
        JOIN mascotas m ON m.id = v.id_mascota
        WHERE v.id_mascota = :mascota_id
          AND (
              :rol = 'ADMIN'
              OR (:rol = 'PROPIETARIO' AND m.id_propietario = :usuario_id)
              OR (:rol = 'VETERINARIO' AND v.id_veterinario = :usuario_id)
          )
        ORDER BY v.fecha_aplicacion DESC
    """)

    result = db.execute(query, {
        "mascota_id": mascota_id,
        "rol": rol,
        "usuario_id": usuario_id,
    })

    return [dict(row._mapping) for row in result]


def obtener_vacuna_por_id(db: Session, vacuna_id: str, rol: str, usuario_id: str):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM vacunas v
        JOIN mascotas m ON m.id = v.id_mascota
        WHERE v.id = :vacuna_id
          AND (
              :rol = 'ADMIN'
              OR (:rol = 'PROPIETARIO' AND m.id_propietario = :usuario_id)
              OR (:rol = 'VETERINARIO' AND v.id_veterinario = :usuario_id)
          )
    """)

    row = db.execute(query, {
        "vacuna_id": vacuna_id,
        "rol": rol,
        "usuario_id": usuario_id,
    }).first()

    return dict(row._mapping) if row else None


def crear_vacuna(db: Session, mascota_id: str, veterinario_id: str, datos: dict):
    query = text("""
        INSERT INTO vacunas (
            id, id_mascota, id_veterinario, nombre,
            fecha_aplicacion, fecha_proxima, lote, estado
        )
        VALUES (
            :id, :id_mascota, :id_veterinario, :nombre,
            :fecha_aplicacion, :fecha_proxima, :lote, :estado
        )
        RETURNING
            id, id_mascota, id_veterinario, nombre,
            fecha_aplicacion, fecha_proxima, lote, estado
    """)

    parametros = {
        **datos,
        "id": f"VAC-{uuid4().hex}",
        "id_mascota": mascota_id,
        "id_veterinario": veterinario_id,
    }

    try:
        row = db.execute(query, parametros).first()
        db.commit()
        return dict(row._mapping) if row else None
    except Exception:
        db.rollback()
        raise


def actualizar_vacuna(db: Session, vacuna_id: str, datos: dict):
    campos_permitidos = {
        "nombre", "fecha_aplicacion", "fecha_proxima", "lote", "estado"
    }

    if not datos or not set(datos).issubset(campos_permitidos):
        return None

    asignaciones = ", ".join(f"{campo} = :{campo}" for campo in datos)

    query = text(f"""
        UPDATE vacunas
        SET {asignaciones}
        WHERE id = :vacuna_id
        RETURNING
            id, id_mascota, id_veterinario, nombre,
            fecha_aplicacion, fecha_proxima, lote, estado
    """)

    try:
        row = db.execute(
            query,
            {**datos, "vacuna_id": vacuna_id},
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