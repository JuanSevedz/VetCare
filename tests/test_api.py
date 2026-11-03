def test_api_inicia_correctamente(test_client):
    response = test_client.get("/docs")

    assert response.status_code == 200

def test_login_propietario(test_client):
    response = test_client.post(
        "/auth/login",
        json={
            "correo": "carlos.rodriguez@vetcare.test",
            "contrasena": "VetCareTest2026*"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
def test_propietario_consulta_sus_citas(test_client):
    login = test_client.post(
        "/auth/login",
        json={
            "correo": "carlos.rodriguez@vetcare.test",
            "contrasena": "VetCareTest2026*"
        }
    )

    token = login.json()["access_token"]

    response = test_client.get(
        "/citas/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_propietario_no_consulta_citas_de_otro_propietario(test_client):
    login = test_client.post(
        "/auth/login",
        json={
            "correo": "carlos.rodriguez@vetcare.test",
            "contrasena": "VetCareTest2026*"
        }
    )

    token = login.json()["access_token"]

    response = test_client.get(
        "/mascotas/PET002",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404
def test_propietario_no_puede_crear_cita_para_mascota_ajena(test_client):
    login = test_client.post(
        "/auth/login",
        json={
            "correo": "carlos.rodriguez@vetcare.test",
            "contrasena": "VetCareTest2026*"
        }
    )

    token = login.json()["access_token"]

    response = test_client.post(
        "/citas/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "id_mascota": "PET002",
            "id_veterinario": "USR002",
            "fecha": "2027-04-12",
            "hora": "10:00",
            "motivo": "Prueba de autorización"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Solo puedes solicitar citas para tus propias mascotas"
    )
def test_propietario_crea_cita_para_su_mascota(test_client):
    login = test_client.post(
        "/auth/login",
        json={
            "correo": "carlos.rodriguez@vetcare.test",
            "contrasena": "VetCareTest2026*"
        }
    )

    token = login.json()["access_token"]

    response = test_client.post(
        "/citas/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "id_mascota": "PET001",
            "id_veterinario": "USR002",
            "fecha": "2027-04-12",
            "hora": "10:00",
            "motivo": "Control veterinario de Max"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id_mascota"] == "PET001"
    assert data["id_veterinario"] == "USR002"
    assert data["estado"] == "Pendiente"
def test_no_permitir_dos_citas_en_el_mismo_horario(test_client):
    login = test_client.post(
        "/auth/login",
        json={
            "correo": "carlos.rodriguez@vetcare.test",
            "contrasena": "VetCareTest2026*"
        }
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    datos_cita = {
        "id_mascota": "PET001",
        "id_veterinario": "USR002",
        "fecha": "2027-04-12",
        "hora": "10:00",
        "motivo": "Prueba de conflicto de horarios"
    }

    primera_respuesta = test_client.post(
        "/citas/",
        headers=headers,
        json=datos_cita
    )

    assert primera_respuesta.status_code == 201

    segunda_respuesta = test_client.post(
        "/citas/",
        headers=headers,
        json=datos_cita
    )

    assert segunda_respuesta.status_code == 409
    assert segunda_respuesta.json()["detail"] == (
        "La mascota o el veterinario ya tiene una cita activa en esa fecha y hora"
    )
