from app.core.auth import crear_access_token


def obtener_headers(usuario_id: str, rol: str) -> dict:
    token = crear_access_token(usuario_id, rol)
    return {"Authorization": f"Bearer {token}"}


def datos_gasto(**cambios):
    datos = {
        "fecha": "2026-11-03",
        "categoria": "Consulta veterinaria",
        "descripcion": "Consulta general de control.",
        "valor": 85000,
    }
    datos.update(cambios)
    return datos


def crear_gasto(test_client, headers=None, mascota_id="PET001", **cambios):
    if headers is None:
        headers = obtener_headers("USR002", "VETERINARIO")

    return test_client.post(
        f"/mascotas/{mascota_id}/gastos",
        headers=headers,
        json=datos_gasto(**cambios),
    )


def test_propietario_consulta_gastos_de_su_mascota(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        "/mascotas/PET001/gastos",
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_propietario_no_consulta_gastos_de_mascota_ajena(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        "/mascotas/PET002/gastos",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_consulta_gastos(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/mascotas/PET001/gastos",
        headers=headers,
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_admin_consulta_gastos(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-GAS-LIST",
            "nombre": "Admin gastos",
            "correo": "admin.gastos.list@vetcare.test",
            "contrasena": hash_password("AdminGas2026*"),
        },
    )
    db_session.commit()

    headers = obtener_headers("USR-ADMIN-GAS-LIST", "ADMIN")
    response = test_client.get(
        "/mascotas/PET001/gastos",
        headers=headers,
    )
    assert response.status_code == 200


def test_no_consultar_gastos_de_mascota_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/mascotas/PET-INEXISTENTE/gastos",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_registra_gasto(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_gasto(test_client, headers)

    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("GAS-")
    assert data["id_mascota"] == "PET001"
    assert data["categoria"] == "Consulta veterinaria"
    assert data["valor"] == 85000


def test_admin_registra_gasto(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-GAS-CREATE",
            "nombre": "Admin gastos",
            "correo": "admin.gastos.create@vetcare.test",
            "contrasena": hash_password("AdminGas2026*"),
        },
    )
    db_session.commit()

    headers = obtener_headers("USR-ADMIN-GAS-CREATE", "ADMIN")
    response = crear_gasto(test_client, headers)

    assert response.status_code == 201
    assert response.json()["id_mascota"] == "PET001"


def test_propietario_no_puede_registrar_gastos(test_client):
    headers = obtener_headers("USR001", "PROPIETARIO")
    response = crear_gasto(test_client, headers)
    assert response.status_code == 403


def test_no_registrar_gasto_para_mascota_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_gasto(
        test_client,
        headers,
        mascota_id="PET-INEXISTENTE",
    )
    assert response.status_code == 404


def test_no_registrar_gasto_con_valor_cero(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_gasto(test_client, headers, valor=0)
    assert response.status_code == 422


def test_no_registrar_gasto_con_valor_negativo(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_gasto(test_client, headers, valor=-1000)
    assert response.status_code == 422


def test_no_registrar_gasto_sin_categoria(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_gasto(test_client, headers, categoria="   ")
    assert response.status_code == 422


def test_no_registrar_gasto_sin_descripcion(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = crear_gasto(test_client, headers, descripcion="   ")
    assert response.status_code == 422


def test_consultar_gasto_registrado(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers)
    assert creada.status_code == 201

    gasto_id = creada.json()["id"]
    response = test_client.get(
        f"/gastos/{gasto_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == gasto_id


def test_propietario_consulta_gasto_de_su_mascota(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.get(
        f"/gastos/{creada.json()['id']}",
        headers=headers_owner,
    )
    assert response.status_code == 200


def test_propietario_no_consulta_gasto_de_mascota_ajena(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR003", "PROPIETARIO")
    response = test_client.get(
        f"/gastos/{creada.json()['id']}",
        headers=headers_owner,
    )
    assert response.status_code == 404


def test_consultar_gasto_inexistente(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    response = test_client.get(
        "/gastos/GAS-INEXISTENTE",
        headers=headers,
    )
    assert response.status_code == 404


def test_veterinario_actualiza_gasto(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/gastos/{creada.json()['id']}",
        headers=headers,
        json={"valor": 95000, "descripcion": "Consulta y control."},
    )

    assert response.status_code == 200
    assert response.json()["valor"] == 95000
    assert response.json()["descripcion"] == "Consulta y control."


def test_admin_actualiza_gasto(test_client, db_session):
    from sqlalchemy import text
    from app.core.security import hash_password

    db_session.execute(
        text("""
            INSERT INTO usuarios (id, nombre, correo, contrasena, rol)
            VALUES (:id, :nombre, :correo, :contrasena, 'ADMIN')
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": "USR-ADMIN-GAS-UPDATE",
            "nombre": "Admin gastos",
            "correo": "admin.gastos.update@vetcare.test",
            "contrasena": hash_password("AdminGas2026*"),
        },
    )
    db_session.commit()

    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers_vet)
    assert creada.status_code == 201

    headers_admin = obtener_headers("USR-ADMIN-GAS-UPDATE", "ADMIN")
    response = test_client.patch(
        f"/gastos/{creada.json()['id']}",
        headers=headers_admin,
        json={"categoria": "Medicamentos"},
    )

    assert response.status_code == 200
    assert response.json()["categoria"] == "Medicamentos"


def test_propietario_no_actualiza_gasto(test_client):
    headers_vet = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers_vet)
    assert creada.status_code == 201

    headers_owner = obtener_headers("USR001", "PROPIETARIO")
    response = test_client.patch(
        f"/gastos/{creada.json()['id']}",
        headers=headers_owner,
        json={"valor": 90000},
    )
    assert response.status_code == 403


def test_no_actualizar_gasto_con_valor_cero(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/gastos/{creada.json()['id']}",
        headers=headers,
        json={"valor": 0},
    )
    assert response.status_code == 422


def test_no_actualizar_gasto_con_valor_negativo(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/gastos/{creada.json()['id']}",
        headers=headers,
        json={"valor": -500},
    )
    assert response.status_code == 422


def test_no_actualizar_gasto_con_cuerpo_vacio(test_client):
    headers = obtener_headers("USR002", "VETERINARIO")
    creada = crear_gasto(test_client, headers)
    assert creada.status_code == 201

    response = test_client.patch(
        f"/gastos/{creada.json()['id']}",
        headers=headers,
        json={},
    )
    assert response.status_code == 422


def test_no_consultar_gastos_sin_token(test_client):
    response = test_client.get("/mascotas/PET001/gastos")
    assert response.status_code == 401


def test_no_registrar_gastos_sin_token(test_client):
    response = test_client.post(
        "/mascotas/PET001/gastos",
        json=datos_gasto(),
    )
    assert response.status_code == 401
