"""Command line interface for the campaign manager."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from ..importers import import_all
from ..services import CampaignEngine, load_engine_from_path

app = typer.Typer(help="Crónicas de la Tierra Media — gestor de campaña")


def _resolve_engine(state_path: Optional[Path]) -> CampaignEngine:
    if state_path:
        return load_engine_from_path(state_path)
    return CampaignEngine()


@app.command()
def estado(state_path: Optional[Path] = typer.Option(None, help="Ruta al archivo de estado")) -> None:
    """Mostrar un resumen del estado actual de la campaña."""

    engine = _resolve_engine(state_path)
    state = engine.state
    typer.echo(f"Día actual: {state.current_day}")
    typer.echo("Regiones:")
    for region in state.regions.values():
        typer.echo(f"  - {region.nombre}: {region.estado} (Eventos: {', '.join(region.eventos_activos) or 'ninguno'})")
    typer.echo("Eventos programados:")
    for event in state.events.values():
        typer.echo(
            f"  - {event.id} ({event.tipo}) día {event.dia_activacion} — estado {event.estado}"
        )
    typer.echo("Misiones activas:")
    for mission in state.missions.values():
        typer.echo(f"  - {mission.id}: {mission.nombre} ({mission.estado}) en {mission.region}")


@app.command()
def avanzar(state_path: Optional[Path] = typer.Option(None, help="Ruta al archivo de estado")) -> None:
    """Avanzar un día en la campaña."""

    engine = _resolve_engine(state_path)
    activated = engine.advance_day()
    if activated:
        typer.echo("Eventos activados:")
        for event in activated:
            typer.echo(f"  - {event.id}: {event.descripcion}")
    else:
        typer.echo("No se activaron eventos en este día.")


@app.command()
def importar(
    directorio: Path = typer.Argument(..., exists=True, file_okay=False, help="Carpeta con archivos JSON"),
    state_path: Optional[Path] = typer.Option(None, help="Ruta al archivo de estado"),
) -> None:
    """Importar datos masivos generados externamente."""

    engine = _resolve_engine(state_path)
    import_all(engine, directorio)
    typer.echo("Datos importados correctamente.")


@app.command()
def log(
    titulo: str,
    descripcion: str,
    state_path: Optional[Path] = typer.Option(None, help="Ruta al archivo de estado"),
) -> None:
    """Añadir una entrada libre al registro de campaña."""

    engine = _resolve_engine(state_path)
    engine.log_decision(titulo=titulo, descripcion=descripcion)
    typer.echo("Entrada registrada.")


if __name__ == "__main__":
    app()
