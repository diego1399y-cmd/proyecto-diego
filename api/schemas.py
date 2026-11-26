"""Qué datos entran y salen de la API (Pydantic).

FastAPI usa estas clases para:
    1. Validar lo que llega: si falta un campo o un valor no tiene sentido
       (un mes 13, una cantidad negativa), responde 422 sin llamar al modelo.
    2. Documentar la API en /docs automáticamente.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EJEMPLO_PEDIDO = {
    "modo_envio": "First Class",
    "tipo_pago": "DEBIT",
    "mercado": "LATAM",
    "segmento_cliente": "Consumer",
    "cantidad": 2,
    "venta": 120.5,
    "tasa_descuento": 0.1,
    "mes_pedido": 6,
    "dia_semana_pedido": 2,
}


class PedidoEntrada(BaseModel):
    """Datos de un pedido en el momento de la compra (antes de enviarlo)."""

    model_config = ConfigDict(json_schema_extra={"examples": [EJEMPLO_PEDIDO]})

    modo_envio: Literal["Standard Class", "Second Class", "First Class", "Same Day"]
    tipo_pago: Literal["DEBIT", "TRANSFER", "PAYMENT", "CASH"]
    mercado: Literal["Africa", "Europe", "LATAM", "Pacific Asia", "USCA"]
    segmento_cliente: Literal["Consumer", "Corporate", "Home Office"]
    cantidad: int = Field(ge=1, le=100, description="Unidades del producto")
    venta: float = Field(gt=0, description="Valor de la venta en USD")
    tasa_descuento: float = Field(ge=0, le=1, description="Descuento entre 0 y 1 (0.1 = 10 %)")
    mes_pedido: int = Field(ge=1, le=12)
    dia_semana_pedido: int = Field(ge=0, le=6, description="0 = lunes … 6 = domingo")

    def a_columnas(self) -> dict:
        """Traduce los nombres de la API a los nombres de columna que conoce el modelo."""
        return {
            "Shipping Mode": self.modo_envio,
            "Type": self.tipo_pago,
            "Market": self.mercado,
            "Customer Segment": self.segmento_cliente,
            "Order Item Quantity": self.cantidad,
            "Sales": self.venta,
            "Order Item Discount Rate": self.tasa_descuento,
            "mes_pedido": self.mes_pedido,
            "dia_semana_pedido": self.dia_semana_pedido,
        }


class PrediccionSalida(BaseModel):
    """Respuesta de /predict."""

    llega_tarde: bool
    probabilidad_tarde: float = Field(description="Entre 0 y 1")
    recomendacion: str