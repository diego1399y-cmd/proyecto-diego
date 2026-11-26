"""API para predecir si un pedido de DataCo va a llegar tarde.

Ejecutar desde la raíz del proyecto:
    uv run uvicorn api.main:app --reload

Documentación interactiva: http://127.0.0.1:8000/docs
"""

import json
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from api.schemas import PedidoEntrada, PrediccionSalida

RAIZ = Path(__file__).resolve().parents[1]
RUTA_MODELO = RAIZ / "models" / "modelo.joblib"
RUTA_METADATOS = RAIZ / "models" / "modelo.json"

# Aquí guardamos el modelo una vez cargado, para no leerlo en cada petición
estado = {"modelo": None, "metadatos": {}}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta una sola vez al arrancar la API: carga el modelo en memoria."""
    if RUTA_MODELO.exists():
        estado["modelo"] = joblib.load(RUTA_MODELO)
    if RUTA_METADATOS.exists():
        estado["metadatos"] = json.loads(RUTA_METADATOS.read_text(encoding="utf-8"))
    yield


app = FastAPI(
    title="API de riesgo de entrega tardía - DataCo",
    description="Predice si un pedido llegará tarde con los datos que se conocen al momento de la compra.",
    version="1.0.0",
    lifespan=lifespan,
)


def obtener_modelo():
    """Devuelve el modelo o responde 503 si todavía no se ha entrenado."""
    if estado["modelo"] is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no cargado. Entrénalo con: uv run python -m proyecto_diego.train",
        )
    return estado["modelo"]


@app.get("/health")
def health():
    """Indica si la API está viva y si el modelo está cargado."""
    cargado = estado["modelo"] is not None
    return {"status": "healthy" if cargado else "degraded", "modelo_cargado": cargado}


@app.get("/model-info")
def model_info():
    """Muestra qué modelo está en uso y sus métricas en test."""
    obtener_modelo()
    return estado["metadatos"]


@app.post("/predict", response_model=PrediccionSalida)
def predict(pedido: PedidoEntrada):
    """Recibe un pedido y devuelve si se espera que llegue tarde."""
    modelo = obtener_modelo()
    datos = pd.DataFrame([pedido.a_columnas()])

    probabilidad = float(modelo.predict_proba(datos)[0, 1])
    llega_tarde = bool(modelo.predict(datos)[0] == 1)

    if llega_tarde:
        recomendacion = "Priorizar este pedido y avisar al cliente de un posible retraso."
    else:
        recomendacion = (
            "Sin alerta. Ojo: el modelo casi no detecta los retrasos de Standard Class."
        )

    return PrediccionSalida(
        llega_tarde=llega_tarde,
        probabilidad_tarde=round(probabilidad, 3),
        recomendacion=recomendacion,
    )