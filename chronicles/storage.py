"""Persistence helpers for campaign state."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import CampaignState


class CampaignDataStore:
    """Handles serialization of campaign state to JSON files."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        if self.path.parent and not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> CampaignState:
        if not self.path.exists():
            return CampaignState()
        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return CampaignState.from_dict(data)

    def save(self, state: CampaignState) -> None:
        serialized = state.to_dict()
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(serialized, f, ensure_ascii=False, indent=2)


def load_campaign(path: Optional[Path] = None) -> CampaignState:
    """Utility function returning a campaign state from disk."""

    path = path or Path("data") / "campaign_state.json"
    store = CampaignDataStore(path)
    return store.load()
