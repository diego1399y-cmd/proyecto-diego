"""Pruebas de la API. Requieren el modelo entrenado:
    uv run python -m proyecto_diego.train
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.schemas import EJEMPLO_PEDIDO


@pytest.fixture
def cliente():
    """Cliente de prueba. El 'with' ejecuta el lifespan, o sea, carga el modelo."""
    with TestClient(app) as c:
        yield c


def test_health_responde_ok(cliente):
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json()["modelo_cargado"] is True


def test_predict_devuelve_prediccion_valida(cliente):
    respuesta = cliente.post("/predict", json=EJEMPLO_PEDIDO)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert isinstance(datos["llega_tarde"], bool)
    assert 0 <= datos["probabilidad_tarde"] <= 1


def test_first_class_se_marca_como_tarde(cliente):
    """Regla que aprendió el modelo: First Class casi siempre llega tarde."""
    pedido = {**EJEMPLO_PEDIDO, "modo_envio": "First Class"}
    respuesta = cliente.post("/predict", json=pedido)
    assert respuesta.json()["llega_tarde"] is True


def test_mes_invalido_da_422(cliente):
    pedido = {**EJEMPLO_PEDIDO, "mes_pedido": 13}
    respuesta = cliente.post("/predict", json=pedido)
    assert respuesta.status_code == 422


def test_campo_faltante_da_422(cliente):
    pedido = {k: v for k, v in EJEMPLO_PEDIDO.items() if k != "venta"}
    respuesta = cliente.post("/predict", json=pedido)
    assert respuesta.status_code == 422