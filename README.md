# Crónicas de la Tierra Media — Sistema de Gestión de Campaña

Aplicación base para gestionar campañas narrativas ambientadas en la Tierra
Media, inspirada en juegos como *La Guerra del Anillo*, *Viajes por la Tierra
Media*, *El Señor de los Anillos LCG* y *Earthborne Rangers*.

## Requisitos

- Python 3.10+
- [Typer](https://typer.tiangolo.com/) para la interfaz de línea de comandos.

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

## Uso rápido

El proyecto incluye una CLI accesible con:

```bash
python -m chronicles.ui.cli --help
```

o bien:

```bash
python main.py --help
```

### Importar datos iniciales

```bash
python -m chronicles.ui.cli importar data/sample_import
```

### Avanzar el día y activar eventos

```bash
python -m chronicles.ui.cli avanzar
```

### Consultar el estado general

```bash
python -m chronicles.ui.cli estado
```

Los datos se guardan por defecto en `data/campaign_state.json`. Se incluye
`data/sample_campaign.json` como referencia del formato completo que maneja la
aplicación.

## Extensiones futuras

- Interfaz visual (p. ej. Streamlit) reutilizando `CampaignEngine`.
- Editor interno de eventos y misiones.
- Sincronización multijugador.
- Motor de generación procedural de encuentros.
