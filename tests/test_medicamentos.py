from app.core.auth import crear_access_token


# ============================================================
# AUTENTICACIÓN DE PRUEBAS
# ============================================================

def obtener_headers(usuario_id: str, rol: str) -> dict:
    token = crear_access_token(usuario_id, rol)
    return {"Authorization": f"Bearer {token}"}


# ============================================================
# CONSULTA DE MEDICAMENTOS
# ============================================================

def test_propietario_lista_medicamentos_de_su_consulta(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get("/consultas/CONS001/medicamentos", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(m["id"] == "MED001" for m in response.json())


def test_veterinario_lista_medicamentos_de_su_consulta(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get("/consultas/CONS001/medicamentos", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(m["id"] == "MED001" for m in response.json())


def test_propietario_consulta_medicamento_individual(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get("/medicamentos/MED001", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "MED001"
    assert data["id_consulta"] == "CONS001"
    assert data["nombre"] == "Crema dermatológica veterinaria"


def test_veterinario_consulta_medicamento_individual(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get("/medicamentos/MED001", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == "MED001"


def test_propietario_no_consulta_medicamento_de_otra_mascota(test_client):
    # USR003 es propietario de PET002; MED001 corresponde a PET001.
    headers = obtener_headers("USR003", "PROPIETARIO")
    response = test_client.get("/medicamentos/MED001", headers=headers)
    assert response.status_code == 404


def test_consultar_medicamento_inexistente_devuelve_404(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get("/medicamentos/MED-INEXISTENTE", headers=headers)
    assert response.status_code == 404


def test_consultar_medicamentos_de_consulta_inexistente_devuelve_404(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get("/consultas/CONS-INEXISTENTE/medicamentos", headers=headers)
    assert response.status_code == 404


# ============================================================
# CREACIÓN DE MEDICAMENTOS
# ============================================================

def test_veterinario_puede_registrar_medicamento(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/consultas/CONS001/medicamentos",
        headers=headers,
        json={
            "nombre": "Medicamento de prueba",
            "dosis": "100 mg",
            "frecuencia": "Cada 12 horas",
            "duracion": "5 días",
            "fecha_inicio": "2026-11-03",
            "fecha_fin": "2026-11-08",
            "estado": "Activo",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("MED-")
    assert data["id_consulta"] == "CONS001"
    assert data["nombre"] == "Medicamento de prueba"
    assert data["dosis"] == "100 mg"
    assert data["frecuencia"] == "Cada 12 horas"
    assert data["duracion"] == "5 días"
    assert data["estado"] == "Activo"


def test_administrador_puede_registrar_medicamento(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, :rol)
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-MED-TEST",
            "nombre": "Administrador de pruebas",
            "correo": "admin.medicamentos.test@vetcare.test",
            "contrasena": hash_password("AdminTest2026*"),
            "rol": "ADMIN",
        },
    )
    db_session.commit()
    headers = obtener_headers("USR-ADMIN-MED-TEST", "ADMIN")
    response = test_client.post(
        "/consultas/CONS001/medicamentos",
        headers=headers,
        json={
            "nombre": "Medicamento formulado por administrador",
            "dosis": "50 mg",
            "frecuencia": "Una vez al día",
            "duracion": "3 días",
            "fecha_inicio": "2026-11-03",
            "fecha_fin": "2026-11-06",
            "estado": "Activo",
        },
    )
    assert response.status_code == 201
    assert response.json()["id_consulta"] == "CONS001"


def test_propietario_no_puede_registrar_medicamentos(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.post(
        "/consultas/CONS001/medicamentos",
        headers=headers,
        json={
            "nombre": "Medicamento no autorizado",
            "dosis": "100 mg",
            "frecuencia": "Cada 12 horas",
            "duracion": "5 días",
            "fecha_inicio": "2026-11-03",
            "fecha_fin": "2026-11-08",
            "estado": "Activo",
        },
    )
    assert response.status_code == 403


def test_veterinario_no_puede_registrar_en_consulta_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/consultas/CONS-INEXISTENTE/medicamentos",
        headers=headers,
        json={
            "nombre": "Medicamento de prueba",
            "dosis": "100 mg",
            "frecuencia": "Cada 12 horas",
            "duracion": "5 días",
            "fecha_inicio": "2026-11-03",
            "fecha_fin": "2026-11-08",
            "estado": "Activo",
        },
    )
    assert response.status_code == 404


def test_no_registrar_medicamento_con_fecha_fin_anterior(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/consultas/CONS001/medicamentos",
        headers=headers,
        json={
            "nombre": "Medicamento con fechas inválidas",
            "dosis": "100 mg",
            "frecuencia": "Cada 12 horas",
            "duracion": "5 días",
            "fecha_inicio": "2026-11-10",
            "fecha_fin": "2026-11-05",
            "estado": "Activo",
        },
    )
    assert response.status_code == 422


def test_no_registrar_medicamento_con_estado_invalido(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/consultas/CONS001/medicamentos",
        headers=headers,
        json={
            "nombre": "Medicamento con estado inválido",
            "dosis": "100 mg",
            "frecuencia": "Cada 12 horas",
            "duracion": "5 días",
            "fecha_inicio": "2026-11-03",
            "fecha_fin": "2026-11-08",
            "estado": "Pendiente",
        },
    )
    assert response.status_code == 422


def test_no_registrar_medicamento_con_nombre_vacio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/consultas/CONS001/medicamentos",
        headers=headers,
        json={
            "nombre": "   ",
            "dosis": "100 mg",
            "frecuencia": "Cada 12 horas",
            "duracion": "5 días",
            "fecha_inicio": "2026-11-03",
            "fecha_fin": "2026-11-08",
            "estado": "Activo",
        },
    )
    assert response.status_code == 422


def test_no_registrar_medicamento_sin_campo_requerido(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/consultas/CONS001/medicamentos",
        headers=headers,
        json={
            "nombre": "Medicamento incompleto",
            "dosis": "100 mg",
            "frecuencia": "Cada 12 horas",
            "duracion": "5 días",
            "fecha_inicio": "2026-11-03",
            "estado": "Activo",
        },
    )
    assert response.status_code == 422


# ============================================================
# ACTUALIZACIÓN DE MEDICAMENTOS
# ============================================================

def test_veterinario_puede_actualizar_medicamento(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.patch(
        "/medicamentos/MED001",
        headers=headers,
        json={
            "estado": "Finalizado",
            "dosis": "Aplicación tópica actualizada",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "MED001"
    assert data["estado"] == "Finalizado"
    assert data["dosis"] == "Aplicación tópica actualizada"


def test_administrador_puede_actualizar_medicamento(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, :rol)
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-MED-UPDATE",
            "nombre": "Administrador de pruebas",
            "correo": "admin.update.test@vetcare.test",
            "contrasena": hash_password("AdminTest2026*"),
            "rol": "ADMIN",
        },
    )
    db_session.commit()
    headers = obtener_headers("USR-ADMIN-MED-UPDATE", "ADMIN")
    response = test_client.patch(
        "/medicamentos/MED001",
        headers=headers,
        json={"estado": "Suspendido"},
    )
    assert response.status_code == 200
    assert response.json()["estado"] == "Suspendido"


def test_propietario_no_puede_actualizar_medicamento(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.patch(
        "/medicamentos/MED001",
        headers=headers,
        json={"estado": "Finalizado"},
    )
    assert response.status_code == 403


def test_veterinario_no_puede_actualizar_medicamento_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.patch(
        "/medicamentos/MED-INEXISTENTE",
        headers=headers,
        json={"estado": "Finalizado"},
    )
    assert response.status_code == 404


def test_no_actualizar_medicamento_con_estado_invalido(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.patch(
        "/medicamentos/MED001",
        headers=headers,
        json={"estado": "Pendiente"},
    )
    assert response.status_code == 422


def test_no_actualizar_medicamento_con_fechas_inconsistentes(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.patch(
        "/medicamentos/MED001",
        headers=headers,
        json={
            "fecha_inicio": "2026-10-10",
            "fecha_fin": "2026-10-01",
        },
    )
    assert response.status_code == 422


def test_no_actualizar_medicamento_con_campo_nulo(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.patch(
        "/medicamentos/MED001",
        headers=headers,
        json={"nombre": None},
    )
    assert response.status_code == 422


def test_no_actualizar_medicamento_con_cuerpo_vacio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.patch(
        "/medicamentos/MED001",
        headers=headers,
        json={},
    )
    assert response.status_code == 422


def test_propietario_no_actualiza_medicamento_de_otra_mascota(test_client):
    headers = obtener_headers("USR003", "PROPIETARIO")
    response = test_client.patch(
        "/medicamentos/MED001",
        headers=headers,
        json={"estado": "Finalizado"},
    )
    # La ruta restringe la operación al rol veterinario/administrador.
    assert response.status_code == 403


# ============================================================
# AUTENTICACIÓN
# ============================================================

def test_no_consultar_medicamentos_sin_token(test_client):
    response = test_client.get("/consultas/CONS001/medicamentos")
    assert response.status_code == 401


def test_no_registrar_medicamentos_sin_token(test_client):
    response = test_client.post(
        "/consultas/CONS001/medicamentos",
        json={
            "nombre": "Medicamento sin autenticación",
            "dosis": "100 mg",
            "frecuencia": "Cada 12 horas",
            "duracion": "5 días",
            "fecha_inicio": "2026-11-03",
            "fecha_fin": "2026-11-08",
            "estado": "Activo",
        },
    )
    assert response.status_code == 401
