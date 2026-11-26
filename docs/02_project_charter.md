# Project Charter: Predicción de entregas tardías en DataCo

> Documento de una página que alinea el proyecto con el negocio. Versión final, actualizada con los resultados del modelo.

**Integrante:** Diego Andrés Fernández González (trabajo individual) · **Fecha:** 2026-11-25 · **Versión:** 1.0

## 1. Contexto y problema de negocio

El 57,3 % de los pedidos enviados por DataCo llega tarde. Hoy el retraso se detecta cuando ya ocurrió, así que no hay tiempo de acelerar el despacho, cambiar de transportadora o avisar al cliente. Esto afecta la satisfacción del cliente y la reputación de la empresa.

## 2. Objetivo

| Nivel | Descripción |
|---|---|
| **Negocio** | Subir la tasa de entregas a tiempo del 42,7 % al 55 % en el primer semestre de 2027 |
| **Ciencia de datos** | Clasificar cada pedido, al momento de la compra, según si llegará tarde o no |
| **Tipo de problema** | Clasificación binaria |
| **Variable objetivo** | `Late_delivery_risk` (1 = tarde, 0 = a tiempo) |

## 3. Criterios de éxito

| Tipo | Métrica | Umbral | Resultado |
|---|---|---|---|
| Negocio (KPI) | Tasa de entregas a tiempo | 55 % | Se mide cuando el modelo esté en uso |
| Modelo | *Recall* de la clase "tarde" en test | ≥ 0,80 | **0,557: no se cumple** |
| *Baseline* a superar | Predecir siempre "tarde" | F1 = 0,728 | F1 del modelo = 0,679: no lo supera |

**Lectura del resultado:** el modelo no cumple la meta de *recall*, pero cuando marca un pedido como tardío acierta 87 de cada 100 veces (precision 0,870), frente a 57 del *baseline*. Sirve para priorizar los pedidos de First y Second Class, no para Standard Class.

## 4. Datos

| Fuente | Descripción | Filas × columnas | Acceso |
|---|---|---|---|
| [Kaggle: DataCo Smart Supply Chain](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) | Pedidos de DataCo Global, enero 2015 a enero 2018 | 180.519 × 53 | Público (CC BY 4.0), descargado el 1 de noviembre de 2026 |

**¿Qué representa una fila?** Un producto dentro de un pedido.

## 5. Alcance

- **Incluye:** limpieza reproducible, EDA, comparación de un *baseline* con dos modelos, pipeline de entrenamiento y una API con FastAPI para consultar el riesgo de cada pedido.
- **No incluye:** conexión con los sistemas reales de DataCo, cálculo de costos de los retrasos ni recomendación automática de cuántos días prometer.

## 6. Riesgos y supuestos

| Riesgo | Probabilidad | Impacto | Mitigación | ¿Qué pasó? |
|---|---|---|---|---|
| *Data leakage*: columnas que solo se conocen después de la entrega | Alta | Alto | Excluir `Delivery Status`, días reales y fecha de envío | Se confirmó: reproducían el objetivo en el 97,5 % de las filas. Se excluyeron. |
| Filas que distorsionan el objetivo | Media | Alto | Revisar `Order Status` | 7.754 pedidos cancelados o con sospecha de fraude aparecían como "a tiempo". Se eliminaron. |
| Clases desbalanceadas | Baja | Medio | Medir *recall* y F1, no solo *accuracy* | Las clases están casi balanceadas (57 % / 43 %). |
| Las variables disponibles no explican el retraso | Media | Alto | Comparar contra un *baseline* | **Ocurrió:** el modelo no detecta los retrasos de Standard Class. Se necesitan datos de transportadora, bodega o distancia. |

## 7. Plan (cronograma del curso)

| Fecha | Fase CRISP-DM | Entregable | Responsable |
|---|---|---|---|
| 26 de octubre | Negocio + Datos | Problema, KPIs y perfil de los datos | Diego |
| 27 de octubre | Preparación + EDA | Limpieza y 3 hallazgos | Diego |
| 28 de octubre | Modelado + Evaluación | *Baseline* y dos modelos | Diego |
| 11 de noviembre | Pipeline + Despliegue | Scripts reproducibles y API con pruebas | Diego |
| Sustentación | Presentación | Presentación de 10-12 minutos con demo | Diego |

## 8. Stakeholders

| Persona/rol | Interés | Cómo se le comunica |
|---|---|---|
| Coordinador de logística / despachos | Saber qué pedidos priorizar cada día | Consulta a la API por cada pedido nuevo |
| Gerencia de operaciones | Mejorar la tasa de entregas a tiempo | Reporte mensual de los KPIs |
| Servicio al cliente | Avisar al cliente antes de que el pedido llegue tarde | Alerta cuando el modelo marca un pedido en riesgo |