# Predicción de entregas tardías en la cadena de suministro

> Modelo de clasificación que predice si un pedido llegará tarde a partir de sus datos de envío, cliente y producto, para que el área de logística pueda priorizar pedidos en riesgo.    Proyecto del curso Proyecto 1: Introducción a la Analítica.

## Equipo

| Integrante | Rol principal | GitHub |
|---|---|---|
| Diego Andrés Fernández González | Datos, EDA, modelado y API  | @diego1399y-cmd |

## Dataset

**DataCo Smart Supply Chain for Big Data Analysis**

- **Fuente:** [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) · original en [Mendeley Data](https://data.mendeley.com/datasets/8gx2fvg2k6/5) (Constante, Silva y Pereira; licencia CC BY 4.0)
- **Descripción:** registros de pedidos de la empresa DataCo Global entre 2015 y 2019, con información de envío (modo de envío, días programados y reales), clientes, productos (ropa, deportes, electrónica), ventas, descuentos, beneficios y ubicación de origen y destino.
- **Tamaño:** 180.519 filas × 53 columnas
- **Variable objetivo:** `Late_delivery_risk` (1 = entrega tardía, 0 = entrega a tiempo)
- **Tipo de problema:** clasificación binaria
- **Archivo principal:** `DataCoSupplyChainDataset.csv` (va en `data/raw/`, no se sube al repositorio por su tamaño)

## Problema de negocio

_(se completa en el módulo 02)_

## Cómo ejecutar

```bash
uv sync
uv run jupyter lab
```

## Estructura

```
├── data/raw/          ← datos originales
├── data/processed/    ← datos limpios (generados)
├── docs/              ← problema, charter, decisiones
├── notebooks/         ← exploración
├── src/               ← código reutilizable (limpieza, train, api)
└── models/            ← modelos entrenados (generados)
```

## Avance

- [x] 00 Entorno con uv
- [x] 01 Repositorio en GitHub
- [ ] 02 Problema y KPIs
- [ ] 03 Project charter
- [ ] 04 Limpieza
- [ ] 05 EDA
- [ ] 06 Baseline
- [ ] 07 Pipeline de entrenamiento
- [ ] 08 API
- [ ] 09 Entrega final