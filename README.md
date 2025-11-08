# Crónicas de la Tierra Media — Sistema de Gestión de Campaña

Aplicación base para gestionar campañas narrativas ambientadas en la Tierra
Media, inspirada en juegos como *La Guerra del Anillo*, *Viajes por la Tierra
Media*, *El Señor de los Anillos LCG* y *Earthborne Rangers*.

## Requisitos

- Python 3.10 o superior.
- `pip` para instalar dependencias (opcionalmente dentro de un entorno virtual).
- Dependencias listadas en `requirements.txt` (Typer, Flask y utilidades estándar).

### Preparación del entorno

1. Sitúate en la raíz del proyecto (la carpeta que contiene este README):

   ```bash
   cd Scrapear
   ```

2. (Opcional) Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows usa: .venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

Una vez hecho esto, ya puedes ejecutar tanto la CLI como la interfaz web desde la raíz del repositorio.

## Uso rápido

### Interfaz de línea de comandos (CLI)

La CLI está pensada para ejecutarse desde la raíz del proyecto. Puedes consultar la ayuda general con:

```bash
python -m chronicles.ui.cli --help
```

o bien:

```bash
python main.py --help
```

#### Importar datos iniciales

Carga el conjunto de datos de ejemplo que viene en `data/sample_import` (esto generará el archivo `data/campaign_state.json` si aún no existe):

```bash
python -m chronicles.ui.cli importar data/sample_import
```

#### Avanzar el día y activar eventos

```bash
python -m chronicles.ui.cli avanzar
```

#### Consultar el estado general de la campaña

```bash
python -m chronicles.ui.cli estado
```

### Interfaz web

La aplicación Flask también se ejecuta desde la raíz del proyecto. Iníciala con:

```bash
python -m chronicles.ui.web
```

Por defecto expondrá la web en `http://127.0.0.1:8000/`. Desde el panel principal podrás revisar regiones, héroes, misiones y el registro de campaña, además de avanzar el día con un botón.

### Ubicación de los datos

Los datos persistentes se guardan por defecto en `data/campaign_state.json`. Se incluye `data/sample_campaign.json` como referencia del formato completo que maneja la aplicación.

## Extensiones futuras

- Mejoras en la interfaz web (mapa interactivo, edición de entidades).
- Editor interno de eventos y misiones.
- Sincronización multijugador.
- Motor de generación procedural de encuentros.
