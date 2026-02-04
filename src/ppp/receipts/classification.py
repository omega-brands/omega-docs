"""
Classification Receipt Schema for Documentation Governance Workflow.

This schema represents an immutable record of a document's classification
against the documentation placement policy. Each receipt documents:
- What the document claims to be (detected audience, claims, purpose)
- Where it currently lives (source repo and path)
- Where policy says it should live (target repo)
- What policy rules apply
- Classification decision (ALLOW/MITIGATE/DENY)

All receipts are deterministically hashed for auditability and replayability.

Doctrine: "Meaning follows placement. Placement follows governance."
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import json


@dataclass
class ClassificationReceipt:
    """
    Immutable record of a document's classification against placement policy.

    This receipt serves as:
    - Evidence of policy evaluation
    - Audit trail for classification decision
    - Replay-able classification point
    - Input to human decision gate (if MITIGATE/DENY)
    """

    # Identity (required)
    receipt_id: str                            # Unique receipt identifier
    workflow_id: str                           # Parent workflow ID
    document_id: str                           # Document being classified

    # Document Location & Metadata (required)
    source_repo: str                           # Current repository (omega-docs, etc.)
    source_path: str                           # Full path within repo
    document_name: str                         # Filename

    # Classification (required)
    detected_audience: str                     # public / internal / ambiguous

    # Policy Evaluation (required)
    target_repo: str                           # Where policy says doc should live
    policy_decision: str                       # ALLOW / MITIGATE / DENY

    # Defaults with factory functions
    detected_claims: List[str] = field(default_factory=list)  # claim types detected
    violated_rules: List[str] = field(default_factory=list)  # Rules violated

    # Optional metadata
    detected_purpose: Optional[str] = None     # Inferred purpose
    policy_rationale: Optional[str] = None     # Why this decision was made
    suggested_action: Optional[str] = None     # What to do if MITIGATE/DENY
    remediation_reason: Optional[str] = None   # Why remediation is needed

    # Policy Context (with defaults)
    policy_id: str = "docs-placement-policy"
    policy_version: str = "1.0.0"
    policy_enforcement_mode: str = "fail_closed"

    # Timestamp & Integrity (with defaults)
    timestamp: str = ""                        # ISO 8601 timestamp
    receipt_hash: str = ""                     # SHA256 of canonical JSON

    def __post_init__(self):
        """Validate and compute hash after initialization."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

        # Validate decision type
        if self.policy_decision not in ["ALLOW", "MITIGATE", "DENY"]:
            raise ValueError(f"Invalid policy_decision: {self.policy_decision}")

        # Validate repo names
        valid_repos = ["omega-docs", "omega-docs-internal", "keon-docs", "keon-docs-internal"]
        if self.source_repo not in valid_repos:
            raise ValueError(f"Invalid source_repo: {self.source_repo}")
        if self.target_repo not in valid_repos:
            raise ValueError(f"Invalid target_repo: {self.target_repo}")

        # Compute receipt hash
        self.receipt_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute canonical hash of this classification receipt."""
        from .schema import CanonicalSerializer

        canonical = CanonicalSerializer.canonical_json(self.to_dict_for_hashing())
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    def to_dict_for_hashing(self) -> Dict[str, Any]:
        """Get dict for hashing (excludes receipt_hash itself)."""
        d = asdict(self)
        d.pop('receipt_hash', None)  # Exclude the hash itself from hashing
        return d

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = value
        return result


@dataclass
class ClassificationBatch:
    """
    A batch of classification receipts from a single workflow execution.

    This represents one complete "sweep" of the codebase and is itself
    a receipted artifact.
    """

    batch_id: str                              # Unique batch identifier
    workflow_id: str                           # Parent workflow
    timestamp: str                             # When batch was finalized
    policy_id: str                             # Policy used
    policy_version: str                        # Policy version

    receipts: List[ClassificationReceipt] = field(default_factory=list)

    # Statistics
    total_documents: int = 0
    allow_count: int = 0
    mitigate_count: int = 0
    deny_count: int = 0

    # Repo breakdown
    repo_breakdown: Dict[str, int] = field(default_factory=dict)

    # Claim detection summary
    claims_detected: Dict[str, int] = field(default_factory=dict)

    # Batch-level summary
    batch_summary: Optional[str] = None
    batch_hash: str = ""

    def __post_init__(self):
        """Validate and compute batch hash."""
        # Compute statistics
        self.total_documents = len(self.receipts)
        self.allow_count = sum(1 for r in self.receipts if r.policy_decision == "ALLOW")
        self.mitigate_count = sum(1 for r in self.receipts if r.policy_decision == "MITIGATE")
        self.deny_count = sum(1 for r in self.receipts if r.policy_decision == "DENY")

        # Compute repo breakdown
        self.repo_breakdown = {}
        for receipt in self.receipts:
            self.repo_breakdown[receipt.source_repo] = self.repo_breakdown.get(receipt.source_repo, 0) + 1

        # Compute claims detected
        self.claims_detected = {}
        for receipt in self.receipts:
            for claim in receipt.detected_claims:
                self.claims_detected[claim] = self.claims_detected.get(claim, 0) + 1

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
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "total_documents": self.total_documents,
            "allow_count": self.allow_count,
            "mitigate_count": self.mitigate_count,
            "deny_count": self.deny_count,
            "repo_breakdown": self.repo_breakdown,
            "claims_detected": self.claims_detected,
            "receipts_count": len(self.receipts),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "batch_id": self.batch_id,
            "workflow_id": self.workflow_id,
            "timestamp": self.timestamp,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "total_documents": self.total_documents,
            "allow_count": self.allow_count,
            "mitigate_count": self.mitigate_count,
            "deny_count": self.deny_count,
            "repo_breakdown": self.repo_breakdown,
            "claims_detected": self.claims_detected,
            "batch_summary": self.batch_summary,
            "batch_hash": self.batch_hash,
            "receipts": [r.to_dict() for r in self.receipts],
        }

    def get_mitigations(self) -> List[ClassificationReceipt]:
        """Get all MITIGATE receipts (items needing human review)."""
        return [r for r in self.receipts if r.policy_decision == "MITIGATE"]

    def get_denials(self) -> List[ClassificationReceipt]:
        """Get all DENY receipts (policy violations)."""
        return [r for r in self.receipts if r.policy_decision == "DENY"]

    def get_by_repo(self, repo: str) -> List[ClassificationReceipt]:
        """Get all receipts from a specific source repo."""
        return [r for r in self.receipts if r.source_repo == repo]

    def get_by_decision(self, decision: str) -> List[ClassificationReceipt]:
        """Get all receipts with a specific policy decision."""
        return [r for r in self.receipts if r.policy_decision == decision]
