from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


def _convertir_fila(fila):
    return dict(fila._mapping) if fila is not None else None


def obtener_historias_clinicas(
    db: Session,
    rol: str,
    usuario_id: str,
):
    consulta = """
        SELECT
            h.id,
            h.id_mascota,
            h.fecha_creacion
        FROM historias_clinicas h
        JOIN mascotas m ON m.id = h.id_mascota
    """

    if rol == "ADMIN":
        consulta += " ORDER BY h.fecha_creacion DESC"
        parametros = {}

    elif rol == "VETERINARIO":
        consulta += """
            WHERE EXISTS (
                SELECT 1
                FROM citas c
                WHERE c.id_mascota = h.id_mascota
                  AND c.id_veterinario = :usuario_id
            )
            ORDER BY h.fecha_creacion DESC
        """

        parametros = {"usuario_id": usuario_id}

    else:
        consulta += """
            WHERE m.id_propietario = :usuario_id
            ORDER BY h.fecha_creacion DESC
        """

        parametros = {"usuario_id": usuario_id}

    resultado = db.execute(
        text(consulta),
        parametros,
    )

    return [
        dict(fila._mapping)
        for fila in resultado
    ]


def obtener_historia_clinica_por_id(
    db: Session,
    historia_id: str,
    rol: str,
    usuario_id: str,
):
    consulta = text("""
        SELECT
            h.id,
            h.id_mascota,
            h.fecha_creacion
        FROM historias_clinicas h
        JOIN mascotas m ON m.id = h.id_mascota
        WHERE h.id = :historia_id
          AND (
              :rol = 'ADMIN'
              OR (
                  :rol = 'PROPIETARIO'
                  AND m.id_propietario = :usuario_id
              )
              OR (
                  :rol = 'VETERINARIO'
                  AND EXISTS (
                      SELECT 1
                      FROM citas c
                      WHERE c.id_mascota = h.id_mascota
                        AND c.id_veterinario = :usuario_id
                  )
              )
          )
    """)

    resultado = db.execute(
        consulta,
        {
            "historia_id": historia_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    )

    return _convertir_fila(resultado.first())


def obtener_historia_por_mascota(
    db: Session,
    mascota_id: str,
):
    resultado = db.execute(
        text("""
            SELECT
                id,
                id_mascota,
                fecha_creacion
            FROM historias_clinicas
            WHERE id_mascota = :mascota_id
        """),
        {"mascota_id": mascota_id},
    )

    return _convertir_fila(resultado.first())


def mascota_existe(
    db: Session,
    mascota_id: str,
):
    resultado = db.execute(
        text("""
            SELECT 1
            FROM mascotas
            WHERE id = :mascota_id
        """),
        {"mascota_id": mascota_id},
    )

    return resultado.first() is not None


def mascota_pertenece_a_propietario(
    db: Session,
    mascota_id: str,
    propietario_id: str,
):
    resultado = db.execute(
        text("""
            SELECT 1
            FROM mascotas
            WHERE id = :mascota_id
              AND id_propietario = :propietario_id
        """),
        {
            "mascota_id": mascota_id,
            "propietario_id": propietario_id,
        },
    )

    return resultado.first() is not None


def crear_historia_clinica(
    db: Session,
    mascota_id: str,
):
    datos = {
        "id": f"HCL-{uuid4().hex}",
        "id_mascota": mascota_id,
    }

    consulta = text("""
        INSERT INTO historias_clinicas (
            id,
            id_mascota,
            fecha_creacion
        )
        VALUES (
            :id,
            :id_mascota,
            CURRENT_DATE
        )
        RETURNING
            id,
            id_mascota,
            fecha_creacion
    """)

    try:
        resultado = db.execute(consulta, datos)
        fila = resultado.first()

        if fila is None:
            raise RuntimeError(
                "No se pudo crear la historia clínica"
            )

        historia = dict(fila._mapping)
        db.commit()

        return historia

    except Exception:
        db.rollback()
        raise