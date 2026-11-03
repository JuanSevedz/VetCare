from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


COLUMNAS = """
    g.id,
    g.id_mascota,
    g.fecha,
    g.categoria,
    g.descripcion,
    g.valor
"""


def listar_gastos_mascota(
    db: Session,
    mascota_id: str,
    rol: str,
    usuario_id: str,
):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM gastos g
        JOIN mascotas m ON m.id = g.id_mascota
        WHERE g.id_mascota = :mascota_id
          AND (
              :rol IN ('ADMIN', 'VETERINARIO')
              OR (
                  :rol = 'PROPIETARIO'
                  AND m.id_propietario = :usuario_id
              )
          )
        ORDER BY g.fecha DESC
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


def obtener_gasto_por_id(
    db: Session,
    gasto_id: str,
    rol: str,
    usuario_id: str,
):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM gastos g
        JOIN mascotas m ON m.id = g.id_mascota
        WHERE g.id = :gasto_id
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
            "gasto_id": gasto_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    ).first()

    return dict(row._mapping) if row else None


def crear_gasto(
    db: Session,
    mascota_id: str,
    datos: dict,
):
    query = text("""
        INSERT INTO gastos (
            id,
            id_mascota,
            fecha,
            categoria,
            descripcion,
            valor
        )
        VALUES (
            :id,
            :id_mascota,
            :fecha,
            :categoria,
            :descripcion,
            :valor
        )
        RETURNING
            id,
            id_mascota,
            fecha,
            categoria,
            descripcion,
            valor
    """)

    parametros = {
        **datos,
        "id": f"GAS-{uuid4().hex}",
        "id_mascota": mascota_id,
    }

    try:
        row = db.execute(query, parametros).first()
        db.commit()

        return dict(row._mapping) if row else None

    except Exception:
        db.rollback()
        raise


def actualizar_gasto(
    db: Session,
    gasto_id: str,
    datos: dict,
):
    campos_permitidos = {
        "fecha",
        "categoria",
        "descripcion",
        "valor",
    }

    if not datos or not set(datos).issubset(campos_permitidos):
        return None

    asignaciones = ", ".join(
        f"{campo} = :{campo}"
        for campo in datos
    )

    query = text(f"""
        UPDATE gastos
        SET {asignaciones}
        WHERE id = :gasto_id
        RETURNING
            id,
            id_mascota,
            fecha,
            categoria,
            descripcion,
            valor
    """)

    try:
        row = db.execute(
            query,
            {
                **datos,
                "gasto_id": gasto_id,
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