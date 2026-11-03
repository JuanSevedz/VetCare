from app.core.auth import crear_access_token


def obtener_headers(usuario_id: str, rol: str) -> dict:
    token = crear_access_token(usuario_id, rol)
    return {"Authorization": f"Bearer {token}"}


def datos_recordatorio(**cambios):
    datos = {
        "categoria": "Vacunación",
        "fecha": "2026-12-15",
        "descripcion": "Aplicar refuerzo de vacuna antirrábica.",
        "estado": "Pendiente",
    }
    datos.update(cambios)
    return datos


def crear_recordatorio(test_client, headers=None, mascota_id="PET001", **cambios):
    if headers is None:
        headers = obtener_headers("USR002", "VETERINARIO")

    return test_client.post(
        f"/mascotas/{mascota_id}/recordatorios",
        headers=headers,
        json=datos_recordatorio(**cambios),
    )


def test_propietario_consulta_recordatorios_de_su_mascota(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        "/mascotas/PET001/recordatorios",
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_propietario_no_consulta_recordatorios_de_mascota_ajena(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        "/mascotas/PET002/recordatorios",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_consulta_recordatorios(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/mascotas/PET001/recordatorios",
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_admin_consulta_recordatorios(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-REC-LIST",
            "nombre": "Admin recordatorios",
            "correo": "admin.recordatorios.list@vetcare.test",
            "contrasena": hash_password("AdminRec2026*"),
        },
    )
    db_session.commit()

    headers = obtener_headers("USR-ADMIN-REC-LIST", "ADMIN")
    response = test_client.get(
        "/mascotas/PET001/recordatorios",
        headers=headers,
    )
    assert response.status_code == 200


def test_no_consultar_recordatorios_de_mascota_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/mascotas/PET-INEXISTENTE/recordatorios",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_registra_recordatorio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_recordatorio(test_client, headers)

    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("REC-")
    assert data["id_mascota"] == "PET001"
    assert data["categoria"] == "Vacunación"
    assert data["estado"] == "Pendiente"


def test_admin_registra_recordatorio(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-REC-CREATE",
            "nombre": "Admin recordatorios",
            "correo": "admin.recordatorios.create@vetcare.test",
            "contrasena": hash_password("AdminRec2026*"),
        },
    )
    db_session.commit()

    headers = obtener_headers("USR-ADMIN-REC-CREATE", "ADMIN")
    response = crear_recordatorio(test_client, headers)

    assert response.status_code == 201
    assert response.json()["id_mascota"] == "PET001"


def test_propietario_no_puede_registrar_recordatorios(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = crear_recordatorio(test_client, headers)

    assert response.status_code == 403


def test_no_registrar_recordatorio_para_mascota_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_recordatorio(
        test_client,
        headers,
        mascota_id="PET-INEXISTENTE",
    )
    assert response.status_code == 404


def test_no_registrar_recordatorio_con_estado_invalido(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_recordatorio(
        test_client,
        headers,
        estado="En proceso",
    )
    assert response.status_code == 422


def test_no_registrar_recordatorio_sin_categoria(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_recordatorio(
        test_client,
        headers,
        categoria="   ",
    )
    assert response.status_code == 422


def test_no_registrar_recordatorio_sin_descripcion(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_recordatorio(
        test_client,
        headers,
        descripcion="   ",
    )
    assert response.status_code == 422


def test_consultar_recordatorio_registrado(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_recordatorio(test_client, headers)
    assert creada.status_code == 201

    recordatorio_id = creada.json()["id"]
    response = test_client.get(
        f"/recordatorios/{recordatorio_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == recordatorio_id


def test_propietario_consulta_recordatorio_de_su_mascota(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_recordatorio(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        f"/recordatorios/{creada.json()['id']}",
        headers=headers_owner,
    )
    assert response.status_code == 200


def test_propietario_no_consulta_recordatorio_de_mascota_ajena(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_recordatorio(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR003", "PROPIETARIO")
    response = test_client.get(
        f"/recordatorios/{creada.json()['id']}",
        headers=headers_owner,
    )
    assert response.status_code == 404


def test_consultar_recordatorio_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/recordatorios/REC-INEXISTENTE",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_actualiza_recordatorio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_recordatorio(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/recordatorios/{creada.json()['id']}",
        headers=headers,
        json={"estado": "Completado"},
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "Completado"


def test_admin_actualiza_recordatorio(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-REC-UPDATE",
            "nombre": "Admin recordatorios",
            "correo": "admin.recordatorios.update@vetcare.test",
            "contrasena": hash_password("AdminRec2026*"),
        },
    )
    db_session.commit()

    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_recordatorio(test_client, headers_vet)
    assert creada.status_code == 201

    headers_admin = obtener_headers("USR-ADMIN-REC-UPDATE", "ADMIN")
    response = test_client.patch(
        f"/recordatorios/{creada.json()['id']}",
        headers=headers_admin,
        json={"estado": "Cancelado"},
    )

    assert response.status_code == 200
    assert response.json()["estado"] == "Cancelado"


def test_propietario_no_actualiza_recordatorio(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_recordatorio(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.patch(
        f"/recordatorios/{creada.json()['id']}",
        headers=headers_owner,
        json={"estado": "Completado"},
    )
    assert response.status_code == 403


def test_no_actualizar_recordatorio_con_estado_invalido(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_recordatorio(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/recordatorios/{creada.json()['id']}",
        headers=headers,
        json={"estado": "En proceso"},
    )
    assert response.status_code == 422


def test_no_actualizar_recordatorio_con_cuerpo_vacio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_recordatorio(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/recordatorios/{creada.json()['id']}",
        headers=headers,
        json={},
    )
    assert response.status_code == 422


def test_no_consultar_recordatorios_sin_token(test_client):
    response = test_client.get("/mascotas/PET001/recordatorios")
    assert response.status_code == 401


def test_no_registrar_recordatorio_sin_token(test_client):
    response = test_client.post(
        "/mascotas/PET001/recordatorios",
        json=datos_recordatorio(),
    )
    assert response.status_code == 401
