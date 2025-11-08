# Crónicas de la Tierra Media — Arquitectura Base

Este documento resume la estructura inicial del sistema de gestión de campaña.

## Paquete `chronicles`

El núcleo de la aplicación se encuentra en el paquete `chronicles` y está
organizado en capas:

- `chronicles.models`: define las entidades principales (`Region`, `Event`,
  `Mission`, `Hero`) y la estructura agregada `CampaignState`. Las clases usan
  `dataclasses` para facilitar la serialización a JSON y poder ampliarse con
  nuevos atributos sin romper la compatibilidad.
- `chronicles.storage`: provee la clase `CampaignDataStore`, responsable de
  persistir un `CampaignState` en disco. Almacena los datos en formato JSON
  legible por otras herramientas (incluidas IAs externas).
- `chronicles.services`: contiene `CampaignEngine`, servicio de alto nivel que
  implementa reglas de negocio como avanzar el día, activar eventos, actualizar
  misiones y registrar decisiones.
- `chronicles.importers`: utilidades para cargar datos masivos (regiones,
  eventos, misiones, héroes) generados por otras herramientas o IAs.
- `chronicles.ui.cli`: interfaz de línea de comandos basada en Typer que expone
  comandos esenciales (`estado`, `avanzar`, `importar`, `log`).

## Datos de ejemplo

- `data/campaign_state.json`: se crea automáticamente al ejecutar comandos si no
  existe. Se incluye `data/sample_campaign.json` como ejemplo de estructura.
- `data/sample_import/`: carpeta con archivos JSON separados por tipo de entidad
  listos para ser importados con `python -m chronicles.ui.cli importar data/sample_import`.

## Flujo principal

1. **Importar o crear datos** con la CLI (`importar`).
2. **Avanzar el día** con `avanzar`, lo que activa eventos según su
   `dia_activacion` y registra lo ocurrido en el log global.
3. **Consultar estado** con `estado`, que resume mapa, eventos y misiones.
4. **Registrar decisiones** puntuales con `log` para mantener el diario de la
   campaña.

Esta base está pensada para crecer hacia una interfaz visual (p. ej. Streamlit)
reutilizando `CampaignEngine` como capa de dominio.
