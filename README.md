# Predicción de entregas tardías en la cadena de suministro

> Modelo de clasificación que predice si un pedido llegará tarde a partir de sus datos de envío, cliente y producto, para que el área de logística pueda priorizar los pedidos en riesgo. Proyecto del curso Proyecto 1: Introducción a la Analítica (Universidad de Medellín).

## Equipo

| Integrante | Rol principal | GitHub |
|---|---|---|
| Diego Andrés Fernández González | Datos, EDA, modelado y API (trabajo individual) | @diego1399y-cmd |

## Problema de negocio

- **Decisión que se quiere mejorar:** qué pedidos priorizar (cambiar de transportadora, acelerar el despacho o avisar al cliente) antes de que lleguen tarde.
- **Quién decide:** el coordinador de logística / despachos.
- **Tipo de análisis principal:** predictivo (clasificación), apoyado en análisis descriptivo y diagnóstico.
- **Criterio de éxito:** en los datos de prueba, detectar al menos el 80 % de los pedidos que llegarán tarde (*recall* ≥ 0,80) con un F1 superior al del *baseline*.
- **KPI 1:** tasa de entregas a tiempo = pedidos a tiempo / pedidos despachados. Pasar del 42,7 % actual al 55 % durante el primer semestre de 2027, medida cada mes.
- **KPI 2:** tasa de entregas tardías en First Class. Bajarla del 100 % actual al 30 % en el primer trimestre de 2027, medida cada mes.

## Dataset

**DataCo Smart Supply Chain for Big Data Analysis**

- **Fuente:** [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) · original en [Mendeley Data](https://data.mendeley.com/datasets/8gx2fvg2k6/5) (Constante, Silva y Pereira; licencia CC BY 4.0)
- **Descripción:** pedidos de la empresa DataCo Global entre enero de 2015 y enero de 2018, con información del envío, el cliente, el producto, las ventas y el destino.
- **Una fila es:** un producto dentro de un pedido (línea de pedido).
- **Tamaño:** 180.519 filas × 53 columnas (172.765 filas después de la limpieza).
- **Variable objetivo:** `Late_delivery_risk` (1 = entrega tardía, 0 = entrega a tiempo). 57,3 % de las filas son tardías después de la limpieza (54,8 % en los datos originales).
- **Tipo de problema:** clasificación binaria.
- **Archivo:** `data/raw/dataco.csv`. No se sube al repositorio porque pesa 95 MB: se descarga de Kaggle (`DataCoSupplyChainDataset.csv`) y se guarda con ese nombre.

### Diccionario de datos

| Variable | Tipo | Qué representa | Unidades / valores | Uso en el proyecto |
|---|---|---|---|---|
| `Type` | Texto | Tipo de transacción del pago | DEBIT, TRANSFER, PAYMENT, CASH | Variable |
| `Days for shipping (real)` | Entero | Días que realmente tardó el envío | días | **Excluida: data leakage** |
| `Days for shipment (scheduled)` | Entero | Días de entrega prometidos al cliente | días (0, 1, 2 o 4) | Variable |
| `Benefit per order` | Decimal | Ganancia del pedido | USD | Variable |
| `Sales per customer` | Decimal | Ventas totales por cliente | USD | Eliminada (copia de Order Item Total) |
| `Delivery Status` | Texto | Estado final de la entrega | Advance shipping, Late delivery, Shipping canceled, Shipping on time | **Excluida: data leakage** |
| `Late_delivery_risk` | Entero (0/1) | Si el pedido llegó tarde | 1 = tarde, 0 = a tiempo | **Objetivo** |
| `Category Id` | Entero | Código de la categoría del producto | código | Excluida (identificador) |
| `Category Name` | Texto | Categoría del producto | p. ej. Cleats, Fishing | Variable |
| `Customer City` | Texto | Ciudad del cliente | texto | Variable |
| `Customer Country` | Texto | País del cliente | EE. UU., Puerto Rico | Variable |
| `Customer Email` | Texto | Correo del cliente (enmascarado) | XXXXXXXXX | Eliminada (dato personal) |
| `Customer Fname` | Texto | Nombre del cliente | texto | Eliminada (dato personal) |
| `Customer Id` | Entero | Código del cliente | código | Excluida (identificador) |
| `Customer Lname` | Texto | Apellido del cliente | texto | Eliminada (dato personal) |
| `Customer Password` | Texto | Clave del cliente (enmascarada) | XXXXXXXXX | Eliminada (dato personal) |
| `Customer Segment` | Texto | Tipo de cliente | Consumer, Corporate, Home Office | Variable |
| `Customer State` | Texto | Estado donde está registrada la tienda | código de estado | Variable |
| `Customer Street` | Texto | Dirección de la tienda/cliente | texto | Eliminada (dato personal) |
| `Customer Zipcode` | Decimal | Código postal del cliente | código | Excluida (identificador) |
| `Department Id` | Entero | Código del departamento de la tienda | código | Excluida (identificador) |
| `Department Name` | Texto | Departamento de la tienda | p. ej. Fitness, Apparel | Variable |
| `Latitude` | Decimal | Latitud de la tienda | grados | Variable |
| `Longitude` | Decimal | Longitud de la tienda | grados | Variable |
| `Market` | Texto | Mercado de destino del pedido | Africa, Europe, LATAM, Pacific Asia, USCA | Variable |
| `Order City` | Texto | Ciudad de destino | texto | Variable |
| `Order Country` | Texto | País de destino | texto | Variable |
| `Order Customer Id` | Entero | Código del cliente en el pedido | código | Excluida (copia de Customer Id) |
| `order date (DateOrders)` | Fecha (texto) | Fecha y hora del pedido | mes/día/año hora:min | Convertida a fecha; de ella salen año, mes, día de la semana y hora |
| `Order Id` | Entero | Código del pedido | código | Excluida (identificador) |
| `Order Item Cardprod Id` | Entero | Código del producto leído por RFID | código | Excluida (copia de Product Card Id) |
| `Order Item Discount` | Decimal | Valor del descuento | USD | Variable |
| `Order Item Discount Rate` | Decimal | Porcentaje de descuento | proporción (0 a 0,25) | Variable |
| `Order Item Id` | Entero | Código de la línea de pedido | código único por fila | Excluida (identificador) |
| `Order Item Product Price` | Decimal | Precio del producto sin descuento | USD | Eliminada (copia de Product Price) |
| `Order Item Profit Ratio` | Decimal | Margen de ganancia de la línea | proporción | Variable |
| `Order Item Quantity` | Entero | Unidades del producto en el pedido | unidades | Variable |
| `Sales` | Decimal | Valor de la venta | USD | Variable |
| `Order Item Total` | Decimal | Total de la línea después del descuento | USD | Variable |
| `Order Profit Per Order` | Decimal | Ganancia del pedido | USD | Eliminada (copia de Benefit per order) |
| `Order Region` | Texto | Región de destino | 23 regiones (p. ej. South America, Western Europe) | Variable |
| `Order State` | Texto | Estado o provincia de destino | texto | Variable |
| `Order Status` | Texto | Estado del pedido | COMPLETE, PENDING, CLOSED, CANCELED, SUSPECTED_FRAUD… | Variable (se eliminan CANCELED y SUSPECTED_FRAUD) |
| `Order Zipcode` | Decimal | Código postal de destino | código (86 % vacío) | Eliminada (casi vacía) |
| `Product Card Id` | Entero | Código del producto | código | Excluida (identificador) |
| `Product Category Id` | Entero | Código de categoría del producto | código | Excluida (copia de Category Id) |
| `Product Description` | Decimal | Descripción del producto | 100 % vacía | Eliminada (vacía) |
| `Product Image` | Texto | Enlace a la imagen del producto | URL | Eliminada |
| `Product Name` | Texto | Nombre del producto | texto | Variable |
| `Product Price` | Decimal | Precio del producto | USD | Variable |
| `Product Status` | Entero | Disponibilidad del producto | siempre 0 | Eliminada (constante) |
| `shipping date (DateOrders)` | Fecha (texto) | Fecha y hora real del envío | mes/día/año hora:min | **Excluida: data leakage** |
| `Shipping Mode` | Texto | Modo de envío | Standard Class, Second Class, First Class, Same Day | Variable |

## Hallazgos principales (EDA)

1. **El modo de envío es lo que más explica el retraso:** First Class llega tarde el 100 % de las veces, Second Class el 80 % y Standard Class el 40 %.
2. **El problema es la promesa, no la lentitud:** First Class promete 1 día y tarda 2; Second Class promete 2 y tarda 4. Los días reales no se pueden usar en el modelo porque son *data leakage*.
3. **El mercado de destino y las características del pedido no cambian el retraso:** a igual modo de envío, los 5 mercados difieren como máximo 5 puntos porcentuales.

El análisis completo, la limpieza y el registro de decisiones están en [`notebooks/proyecto_equipo.ipynb`](notebooks/proyecto_equipo.ipynb).

## Resultados del modelo

Se compararon tres modelos en los datos de prueba (20 %, 34.553 filas). La clase positiva es **1 = pedido tarde**.

| Modelo | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| *Baseline* (siempre "tarde") | 0,573 | 0,573 | 1,000 | 0,728 |
| Regresión logística | 0,698 | 0,885 | 0,543 | 0,673 |
| **Árbol de decisión (elegido)** | **0,699** | **0,870** | **0,557** | **0,679** |

- **Criterio de éxito: no se cumple.** El recall es 0,557 (meta: 0,80) y el F1 queda por debajo del *baseline*. El *baseline* tiene recall y F1 altos solo porque marca todos los pedidos como tardíos, lo que no sirve para priorizar.
- **Lo que sí logra:** cuando el modelo marca un pedido como tardío, acierta 87 de cada 100 veces (frente a 57 del *baseline*). Sin *overfitting*: train y test dan casi igual.
- **Dónde falla:** detecta el 100 % de los tardíos de First Class y Second Class, pero **ninguno de Standard Class**. Las variables disponibles no explican qué pedidos de Standard Class se retrasan.
- **Conclusión para el negocio:** el retraso depende sobre todo del modo de envío y de una promesa de entrega mal calculada. Ajustar los días prometidos de First y Second Class tendría más impacto que el modelo.

## Cómo ejecutar

Requisitos: [uv](https://docs.astral.sh/uv/) y el archivo `data/raw/dataco.csv` descargado de Kaggle (ver [Dataset](#dataset)).

```bash
# 1. Instalar dependencias
uv sync

# 2. Limpiar los datos -> data/processed/datos_limpios.csv
uv run python -m proyecto_diego.limpieza

# 3. Entrenar el modelo -> models/modelo.joblib y models/modelo.json
uv run python -m proyecto_diego.train

# 4. Levantar la API
uv run uvicorn api.main:app --reload

# 5. Correr las pruebas (en otra terminal, con el modelo ya entrenado)
uv run pytest -v
```

El análisis completo está en `notebooks/proyecto_equipo.ipynb` (kernel `.venv`, *Run All*). Los scripts del paso 2 y 3 reproducen exactamente la limpieza y el modelo del notebook.

## API

Documentación interactiva: http://127.0.0.1:8000/docs

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Indica si la API está activa y si el modelo está cargado |
| GET | `/model-info` | Muestra el modelo en uso y sus métricas en test |
| POST | `/predict` | Recibe un pedido y devuelve si se espera que llegue tarde |

Ejemplo de entrada para `/predict`:

```json
{
  "modo_envio": "First Class",
  "tipo_pago": "DEBIT",
  "mercado": "LATAM",
  "segmento_cliente": "Consumer",
  "cantidad": 2,
  "venta": 120.5,
  "tasa_descuento": 0.1,
  "mes_pedido": 6,
  "dia_semana_pedido": 2
}
```

Respuesta:

```json
{
  "llega_tarde": true,
  "probabilidad_tarde": 1.0,
  "recomendacion": "Priorizar este pedido y avisar al cliente de un posible retraso."
}
```

Si faltan campos o un valor no es válido (por ejemplo, `mes_pedido: 13`), la API responde **422**. Si el modelo no se ha entrenado, responde **503**.

## Estructura

```
├── api/               ← API con FastAPI (main.py, schemas.py)
├── data/raw/          ← datos originales (dataco.csv, no se sube)
├── data/processed/    ← datos limpios (generados por limpieza.py)
├── docs/              ← documentación del proyecto
├── models/            ← modelo entrenado (generado por train.py, no se sube)
├── notebooks/         ← notebook del proyecto
├── src/proyecto_diego/
│   ├── limpieza.py    ← limpieza reproducible
│   └── train.py       ← entrenamiento y métricas
└── tests/             ← pruebas de la API (pytest)
```

## Avance

- [x] 00 Entorno con uv
- [x] 01 Repositorio en GitHub
- [x] 02 Problema, KPIs y comprensión de los datos
- [x] 03 Limpieza y EDA
- [x] 04 Modelado y métricas
- [x] 05 Pipeline y API
- [ ] 06 Entrega final