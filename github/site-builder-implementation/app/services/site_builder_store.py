from __future__ import annotations

from typing import Dict

from .site_builder_state import SiteBuilderState


class InMemorySiteBuilderStore:
    def __init__(self) -> None:
        self._store: Dict[str, SiteBuilderState] = {}

    def get_state(self, session_id: str) -> SiteBuilderState:
        return self._store.get(session_id) or SiteBuilderState()

    def save_state(self, session_id: str, state: SiteBuilderState) -> None:
        self._store[session_id] = state

    def reset_state(self, session_id: str) -> None:
        self._store[session_id] = SiteBuilderState()
