from app.core.auth import crear_access_token


def obtener_headers(usuario_id: str, rol: str) -> dict:
    token = crear_access_token(usuario_id, rol)
    return {"Authorization": f"Bearer {token}"}


def datos_solicitud(**cambios):
    datos = {
        "descripcion": "Solicito seguimiento de la evolución de mi mascota."
    }
    datos.update(cambios)
    return datos


def crear_solicitud(test_client, headers=None, mascota_id="PET001", **cambios):
    if headers is None:
        headers = obtener_headers("USR001", "PROPIETARIO")
    return test_client.post(
        f"/mascotas/{mascota_id}/solicitudes-seguimiento",
        headers=headers,
        json=datos_solicitud(**cambios),
    )


def test_propietario_lista_solicitudes_de_su_mascota(test_client):
    response = test_client.get(
        "/mascotas/PET001/solicitudes-seguimiento",
        headers=obtener_headers("USR001", "PROPIETARIO"),
    )
    assert response.status_code == 200
    assert any(x["id"] == "SOL001" for x in response.json())


def test_propietario_no_lista_solicitudes_de_mascota_ajena(test_client):
    response = test_client.get(
        "/mascotas/PET002/solicitudes-seguimiento",
        headers=obtener_headers("USR001", "PROPIETARIO"),
    )
    assert response.status_code == 404


def test_veterinario_lista_solicitudes(test_client):
    response = test_client.get(
        "/mascotas/PET001/solicitudes-seguimiento",
        headers=obtener_headers("USR002", "VETERINARIO"),
    )
    assert response.status_code == 200


def test_mascota_inexistente_al_listar_solicitudes(test_client):
    response = test_client.get(
        "/mascotas/PET-NO-EXISTE/solicitudes-seguimiento",
        headers=obtener_headers("USR002", "VETERINARIO"),
    )
    assert response.status_code == 404


def test_propietario_crea_solicitud(test_client):
    response = crear_solicitud(test_client)
    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("SOL-")
    assert data["id_propietario"] == "USR001"
    assert data["id_mascota"] == "PET001"
    assert data["estado"] == "Pendiente"


def test_propietario_no_crea_solicitud_para_mascota_ajena(test_client):
    response = crear_solicitud(
        test_client,
        mascota_id="PET002",
    )
    assert response.status_code == 404


def test_veterinario_no_crea_solicitud(test_client):
    response = crear_solicitud(
        test_client,
        headers=obtener_headers("USR002", "VETERINARIO"),
    )
    assert response.status_code == 403


def test_no_crea_solicitud_para_mascota_inexistente(test_client):
    response = crear_solicitud(test_client, mascota_id="PET-NO-EXISTE")
    assert response.status_code == 404


def test_no_crea_solicitud_con_descripcion_vacia(test_client):
    response = crear_solicitud(test_client, descripcion="   ")
    assert response.status_code == 422


def test_no_crea_solicitud_sin_descripcion(test_client):
    response = test_client.post(
        "/mascotas/PET001/solicitudes-seguimiento",
        headers=obtener_headers("USR001", "PROPIETARIO"),
        json={},
    )
    assert response.status_code == 422


def test_propietario_consulta_su_solicitud(test_client):
    response = test_client.get(
        "/solicitudes-seguimiento/SOL001",
        headers=obtener_headers("USR001", "PROPIETARIO"),
    )
    assert response.status_code == 200
    assert response.json()["id"] == "SOL001"


def test_propietario_no_consulta_solicitud_ajena(test_client):
    response = test_client.get(
        "/solicitudes-seguimiento/SOL001",
        headers=obtener_headers("USR003", "PROPIETARIO"),
    )
    assert response.status_code == 404


def test_veterinario_consulta_solicitud(test_client):
    response = test_client.get(
        "/solicitudes-seguimiento/SOL001",
        headers=obtener_headers("USR002", "VETERINARIO"),
    )
    assert response.status_code == 200


def test_solicitud_inexistente(test_client):
    response = test_client.get(
        "/solicitudes-seguimiento/SOL-NO-EXISTE",
        headers=obtener_headers("USR002", "VETERINARIO"),
    )
    assert response.status_code == 404


def test_veterinario_actualiza_estado_solicitud(test_client):
    response = test_client.patch(
        "/solicitudes-seguimiento/SOL001",
        headers=obtener_headers("USR002", "VETERINARIO"),
        json={"estado": "En proceso"},
    )
    assert response.status_code == 200
    assert response.json()["estado"] == "En proceso"


def test_propietario_no_actualiza_estado_solicitud(test_client):
    response = test_client.patch(
        "/solicitudes-seguimiento/SOL001",
        headers=obtener_headers("USR001", "PROPIETARIO"),
        json={"estado": "Cancelada"},
    )
    assert response.status_code == 403


def test_no_actualiza_estado_no_permitido(test_client):
    response = test_client.patch(
        "/solicitudes-seguimiento/SOL001",
        headers=obtener_headers("USR002", "VETERINARIO"),
        json={"estado": "Aprobada"},
    )
    assert response.status_code == 422


def test_no_actualiza_solicitud_con_cuerpo_vacio(test_client):
    response = test_client.patch(
        "/solicitudes-seguimiento/SOL001",
        headers=obtener_headers("USR002", "VETERINARIO"),
        json={},
    )
    assert response.status_code == 422


def test_no_actualiza_solicitud_inexistente(test_client):
    response = test_client.patch(
        "/solicitudes-seguimiento/SOL-NO-EXISTE",
        headers=obtener_headers("USR002", "VETERINARIO"),
        json={"estado": "Atendida"},
    )
    assert response.status_code == 404


def test_listar_solicitudes_sin_token(test_client):
    response = test_client.get(
        "/mascotas/PET001/solicitudes-seguimiento"
    )
    assert response.status_code == 401


def test_crear_solicitud_sin_token(test_client):
    response = test_client.post(
        "/mascotas/PET001/solicitudes-seguimiento",
        json=datos_solicitud(),
    )
    assert response.status_code == 401


def test_actualizar_solicitud_sin_token(test_client):
    response = test_client.patch(
        "/solicitudes-seguimiento/SOL001",
        json={"estado": "Atendida"},
    )
    assert response.status_code == 401
