# Registro de decisiones de limpieza (módulo 04)

Las decisiones se aplican igual en el notebook (sección 3) y en el script `src/proyecto_diego/limpieza.py`, que se ejecuta con:

```bash
uv run python -m proyecto_diego.limpieza
```

**Resultado:** de 180.519 filas × 53 columnas se pasa a **172.765 filas × 44 columnas**. La proporción de pedidos tardíos sube del 54,8 % al 57,3 %.

| # | Columna(s) | Problema | Decisión | Justificación | Responsable |
|---|---|---|---|---|---|
| 1 | `Order Status` | 7.754 pedidos `CANCELED` o `SUSPECTED_FRAUD` aparecen con `Late_delivery_risk = 0` | Eliminar esas filas (4,3 % de los datos) | Nunca se enviaron, así que no son entregas a tiempo. Dejarlos enseñaría al modelo algo falso. | Diego |
| 2a | `Product Description`, `Order Zipcode` | Vacías (100 % y 86 % de nulos) | Eliminar las columnas | No hay información que rescatar | Diego |
| 2b | `Product Status`, `Product Image` | Constante (siempre 0) y enlaces a imágenes | Eliminar las columnas | No ayudan a distinguir un pedido de otro | Diego |
| 2c | `Customer Email`, `Customer Password`, `Customer Fname`, `Customer Lname`, `Customer Street` | Datos personales (el correo y la clave vienen enmascarados: `XXXXXXXXX`) | Eliminar las columnas | No explican el retraso y los datos personales no deben usarse en un modelo | Diego |
| 2d | `Order Profit Per Order`, `Sales per customer`, `Order Item Product Price` | Copias exactas de `Benefit per order`, `Order Item Total` y `Product Price` | Eliminar las copias | Repetir la misma información no aporta nada y genera multicolinealidad | Diego |
| 3 | `order date (DateOrders)` | Fecha guardada como texto (`mes/día/año hora:min`) | Convertir a fecha y crear `anio_pedido`, `mes_pedido` y `dia_semana_pedido` | Permite probar si el momento del pedido influye en el retraso | Diego |
| 4 | `Delivery Status`, `Days for shipping (real)`, `shipping date (DateOrders)` | Solo se conocen **después** de la entrega y reproducen el objetivo en el 97,5 % de las filas | No se borran, pero se excluyen del modelo | Usarlas sería *data leakage*. Se conservan para explicar el problema en el EDA. | Diego |
| 5 | Identificadores (`Order Id`, `Customer Id`, `Order Item Id`, `Product Card Id`, etc.) | Un valor distinto por fila o por cliente | Excluir del modelo | Un código no explica por qué un pedido llega tarde | Diego |
| 6 | Archivo `dataco.csv` | Viene en codificación latin-1, no en utf-8 | Leerlo con `encoding="latin-1"` | Con utf-8 la lectura falla por las tildes y caracteres especiales | Diego |

## Lo que no fue necesario hacer

- **Duplicados:** no se encontraron filas repetidas.
- **Nulos en `Customer Lname` y `Customer Zipcode`:** son muy pocos y esas columnas no entran al modelo, así que no se imputan.
- **Imputación en el modelo:** si llegara un nulo en las variables del modelo, el pipeline lo rellena con la mediana (numéricas) o la categoría más frecuente (categóricas), aprendiendo solo de los datos de entrenamiento.