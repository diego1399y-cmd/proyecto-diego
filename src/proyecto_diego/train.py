"""Entrena el modelo de entregas tardías y lo guarda listo para la API.

Uso (desde la carpeta proyecto-diego):

    uv run python -m proyecto_diego.train

Hace lo mismo que la sección 5 del notebook:
    1. Carga los datos limpios (si no existen, los genera desde data/raw).
    2. Separa train y test (80/20) con la semilla 42.
    3. Entrena el árbol de decisión elegido.
    4. Evalúa en test y revisa el criterio de éxito (recall >= 0,80).
    5. Reentrena con todos los datos y guarda el modelo y sus metadatos.
"""

import json
from datetime import datetime

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from proyecto_diego.limpieza import OBJETIVO, RAIZ, cargar_limpios

SEMILLA = 42
CRITERIO_RECALL = 0.80

VARIABLES_NUMERICAS = [
    "Order Item Quantity", "Sales", "Order Item Discount Rate",
    "mes_pedido", "dia_semana_pedido",
]
VARIABLES_CATEGORICAS = ["Shipping Mode", "Type", "Market", "Customer Segment"]
VARIABLES = VARIABLES_NUMERICAS + VARIABLES_CATEGORICAS

CARPETA_MODELOS = RAIZ / "models"
RUTA_MODELO = CARPETA_MODELOS / "modelo.joblib"
RUTA_METADATOS = CARPETA_MODELOS / "modelo.json"


def construir_pipeline():
    """Preparación de variables + árbol de decisión (igual que en el notebook)."""
    preprocesamiento = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()),
         VARIABLES_NUMERICAS),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                              OneHotEncoder(handle_unknown="ignore")),
         VARIABLES_CATEGORICAS),
    ])
    arbol = DecisionTreeClassifier(max_depth=5, random_state=SEMILLA)
    return make_pipeline(preprocesamiento, arbol)


def evaluar(y_real, y_pred) -> dict:
    """Métricas para la clase 1 (pedido tarde)."""
    return {
        "accuracy": round(accuracy_score(y_real, y_pred), 3),
        "precision": round(precision_score(y_real, y_pred, pos_label=1), 3),
        "recall": round(recall_score(y_real, y_pred, pos_label=1), 3),
        "F1": round(f1_score(y_real, y_pred, pos_label=1), 3),
    }


def main() -> None:
    # 1-2. Datos
    df = cargar_limpios()
    X, y = df[VARIABLES], df[OBJETIVO]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEMILLA, stratify=y,
    )
    print(f"Datos: {len(df):,} pedidos · train={len(X_train):,} · test={len(X_test):,}")

    # 3-4. Entrenar y evaluar
    modelo = construir_pipeline()
    modelo.fit(X_train, y_train)
    metricas = evaluar(y_test, modelo.predict(X_test))
    cumple = metricas["recall"] >= CRITERIO_RECALL
    print(f"Test: {metricas}")
    print(f"Criterio de éxito (recall >= {CRITERIO_RECALL}): {'CUMPLE' if cumple else 'NO CUMPLE'}")

    # 5. Reentrenar con todos los datos y guardar
    modelo.fit(X, y)
    CARPETA_MODELOS.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, RUTA_MODELO)
    metadatos = {
        "modelo": "Árbol de decisión (max_depth=5)",
        "entrenado_en": datetime.now().isoformat(timespec="seconds"),
        "variables_numericas": VARIABLES_NUMERICAS,
        "variables_categoricas": VARIABLES_CATEGORICAS,
        "metricas_test": metricas,
        "cumple_criterio_exito": cumple,
        "n_entrenamiento_final": len(X),
    }
    RUTA_METADATOS.write_text(json.dumps(metadatos, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Modelo guardado en {RUTA_MODELO.relative_to(RAIZ)}")
    print(f"Metadatos en {RUTA_METADATOS.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()