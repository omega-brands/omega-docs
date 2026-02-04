"""
Human Decision Receipt Schema for Governed Remediation Workflows.

This schema represents an explicit human decision in a governed workflow.
It is non-delegable, immutable once recorded, and serves as the audit trail
for how humans exercise authority within governance constraints.

Doctrine: "Governance detects. Humans decide. Verification confirms. Receipts prove."
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
import hashlib
import json


class HumanDecisionType(Enum):
    """Valid human decision types."""
    ACCEPT = "ACCEPT"          # Accept proposed rewrite verbatim
    MODIFY = "MODIFY"          # Provide alternative rewrite
    REJECT = "REJECT"          # Decline remediation (requires rationale)


@dataclass
class HumanDecisionReceipt:
    """
    Immutable record of a human decision within a governed workflow.

    This receipt serves as:
    - Proof of human authority exercised
    - Audit trail for decision rationale
    - Replay-able decision point
    - Non-delegable accountability marker
    """

    # Identity
    decision_id: str                           # Unique decision identifier
    workflow_id: str                           # Parent workflow ID
    finding_id: str                            # Finding being decided upon

    # Decision
    decision_type: str                         # ACCEPT / MODIFY / REJECT
    authority: str                             # Human name or role (required)
    timestamp: str                             # ISO 8601 timestamp

    # Rationale
    rationale: Optional[str] = None            # Required if REJECT, optional otherwise
    context_notes: Optional[str] = None        # Additional context (optional)

    # Modified content (if MODIFY)
    modified_content: Optional[str] = None     # Human-provided alternative text

    # Policy context
    policy_id: str = "docs-governance-tone"
    policy_version: str = "1.0.0"

    # Original finding context (for audit trail)
    original_finding_location: str = ""        # file:line format
    original_finding_rule_id: str = ""
    original_finding_severity: str = ""

    # Governance
    fail_closed: bool = True                   # Decision was made under fail-closed policy

    # Hashing
    decision_hash: str = ""                    # SHA256 of canonical JSON (computed)

    def __post_init__(self):
        """Validate and compute hash after initialization."""
        if self.decision_type not in [d.value for d in HumanDecisionType]:
            raise ValueError(f"Invalid decision_type: {self.decision_type}")

        if self.decision_type == HumanDecisionType.REJECT.value and not self.rationale:
            raise ValueError("REJECT decisions require a rationale")

        if self.decision_type == HumanDecisionType.MODIFY.value and not self.modified_content:
            raise ValueError("MODIFY decisions require modified_content")

        if not self.authority or self.authority.strip() == "":
            raise ValueError("authority (human name/role) is required")

        # Compute decision hash
        self.decision_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute canonical hash of this decision."""
        from .schema import CanonicalSerializer

        canonical = CanonicalSerializer.canonical_json(self.to_dict_for_hashing())
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    def to_dict_for_hashing(self) -> Dict[str, Any]:
        """Get dict for hashing (excludes decision_hash itself)."""
        d = asdict(self)
        d.pop('decision_hash', None)  # Exclude the hash itself from hashing
        return d

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result

    @staticmethod
    def validate_batch(decisions: list) -> bool:
        """Validate a batch of decisions for consistency."""
        if not decisions:
            return True

        # Check that all decisions have same workflow_id
        workflow_ids = set(d.workflow_id for d in decisions)
        if len(workflow_ids) > 1:
            raise ValueError(f"Mixed workflow IDs in batch: {workflow_ids}")

        # Check that finding_ids are unique
        finding_ids = [d.finding_id for d in decisions]
        if len(finding_ids) != len(set(finding_ids)):
            raise ValueError("Duplicate finding_ids in decision batch")

        return True


@dataclass
class HumanDecisionBatch:
    """
    A batch of related human decisions from a single decision gate.

    This represents one "round" of human decision-making and is itself
    a receipted artifact.
    """

    batch_id: str                              # Unique batch identifier
    workflow_id: str                           # Parent workflow
    timestamp: str                             # When batch was finalized
    authority: str                             # Who made these decisions
    decisions: list = field(default_factory=list)  # List of HumanDecisionReceipt

    # Statistics
    accept_count: int = 0
    modify_count: int = 0
    reject_count: int = 0

    # Batch-level rationale
    batch_rationale: Optional[str] = None      # High-level summary of decisions

    batch_hash: str = ""                       # SHA256 of batch

    def __post_init__(self):
        """Validate and compute batch hash."""
        HumanDecisionReceipt.validate_batch(self.decisions)

        # Compute statistics
        self.accept_count = sum(1 for d in self.decisions if d.decision_type == "ACCEPT")
        self.modify_count = sum(1 for d in self.decisions if d.decision_type == "MODIFY")
        self.reject_count = sum(1 for d in self.decisions if d.decision_type == "REJECT")

        self.batch_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute canonical hash of entire batch."""
        from .schema import CanonicalSerializer

        canonical = CanonicalSerializer.canonical_json(self.to_dict_for_hashing())
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    def to_dict_for_hashing(self) -> Dict[str, Any]:
        """Get dict for hashing."""
        return {
            "batch_id": self.batch_id,
            "workflow_id": self.workflow_id,
            "timestamp": self.timestamp,
            "authority": self.authority,
            "decisions": [d.to_dict_for_hashing() for d in self.decisions],
            "accept_count": self.accept_count,
            "modify_count": self.modify_count,
            "reject_count": self.reject_count,
            "batch_rationale": self.batch_rationale,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "batch_id": self.batch_id,
            "workflow_id": self.workflow_id,
            "timestamp": self.timestamp,
            "authority": self.authority,
            "decisions": [d.to_dict() for d in self.decisions],
            "accept_count": self.accept_count,
            "modify_count": self.modify_count,
            "reject_count": self.reject_count,
            "batch_rationale": self.batch_rationale,
            "batch_hash": self.batch_hash,
        }
