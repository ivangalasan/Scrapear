"""High level services orchestrating campaign operations."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from .models import (
    CampaignLogEntry,
    CampaignState,
    Event,
    Hero,
    Mission,
    MissionStatus,
    Region,
    RegionState,
)
from .storage import CampaignDataStore


class CampaignEngine:
    """Main entry-point that encapsulates the campaign rules."""

    def __init__(
        self,
        store: Optional[CampaignDataStore] = None,
        state: Optional[CampaignState] = None,
    ) -> None:
        if store is None and state is None:
            default_path = Path("data") / "campaign_state.json"
            store = CampaignDataStore(default_path)
        self._store = store
        self._state = state or (store.load() if store else CampaignState())

    @property
    def state(self) -> CampaignState:
        return self._state

    # ------------------------------------------------------------------
    # Time management
    # ------------------------------------------------------------------
    def advance_day(self) -> List[Event]:
        """Advance the campaign by one day and activate due events."""

        self._state.current_day += 1
        activated: List[Event] = []
        for event in self._state.events.values():
            if event.estado == "Programado" and event.dia_activacion == self._state.current_day:
                event.activate(self._state.current_day)
                activated.append(event)
                self._activate_event_on_regions(event)

        descripcion = "No se activaron eventos" if not activated else \
            "Se activaron: " + ", ".join(event.id for event in activated)
        self._state.append_log(
            CampaignLogEntry(
                dia=self._state.current_day,
                titulo="Avance del día",
                descripcion=descripcion,
                tags=["tiempo"],
            )
        )
        self._persist()
        return activated

    def schedule_event(self, event: Event) -> None:
        self._state.register_event(event)
        self._persist()

    # ------------------------------------------------------------------
    # Region management
    # ------------------------------------------------------------------
    def register_region(self, region: Region) -> None:
        self._state.register_region(region)
        self._persist()

    def update_region_state(self, region_name: str, state: RegionState) -> None:
        region = self._state.regions[region_name]
        region.update_state(state, self._state.current_day)
        self._persist()

    def register_hero(self, hero: Hero) -> None:
        self._state.register_hero(hero)
        self._persist()

    # ------------------------------------------------------------------
    # Mission management
    # ------------------------------------------------------------------
    def register_mission(self, mission: Mission) -> None:
        self._state.register_mission(mission)
        region = self._state.regions.get(mission.region)
        if region:
            region.register_mission(mission.id, self._state.current_day)
        self._persist()

    def update_mission_status(self, mission_id: str, status: MissionStatus) -> None:
        mission = self._state.missions[mission_id]
        mission.update_status(status)
        region = self._state.regions.get(mission.region)
        if region and status in {"Completada", "Fallada"}:
            outcome = "completada" if status == "Completada" else "fallada"
            region.resolve_mission(mission_id, self._state.current_day, outcome)
        self._state.append_log(
            CampaignLogEntry(
                dia=self._state.current_day,
                titulo=f"Misión {mission_id}",
                descripcion=f"Estado actualizado a {status}",
                tags=["misiones"],
            )
        )
        self._persist()

    # ------------------------------------------------------------------
    # Event resolution
    # ------------------------------------------------------------------
    def resolve_event(self, event_id: str, resultado: str, recompensa: Optional[str] = None) -> None:
        event = self._state.events[event_id]
        event.resolve(self._state.current_day, resultado)
        for region_name in event.ubicacion:
            region = self._state.regions.get(region_name)
            if region:
                region.resolve_event(event_id, self._state.current_day, resultado)
                if recompensa:
                    region.historial.append(
                        f"Día {self._state.current_day} - Recompensa obtenida: {recompensa}"
                    )
        self._state.append_log(
            CampaignLogEntry(
                dia=self._state.current_day,
                titulo=f"Evento {event_id}",
                descripcion=f"Resuelto: {resultado}",
                tags=["eventos"],
            )
        )
        self._persist()

    def ignore_event(self, event_id: str) -> None:
        event = self._state.events[event_id]
        event.ignore(self._state.current_day)
        self._state.append_log(
            CampaignLogEntry(
                dia=self._state.current_day,
                titulo=f"Evento {event_id}",
                descripcion="Ignorado por la compañía",
                tags=["eventos"],
            )
        )
        if event.consecuencia_si_ignorado:
            self._state.append_log(
                CampaignLogEntry(
                    dia=self._state.current_day,
                    titulo=f"Consecuencia {event.consecuencia_si_ignorado}",
                    descripcion="Se debe planificar su activación futura.",
                    tags=["eventos", "consecuencias"],
                )
            )
        self._persist()

    # ------------------------------------------------------------------
    # Log helpers
    # ------------------------------------------------------------------
    def log_decision(self, titulo: str, descripcion: str, tags: Optional[Sequence[str]] = None) -> None:
        self._state.append_log(
            CampaignLogEntry(
                dia=self._state.current_day,
                titulo=titulo,
                descripcion=descripcion,
                tags=list(tags or []),
            )
        )
        self._persist()

    # ------------------------------------------------------------------
    # Import helpers
    # ------------------------------------------------------------------
    def import_regions(self, regions: Iterable[Region]) -> None:
        for region in regions:
            self._state.register_region(region)
        self._persist()

    def import_events(self, events: Iterable[Event]) -> None:
        for event in events:
            self._state.register_event(event)
        self._persist()

    def import_missions(self, missions: Iterable[Mission]) -> None:
        for mission in missions:
            self.register_mission(mission)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _activate_event_on_regions(self, event: Event) -> None:
        for region_name in event.ubicacion:
            region = self._state.regions.get(region_name)
            if region:
                region.register_event(event.id, self._state.current_day)

    def _persist(self) -> None:
        if self._store:
            self._store.save(self._state)


def load_engine_from_path(path: Path) -> CampaignEngine:
    """Convenience helper used by UI front-ends."""

    store = CampaignDataStore(path)
    return CampaignEngine(store=store)
