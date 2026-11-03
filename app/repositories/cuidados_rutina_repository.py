from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


COLUMNAS = """
    cr.id,
    cr.id_mascota,
    cr.tipo,
    cr.frecuencia,
    cr.horario,
    cr.notas
"""


def listar_cuidados_mascota(
    db: Session,
    mascota_id: str,
    rol: str,
    usuario_id: str,
):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM cuidados_rutina cr
        JOIN mascotas m ON m.id = cr.id_mascota
        WHERE cr.id_mascota = :mascota_id
          AND (
              :rol IN ('ADMIN', 'VETERINARIO')
              OR (
                  :rol = 'PROPIETARIO'
                  AND m.id_propietario = :usuario_id
              )
          )
        ORDER BY cr.tipo
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


def obtener_cuidado_por_id(
    db: Session,
    cuidado_id: str,
    rol: str,
    usuario_id: str,
):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM cuidados_rutina cr
        JOIN mascotas m ON m.id = cr.id_mascota
        WHERE cr.id = :cuidado_id
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
            "cuidado_id": cuidado_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    ).first()

    return dict(row._mapping) if row else None


def crear_cuidado(
    db: Session,
    mascota_id: str,
    datos: dict,
):
    query = text("""
        INSERT INTO cuidados_rutina (
            id,
            id_mascota,
            tipo,
            frecuencia,
            horario,
            notas
        )
        VALUES (
            :id,
            :id_mascota,
            :tipo,
            :frecuencia,
            :horario,
            :notas
        )
        RETURNING
            id,
            id_mascota,
            tipo,
            frecuencia,
            horario,
            notas
    """)

    parametros = {
        **datos,
        "id": f"CUI-{uuid4().hex}",
        "id_mascota": mascota_id,
    }

    try:
        row = db.execute(query, parametros).first()
        db.commit()

        return dict(row._mapping) if row else None

    except Exception:
        db.rollback()
        raise


def actualizar_cuidado(
    db: Session,
    cuidado_id: str,
    datos: dict,
):
    campos_permitidos = {
        "tipo",
        "frecuencia",
        "horario",
        "notas",
    }

    if not datos or not set(datos).issubset(campos_permitidos):
        return None

    asignaciones = ", ".join(
        f"{campo} = :{campo}"
        for campo in datos
    )

    query = text(f"""
        UPDATE cuidados_rutina
        SET {asignaciones}
        WHERE id = :cuidado_id
        RETURNING
            id,
            id_mascota,
            tipo,
            frecuencia,
            horario,
            notas
    """)

    try:
        row = db.execute(
            query,
            {
                **datos,
                "cuidado_id": cuidado_id,
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