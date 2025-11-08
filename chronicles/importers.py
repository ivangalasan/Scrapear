"""Utilities to import structured data into the campaign engine."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, List

from .models import Event, Hero, Mission, Region


def _iter_payload(path: Path) -> Iterator[dict]:
    if path.suffix.lower() not in {".json"}:
        raise ValueError(f"Formato de archivo no soportado: {path.suffix}")
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, list):
        for item in payload:
            yield item
    else:
        yield payload


def load_regions(path: Path) -> List[Region]:
    return [Region.from_dict(item) for item in _iter_payload(path)]


def load_events(path: Path) -> List[Event]:
    return [Event.from_dict(item) for item in _iter_payload(path)]


def load_missions(path: Path) -> List[Mission]:
    return [Mission.from_dict(item) for item in _iter_payload(path)]


def load_heroes(path: Path) -> List[Hero]:
    return [Hero.from_dict(item) for item in _iter_payload(path)]


def import_all(engine, base_path: Path) -> None:
    """Import campaign artifacts from a directory.

    Expected structure::

        base_path/
            regions.json
            events.json
            missions.json
            heroes.json
    """

    base_path = Path(base_path)
    mapping = {
        "regions.json": (engine.import_regions, load_regions),
        "events.json": (engine.import_events, load_events),
        "missions.json": (engine.import_missions, load_missions),
        "heroes.json": (engine.register_hero, load_heroes),
    }
    for filename, (consumer, loader) in mapping.items():
        file_path = base_path / filename
        if file_path.exists():
            items = loader(file_path)
            if filename == "heroes.json":
                for hero in items:
                    consumer(hero)
            else:
                consumer(items)
