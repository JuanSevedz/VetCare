from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session


COLUMNAS = """
    id,
    id_propietario,
    id_mascota,
    fecha,
    descripcion,
    estado
"""


def listar_solicitudes_mascota(
    db: Session,
    mascota_id: str,
):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM solicitudes_seguimiento
        WHERE id_mascota = :mascota_id
        ORDER BY fecha DESC
    """)

    result = db.execute(
        query,
        {"mascota_id": mascota_id},
    )

    return [dict(row._mapping) for row in result]


def obtener_solicitud_por_id(
    db: Session,
    solicitud_id: str,
    rol: str,
    usuario_id: str,
):
    query = text(f"""
        SELECT {COLUMNAS}
        FROM solicitudes_seguimiento
        WHERE id = :solicitud_id
          AND (
              :rol IN ('ADMIN', 'VETERINARIO')
              OR (
                  :rol = 'PROPIETARIO'
                  AND id_propietario = :usuario_id
              )
          )
    """)

    row = db.execute(
        query,
        {
            "solicitud_id": solicitud_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    ).first()

    return dict(row._mapping) if row else None


def crear_solicitud(
    db: Session,
    propietario_id: str,
    mascota_id: str,
    descripcion: str,
):
    query = text("""
        INSERT INTO solicitudes_seguimiento (
            id,
            id_propietario,
            id_mascota,
            fecha,
            descripcion,
            estado
        )
        VALUES (
            :id,
            :id_propietario,
            :id_mascota,
            CURRENT_DATE,
            :descripcion,
            'Pendiente'
        )
        RETURNING
            id,
            id_propietario,
            id_mascota,
            fecha,
            descripcion,
            estado
    """)

    parametros = {
        "id": f"SOL-{uuid4().hex}",
        "id_propietario": propietario_id,
        "id_mascota": mascota_id,
        "descripcion": descripcion,
    }

    try:
        row = db.execute(query, parametros).first()
        db.commit()

        return dict(row._mapping) if row else None

    except Exception:
        db.rollback()
        raise


def actualizar_estado_solicitud(
    db: Session,
    solicitud_id: str,
    estado: str,
):
    query = text("""
        UPDATE solicitudes_seguimiento
        SET estado = :estado
        WHERE id = :solicitud_id
        RETURNING
            id,
            id_propietario,
            id_mascota,
            fecha,
            descripcion,
            estado
    """)

    try:
        row = db.execute(
            query,
            {
                "solicitud_id": solicitud_id,
                "estado": estado,
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