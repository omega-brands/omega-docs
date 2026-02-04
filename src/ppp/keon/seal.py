"""Keon receipt sealing integration (default: noop)."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class IReceiptSealer(ABC):
    """Interface for receipt sealing."""

    @abstractmethod
    def seal(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Seal a receipt. Returns seal object or original data."""
        pass


class NoopSealer(IReceiptSealer):
    """No-op sealer (default behavior)."""

    def seal(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return receipt data unchanged."""
        return receipt_data


class KeonSealer(IReceiptSealer):
    """Keon sealing stub (not implemented)."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.not_implemented = True

    def seal(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Not implemented; returns data unchanged."""
        # In future, this would integrate with Keon governance
        return receipt_data
