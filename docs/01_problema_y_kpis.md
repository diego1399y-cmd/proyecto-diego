# Problema y KPIs (módulo 02)

## Tema

Predicción de entregas tardías en la cadena de suministro de DataCo Global.

## Dataset

- **Nombre:** DataCo Smart Supply Chain for Big Data Analysis
- **Fuente:** [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis), original en Mendeley Data (licencia CC BY 4.0)
- **Fecha de descarga:** 1 de noviembre de 2026
- **Tamaño:** 180.519 filas × 53 columnas (172.765 filas después de la limpieza)
- **Periodo:** enero de 2015 a enero de 2018
- **Una fila es:** un producto dentro de un pedido. Un mismo pedido (`Order Id`) puede tener varias filas, una por producto.

## ¿Quién decide y qué decisión?

- **Quién:** el coordinador de logística o de despachos de DataCo.
- **Decisión:** qué pedidos priorizar (acelerar el despacho, cambiar de transportadora o avisar al cliente) **antes** de que lleguen tarde. Hoy el problema se detecta cuando el pedido ya está retrasado.

## Preguntas por tipo de análisis

| Tipo | Pregunta |
|---|---|
| Descriptivo | ¿Qué porcentaje de los pedidos llega tarde y cómo cambia según el modo de envío y el mercado? |
| Diagnóstico | ¿Por qué se retrasan los pedidos? ¿Es porque el envío es lento o porque la promesa de entrega es muy corta? |
| **Predictivo (principal)** | Al momento de la compra, ¿se puede saber si un pedido llegará tarde? |
| Prescriptivo | ¿Cuántos días se deberían prometer en cada modo de envío para reducir los retrasos? |

**Variable objetivo:** `Late_delivery_risk` (1 = llegó tarde, 0 = a tiempo o antes).

**Criterio de éxito del modelo:** detectar al menos el 80 % de los pedidos que llegan tarde en los datos de prueba (*recall* ≥ 0,80) y superar al *baseline*. Se eligió *recall* porque en logística el error más caro es que se escape un pedido tardío sin avisarle al cliente.

## KPIs SMART

| KPI | Fórmula | Meta | Periodo | Columnas |
|---|---|---|---|---|
| Tasa de entregas a tiempo | pedidos entregados a tiempo / pedidos despachados | Pasar del 42,7 % al 55 % | Primer semestre de 2027, medida cada mes | `Late_delivery_risk`, `Order Status` |
| Tasa de entregas tardías en First Class | pedidos First Class tardíos / pedidos First Class despachados | Bajar del 100 % al 30 % | Primer trimestre de 2027, medida cada mes | `Late_delivery_risk`, `Shipping Mode` |