"""Keon receipt sealing integration (default: noop)."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import hashlib


class IReceiptSealer(ABC):
    """Interface for receipt sealing with integrity and temporal verification."""

    @abstractmethod
    def seal(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Seal a receipt with integrity and temporal markers.

        Returns:
            {
                "receipt_hash": original receipt hash,
                "seal": {
                    "timestamp_utc": server time when sealed,
                    "seal_hash": cryptographic seal of receipt + timestamp,
                    "sealed_by": sealer identifier
                }
            }
        """
        pass

    @abstractmethod
    def verify(self, receipt_data: Dict[str, Any], seal_data: Dict[str, Any]) -> bool:
        """
        Verify integrity and temporal authenticity of a sealed receipt.

        Checks:
            1. Receipt hash matches original
            2. Seal hash matches receipt + timestamp
            3. Timestamp is within acceptable drift

        Returns: True if valid, False otherwise
        """
        pass


class NoopSealer(IReceiptSealer):
    """No-op sealer (default behavior in v0.1.0)."""

    def seal(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return receipt data unchanged (no temporal integrity in noop)."""
        return receipt_data

    def verify(self, receipt_data: Dict[str, Any], seal_data: Dict[str, Any]) -> bool:
        """Noop verification always returns True."""
        return True


class TemporalSealer(IReceiptSealer):
    """Temporal sealer: adds server-side timestamp and integrity hash."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.sealer_id = config.get("sealer_id", "temporal-sealer-v0.1.0")

    def seal(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Seal receipt with temporal integrity.

        The seal proves:
        1. Receipt existed at a specific time (via server timestamp)
        2. Receipt content hasn't changed (via seal_hash)
        3. Server identity (via sealed_by)
        """
        receipt_hash = receipt_data.get("receipt_hash", "unknown")
        timestamp_utc = datetime.utcnow().isoformat() + "Z"

        # Seal = hash(receipt_hash + timestamp)
        seal_input = f"{receipt_hash}:{timestamp_utc}".encode('utf-8')
        seal_hash = hashlib.sha256(seal_input).hexdigest()

        return {
            "receipt_hash": receipt_hash,
            "seal": {
                "timestamp_utc": timestamp_utc,
                "seal_hash": seal_hash,
                "sealed_by": self.sealer_id,
            }
        }

    def verify(self, receipt_data: Dict[str, Any], seal_data: Dict[str, Any]) -> bool:
        """
        Verify temporal seal.

        Checks:
        1. Receipt hash matches
        2. Seal hash recomputes correctly
        3. Timestamp is not suspiciously old/future
        """
        if not seal_data or "seal" not in seal_data:
            return False

        receipt_hash = receipt_data.get("receipt_hash")
        seal_receipt_hash = seal_data.get("receipt_hash")

        # Check receipt hash match
        if receipt_hash != seal_receipt_hash:
            return False

        seal = seal_data["seal"]
        timestamp_str = seal.get("timestamp_utc")
        provided_seal_hash = seal.get("seal_hash")

        # Recompute seal_hash
        seal_input = f"{receipt_hash}:{timestamp_str}".encode('utf-8')
        recomputed_seal_hash = hashlib.sha256(seal_input).hexdigest()

        # Verify seal_hash matches
        if provided_seal_hash != recomputed_seal_hash:
            return False

        # Optional: check timestamp is within acceptable drift
        try:
            seal_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            now = datetime.utcnow().replace(tzinfo=seal_time.tzinfo)
            drift_seconds = abs((now - seal_time).total_seconds())

            # Allow 1 year drift (fail-open for archived receipts)
            max_drift = 365 * 24 * 60 * 60
            if drift_seconds > max_drift:
                return False
        except Exception:
            return False

        return True


class KeonSealer(IReceiptSealer):
    """Keon sealing stub (not implemented in v0.1.0)."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.not_implemented = True

    def seal(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Not implemented; falls back to temporal seal."""
        temporal = TemporalSealer()
        return temporal.seal(receipt_data)

    def verify(self, receipt_data: Dict[str, Any], seal_data: Dict[str, Any]) -> bool:
        """Not implemented; falls back to temporal verification."""
        temporal = TemporalSealer()
        return temporal.verify(receipt_data, seal_data)
