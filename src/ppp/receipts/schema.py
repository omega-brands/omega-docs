"""Receipt schema and deterministic canonicalization."""

import json
import hashlib
from dataclasses import dataclass, asdict
from typing import Any, Dict
from datetime import datetime


@dataclass
class Receipt:
    """PPP Receipt structure."""
    receipt_id: str
    run_id: str
    agent_id: str
    timestamp: str
    event: str
    phase: str
    status: str
    input_hash: str
    output_hash: str
    receipt_hash: str
    policy: Dict[str, Any]
    decision: Dict[str, Any]
    artifacts: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    failure_stage: str = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


class CanonicalSerializer:
    """Deterministic JSON canonicalization for PPP receipts."""

    VERSION = "1.0"

    @staticmethod
    def _normalize_value(value: Any) -> Any:
        """Normalize a value for canonical serialization."""
        if isinstance(value, dict):
            # Sort keys and normalize values
            return {k: CanonicalSerializer._normalize_value(value[k])
                    for k in sorted(value.keys())}
        elif isinstance(value, list):
            # Normalize list items but preserve order (don't sort)
            return [CanonicalSerializer._normalize_value(item) for item in value]
        elif isinstance(value, float):
            # Store floats as fixed-precision strings to avoid cross-platform drift
            # Format: multiply by 1,000,000 to avoid scientific notation for small numbers
            if value == 0.0:
                return "0.0"
            elif value % 1 == 0:
                # Whole number: store as string representation
                return f"{int(value)}.0"
            else:
                # Fractional: store with 15 decimal places (IEEE 754 precision)
                return "{:.15f}".format(value).rstrip('0')
        elif isinstance(value, bool):
            # Ensure booleans are lowercase
            return value
        elif value is None:
            return None
        else:
            # Convert to string for other types
            return str(value)

    @staticmethod
    def canonical_json(obj: Dict[str, Any]) -> str:
        """Serialize object to canonical JSON."""
        normalized = CanonicalSerializer._normalize_value(obj)
        # Use separators without spaces, sort keys
        return json.dumps(normalized, separators=(',', ':'), sort_keys=True, ensure_ascii=True)

    @staticmethod
    def hash_payload(obj: Dict[str, Any]) -> str:
        """Generate SHA256 hash of canonical payload."""
        canonical = CanonicalSerializer.canonical_json(obj)
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    @staticmethod
    def create_receipt(
        receipt_id: str,
        run_id: str,
        agent_id: str,
        event: str,
        phase: str,
        status: str,
        policy: Dict[str, Any],
        decision: Dict[str, Any],
        input_payload: Dict[str, Any] = None,
        output_payload: Dict[str, Any] = None,
        artifacts: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
        failure_stage: str = None,
    ) -> Receipt:
        """Create a new receipt with deterministic hashing."""
        
        # Generate hashes
        input_hash = CanonicalSerializer.hash_payload(input_payload or {})
        output_hash = CanonicalSerializer.hash_payload(output_payload or {})
        
        # Build receipt payload (excluding timestamp from hash)
        receipt_payload = {
            "receipt_id": receipt_id,
            "run_id": run_id,
            "agent_id": agent_id,
            "event": event,
            "phase": phase,
            "status": status,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "policy": policy,
            "decision": decision,
        }
        
        if artifacts:
            receipt_payload["artifacts"] = artifacts
        if metadata:
            receipt_payload["metadata"] = metadata
        if failure_stage:
            receipt_payload["failure_stage"] = failure_stage
        
        # Generate receipt hash (deterministic, excludes timestamp)
        receipt_hash = CanonicalSerializer.hash_payload(receipt_payload)
        
        # Create receipt with timestamp
        receipt = Receipt(
            receipt_id=receipt_id,
            run_id=run_id,
            agent_id=agent_id,
            timestamp=datetime.utcnow().isoformat() + "Z",
            event=event,
            phase=phase,
            status=status,
            input_hash=input_hash,
            output_hash=output_hash,
            receipt_hash=receipt_hash,
            policy=policy,
            decision=decision,
            artifacts=artifacts,
            metadata=metadata,
            failure_stage=failure_stage,
        )
        
        return receipt

    @staticmethod
    def verify_receipt_hash(receipt: Receipt) -> bool:
        """Verify that receipt hash is correct (deterministic)."""
        receipt_dict = receipt.to_dict()
        # Remove timestamp and hash for verification
        receipt_dict.pop("timestamp", None)
        receipt_dict.pop("receipt_hash", None)
        
        recomputed_hash = CanonicalSerializer.hash_payload(receipt_dict)
        return recomputed_hash == receipt.receipt_hash
