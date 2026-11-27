# Modelado (módulo 06)

## Tipo de problema y métrica principal (y por qué)

- **Tipo de problema:** clasificación binaria. Objetivo: `Late_delivery_risk` (1 = pedido tarde).
- **Métrica principal: *recall* de la clase 1.** De todos los pedidos que llegan tarde, ¿cuántos detecta el modelo? En logística el error más caro es que se escape un pedido tardío sin avisar al cliente.
- **Métricas de apoyo:** *precision* (de los pedidos que el modelo marca como tardíos, ¿cuántos lo son?) y F1 (balance entre las dos).
- **Criterio de éxito:** *recall* ≥ 0,80 en test y F1 mayor que el del *baseline*.

## Datos y variables

- **Partición:** 80 % entrenamiento (138.212 filas) y 20 % prueba (34.553 filas), estratificada por el objetivo y con `random_state=42`.
- **Variables (9), solo las que se conocen al momento de la compra:**
  - Categóricas: `Shipping Mode`, `Type`, `Market`, `Customer Segment`
  - Numéricas: `Order Item Quantity`, `Sales`, `Order Item Discount Rate`, `mes_pedido`, `dia_semana_pedido`
- **Excluidas por *data leakage*:** `Delivery Status`, `Days for shipping (real)` y `shipping date (DateOrders)`.
- **`Days for shipment (scheduled)` no se usa** porque dice lo mismo que `Shipping Mode`: cada modo tiene un plazo fijo.

## Pipeline

```
Pipeline
├── preprocesamiento (ColumnTransformer)
│   ├── numéricas:   SimpleImputer(median) → StandardScaler
│   └── categóricas: SimpleImputer(most_frequent) → OneHotEncoder(handle_unknown="ignore")
└── modelo: DecisionTreeClassifier(max_depth=5, random_state=42)
```

El preprocesamiento aprende **solo de los datos de entrenamiento** (dentro del pipeline), lo que evita la fuga de información. Se entrena con:

```bash
uv run python -m proyecto_diego.train
```

## Comparación (*baseline* vs. modelos)

| Modelo | Accuracy (train / test) | Precision (train / test) | Recall (train / test) | F1 (train / test) |
|---|---|---|---|---|
| *Baseline* (siempre "tarde") | 0,573 / 0,573 | 0,573 / 0,573 | 1,000 / 1,000 | 0,728 / 0,728 |
| Regresión logística | 0,697 / 0,698 | 0,887 / 0,885 | 0,540 / 0,543 | 0,671 / 0,673 |
| **Árbol de decisión** | **0,699 / 0,699** | **0,874 / 0,870** | **0,554 / 0,557** | **0,678 / 0,679** |

## Modelo elegido y justificación

**Árbol de decisión (profundidad máxima 5).**

- Tiene el mejor *recall* y F1 en test de los dos modelos reales.
- Sus reglas se pueden explicar al coordinador de logística.
- **No hay *overfitting*:** train y test dan casi lo mismo.

## Métrica en test (una sola vez)

| Métrica | Valor | Meta | ¿Cumple? |
|---|---|---|---|
| *Recall* (clase 1) | 0,557 | ≥ 0,80 | **No** |
| F1 | 0,679 | > 0,728 (*baseline*) | **No** |
| *Precision* | 0,870 | (apoyo) | 87 de cada 100 alertas son correctas |

El *baseline* tiene *recall* 1,0 y F1 alto solo porque marca **todos** los pedidos como tardíos. Eso no sirve para priorizar: si todo es urgente, nada lo es. El modelo sube la *precision* de 0,573 a 0,870.

## Análisis de errores y límites

Pedidos que de verdad llegaron tarde en test, por modo de envío:

| Modo de envío | Tardíos | Detectados | Se escapan | *Recall* |
|---|---|---|---|---|
| First Class | 5.282 | 5.282 | 0 | 1,00 |
| Second Class | 5.468 | 5.468 | 0 | 1,00 |
| Same Day | 920 | 269 | 651 | 0,29 |
| Standard Class | 8.125 | 0 | 8.125 | 0,00 |
| **Total** | **19.795** | **11.019** | **8.776** | **0,557** |

- **El modelo aprendió casi una sola regla:** "First o Second Class → tarde; Standard Class → a tiempo".
- **Límite principal:** no detecta ningún retraso de Standard Class (el 41 % de los tardíos). Con las variables del dataset (mercado, cliente, cantidad, fecha) no se puede saber cuáles pedidos de Standard Class se van a retrasar.
- **Conclusión para el negocio:** la causa principal del retraso es una **promesa de entrega mal calculada** (First Class promete 1 día y tarda 2; Second Class promete 2 y tarda 4). Ajustar esas promesas tendría más impacto que el modelo.

## Siguientes pasos

1. Conseguir variables que expliquen los retrasos de Standard Class: transportadora, bodega de salida, distancia, carga de trabajo del día.
2. Ajustar el umbral de decisión (hoy 0,5) usando un conjunto de **validación**, no el de test, para subir el *recall* a costa de algo de *precision*.
3. Probar modelos más flexibles (por ejemplo, *random forest*) cuando haya variables nuevas.