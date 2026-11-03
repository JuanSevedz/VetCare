import pytest
from sqlalchemy import text
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from app.core.auth import crear_access_token


# ============================================================
# AUTENTICACIÓN DE PRUEBAS
# ============================================================

def obtener_headers(usuario_id, rol):
    token = crear_access_token(usuario_id, rol)

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def segundo_veterinario(db_session):
    db_session.execute(
        text("""
            INSERT INTO usuarios (
                id, nombre, correo, contrasena, telefono, rol
            )
            VALUES (
                'USR004',
                'Pedro Ramírez',
                'pedro.ramirez@vetcare.test',
                'hash_test_004',
                '3021234567',
                'VETERINARIO'
            )
        """)
    )

    db_session.execute(
        text("""
            INSERT INTO personal_veterinario (
                id_usuario, especialidad, numero_licencia
            )
            VALUES (
                'USR004',
                'Medicina veterinaria general',
                'LIC-VET-004'
            )
        """)
    )

    return obtener_headers("USR004", "VETERINARIO")
# ============================================================
# HISTORIAS CLÍNICAS
# ============================================================

def test_propietario_consulta_su_historia_clinica(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.get(
        "/historias-clinicas/HC001",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "HC001"
    assert data["id_mascota"] == "PET001"


def test_propietario_no_consulta_historia_de_otra_mascota(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.get(
        "/historias-clinicas/HC002",
        headers=headers,
    )

    assert response.status_code == 404


def test_no_permitir_historia_clinica_duplicada(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/historias-clinicas/",
        headers=headers,
        json={
            "id_mascota": "PET001"
        },
    )

    assert response.status_code == 409


def test_propietario_no_crea_historia_para_mascota_ajena(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/historias-clinicas/",
        headers=headers,
        json={
            "id_mascota": "PET002"
        },
    )

    assert response.status_code == 403


def test_historia_clinica_de_mascota_inexistente(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/historias-clinicas/",
        headers=headers,
        json={
            "id_mascota": "PET999"
        },
    )

    assert response.status_code == 404


# ============================================================
# CONSULTAS VETERINARIAS
# ============================================================

def test_propietario_consulta_su_consulta_medica(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.get(
        "/consultas/CONS001",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "CONS001"
    assert data["id_historia_clinica"] == "HC001"
    assert data["id_veterinario"] == "USR002"


def test_propietario_no_consulta_historia_medica_ajena(test_client):
    headers = obtener_headers("USR003", "PROPIETARIO")

    response = test_client.get(
        "/consultas/CONS001",
        headers=headers,
    )

    assert response.status_code == 404


def test_propietario_no_puede_registrar_consulta(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/consultas/",
        headers=headers,
        json={
            "id_historia_clinica": "HC001",
            "id_cita": "CIT001",
            "fecha": "2026-09-20",
            "motivo": "Control veterinario",
            "diagnostico": "Paciente estable",
            "tratamiento": "Seguimiento"
        },
    )

    assert response.status_code == 403


# ============================================================
# FLUJO COMPLETO DE CONSULTA
# ============================================================

def test_registrar_consulta_y_actualizar_cita(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.post(
        "/consultas/",
        headers=headers,
        json={
            "id_historia_clinica": "HC002",
            "id_cita": "CIT002",
            "fecha": "2026-09-28",
            "motivo": "Vacunación anual",
            "diagnostico": "Paciente en buen estado general.",
            "tratamiento": "Aplicación de vacuna según esquema."
        },
    )

    assert response.status_code == 201

    consulta = response.json()

    assert consulta["id"].startswith("CON-")
    assert consulta["id_historia_clinica"] == "HC002"
    assert consulta["id_veterinario"] == "USR002"
    assert consulta["id_cita"] == "CIT002"

    consulta_id = consulta["id"]

    # Verificar que la cita cambió a Atendida.
    citas = test_client.get(
        "/citas/",
        headers=headers,
    )

    assert citas.status_code == 200

    cita = next(
        item for item in citas.json()
        if item["id"] == "CIT002"
    )

    assert cita["estado"] == "Atendida"

    # Verificar que no se permita registrar otra consulta.
    duplicada = test_client.post(
        "/consultas/",
        headers=headers,
        json={
            "id_historia_clinica": "HC002",
            "id_cita": "CIT002",
            "fecha": "2026-09-28",
            "motivo": "Segunda consulta",
            "diagnostico": "Paciente estable",
            "tratamiento": "Seguimiento"
        },
    )

    assert duplicada.status_code == 409

    # Registrar un síntoma.
    sintoma = test_client.post(
        f"/consultas/{consulta_id}/sintomas",
        headers=headers,
        json={
            "sintoma": "Temperatura corporal ligeramente elevada."
        },
    )

    assert sintoma.status_code == 201
    assert sintoma.json()["sintoma"] == (
        "Temperatura corporal ligeramente elevada."
    )

    # Consultar síntomas.
    sintomas = test_client.get(
        f"/consultas/{consulta_id}/sintomas",
        headers=headers,
    )

    assert sintomas.status_code == 200
    assert len(sintomas.json()) == 1

    # Registrar una observación.
    observacion = test_client.post(
        f"/consultas/{consulta_id}/observaciones",
        headers=headers,
        json={
            "observacion": "Se recomienda seguimiento de la evolución."
        },
    )

    assert observacion.status_code == 201

    # Consultar observaciones.
    observaciones = test_client.get(
        f"/consultas/{consulta_id}/observaciones",
        headers=headers,
    )

    assert observaciones.status_code == 200
    assert len(observaciones.json()) == 1

    # Actualizar diagnóstico y tratamiento.
    actualizacion = test_client.patch(
        f"/consultas/{consulta_id}",
        headers=headers,
        json={
            "diagnostico": "Paciente estable después de la valoración.",
            "tratamiento": "Seguimiento y control preventivo."
        },
    )

    assert actualizacion.status_code == 200

    data_actualizada = actualizacion.json()

    assert data_actualizada["diagnostico"] == (
        "Paciente estable después de la valoración."
    )

    assert data_actualizada["tratamiento"] == (
        "Seguimiento y control preventivo."
    )


# ============================================================
# CONTROL DE PERMISOS SOBRE SÍNTOMAS Y OBSERVACIONES
# ============================================================

def test_propietario_no_puede_registrar_sintomas(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/consultas/CONS001/sintomas",
        headers=headers,
        json={
            "sintoma": "Prueba de permisos"
        },
    )

    assert response.status_code == 403


def test_propietario_no_puede_registrar_observaciones(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/consultas/CONS001/observaciones",
        headers=headers,
        json={
            "observacion": "Prueba de permisos"
        },
    )

    assert response.status_code == 403
# ============================================================
# VALIDACIONES ADICIONALES DE CONSULTAS
# ============================================================

def test_consulta_inexistente(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.get(
        "/consultas/CONS999",
        headers=headers,
    )

    assert response.status_code == 404


def test_veterinario_no_puede_crear_historia_clinica(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.post(
        "/historias-clinicas/",
        headers=headers,
        json={
            "id_mascota": "PET001"
        },
    )

    assert response.status_code == 403


def test_veterinario_consulta_sus_consultas(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.get(
        "/consultas/",
        headers=headers,
    )

    assert response.status_code == 200

    consultas = response.json()

    assert any(
        consulta["id"] == "CONS001"
        for consulta in consultas
    )


def test_propietario_consulta_su_listado_de_historias(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.get(
        "/historias-clinicas/",
        headers=headers,
    )

    assert response.status_code == 200

    historias = response.json()

    assert all(
        historia["id_mascota"] == "PET001"
        for historia in historias
    )
# ============================================================
# VALIDACIONES DE FECHAS Y ESTADOS DE CONSULTAS
# ============================================================

def test_no_permitir_consulta_con_fecha_futura(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.post(
        "/consultas/",
        headers=headers,
        json={
            "id_historia_clinica": "HC002",
            "id_cita": "CIT002",
            "fecha": "2099-12-31",
            "motivo": "Control veterinario",
            "diagnostico": "Paciente estable",
            "tratamiento": "Seguimiento"
        },
    )

    assert response.status_code == 422
    assert "futuro" in response.json()["detail"]


def test_no_permitir_consulta_con_fecha_diferente_a_cita(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.post(
        "/consultas/",
        headers=headers,
        json={
            "id_historia_clinica": "HC002",
            "id_cita": "CIT002",
            "fecha": "2026-09-27",
            "motivo": "Control veterinario",
            "diagnostico": "Paciente estable",
            "tratamiento": "Seguimiento"
        },
    )

    assert response.status_code == 422
    assert "coincidir" in response.json()["detail"]


def test_no_permitir_consulta_para_cita_atendida(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.post(
        "/consultas/",
        headers=headers,
        json={
            "id_historia_clinica": "HC001",
            "id_cita": "CIT001",
            "fecha": "2026-09-20",
            "motivo": "Nueva valoración",
            "diagnostico": "Paciente estable",
            "tratamiento": "Seguimiento"
        },
    )

    assert response.status_code == 409
    assert "confirmada" in response.json()["detail"]

# ============================================================
# AISLAMIENTO ENTRE VETERINARIOS
# ============================================================

def test_veterinario_no_consulta_consulta_de_otro_veterinario(
    test_client,
    segundo_veterinario,
):
    response = test_client.get(
        "/consultas/CONS001",
        headers=segundo_veterinario,
    )

    assert response.status_code == 404


def test_veterinario_no_modifica_consulta_de_otro_veterinario(
    test_client,
    segundo_veterinario,
):
    response = test_client.patch(
        "/consultas/CONS001",
        headers=segundo_veterinario,
        json={
            "diagnostico": "Intento de modificación no autorizado."
        },
    )

    assert response.status_code == 404


def test_veterinario_no_lista_consultas_de_otro_veterinario(
    test_client,
    segundo_veterinario,
):
    response = test_client.get(
        "/consultas/",
        headers=segundo_veterinario,
    )

    assert response.status_code == 200

    consultas = response.json()

    assert all(
        consulta["id_veterinario"] == "USR004"
        for consulta in consultas
    )

    assert not any(
        consulta["id"] == "CONS001"
        for consulta in consultas
    )
# ============================================================
# PRUEBAS DE PERMISOS Y TRANSICIONES DE CITAS
# ============================================================

def _crear_cita_pendiente(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/citas/",
        headers=headers,
        json={
            "id_mascota": "PET001",
            "id_veterinario": "USR002",
            "fecha": "2027-04-12",
            "hora": "10:00",
            "motivo": "Prueba de transiciones"
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_propietario_no_puede_confirmar_cita(test_client):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Confirmada"},
    )

    assert response.status_code == 403


def test_propietario_no_puede_cambiar_veterinario(test_client):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"id_veterinario": "USR002"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "No puedes cambiar el veterinario asignado"
    )


def test_veterinario_no_puede_modificar_fecha_cita(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.patch(
        "/citas/CIT002",
        headers=headers,
        json={"fecha": "2027-04-13"},
    )

    assert response.status_code == 403


def test_veterinario_no_puede_atender_cita_pendiente(test_client):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Atendida"},
    )

    assert response.status_code == 409


def test_no_permitir_reabrir_cita_atendida(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.patch(
        "/citas/CIT001",
        headers=headers,
        json={"estado": "Confirmada"},
    )

    assert response.status_code == 409


def test_no_permitir_modificar_cita_cancelada(test_client):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR001", "PROPIETARIO")

    cancelacion = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Cancelada"},
    )

    assert cancelacion.status_code == 200
    assert cancelacion.json()["estado"] == "Cancelada"

    modificacion = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"motivo": "Intento de modificación"},
    )

    assert modificacion.status_code == 409

def test_propietario_puede_cancelar_cita_pendiente(test_client):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Cancelada"},
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "Cancelada"


def test_veterinario_puede_confirmar_cita_pendiente(test_client):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Confirmada"},
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "Confirmada"


def test_veterinario_puede_atender_cita_confirmada(test_client):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR002", "VETERINARIO")

    confirmacion = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Confirmada"},
    )

    assert confirmacion.status_code == 200

    atencion = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Atendida"},
    )

    assert atencion.status_code == 200
    assert atencion.json()["estado"] == "Atendida"


def test_veterinario_puede_cancelar_cita_confirmada(test_client):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR002", "VETERINARIO")

    confirmacion = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Confirmada"},
    )

    assert confirmacion.status_code == 200

    cancelacion = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"estado": "Cancelada"},
    )

    assert cancelacion.status_code == 200
    assert cancelacion.json()["estado"] == "Cancelada"



def test_veterinario_no_puede_tener_citas_simultaneas(
    test_client
):
    # Primera cita: mascota PET001 con veterinario USR002.
    _crear_cita_pendiente(test_client)

    # Segunda cita: mascota PET002, mismo veterinario,
    # misma fecha y hora.
    headers = obtener_headers("USR003", "PROPIETARIO")

    response = test_client.post(
        "/citas/",
        headers=headers,
        json={
            "id_mascota": "PET002",
            "id_veterinario": "USR002",
            "fecha": "2027-04-12",
            "hora": "10:00",
            "motivo": "Prueba de conflicto entre mascotas",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "La mascota o el veterinario ya tiene una cita activa "
        "en esa fecha y hora"
    )


def test_cita_cancelada_libera_horario_del_veterinario(
    test_client
):
    # Crear primera cita para PET001.
    cita_id = _crear_cita_pendiente(test_client)

    # Cancelarla como propietario.
    headers_propietario = obtener_headers(
        "USR001",
        "PROPIETARIO",
    )

    cancelacion = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers_propietario,
        json={"estado": "Cancelada"},
    )

    assert cancelacion.status_code == 200
    assert cancelacion.json()["estado"] == "Cancelada"

    # Intentar reservar el mismo horario para PET002
    # con el mismo veterinario.
    headers_otro_propietario = obtener_headers(
        "USR003",
        "PROPIETARIO",
    )

    nueva_cita = test_client.post(
        "/citas/",
        headers=headers_otro_propietario,
        json={
            "id_mascota": "PET002",
            "id_veterinario": "USR002",
            "fecha": "2027-04-12",
            "hora": "10:00",
            "motivo": "Nueva reserva después de cancelación",
        },
    )

    assert nueva_cita.status_code == 201
    assert nueva_cita.json()["estado"] == "Pendiente"

def test_propietario_puede_reprogramar_cita_a_horario_disponible(
    test_client
):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={
            "fecha": "2027-04-13",
            "hora": "10:30",
        },
    )

    assert response.status_code == 200
    assert response.json()["fecha"] == "2027-04-13"
    assert response.json()["hora"] == "10:30"


def test_no_permitir_reprogramar_cita_a_horario_ocupado(
    test_client
):
    # Primera cita: PET001, USR002, 12 de abril a las 10:00.
    cita_id = _crear_cita_pendiente(test_client)

    # Segunda cita: PET002, mismo veterinario,
    # 13 de abril a las 10:00.
    headers_ana = obtener_headers("USR003", "PROPIETARIO")

    segunda_cita = test_client.post(
        "/citas/",
        headers=headers_ana,
        json={
            "id_mascota": "PET002",
            "id_veterinario": "USR002",
            "fecha": "2027-04-13",
            "hora": "10:00",
            "motivo": "Prueba de disponibilidad",
        },
    )

    assert segunda_cita.status_code == 201

    # Intentar reprogramar la primera cita al horario ocupado.
    headers_carlos = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers_carlos,
        json={
            "fecha": "2027-04-13",
            "hora": "10:00",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "La mascota o el veterinario ya tiene otra cita activa "
        "en esa fecha y hora"
    )


def test_no_permitir_reprogramar_cita_a_fecha_pasada(
    test_client
):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"fecha": "2020-01-01"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "La fecha de la cita no puede estar en el pasado"
    )


def test_no_permitir_reprogramar_cita_a_domingo(
    test_client
):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"fecha": "2027-04-18"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "VetCare no atiende los domingos"
    )


def test_no_permitir_reprogramar_cita_fuera_del_horario(
    test_client
):
    cita_id = _crear_cita_pendiente(test_client)
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers,
        json={"hora": "19:00"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "Las citas deben programarse entre las 08:00 y las 18:00"
    )
def test_propietario_solo_consulta_sus_citas(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.get(
        "/citas/",
        headers=headers,
    )

    assert response.status_code == 200

    ids_mascotas = {
        cita["id_mascota"] for cita in response.json()
    }

    assert "PET001" in ids_mascotas
    assert "PET002" not in ids_mascotas


def test_propietario_no_consulta_cita_de_otro_propietario(
    test_client
):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.get(
        "/citas/CIT002",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cita no encontrada"


def test_propietario_no_modifica_cita_de_otro_propietario(
    test_client
):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        "/citas/CIT002",
        headers=headers,
        json={"motivo": "Intento de modificación no autorizada"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cita no encontrada"


def test_propietario_no_cancela_cita_de_otro_propietario(
    test_client
):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.patch(
        "/citas/CIT002",
        headers=headers,
        json={"estado": "Cancelada"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cita no encontrada"


def test_veterinario_no_modifica_cita_de_otro_veterinario(
    test_client,
    db_session,
):
    # Crear un segundo usuario veterinario para la prueba.
    db_session.execute(
        text("""
            INSERT INTO usuarios (
                id,
                nombre,
                correo,
                contrasena,
                telefono,
                rol
            )
            VALUES (
                'USR004',
                'Pedro Ramírez',
                'pedro.ramirez@vetcare.test',
                'hash_demo_004',
                '3001112233',
                'VETERINARIO'
            )
        """)
    )

    db_session.execute(
        text("""
            INSERT INTO personal_veterinario (
                id_usuario,
                especialidad,
                numero_licencia
            )
            VALUES (
                'USR004',
                'Medicina veterinaria',
                'LIC-VET-004'
            )
        """)
    )

    # Asignar CIT002 al segundo veterinario.
    db_session.execute(
        text("""
            UPDATE citas
            SET id_veterinario = 'USR004'
            WHERE id = 'CIT002'
        """)
    )

    # USR002 intenta cancelar una cita asignada a USR004.
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.patch(
        "/citas/CIT002",
        headers=headers,
        json={"estado": "Cancelada"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Cita no encontrada"

def _preparar_veterinario_adicional_y_admin(db_session):
    db_session.execute(
        text("""
            INSERT INTO usuarios (
                id, nombre, correo, contrasena, telefono, rol
            )
            VALUES
                (
                    'USR004',
                    'Pedro Ramírez',
                    'pedro.ramirez@vetcare.test',
                    'hash_demo_004',
                    '3001112233',
                    'VETERINARIO'
                ),
                (
                    'USR005',
                    'Administrador de prueba',
                    'admin@vetcare.test',
                    'hash_demo_005',
                    '3001112234',
                    'ADMIN'
                )
        """)
    )

    db_session.execute(
        text("""
            INSERT INTO personal_veterinario (
                id_usuario,
                especialidad,
                numero_licencia
            )
            VALUES (
                'USR004',
                'Medicina veterinaria general',
                'LIC-VET-004'
            )
        """)
    )
def test_no_permitir_cita_para_mascota_inexistente(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/citas/",
        headers=headers,
        json={
            "id_mascota": "PET999",
            "id_veterinario": "USR002",
            "fecha": "2027-04-12",
            "hora": "10:00",
            "motivo": "Prueba de mascota inexistente",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Solo puedes solicitar citas para tus propias mascotas"
    )


def test_no_permitir_cita_con_veterinario_inexistente(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")

    response = test_client.post(
        "/citas/",
        headers=headers,
        json={
            "id_mascota": "PET001",
            "id_veterinario": "USR999",
            "fecha": "2027-04-12",
            "hora": "10:00",
            "motivo": "Prueba de veterinario inexistente",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "El veterinario seleccionado no tiene un perfil válido"
    )


def test_admin_puede_cambiar_veterinario_si_hay_disponibilidad(
    test_client,
    db_session,
):
    _preparar_veterinario_adicional_y_admin(db_session)

    # Crear cita para PET002 con el veterinario USR004.
    headers_propietario = obtener_headers(
        "USR003",
        "PROPIETARIO",
    )

    creacion = test_client.post(
        "/citas/",
        headers=headers_propietario,
        json={
            "id_mascota": "PET002",
            "id_veterinario": "USR004",
            "fecha": "2027-04-13",
            "hora": "10:00",
            "motivo": "Prueba de reasignación",
        },
    )

    assert creacion.status_code == 201

    cita_id = creacion.json()["id"]

    # El administrador cambia el veterinario a USR002.
    headers_admin = obtener_headers("USR005", "ADMIN")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers_admin,
        json={"id_veterinario": "USR002"},
    )

    assert response.status_code == 200
    assert response.json()["id_veterinario"] == "USR002"


def test_no_permitir_cambiar_a_veterinario_con_horario_ocupado(
    test_client,
    db_session,
):
    _preparar_veterinario_adicional_y_admin(db_session)

    # Primera cita: PET001 con USR002 a las 10:00.
    _crear_cita_pendiente(test_client)

    # Segunda cita: PET002 con USR004 en el mismo horario.
    headers_propietario = obtener_headers(
        "USR003",
        "PROPIETARIO",
    )

    segunda_cita = test_client.post(
        "/citas/",
        headers=headers_propietario,
        json={
            "id_mascota": "PET002",
            "id_veterinario": "USR004",
            "fecha": "2027-04-12",
            "hora": "10:00",
            "motivo": "Prueba de conflicto de reasignación",
        },
    )

    assert segunda_cita.status_code == 201

    cita_id = segunda_cita.json()["id"]

    # Intentar asignar la segunda cita a USR002.
    headers_admin = obtener_headers("USR005", "ADMIN")

    response = test_client.patch(
        f"/citas/{cita_id}",
        headers=headers_admin,
        json={"id_veterinario": "USR002"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "La mascota o el veterinario ya tiene otra cita activa "
        "en esa fecha y hora"
    )


def test_no_permitir_reasignar_a_veterinario_inexistente(
    test_client,
    db_session,
):
    _preparar_veterinario_adicional_y_admin(db_session)

    headers_admin = obtener_headers("USR005", "ADMIN")

    response = test_client.patch(
        "/citas/CIT002",
        headers=headers_admin,
        json={"id_veterinario": "USR999"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "El veterinario seleccionado no tiene un perfil válido"
    )

def test_error_al_insertar_consulta_revierte_estado_de_cita(
    test_client,
    db_session,
):
    from unittest.mock import patch

    headers = obtener_headers("USR002", "VETERINARIO")

    datos = {
        "id_historia_clinica": "HC002",
        "id_cita": "CIT002",
        "fecha": "2026-09-28",
        "motivo": "Prueba transaccional",
        "diagnostico": "Diagnóstico de prueba",
        "tratamiento": "Tratamiento de prueba",
    }

    with patch(
        "app.repositories.consulta_repository.db.execute",
        side_effect=IntegrityError(
            "INSERT",
            {},
            Exception("Error simulado"),
        ),
    ):
        pass

def test_error_al_insertar_consulta_revierte_estado_de_cita(
    test_client,
    db_session,
):
    headers = obtener_headers("USR002", "VETERINARIO")

    datos = {
        "id_historia_clinica": "HC002",
        "id_cita": "CIT002",
        "fecha": "2026-09-28",
        "motivo": "Prueba transaccional",
        "diagnostico": "Diagnóstico de prueba",
        "tratamiento": "Tratamiento de prueba",
    }

    ejecutar_original = db_session.execute

    def ejecutar_con_error_controlado(statement, *args, **kwargs):
        sql = str(statement).upper()

        # Simular un error exclusivamente al insertar la consulta.
        if "INSERT INTO CONSULTAS" in sql:
            raise IntegrityError(
                statement,
                kwargs,
                Exception("Error simulado al insertar consulta"),
            )

        return ejecutar_original(statement, *args, **kwargs)

    with patch.object(
        db_session,
        "execute",
        side_effect=ejecutar_con_error_controlado,
    ):
        response = test_client.post(
            "/consultas/",
            headers=headers,
            json=datos,
        )

    # El servicio debe responder con conflicto por el error de integridad.
    assert response.status_code == 409

    # La actualización de la cita debe haberse revertido.
    resultado_cita = db_session.execute(
        text("""
            SELECT estado
            FROM citas
            WHERE id = 'CIT002'
        """)
    ).scalar()

    assert resultado_cita == "Confirmada"

    # No debe existir una consulta parcialmente registrada.
    cantidad_consultas = db_session.execute(
        text("""
            SELECT COUNT(*)
            FROM consultas
            WHERE id_cita = 'CIT002'
        """)
    ).scalar()

    assert cantidad_consultas == 0

def test_no_permitir_consulta_con_cita_de_otra_mascota(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.post(
        "/consultas/",
        headers=headers,
        json={
            "id_historia_clinica": "HC002",
            "id_cita": "CIT001",
            "fecha": "2026-09-20",
            "motivo": "Prueba de integridad",
            "diagnostico": "Diagnóstico de prueba",
            "tratamiento": "Tratamiento de prueba",
        },
    )

    assert response.status_code == 404

def test_no_permitir_registrar_sintoma_en_consulta_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.post(
        "/consultas/CONS-INEXISTENTE/sintomas",
        headers=headers,
        json={
            "sintoma": "Fiebre",
        },
    )

    assert response.status_code == 404

def test_no_permitir_registrar_observacion_en_consulta_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")

    response = test_client.post(
        "/consultas/CONS-INEXISTENTE/observaciones",
        headers=headers,
        json={
            "observacion": "Observación de prueba",
        },
    )

    assert response.status_code == 404