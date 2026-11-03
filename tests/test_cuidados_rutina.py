from app.core.auth import crear_access_token


def obtener_headers(usuario_id: str, rol: str) -> dict:
    token = crear_access_token(usuario_id, rol)
    return {"Authorization": f"Bearer {token}"}


def datos_cuidado(**cambios):
    datos = {
        "tipo": "Alimentación",
        "frecuencia": "Dos veces al día",
        "horario": "08:00 y 18:00",
        "notas": "Servir la porción recomendada.",
    }
    datos.update(cambios)
    return datos


def crear_cuidado(
    test_client,
    headers=None,
    mascota_id="PET001",
    **cambios,
):
    if headers is None:
        headers = obtener_headers("USR002", "VETERINARIO")

    return test_client.post(
        f"/mascotas/{mascota_id}/cuidados",
        headers=headers,
        json=datos_cuidado(**cambios),
    )


def test_propietario_consulta_cuidados_de_su_mascota(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        "/mascotas/PET001/cuidados",
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_propietario_no_consulta_cuidados_de_mascota_ajena(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        "/mascotas/PET002/cuidados",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_consulta_cuidados(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/mascotas/PET001/cuidados",
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_admin_consulta_cuidados(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-CUI-LIST",
            "nombre": "Admin cuidados",
            "correo": "admin.cuidados.list@vetcare.test",
            "contrasena": hash_password("AdminCui2026*"),
        },
    )
    db_session.commit()

    headers = obtener_headers("USR-ADMIN-CUI-LIST", "ADMIN")
    response = test_client.get(
        "/mascotas/PET001/cuidados",
        headers=headers,
    )
    assert response.status_code == 200


def test_no_consultar_cuidados_de_mascota_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/mascotas/PET-INEXISTENTE/cuidados",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_registra_cuidado(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_cuidado(test_client, headers)

    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("CUI-")
    assert data["id_mascota"] == "PET001"
    assert data["tipo"] == "Alimentación"
    assert data["frecuencia"] == "Dos veces al día"


def test_admin_registra_cuidado(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-CUI-CREATE",
            "nombre": "Admin cuidados",
            "correo": "admin.cuidados.create@vetcare.test",
            "contrasena": hash_password("AdminCui2026*"),
        },
    )
    db_session.commit()

    headers = obtener_headers("USR-ADMIN-CUI-CREATE", "ADMIN")
    response = crear_cuidado(test_client, headers)

    assert response.status_code == 201
    assert response.json()["id_mascota"] == "PET001"


def test_propietario_no_puede_registrar_cuidados(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = crear_cuidado(test_client, headers)
    assert response.status_code == 403


def test_no_registrar_cuidado_para_mascota_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_cuidado(
        test_client,
        headers,
        mascota_id="PET-INEXISTENTE",
    )
    assert response.status_code == 404


def test_no_registrar_cuidado_sin_tipo(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_cuidado(test_client, headers, tipo="   ")
    assert response.status_code == 422


def test_no_registrar_cuidado_sin_frecuencia(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_cuidado(test_client, headers, frecuencia="   ")
    assert response.status_code == 422


def test_no_registrar_cuidado_sin_horario(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_cuidado(test_client, headers, horario="   ")
    assert response.status_code == 422


def test_registrar_cuidado_sin_notas(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_cuidado(test_client, headers, notas=None)

    assert response.status_code == 201
    assert response.json()["notas"] is None


def test_consultar_cuidado_registrado(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers)
    assert creada.status_code == 201

    cuidado_id = creada.json()["id"]
    response = test_client.get(
        f"/cuidados/{cuidado_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == cuidado_id


def test_propietario_consulta_cuidado_de_su_mascota(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        f"/cuidados/{creada.json()['id']}",
        headers=headers_owner,
    )
    assert response.status_code == 200


def test_propietario_no_consulta_cuidado_de_mascota_ajena(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR003", "PROPIETARIO")
    response = test_client.get(
        f"/cuidados/{creada.json()['id']}",
        headers=headers_owner,
    )
    assert response.status_code == 404


def test_consultar_cuidado_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/cuidados/CUI-INEXISTENTE",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_actualiza_cuidado(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/cuidados/{creada.json()['id']}",
        headers=headers,
        json={"frecuencia": "Una vez al día"},
    )

    assert response.status_code == 200
    assert response.json()["frecuencia"] == "Una vez al día"


def test_admin_actualiza_cuidado(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-CUI-UPDATE",
            "nombre": "Admin cuidados",
            "correo": "admin.cuidados.update@vetcare.test",
            "contrasena": hash_password("AdminCui2026*"),
        },
    )
    db_session.commit()

    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers_vet)
    assert creada.status_code == 201

    headers_admin = obtener_headers("USR-ADMIN-CUI-UPDATE", "ADMIN")
    response = test_client.patch(
        f"/cuidados/{creada.json()['id']}",
        headers=headers_admin,
        json={"tipo": "Higiene"},
    )

    assert response.status_code == 200
    assert response.json()["tipo"] == "Higiene"


def test_propietario_no_actualiza_cuidado(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.patch(
        f"/cuidados/{creada.json()['id']}",
        headers=headers_owner,
        json={"frecuencia": "Cada día"},
    )
    assert response.status_code == 403


def test_no_actualizar_cuidado_con_cuerpo_vacio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/cuidados/{creada.json()['id']}",
        headers=headers,
        json={},
    )
    assert response.status_code == 422


def test_no_actualizar_cuidado_con_tipo_vacio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/cuidados/{creada.json()['id']}",
        headers=headers,
        json={"tipo": "   "},
    )
    assert response.status_code == 422


def test_actualizar_cuidado_eliminando_notas(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_cuidado(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/cuidados/{creada.json()['id']}",
        headers=headers,
        json={"notas": None},
    )

    assert response.status_code == 200
    assert response.json()["notas"] is None


def test_no_consultar_cuidados_sin_token(test_client):
    response = test_client.get("/mascotas/PET001/cuidados")
    assert response.status_code == 401


def test_no_registrar_cuidados_sin_token(test_client):
    response = test_client.post(
        "/mascotas/PET001/cuidados",
        json=datos_cuidado(),
    )
    assert response.status_code == 401
