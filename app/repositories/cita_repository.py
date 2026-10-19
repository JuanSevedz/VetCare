from sqlalchemy import text
from sqlalchemy.orm import Session
from uuid import uuid4

COLUMNAS_CITA = """
    c.id,
    c.id_mascota,
    c.id_veterinario,
    c.fecha,
    c.hora,
    c.motivo,
    c.estado
"""


def _convertir_fila(fila):
    return dict(fila._mapping) if fila is not None else None


def obtener_citas(
    db: Session,
    rol: str,
    usuario_id: str,
):
    consulta_base = f"""
        SELECT DISTINCT {COLUMNAS_CITA}
        FROM citas c
        JOIN mascotas m ON m.id = c.id_mascota
    """

    if rol == "ADMIN":
        consulta = consulta_base + " ORDER BY c.fecha, c.hora"
        resultado = db.execute(text(consulta))

    elif rol == "VETERINARIO":
        consulta = consulta_base + """
            WHERE c.id_veterinario = :usuario_id
            ORDER BY c.fecha, c.hora
        """
        resultado = db.execute(
            text(consulta),
            {"usuario_id": usuario_id},
        )

    else:
        consulta = consulta_base + """
            WHERE m.id_propietario = :usuario_id
            ORDER BY c.fecha, c.hora
        """
        resultado = db.execute(
            text(consulta),
            {"usuario_id": usuario_id},
        )

    return [dict(fila._mapping) for fila in resultado]


def obtener_cita_por_id(
    db: Session,
    cita_id: str,
    rol: str,
    usuario_id: str,
):
    consulta = text(f"""
        SELECT {COLUMNAS_CITA}
        FROM citas c
        JOIN mascotas m ON m.id = c.id_mascota
        WHERE c.id = :cita_id
          AND (
              :rol = 'ADMIN'
              OR (:rol = 'VETERINARIO' AND c.id_veterinario = :usuario_id)
              OR (:rol = 'PROPIETARIO' AND m.id_propietario = :usuario_id)
          )
    """)

    resultado = db.execute(
        consulta,
        {
            "cita_id": cita_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    )

    return _convertir_fila(resultado.first())


def mascota_pertenece_a_propietario(
    db: Session,
    mascota_id: str,
    propietario_id: str,
) -> bool:
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


def veterinario_existe(
    db: Session,
    veterinario_id: str,
) -> bool:
    resultado = db.execute(
        text("""
            SELECT 1
            FROM personal_veterinario
            WHERE id_usuario = :veterinario_id
        """),
        {"veterinario_id": veterinario_id},
    )

    return resultado.first() is not None


def crear_cita(db: Session, datos: dict):
    # Generar un identificador único en el backend.
    datos_insertar = {
        **datos,
        "id": f"CIT-{uuid4().hex}",
    }

    consulta = text("""
        INSERT INTO citas (
            id,
            id_mascota,
            id_veterinario,
            fecha,
            hora,
            motivo,
            estado
        )
        VALUES (
            :id,
            :id_mascota,
            :id_veterinario,
            :fecha,
            :hora,
            :motivo,
            'Pendiente'
        )
        RETURNING
            id,
            id_mascota,
            id_veterinario,
            fecha,
            hora,
            motivo,
            estado
    """)

    try:
        resultado = db.execute(consulta, datos_insertar)
        fila = resultado.first()

        if fila is None:
            raise RuntimeError("No se pudo crear la cita")

        cita = dict(fila._mapping)
        db.commit()

        return cita

    except Exception:
        db.rollback()
        raise

def actualizar_cita(
    db: Session,
    cita_id: str,
    rol: str,
    usuario_id: str,
    datos: dict,
):
    campos_permitidos = {
        "fecha",
        "hora",
        "motivo",
        "estado",
        "id_veterinario",
    }

    if not datos or not set(datos).issubset(campos_permitidos):
        return None

    asignaciones = ", ".join(
        f"{campo} = :{campo}" for campo in datos
    )

    consulta = text(f"""
        UPDATE citas c
        SET {asignaciones}
        WHERE c.id = :cita_id
          AND (
              :rol = 'ADMIN'
              OR (
                  :rol = 'VETERINARIO'
                  AND c.id_veterinario = :usuario_id
              )
              OR (
                  :rol = 'PROPIETARIO'
                  AND EXISTS (
                      SELECT 1
                      FROM mascotas m
                      WHERE m.id = c.id_mascota
                        AND m.id_propietario = :usuario_id
                  )
              )
          )
        RETURNING
            c.id,
            c.id_mascota,
            c.id_veterinario,
            c.fecha,
            c.hora,
            c.motivo,
            c.estado
    """)

    try:
        resultado = db.execute(
            consulta,
            {
                **datos,
                "cita_id": cita_id,
                "rol": rol,
                "usuario_id": usuario_id,
            },
        )

        fila = resultado.first()

        if fila is None:
            db.rollback()
            return None

        cita = dict(fila._mapping)
        db.commit()
        return cita

    except Exception:
        db.rollback()
        raise

def existe_conflicto_cita(
    db: Session,
    id_mascota: str,
    id_veterinario: str,
    fecha,
    hora: str,
    excluir_cita_id: str | None = None,
) -> bool:
    consulta = text("""
        SELECT EXISTS (
            SELECT 1
            FROM citas c
            WHERE c.fecha = :fecha
              AND c.hora = :hora
              AND c.estado <> 'Cancelada'
              AND (
                  c.id_mascota = :id_mascota
                  OR c.id_veterinario = :id_veterinario
              )
              AND (
                  CAST(:excluir_cita_id AS VARCHAR) IS NULL
                  OR c.id <> :excluir_cita_id
              )
        )
    """)

    resultado = db.execute(
        consulta,
        {
            "id_mascota": id_mascota,
            "id_veterinario": id_veterinario,
            "fecha": fecha,
            "hora": hora,
            "excluir_cita_id": excluir_cita_id,
        },
    )

    return resultado.scalar()