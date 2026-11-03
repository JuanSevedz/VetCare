from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


def _convertir_fila(fila):
    return dict(fila._mapping) if fila is not None else None


def obtener_consultas(
    db: Session,
    rol: str,
    usuario_id: str,
):
    consulta = """
        SELECT
            c.id,
            c.id_historia_clinica,
            c.id_veterinario,
            c.id_cita,
            c.fecha,
            c.motivo,
            c.diagnostico,
            c.tratamiento
        FROM consultas c
        JOIN historias_clinicas h
            ON h.id = c.id_historia_clinica
        JOIN mascotas m
            ON m.id = h.id_mascota
    """

    if rol == "ADMIN":
        consulta += " ORDER BY c.fecha DESC"
        parametros = {}

    elif rol == "VETERINARIO":
        consulta += """
            WHERE c.id_veterinario = :usuario_id
            ORDER BY c.fecha DESC
        """

        parametros = {"usuario_id": usuario_id}

    else:
        consulta += """
            WHERE m.id_propietario = :usuario_id
            ORDER BY c.fecha DESC
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


def obtener_consulta_por_id(
    db: Session,
    consulta_id: str,
    rol: str,
    usuario_id: str,
):
    consulta = text("""
        SELECT
            c.id,
            c.id_historia_clinica,
            c.id_veterinario,
            c.id_cita,
            c.fecha,
            c.motivo,
            c.diagnostico,
            c.tratamiento
        FROM consultas c
        JOIN historias_clinicas h
            ON h.id = c.id_historia_clinica
        JOIN mascotas m
            ON m.id = h.id_mascota
        WHERE c.id = :consulta_id
          AND (
              :rol = 'ADMIN'
              OR (
                  :rol = 'VETERINARIO'
                  AND c.id_veterinario = :usuario_id
              )
              OR (
                  :rol = 'PROPIETARIO'
                  AND m.id_propietario = :usuario_id
              )
          )
    """)

    resultado = db.execute(
        consulta,
        {
            "consulta_id": consulta_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    )

    return _convertir_fila(resultado.first())


def obtener_cita_para_consulta(
    db: Session,
    cita_id: str,
    historia_id: str,
):
    resultado = db.execute(
        text("""
            SELECT
                c.id,
                c.id_mascota,
                c.id_veterinario,
                c.fecha,
                c.estado
            FROM citas c
            JOIN mascotas m
                ON m.id = c.id_mascota
            JOIN historias_clinicas h
                ON h.id_mascota = m.id
            WHERE c.id = :cita_id
              AND h.id = :historia_id
        """),
        {
            "cita_id": cita_id,
            "historia_id": historia_id,
        },
    )

    return _convertir_fila(resultado.first())


def existe_consulta_por_cita(
    db: Session,
    cita_id: str,
):
    resultado = db.execute(
        text("""
            SELECT 1
            FROM consultas
            WHERE id_cita = :cita_id
        """),
        {"cita_id": cita_id},
    )

    return resultado.first() is not None


def crear_consulta(
    db: Session,
    datos: dict,
):
    datos_insertar = {
        **datos,
        "id": f"CON-{uuid4().hex}",
    }

    try:
        # La cita debe pertenecer al veterinario y estar confirmada.
        resultado_cita = db.execute(
            text("""
                UPDATE citas
                SET estado = 'Atendida'
                WHERE id = :id_cita
                  AND id_veterinario = :id_veterinario
                  AND estado = 'Confirmada'
                RETURNING id
            """),
            {
                "id_cita": datos_insertar["id_cita"],
                "id_veterinario": datos_insertar["id_veterinario"],
            },
        )

        if resultado_cita.first() is None:
            db.rollback()
            return None

        resultado = db.execute(
            text("""
                INSERT INTO consultas (
                    id,
                    id_historia_clinica,
                    id_veterinario,
                    id_cita,
                    fecha,
                    motivo,
                    diagnostico,
                    tratamiento
                )
                VALUES (
                    :id,
                    :id_historia_clinica,
                    :id_veterinario,
                    :id_cita,
                    :fecha,
                    :motivo,
                    :diagnostico,
                    :tratamiento
                )
                RETURNING
                    id,
                    id_historia_clinica,
                    id_veterinario,
                    id_cita,
                    fecha,
                    motivo,
                    diagnostico,
                    tratamiento
            """),
            datos_insertar,
        )

        fila = resultado.first()

        if fila is None:
            raise RuntimeError(
                "No se pudo registrar la consulta"
            )

        consulta = dict(fila._mapping)

        db.commit()

        return consulta

    except Exception:
        db.rollback()
        raise


def actualizar_consulta(
    db: Session,
    consulta_id: str,
    datos: dict,
):
    campos_permitidos = {
        "diagnostico",
        "tratamiento",
    }

    if not datos or not set(datos).issubset(campos_permitidos):
        return None

    asignaciones = ", ".join(
        f"{campo} = :{campo}"
        for campo in datos
    )

    try:
        resultado = db.execute(
            text(f"""
                UPDATE consultas
                SET {asignaciones}
                WHERE id = :consulta_id
                RETURNING
                    id,
                    id_historia_clinica,
                    id_veterinario,
                    id_cita,
                    fecha,
                    motivo,
                    diagnostico,
                    tratamiento
            """),
            {
                **datos,
                "consulta_id": consulta_id,
            },
        )

        fila = resultado.first()

        if fila is None:
            db.rollback()
            return None

        consulta = dict(fila._mapping)
        db.commit()

        return consulta

    except Exception:
        db.rollback()
        raise


def obtener_sintomas(
    db: Session,
    consulta_id: str,
):
    resultado = db.execute(
        text("""
            SELECT id, id_consulta, sintoma
            FROM sintomas_consulta
            WHERE id_consulta = :consulta_id
            ORDER BY id
        """),
        {"consulta_id": consulta_id},
    )

    return [
        dict(fila._mapping)
        for fila in resultado
    ]


def obtener_observaciones(
    db: Session,
    consulta_id: str,
):
    resultado = db.execute(
        text("""
            SELECT id, id_consulta, observacion
            FROM observaciones_consulta
            WHERE id_consulta = :consulta_id
            ORDER BY id
        """),
        {"consulta_id": consulta_id},
    )

    return [
        dict(fila._mapping)
        for fila in resultado
    ]


def crear_sintoma(
    db: Session,
    consulta_id: str,
    sintoma: str,
):
    datos = {
        "id": f"SINT-{uuid4().hex}",
        "id_consulta": consulta_id,
        "sintoma": sintoma,
    }

    try:
        resultado = db.execute(
            text("""
                INSERT INTO sintomas_consulta (
                    id,
                    id_consulta,
                    sintoma
                )
                VALUES (
                    :id,
                    :id_consulta,
                    :sintoma
                )
                RETURNING id, id_consulta, sintoma
            """),
            datos,
        )

        fila = resultado.first()
        registro = dict(fila._mapping)

        db.commit()

        return registro

    except Exception:
        db.rollback()
        raise


def crear_observacion(
    db: Session,
    consulta_id: str,
    observacion: str,
):
    datos = {
        "id": f"OBS-{uuid4().hex}",
        "id_consulta": consulta_id,
        "observacion": observacion,
    }

    try:
        resultado = db.execute(
            text("""
                INSERT INTO observaciones_consulta (
                    id,
                    id_consulta,
                    observacion
                )
                VALUES (
                    :id,
                    :id_consulta,
                    :observacion
                )
                RETURNING id, id_consulta, observacion
            """),
            datos,
        )

        fila = resultado.first()
        registro = dict(fila._mapping)

        db.commit()

        return registro

    except Exception:
        db.rollback()
        raise