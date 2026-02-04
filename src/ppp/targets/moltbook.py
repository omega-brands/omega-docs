"""Moltbook target stub (not implemented)."""

from typing import List, Dict, Any
from .base import TargetBase
from .mock import MockTarget


class MoltbookTarget(TargetBase):
    """
    Moltbook target stub.
    
    This target is not implemented. It exists as a placeholder for future implementation.
    All calls fall back to MockTarget.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.fallback = MockTarget(config)
        self.not_implemented = True

    def discover(self) -> List[Dict[str, Any]]:
        """Not implemented; falls back to mock."""
        return self.fallback.discover()

    def observe(self, target_id: str) -> Dict[str, Any]:
        """Not implemented; falls back to mock."""
        return self.fallback.observe(target_id)

    def participate(self, target_id: str, thread_id: str, draft_text: str) -> Dict[str, Any]:
        """Not implemented; falls back to mock."""
        return self.fallback.participate(target_id, thread_id, draft_text)
