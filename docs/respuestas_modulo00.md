# Respuestas Módulo 00: Entornos con uv

## Paso 2: Revisar lo que se generó

**1. ¿Qué versión exacta de pandas quedó en uv.lock? ¿Qué rango quedó en pyproject.toml?**
En uv.lock quedó la versión exacta 3.1.0. En pyproject.toml quedó el rango `pandas>=3.1.0`, es decir, cualquier versión igual o mayor a 3.1.0.

**2. ¿Cuántos paquetes hay en uv.lock? ¿Por qué son muchos más que los que instalé?**
Hay 120 paquetes, aunque instalé solo 9 (7 principales y 2 de desarrollo). Cada librería depende de otras: por ejemplo, pandas necesita numpy y python-dateutil, y jupyter trae decenas de paquetes. uv.lock guarda todas esas dependencias con su versión exacta.

**3. ¿Qué pasa si borro .venv/ y ejecuto uv run python -c "import pandas"?**
uv detecta que no existe el entorno, lo vuelve a crear automáticamente ("Creating virtual environment at: .venv"), instala los 117 paquetes según uv.lock en unos 3 segundos y el import funciona. Por eso .venv no es necesario compartirlo.

## Paso 3: Reproducibilidad
Trabajé de forma individual, así que copié el proyecto a otra carpeta (prueba-copia), borré su .venv y ejecuté `uv sync`. En las dos carpetas obtuve las mismas versiones: pandas 3.1.0 y scikit-learn 1.9.1.

## Preguntas para la plenaria

**¿Por qué .venv/ no se comparte pero uv.lock sí?**
.venv pesa cientos de MB, depende del sistema operativo y se puede recrear en segundos con `uv sync`. uv.lock es liviano y contiene la "receta" exacta de versiones para que cualquier persona obtenga el mismo entorno.

**¿Qué error me salió y cómo lo resolví?**
Al clonar el repositorio, PowerShell no reconocía el comando `git` porque no lo tenía instalado. Lo instalé con `winget install --id Git.Git -e --source winget`, cerré y volví a abrir la terminal, y funcionó.

**¿Qué ventaja tiene uv frente a pip install global?**
Cada proyecto tiene su propio entorno con versiones fijas, y cualquiera puede reproducirlo exactamente con un solo comando (`uv sync`), sin conflictos entre proyectos.