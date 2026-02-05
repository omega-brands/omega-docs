#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Remediation Receipt Schemas

Immutable records for language remediation decisions and changes.
Part of WF_DOCS_REMEDIATION_GOVERNANCE_v1.

Schemas:
- RemediationSuggestion: Per-claim language suggestion
- RemediationRecord: Per-file audit/classification/policy evaluation record
- RemediationReceipt: Per-file change record (immutable, hashed)
- RemediationBatch: Aggregated batch summary
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime
import hashlib
import json


@dataclass
class RemediationSuggestion:
    """Suggested language change for a single guarantee claim."""
    claim_text: str
    claim_type: str  # Type A, B, C, D
    confidence: float  # 0.0-1.0
    suggested_replacement: str
    replacement_confidence: float
    line_number: int
    context_before: str
    context_after: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RemediationAuditRecord:
    """Phase 1 audit: file extraction with guarantee language context."""
    audit_id: str
    document_id: str
    directive_id: str  # C, G, K
    source_repo: str
    file_path: str
    file_hash_pre: str  # SHA256 of original
    guarantee_claims_found: int
    context_snippets: List[str]
    timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RemediationClassificationRecord:
    """Phase 2 classification: claim types + confidence."""
    classification_id: str
    audit_id: str
    document_id: str
    directive_id: str
    claim_count: int
    claims_by_type: Dict[str, int]  # {"Type A": 5, "Type B": 3, ...}
    confidence_distribution: Dict[str, int]  # {"0.95-1.0": 3, "0.70-0.94": 4, "<0.70": 1}
    suggested_remediations: List[RemediationSuggestion] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        data = asdict(self)
        data['suggested_remediations'] = [s.to_dict() for s in self.suggested_remediations]
        return data


@dataclass
class RemediationPolicyEvaluationRecord:
    """Phase 3 policy evaluation: fail-closed rule check."""
    evaluation_id: str
    classification_id: str
    document_id: str
    directive_id: str
    policy_decision: str  # PROCEED / REVIEW / BLOCK
    claims_proceeding: int  # Confidence 0.95+
    claims_requiring_review: int  # Confidence 0.70-0.94
    claims_blocked: int  # Confidence <0.70
    violated_rules: List[str]  # Rules that would block (if BLOCK decision)
    applicable_policy_rules: List[str]  # Rules applied
    confidence_distribution: Dict[str, int]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RemediationReceipt:
    """Phase 6: Immutable record of applied remediation change (or approval to change)."""
    receipt_id: str
    document_id: str
    directive_id: str  # C, G, K
    source_repo: str
    file_path: str
    source_classification_receipt_id: str  # Links back to Phase 4 categorization
    source_directive_id: str  # The directive that authorized remediation

    # Before state
    file_hash_pre: str  # SHA256 of original
    guarantee_claims_original: List[str]

    # Remediation approved/applied
    changes_approved: int  # Count of transformations approved
    changes_applied: int  # Count of transformations applied (0 if Phase 6 sealed, >0 if post-apply)
    changes_details: List[Dict] = field(default_factory=list)  # [{"old": "...", "new": "...", "confidence": 0.98}, ...]

    # After state
    file_hash_post: Optional[str] = None  # SHA256 of modified (populated post-apply)
    guarantee_claims_remaining: int = 0  # Should be 0 (populated post-apply)

    # Metadata
    authority: str = "User"
    phase: str = "6-remediation"  # Indicates Phase 6 evidence pack
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    receipt_hash: str = ""  # Populated at seal time

    def to_dict(self) -> dict:
        data = asdict(self)
        return data

    def compute_hash(self) -> str:
        """Compute deterministic SHA256 hash (immutable receipt)."""
        # Create canonical JSON representation
        canonical = {
            "receipt_id": self.receipt_id,
            "document_id": self.document_id,
            "directive_id": self.directive_id,
            "source_repo": self.source_repo,
            "file_path": self.file_path,
            "file_hash_pre": self.file_hash_pre,
            "file_hash_post": self.file_hash_post,
            "changes_approved": self.changes_approved,
            "changes_applied": self.changes_applied,
            "authority": self.authority,
            "timestamp": self.timestamp,
        }
        json_str = json.dumps(canonical, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(json_str.encode()).hexdigest()


@dataclass
class RemediationBatch:
    """Aggregated batch summary (per-directive or total)."""
    batch_id: str
    directive_id: str  # C, G, K, or "all"
    files_total: int
    files_proceeding: int
    files_requiring_review: int
    files_blocked: int

    # Approval status
    approved: bool = False
    approval_timestamp: Optional[str] = None
    approval_authority: str = "User"
    approval_rationale: str = ""

    # Evidence
    receipts: List[RemediationReceipt] = field(default_factory=list)

    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        data = asdict(self)
        data['receipts'] = [r.to_dict() for r in self.receipts]
        return data

    @property
    def approval_status(self) -> str:
        if self.approved:
            return f"APPROVED at {self.approval_timestamp}"
        return "PENDING"

    @property
    def completion_percentage(self) -> float:
        if self.files_total == 0:
            return 0.0
        approved_count = sum(1 for r in self.receipts if r.changes_applied > 0)
        return (approved_count / self.files_total) * 100
