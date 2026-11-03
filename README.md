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
- **Variable objetivo:** `Late_delivery_risk` (1 = entrega tardía, 0 = entrega a tiempo). 54,8 % de las filas son tardías.
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

## Cómo ejecutar

```bash
uv sync
uv run jupyter lab
```

Abrir `notebooks/proyecto_equipo.ipynb` con el kernel `.venv` y ejecutar todo (*Run All*).

## Estructura

```
├── data/raw/          ← datos originales (dataco.csv, no se sube)
├── data/processed/    ← datos limpios (generados por el notebook)
├── docs/              ← respuestas y acuerdos
├── notebooks/         ← notebook del proyecto
├── src/               ← código reutilizable
└── models/            ← modelos entrenados (generados)
```

## Avance

- [x] 00 Entorno con uv
- [x] 01 Repositorio en GitHub
- [x] 02 Problema, KPIs y comprensión de los datos
- [x] 03 Limpieza y EDA
- [ ] 04 Modelado y métricas
- [ ] 05 Pipeline y API
- [ ] 06 Entrega final
