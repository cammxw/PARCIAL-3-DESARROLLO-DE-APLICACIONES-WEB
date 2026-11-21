import pytest
from fastapi.testclient import TestClient

from app.logic import EntradaInvalida, Equipo, analizar, consumo_mensual_kwh
from app.main import app

cliente = TestClient(app)

datosValidos = {
    "nombre": ["Nevera", "Televisor"],
    "potencia": ["150", "100"],
    "horas": ["24", "5"],
    "tarifa": "800",
    "reduccion": "10",
}


def test_consumo_mensual_kwh():
    assert consumo_mensual_kwh(100, 5) == 15.0


def test_analizar_totales_y_ahorro():
    equipos = [Equipo("Nevera", 150, 24), Equipo("Televisor", 100, 5)]
    r = analizar(equipos, 800, 10)
    assert r["total_kwh"] == pytest.approx(123.0)
    assert r["total_costo"] == pytest.approx(98400)
    assert r["mayor"] == "Nevera"
    assert r["ahorro"] == pytest.approx(9840)


def test_ruta_inicio_responde():
    r = cliente.get("/")
    assert r.status_code == 200
    assert "EnergiaHogar" in r.text


def test_ruta_analizar_muestra_resultado():
    r = cliente.post("/analizar", data=datosValidos)
    assert r.status_code == 200
    assert "Nevera" in r.text
    assert "123.00 kWh" in r.text


def test_potencia_negativa_devuelve_error():
    datos = dict(datosValidos, potencia=["-5", "100"])
    r = cliente.post("/analizar", data=datos)
    assert r.status_code == 400
    assert "debe ser mayor que cero" in r.text


def test_horas_fuera_de_rango():
    datos = dict(datosValidos, horas=["30", "5"])
    r = cliente.post("/analizar", data=datos)
    assert r.status_code == 400


def test_tarifa_invalida_lanza_excepcion():
    with pytest.raises(EntradaInvalida):
        analizar([Equipo("Lampara", 10, 4)], 0)
