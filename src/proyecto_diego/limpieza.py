"""Limpieza de los datos de DataCo.

Repite en código las mismas decisiones de la sección 3 del notebook,
para que el modelo se pueda reentrenar sin abrir Jupyter.
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]  # carpeta proyecto-diego
ARCHIVO_CRUDO = RAIZ / "data" / "raw" / "dataco.csv"
ARCHIVO_LIMPIO = RAIZ / "data" / "processed" / "datos_limpios.csv"

OBJETIVO = "Late_delivery_risk"

# Decisión 1: pedidos que nunca se enviaron
ESTADOS_NO_ENVIADOS = ["CANCELED", "SUSPECTED_FRAUD"]

# Decisión 2: columnas vacías, constantes, con datos personales o copias de otras
COLUMNAS_SIN_VALOR = [
    "Product Description", "Order Zipcode", "Product Image", "Product Status",
    "Customer Email", "Customer Password", "Customer Fname", "Customer Lname",
    "Customer Street",
    "Order Profit Per Order", "Sales per customer", "Order Item Product Price",
]


def cargar_crudos(ruta: Path = ARCHIVO_CRUDO) -> pd.DataFrame:
    """Lee el CSV original. Viene en latin-1, no en utf-8."""
    return pd.read_csv(ruta, encoding="latin-1")


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica las 3 decisiones de limpieza y devuelve una copia limpia."""
    df = df.dropna(subset=[OBJETIVO])

    # Decisión 1
    df = df[~df["Order Status"].isin(ESTADOS_NO_ENVIADOS)]

    # Decisión 2
    df = df.drop(columns=COLUMNAS_SIN_VALOR)

    # Decisión 3: fecha del pedido y variables de calendario
    df = df.copy()
    fecha = pd.to_datetime(df["order date (DateOrders)"], format="%m/%d/%Y %H:%M")
    df["order date (DateOrders)"] = fecha
    df["anio_pedido"] = fecha.dt.year
    df["mes_pedido"] = fecha.dt.month
    df["dia_semana_pedido"] = fecha.dt.day_of_week  # 0 = lunes
    return df


def cargar_limpios() -> pd.DataFrame:
    """Devuelve los datos limpios. Si no existen, los genera desde los crudos."""
    if ARCHIVO_LIMPIO.exists():
        return pd.read_csv(ARCHIVO_LIMPIO)
    df = limpiar(cargar_crudos())
    ARCHIVO_LIMPIO.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ARCHIVO_LIMPIO, index=False)
    return df


if __name__ == "__main__":
    df = limpiar(cargar_crudos())
    ARCHIVO_LIMPIO.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ARCHIVO_LIMPIO, index=False)
    print(f"Datos limpios: {df.shape[0]:,} filas y {df.shape[1]} columnas")
    print(f"Pedidos tarde: {df[OBJETIVO].mean():.1%}")
    print(f"Guardado en {ARCHIVO_LIMPIO.relative_to(RAIZ)}")