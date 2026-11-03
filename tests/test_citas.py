import pytest
from datetime import date

from fastapi import HTTPException
from app.services.cita_service import validar_horario_atencion


def test_horario_valido():
    validar_horario_atencion(
        fecha=date(2027, 3, 15),
        hora="09:00",
    )


def test_no_permitir_domingo():
    with pytest.raises(HTTPException) as error:
        validar_horario_atencion(
            fecha=date(2027, 3, 14),
            hora="10:00",
        )

    assert error.value.status_code == 422
    assert error.value.detail == "VetCare no atiende los domingos"


def test_no_permitir_hora_fuera_de_atencion():
    with pytest.raises(HTTPException) as error:
        validar_horario_atencion(
            fecha=date(2027, 3, 15),
            hora="19:00",
        )

    assert error.value.status_code == 422


def test_no_permitir_intervalos_diferentes_a_30_minutos():
    with pytest.raises(HTTPException) as error:
        validar_horario_atencion(
            fecha=date(2027, 3, 15),
            hora="09:15",
        )

    assert error.value.status_code == 422


def test_permitir_hora_limite_inicial():
    validar_horario_atencion(
        fecha=date(2027, 3, 15),
        hora="08:00",
    )


def test_no_permitir_hora_limite_final():
    with pytest.raises(HTTPException) as error:
        validar_horario_atencion(
            fecha=date(2027, 3, 15),
            hora="18:00",
        )

    assert error.value.status_code == 422