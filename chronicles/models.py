"""Domain models for the Crónicas de la Tierra Media campaign manager."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Literal, Optional

RegionState = Literal["Estabilizada", "Amenazada", "Corrompida", "Aliada"]
EventType = Literal["Local", "Global"]
EventStatus = Literal["Programado", "Activo", "Resuelto", "Ignorado"]
MissionStatus = Literal["Pendiente", "En progreso", "Completada", "Fallada"]
HeroState = Literal["Sano", "Herido", "Agotado", "Derrotado"]


@dataclass
class CampaignLogEntry:
    """Chronological entry representing a relevant campaign event."""

    dia: int
    titulo: str
    descripcion: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "CampaignLogEntry":
        return cls(
            dia=int(data.get("dia", 0)),
            titulo=data.get("titulo", ""),
            descripcion=data.get("descripcion", ""),
            tags=list(data.get("tags", [])),
        )


@dataclass
class Region:
    """Representation of a map region and its current status."""

    nombre: str
    estado: RegionState = "Estabilizada"
    eventos_activos: List[str] = field(default_factory=list)
    misiones_activas: List[str] = field(default_factory=list)
    historial: List[str] = field(default_factory=list)

    def register_event(self, event_id: str, dia: int) -> None:
        if event_id not in self.eventos_activos:
            self.eventos_activos.append(event_id)
        self.historial.append(f"Día {dia} - Se activó {event_id}")

    def resolve_event(self, event_id: str, dia: int, outcome: str) -> None:
        if event_id in self.eventos_activos:
            self.eventos_activos.remove(event_id)
        self.historial.append(f"Día {dia} - {event_id} {outcome}")

    def update_state(self, nuevo_estado: RegionState, dia: Optional[int] = None) -> None:
        if nuevo_estado != self.estado:
            self.estado = nuevo_estado
            if dia is not None:
                self.historial.append(f"Día {dia} - Región marcada como {nuevo_estado}")

    def register_mission(self, mission_id: str, dia: int) -> None:
        if mission_id not in self.misiones_activas:
            self.misiones_activas.append(mission_id)
            self.historial.append(f"Día {dia} - Se activó misión {mission_id}")

    def resolve_mission(self, mission_id: str, dia: int, outcome: str) -> None:
        if mission_id in self.misiones_activas:
            self.misiones_activas.remove(mission_id)
        self.historial.append(f"Día {dia} - Misión {mission_id} {outcome}")

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Region":
        return cls(
            nombre=data.get("nombre", ""),
            estado=data.get("estado", "Estabilizada"),
            eventos_activos=list(data.get("eventos_activos", [])),
            misiones_activas=list(data.get("misiones_activas", [])),
            historial=list(data.get("historial", [])),
        )


@dataclass
class Event:
    """Represents a story event that can affect the campaign."""

    id: str
    tipo: EventType
    dia_activacion: int
    ubicacion: List[str]
    descripcion: str
    efecto: str
    consecuencia_si_ignorado: Optional[str] = None
    recompensa_si_resuelto: Optional[str] = None
    cartas_LCG: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    estado: EventStatus = "Programado"
    historial: List[str] = field(default_factory=list)

    def activate(self, dia: int) -> None:
        self.estado = "Activo"
        self.historial.append(f"Día {dia} - Evento activado")

    def resolve(self, dia: int, resultado: str) -> None:
        self.estado = "Resuelto"
        self.historial.append(f"Día {dia} - Resultado: {resultado}")

    def ignore(self, dia: int) -> None:
        self.estado = "Ignorado"
        self.historial.append(f"Día {dia} - Evento ignorado")

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Event":
        return cls(
            id=data.get("id", ""),
            tipo=data.get("tipo", "Local"),
            dia_activacion=int(data.get("dia_activacion", 0)),
            ubicacion=list(data.get("ubicacion", [])),
            descripcion=data.get("descripcion", ""),
            efecto=data.get("efecto", ""),
            consecuencia_si_ignorado=data.get("consecuencia_si_ignorado"),
            recompensa_si_resuelto=data.get("recompensa_si_resuelto"),
            cartas_LCG=list(data.get("cartas_LCG", [])),
            tags=list(data.get("tags", [])),
            estado=data.get("estado", "Programado"),
            historial=list(data.get("historial", [])),
        )


@dataclass
class Mission:
    """Represents an active or scheduled mission."""

    id: str
    nombre: str
    region: str
    estado: MissionStatus = "Pendiente"
    objetivos: List[str] = field(default_factory=list)
    cartas_LCG_usadas: List[str] = field(default_factory=list)
    recompensas: List[str] = field(default_factory=list)
    desencadenada_por: Optional[str] = None

    def update_status(self, nuevo_estado: MissionStatus) -> None:
        self.estado = nuevo_estado

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Mission":
        return cls(
            id=data.get("id", ""),
            nombre=data.get("nombre", ""),
            region=data.get("region", ""),
            estado=data.get("estado", "Pendiente"),
            objetivos=list(data.get("objetivos", [])),
            cartas_LCG_usadas=list(data.get("cartas_LCG_usadas", [])),
            recompensas=list(data.get("recompensas", [])),
            desencadenada_por=data.get("desencadenada_por"),
        )


@dataclass
class Hero:
    """Represents a hero participating in the campaign."""

    nombre: str
    clase: str
    cartas_vinculadas: List[str] = field(default_factory=list)
    aliados: List[str] = field(default_factory=list)
    estado: HeroState = "Sano"
    historial: List[str] = field(default_factory=list)

    def log(self, dia: int, descripcion: str) -> None:
        self.historial.append(f"Día {dia} - {descripcion}")

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Hero":
        return cls(
            nombre=data.get("nombre", ""),
            clase=data.get("clase", ""),
            cartas_vinculadas=list(data.get("cartas_vinculadas", [])),
            aliados=list(data.get("aliados", [])),
            estado=data.get("estado", "Sano"),
            historial=list(data.get("historial", [])),
        )


@dataclass
class CampaignState:
    """Complete snapshot of the campaign progression."""

    current_day: int = 0
    regions: Dict[str, Region] = field(default_factory=dict)
    events: Dict[str, Event] = field(default_factory=dict)
    missions: Dict[str, Mission] = field(default_factory=dict)
    heroes: Dict[str, Hero] = field(default_factory=dict)
    log: List[CampaignLogEntry] = field(default_factory=list)

    def register_region(self, region: Region) -> None:
        self.regions[region.nombre] = region

    def register_event(self, event: Event) -> None:
        self.events[event.id] = event

    def register_mission(self, mission: Mission) -> None:
        self.missions[mission.id] = mission

    def register_hero(self, hero: Hero) -> None:
        self.heroes[hero.nombre] = hero

    def append_log(self, entry: CampaignLogEntry) -> None:
        self.log.append(entry)

    def to_dict(self) -> Dict:
        return {
            "current_day": self.current_day,
            "regions": {key: region.to_dict() for key, region in self.regions.items()},
            "events": {key: event.to_dict() for key, event in self.events.items()},
            "missions": {key: mission.to_dict() for key, mission in self.missions.items()},
            "heroes": {key: hero.to_dict() for key, hero in self.heroes.items()},
            "log": [entry.to_dict() for entry in self.log],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "CampaignState":
        regions = {name: Region.from_dict(region) for name, region in data.get("regions", {}).items()}
        events = {event_id: Event.from_dict(event) for event_id, event in data.get("events", {}).items()}
        missions = {mission_id: Mission.from_dict(mission) for mission_id, mission in data.get("missions", {}).items()}
        heroes = {hero_name: Hero.from_dict(hero) for hero_name, hero in data.get("heroes", {}).items()}
        log = [CampaignLogEntry.from_dict(entry) for entry in data.get("log", [])]
        return cls(
            current_day=int(data.get("current_day", 0)),
            regions=regions,
            events=events,
            missions=missions,
            heroes=heroes,
            log=log,
        )
