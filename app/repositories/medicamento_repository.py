from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


def _convertir_fila(fila):
    return dict(fila._mapping) if fila is not None else None


def obtener_medicamentos_por_consulta(
    db: Session,
    consulta_id: str,
):
    resultado = db.execute(
        text("""
            SELECT
                id,
                id_consulta,
                nombre,
                dosis,
                frecuencia,
                duracion,
                fecha_inicio,
                fecha_fin,
                estado
            FROM medicamentos_formulados
            WHERE id_consulta = :consulta_id
            ORDER BY fecha_inicio DESC, nombre
        """),
        {"consulta_id": consulta_id},
    )

    return [
        dict(fila._mapping)
        for fila in resultado
    ]


def obtener_medicamento_por_id(
    db: Session,
    medicamento_id: str,
    rol: str,
    usuario_id: str,
):
    resultado = db.execute(
        text("""
            SELECT
                mf.id,
                mf.id_consulta,
                mf.nombre,
                mf.dosis,
                mf.frecuencia,
                mf.duracion,
                mf.fecha_inicio,
                mf.fecha_fin,
                mf.estado
            FROM medicamentos_formulados mf
            JOIN consultas c
                ON c.id = mf.id_consulta
            JOIN historias_clinicas h
                ON h.id = c.id_historia_clinica
            JOIN mascotas m
                ON m.id = h.id_mascota
            WHERE mf.id = :medicamento_id
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
        """),
        {
            "medicamento_id": medicamento_id,
            "rol": rol,
            "usuario_id": usuario_id,
        },
    )

    return _convertir_fila(resultado.first())


def crear_medicamento(
    db: Session,
    consulta_id: str,
    datos: dict,
):
    datos_insertar = {
        **datos,
        "id": f"MED-{uuid4().hex}",
        "id_consulta": consulta_id,
    }

    try:
        resultado = db.execute(
            text("""
                INSERT INTO medicamentos_formulados (
                    id,
                    id_consulta,
                    nombre,
                    dosis,
                    frecuencia,
                    duracion,
                    fecha_inicio,
                    fecha_fin,
                    estado
                )
                VALUES (
                    :id,
                    :id_consulta,
                    :nombre,
                    :dosis,
                    :frecuencia,
                    :duracion,
                    :fecha_inicio,
                    :fecha_fin,
                    :estado
                )
                RETURNING
                    id,
                    id_consulta,
                    nombre,
                    dosis,
                    frecuencia,
                    duracion,
                    fecha_inicio,
                    fecha_fin,
                    estado
            """),
            datos_insertar,
        )

        fila = resultado.first()

        if fila is None:
            raise RuntimeError(
                "No se pudo registrar el medicamento"
            )

        medicamento = dict(fila._mapping)

        db.commit()

        return medicamento

    except Exception:
        db.rollback()
        raise


def actualizar_medicamento(
    db: Session,
    medicamento_id: str,
    datos: dict,
):
    campos_permitidos = {
        "nombre",
        "dosis",
        "frecuencia",
        "duracion",
        "fecha_inicio",
        "fecha_fin",
        "estado",
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
                UPDATE medicamentos_formulados
                SET {asignaciones}
                WHERE id = :medicamento_id
                RETURNING
                    id,
                    id_consulta,
                    nombre,
                    dosis,
                    frecuencia,
                    duracion,
                    fecha_inicio,
                    fecha_fin,
                    estado
            """),
            {
                **datos,
                "medicamento_id": medicamento_id,
            },
        )

        fila = resultado.first()

        if fila is None:
            db.rollback()
            return None

        medicamento = dict(fila._mapping)

        db.commit()

        return medicamento

    except Exception:
        db.rollback()
        raise
