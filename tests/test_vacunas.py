from app.core.auth import crear_access_token


def obtener_headers(usuario_id: str, rol: str) -> dict:
    token = crear_access_token(usuario_id, rol)
    return {"Authorization": f"Bearer {token}"}


def datos_vacuna(**cambios):
    datos = {
        "nombre": "Vacuna antirrábica",
        "fecha_aplicacion": "2026-11-03",
        "fecha_proxima": "2027-11-03",
        "lote": "LOTE-TEST-001",
        "estado": "Aplicada",
    }
    datos.update(cambios)
    return datos


def test_propietario_consulta_historial_de_su_mascota(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        "/mascotas/PET001/vacunas",
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_propietario_no_consulta_historial_de_mascota_ajena(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        "/mascotas/PET002/vacunas",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_consulta_historial_de_mascota(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/mascotas/PET001/vacunas",
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_admin_consulta_historial_de_mascota(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-VAC-TEST",
            "nombre": "Admin vacunas",
            "correo": "admin.vacunas@vetcare.test",
            "contrasena": hash_password("AdminVac2026*"),
        },
    )
    db_session.commit()

    headers = obtener_headers("USR-ADMIN-VAC-TEST", "ADMIN")
    response = test_client.get(
        "/mascotas/PET001/vacunas",
        headers=headers,
    )
    assert response.status_code == 200


def test_veterinario_registra_vacuna(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("VAC-")
    assert data["id_mascota"] == "PET001"
    assert data["id_veterinario"] == "USR002"
    assert data["nombre"] == "Vacuna antirrábica"
    assert data["estado"] == "Aplicada"


def test_admin_registra_vacuna(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-VAC-CREATE",
            "nombre": "Admin vacunas",
            "correo": "admin.vac.create@vetcare.test",
            "contrasena": hash_password("AdminVac2026*"),
        },
    )
    db_session.commit()

    headers = obtener_headers("USR-ADMIN-VAC-CREATE", "ADMIN")
    response = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(id_veterinario="USR002"),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id_mascota"] == "PET001"
    assert data["id_veterinario"] == "USR002"

def test_propietario_no_puede_registrar_vacunas(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(),
    )
    assert response.status_code == 403


def test_no_registrar_vacuna_para_mascota_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/mascotas/PET-INEXISTENTE/vacunas",
        headers=headers,
        json=datos_vacuna(),
    )
    assert response.status_code == 404


def test_no_registrar_vacuna_con_fecha_proxima_anterior(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(
            fecha_aplicacion="2026-11-10",
            fecha_proxima="2026-11-05",
        ),
    )
    assert response.status_code == 422


def test_no_registrar_vacuna_con_estado_invalido(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(estado="Cancelada"),
    )
    assert response.status_code == 422


def test_no_registrar_vacuna_sin_nombre(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(nombre="   "),
    )
    assert response.status_code == 422


def test_consultar_vacuna_registrada(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(),
    )
    assert creada.status_code == 201

    vacuna_id = creada.json()["id"]
    response = test_client.get(
        f"/vacunas/{vacuna_id}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["id"] == vacuna_id


def test_propietario_consulta_vacuna_de_su_mascota(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers_vet,
        json=datos_vacuna(),
    )
    assert creada.status_code == 201

    vacuna_id = creada.json()["id"]
    headers_owner = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        f"/vacunas/{vacuna_id}",
        headers=headers_owner,
    )
    assert response.status_code == 200


def test_propietario_no_consulta_vacuna_de_mascota_ajena(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers_vet,
        json=datos_vacuna(),
    )
    assert creada.status_code == 201

    vacuna_id = creada.json()["id"]
    headers_owner = obtener_headers("USR003", "PROPIETARIO")
    response = test_client.get(
        f"/vacunas/{vacuna_id}",
        headers=headers_owner,
    )
    assert response.status_code == 404


def test_consultar_vacuna_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/vacunas/VAC-INEXISTENTE",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_actualiza_su_vacuna(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(),
    )
    assert creada.status_code == 201

    vacuna_id = creada.json()["id"]
    response = test_client.patch(
        f"/vacunas/{vacuna_id}",
        headers=headers,
        json={"estado": "Pendiente"},
    )
    assert response.status_code == 200
    assert response.json()["estado"] == "Pendiente"


def test_propietario_no_actualiza_vacuna(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers_vet,
        json=datos_vacuna(),
    )
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.patch(
        f"/vacunas/{creada.json()['id']}",
        headers=headers_owner,
        json={"estado": "Pendiente"},
    )
    assert response.status_code == 403


def test_no_actualizar_vacuna_con_fechas_inconsistentes(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(),
    )
    assert creada.status_code == 201

    response = test_client.patch(
        f"/vacunas/{creada.json()['id']}",
        headers=headers,
        json={
            "fecha_aplicacion": "2027-01-01",
            "fecha_proxima": "2026-12-01",
        },
    )
    assert response.status_code == 422


def test_no_actualizar_vacuna_con_estado_invalido(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(),
    )
    assert creada.status_code == 201

    response = test_client.patch(
        f"/vacunas/{creada.json()['id']}",
        headers=headers,
        json={"estado": "Cancelada"},
    )
    assert response.status_code == 422


def test_no_actualizar_vacuna_con_cuerpo_vacio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = test_client.post(
        "/mascotas/PET001/vacunas",
        headers=headers,
        json=datos_vacuna(),
    )
    assert creada.status_code == 201

    response = test_client.patch(
        f"/vacunas/{creada.json()['id']}",
        headers=headers,
        json={},
    )
    assert response.status_code == 422


def test_no_consultar_vacunas_sin_token(test_client):
    response = test_client.get("/mascotas/PET001/vacunas")
    assert response.status_code == 401


def test_no_registrar_vacunas_sin_token(test_client):
    response = test_client.post(
        "/mascotas/PET001/vacunas",
        json=datos_vacuna(),
    )
    assert response.status_code == 401
