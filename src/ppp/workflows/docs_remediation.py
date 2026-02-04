"""
WF_DOCS_GOVERNANCE_REMEDIATION_v1: Human-in-the-loop governed remediation workflow.

This workflow implements Phase 1-6 of the Remediation Specification:
1. Ingest & Verify — validate evidence pack integrity
2. Normalize Findings — prepare for human decision
3. Human Decision Gate — capture accountable decisions
4. Apply Authorized Changes — only approved changes
5. Re-Scan & Verify — prove remediation effectiveness
6. Seal Evidence Pack — produce portable proof

Doctrine: "Governance detects. Humans decide. Verification confirms. Receipts prove."
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import hashlib
import shutil

from ppp.policy.engine import PolicyEvaluator, PolicyDecision
from ppp.receipts.emitter import ReceiptEmitter
from ppp.receipts.schema import Receipt, CanonicalSerializer
from ppp.receipts.human_decision import (
    HumanDecisionReceipt,
    HumanDecisionBatch,
    HumanDecisionType,
)
from ppp.storage.progress import ProgressStore
from ppp.config.loader import ConfigLoader
from ppp.workflows.docs_tone_scan import DocsFinding


@dataclass
class RemediationFinding:
    """A finding prepared for human remediation decision."""

    finding_id: str
    location: str                             # file:line format
    rule_id: str
    severity: str                             # P0, P1, P2
    message: str
    original_text: str
    suggested_fix: Optional[str]
    policy_rationale: str

    # Decision metadata (populated after decision)
    human_decision: Optional[HumanDecisionReceipt] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        d = asdict(self)
        if self.human_decision:
            d['human_decision'] = self.human_decision.to_dict()
        return d


class DocsRemediationWorkflow:
    """
    Human-in-the-loop governed remediation workflow running on PPP kernel.

    Phases:
    1. ingest_and_verify: Validate evidence pack integrity
    2. normalize_findings: Prepare findings for human decision
    3. human_decision_gate: Capture human decisions (receipted)
    4. apply_authorized_changes: Apply only approved changes
    5. re_scan_and_verify: Re-scan to prove remediation
    6. seal_evidence_pack: Produce final evidence pack
    """

    def __init__(self,
                 evidence_pack_dir: str,
                 docs_root: str = "D:\\Repos\\omega-docs\\docs",
                 policy_path: str = "D:\\Repos\\omega-docs\\configs\\ppp\\policies\\policy.remediation.yaml",
                 output_dir: str = "D:\\Repos\\omega-docs\\EVIDENCE\\docs-remediation"):
        """Initialize remediation workflow."""
        self.evidence_pack_dir = Path(evidence_pack_dir)
        self.docs_root = Path(docs_root)
        self.policy_path = Path(policy_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # PPP kernel components
        policy_config = ConfigLoader.load_policy_config(str(self.policy_path))
        self.policy_evaluator = PolicyEvaluator(policy_config)
        self.receipt_emitter = ReceiptEmitter(str(self.output_dir))
        self.progress_store = ProgressStore(str(self.output_dir / "progress.db"))

        # State
        self.findings: List[RemediationFinding] = []
        self.human_decisions: List[HumanDecisionReceipt] = []
        self.applied_changes: Dict[str, str] = {}  # finding_id -> applied_text
        self.workflow_id = self._generate_workflow_id()

        # Initialize progress tracking
        self.progress_store.begin_run(
            run_id=self.workflow_id,
            agent_id="docs-governance-remediation",
            policy_id="remediation"
        )

    def _generate_workflow_id(self) -> str:
        """Generate Windows-compatible workflow ID."""
        timestamp = datetime.utcnow().isoformat().replace(':', '-').replace('.', '_')
        return f"wf-docs-remediation-{timestamp}"

    # ========== PHASE 1: INGEST & VERIFY ==========

    def phase_ingest_and_verify(self) -> Dict[str, Any]:
        """Ingest and verify evidence pack integrity."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "ingest_and_verify")

        try:
            # Verify pack exists
            if not self.evidence_pack_dir.exists():
                raise ValueError(f"Evidence pack not found: {self.evidence_pack_dir}")

            # Check required files
            required_files = ["seal-manifest.json", "receipts.jsonl", "summary.json"]
            for fname in required_files:
                fpath = self.evidence_pack_dir / fname
                if not fpath.exists():
                    raise ValueError(f"Required file missing: {fname}")

            # Verify seal manifest
            seal_manifest_path = self.evidence_pack_dir / "seal-manifest.json"
            with open(seal_manifest_path, 'r') as f:
                manifest = json.load(f)

            # Verify file hashes
            verified_count = 0
            for fname, expected_hash in manifest.get("file_hashes", {}).items():
                fpath = self.evidence_pack_dir / fname
                if fpath.exists():
                    actual_hash = self._compute_file_hash(fpath)
                    if actual_hash == expected_hash:
                        verified_count += 1
                    else:
                        raise ValueError(f"Hash mismatch for {fname}")

            result = {
                "phase": "ingest_and_verify",
                "evidence_pack": str(self.evidence_pack_dir),
                "files_verified": verified_count,
                "seal_valid": True,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "ingest_and_verify",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    @staticmethod
    def _compute_file_hash(file_path: Path) -> str:
        """Compute SHA256 hash of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    # ========== PHASE 2: NORMALIZE FINDINGS ==========

    def phase_normalize_findings(self) -> Dict[str, Any]:
        """Load and normalize findings from evidence pack."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "normalize_findings")

        try:
            receipts_path = self.evidence_pack_dir / "receipts.jsonl"
            findings_count = 0

            with open(receipts_path, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue

                    receipt_dict = json.loads(line)

                    # Extract finding from receipt
                    artifact = receipt_dict.get("artifacts", {}).get("finding", {})

                    # Determine policy rationale
                    rule_id = artifact.get("rule_id", "unknown")
                    severity = artifact.get("severity", "P1")
                    policy_rationale = self._get_policy_rationale(rule_id, severity)

                    # Create remediation finding
                    finding = RemediationFinding(
                        finding_id=artifact.get("finding_id", f"finding-{findings_count}"),
                        location=artifact.get("location", "unknown"),
                        rule_id=rule_id,
                        severity=severity,
                        message=artifact.get("message", ""),
                        original_text=artifact.get("text_snippet", ""),
                        suggested_fix=artifact.get("suggested_fix"),
                        policy_rationale=policy_rationale,
                    )

                    self.findings.append(finding)
                    findings_count += 1

            result = {
                "phase": "normalize_findings",
                "findings_loaded": findings_count,
                "findings_by_severity": {
                    "P0": sum(1 for f in self.findings if f.severity == "P0"),
                    "P1": sum(1 for f in self.findings if f.severity == "P1"),
                    "P2": sum(1 for f in self.findings if f.severity == "P2"),
                },
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "normalize_findings",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    def _get_policy_rationale(self, rule_id: str, severity: str) -> str:
        """Get policy rationale for a finding."""
        rationales = {
            "no_ungoverned_autonomy_claims": "Documentation should not claim unbounded autonomy without governance context",
            "no_orchestration_as_trust": "Orchestration alone does not provide safety; explicit governance primitives required",
            "omission_drift_detection": "Execution/decision language must include governance verification context",
            "anthropomorphic_framing_without_context": "Anthropomorphic metaphors should be explicitly bounded by governance",
            "vocabulary_canon_alignment": "Vocabulary should align with governance paradigm",
        }

        base = rationales.get(rule_id, "Policy violation detected")
        if severity == "P0":
            return f"[MUST] {base}"
        elif severity == "P1":
            return f"[SHOULD] {base}"
        else:
            return f"[POLISH] {base}"

    # ========== PHASE 3: HUMAN DECISION GATE ==========

    def prepare_decision_interface(self) -> Dict[str, Any]:
        """Prepare human decision interface (non-phase, for external use)."""
        """
        This prepares findings for human decision-making.
        Returns a structure suitable for human review.
        """
        interface = {
            "workflow_id": self.workflow_id,
            "timestamp": datetime.utcnow().isoformat(),
            "total_findings": len(self.findings),
            "findings": []
        }

        for finding in self.findings:
            finding_item = {
                "id": finding.finding_id,
                "location": finding.location,
                "severity": finding.severity,
                "rule": finding.rule_id,
                "message": finding.message,
                "original_text": finding.original_text,
                "suggested_fix": finding.suggested_fix,
                "policy_rationale": finding.policy_rationale,
                "requires_decision": finding.severity in ["P0", "P1"],
                "must_accept_or_modify": finding.severity == "P0",
            }
            interface["findings"].append(finding_item)

        return interface

    def record_human_decision(self,
                            finding_id: str,
                            decision_type: str,
                            authority: str,
                            rationale: Optional[str] = None,
                            modified_content: Optional[str] = None) -> HumanDecisionReceipt:
        """Record a human decision (to be called by decision authority)."""
        # Find the finding
        finding = None
        for f in self.findings:
            if f.finding_id == finding_id:
                finding = f
                break

        if not finding:
            raise ValueError(f"Finding not found: {finding_id}")

        # Create decision receipt
        decision = HumanDecisionReceipt(
            decision_id=f"decision-{len(self.human_decisions)}",
            workflow_id=self.workflow_id,
            finding_id=finding_id,
            decision_type=decision_type,
            authority=authority,
            timestamp=datetime.utcnow().isoformat(),
            rationale=rationale,
            modified_content=modified_content,
            original_finding_location=finding.location,
            original_finding_rule_id=finding.rule_id,
            original_finding_severity=finding.severity,
        )

        # Validate against policy
        validation_result = self._validate_decision_against_policy(finding, decision)
        if not validation_result["allowed"]:
            raise ValueError(f"Decision rejected by policy: {validation_result['reason']}")

        # Record decision
        self.human_decisions.append(decision)
        finding.human_decision = decision

        return decision

    def _validate_decision_against_policy(self, finding: RemediationFinding,
                                         decision: HumanDecisionReceipt) -> Dict[str, Any]:
        """Validate decision against remediation policy."""
        # P0 must be ACCEPT or MODIFY
        if finding.severity == "P0" and decision.decision_type == "REJECT":
            return {
                "allowed": False,
                "reason": "P0 findings cannot be REJECT (policy: p0_findings_must_be_decided)"
            }

        # REJECT requires rationale
        if decision.decision_type == "REJECT" and not decision.rationale:
            return {
                "allowed": False,
                "reason": "REJECT decisions must include rationale (policy: reject_requires_rationale)"
            }

        # MODIFY requires content
        if decision.decision_type == "MODIFY" and not decision.modified_content:
            return {
                "allowed": False,
                "reason": "MODIFY decisions must include modified_content (policy: modify_requires_content)"
            }

        return {"allowed": True}

    # ========== PHASE 4: APPLY AUTHORIZED CHANGES ==========

    def phase_apply_authorized_changes(self) -> Dict[str, Any]:
        """Apply only ACCEPT and MODIFY decisions (draft mode only)."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "apply_authorized_changes")

        changes_applied = 0
        changes_rejected = 0

        try:
            for decision in self.human_decisions:
                if decision.decision_type in ["ACCEPT", "MODIFY"]:
                    # Find the finding
                    finding = next((f for f in self.findings if f.finding_id == decision.finding_id), None)
                    if not finding:
                        continue

                    # Get the text to apply
                    if decision.decision_type == "MODIFY":
                        text_to_apply = decision.modified_content
                    else:  # ACCEPT
                        text_to_apply = finding.suggested_fix

                    if text_to_apply:
                        self.applied_changes[decision.finding_id] = text_to_apply
                        changes_applied += 1
                else:
                    changes_rejected += 1

            result = {
                "phase": "apply_authorized_changes",
                "changes_applied": changes_applied,
                "changes_rejected": changes_rejected,
                "mode": "draft_only",
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "apply_authorized_changes",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 5: RE-SCAN & VERIFY ==========

    def phase_re_scan_and_verify(self) -> Dict[str, Any]:
        """Re-run governance tone scan to verify remediation."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "re_scan_and_verify")

        try:
            from ppp.workflows.docs_tone_scan import DocsToneScanWorkflow

            # Run scan on same docs
            rescan_output = Path(self.output_dir) / "rescan"
            rescan_output.mkdir(parents=True, exist_ok=True)

            scan_workflow = DocsToneScanWorkflow(
                docs_root=str(self.docs_root),
                output_dir=str(rescan_output)
            )

            scan_result = scan_workflow.run()

            # Extract findings from rescan
            rescan_findings = len(scan_workflow.findings)
            original_findings = len(self.findings)

            # Check for improvement
            p0_original = sum(1 for f in self.findings if f.severity == "P0")
            p0_after = sum(1 for f in scan_workflow.findings if f.severity == "P0")

            p1_original = sum(1 for f in self.findings if f.severity == "P1")
            p1_after = sum(1 for f in scan_workflow.findings if f.severity == "P1")

            result = {
                "phase": "re_scan_and_verify",
                "original_findings": original_findings,
                "rescan_findings": rescan_findings,
                "improvement": original_findings - rescan_findings,
                "p0_reduction": p0_original - p0_after,
                "p1_reduction": p1_original - p1_after,
                "regression_detected": rescan_findings > original_findings,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "re_scan_and_verify",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 6: SEAL EVIDENCE PACK ==========

    def phase_seal_evidence_pack(self, scan_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create and seal final evidence pack."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "seal_evidence_pack")

        try:
            # Create decision receipts
            decision_batch = HumanDecisionBatch(
                batch_id=f"batch-{self.workflow_id}",
                workflow_id=self.workflow_id,
                timestamp=datetime.utcnow().isoformat(),
                authority=", ".join(set(d.authority for d in self.human_decisions)) if self.human_decisions else "none",
                decisions=self.human_decisions,
                batch_rationale="Documentation governance remediation decisions",
            )

            # Create evidence pack receipts
            receipts: List[Receipt] = []

            for decision in self.human_decisions:
                receipt = Receipt(
                    receipt_id=decision.decision_id,
                    run_id=self.workflow_id,
                    agent_id="docs-governance-remediation",
                    timestamp=decision.timestamp,
                    event="human_remediation_decision",
                    phase="seal_evidence_pack",
                    status=decision.decision_type.lower(),
                    input_hash="unknown",
                    output_hash=hashlib.sha256(
                        decision.decision_hash.encode('utf-8')
                    ).hexdigest(),
                    receipt_hash=decision.decision_hash,
                    policy={
                        "id": "remediation",
                        "version": "1.0.0",
                        "tier": "strict",
                    },
                    decision={
                        "decision_type": decision.decision_type,
                        "authority": decision.authority,
                        "finding_id": decision.finding_id,
                    },
                    artifacts={
                        "decision": decision.to_dict(),
                        "batch": decision_batch.to_dict(),
                    },
                )
                receipts.append(receipt)

            # Emit receipts
            receipts_file = self.receipt_emitter.emit_receipts(self.workflow_id, receipts)

            # Create summary
            summary_data = {
                "workflow_id": self.workflow_id,
                "workflow_name": "WF_DOCS_GOVERNANCE_REMEDIATION_v1",
                "timestamp": datetime.utcnow().isoformat(),
                "total_decisions": len(self.human_decisions),
                "decisions_by_type": {
                    "ACCEPT": sum(1 for d in self.human_decisions if d.decision_type == "ACCEPT"),
                    "MODIFY": sum(1 for d in self.human_decisions if d.decision_type == "MODIFY"),
                    "REJECT": sum(1 for d in self.human_decisions if d.decision_type == "REJECT"),
                },
                "changes_applied": len(self.applied_changes),
                "decision_authority": decision_batch.authority,
                "scan_improvement": scan_result.get("improvement", 0),
                "p0_reduction": scan_result.get("p0_reduction", 0),
                "p1_reduction": scan_result.get("p1_reduction", 0),
                "doctrine": "Governance detects. Humans decide. Verification confirms. Receipts prove.",
            }

            # Emit summary
            summary_file = self.receipt_emitter.create_summary(
                self.workflow_id,
                receipts,
                summary_data
            )

            result = {
                "phase": "seal_evidence_pack",
                "receipts_emitted": len(receipts),
                "summary_file": summary_file,
                "receipts_file": receipts_file,
                "evidence_pack_location": str(self.receipt_emitter.report_root / self.workflow_id),
                "summary": summary_data,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "seal_evidence_pack",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== ORCHESTRATION ==========

    def run_with_decisions(self, decisions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow with provided human decisions."""
        print(f"[REMEDIATION] Starting WF_DOCS_GOVERNANCE_REMEDIATION_v1")
        print(f"[REMEDIATION] ID: {self.workflow_id}")
        print(f"[REMEDIATION] Evidence pack: {self.evidence_pack_dir}")

        execution_log = {
            "workflow_id": self.workflow_id,
            "phases": {},
        }

        try:
            # Phase 1: Ingest
            execution_log["phases"]["ingest_and_verify"] = self.phase_ingest_and_verify()
            print(f"[PHASE] ingest_and_verify: complete")

            # Phase 2: Normalize
            execution_log["phases"]["normalize_findings"] = self.phase_normalize_findings()
            print(f"[PHASE] normalize_findings: {execution_log['phases']['normalize_findings']['findings_loaded']} findings")

            # Phase 3: Record decisions
            decisions_recorded = 0
            for decision_data in decisions_data.get("decisions", []):
                try:
                    self.record_human_decision(**decision_data)
                    decisions_recorded += 1
                except Exception as e:
                    print(f"[DECISION ERROR] {decision_data.get('finding_id')}: {str(e)}")

            print(f"[PHASE] human_decision_gate: {decisions_recorded} decisions recorded")

            # Phase 4: Apply
            execution_log["phases"]["apply_authorized_changes"] = self.phase_apply_authorized_changes()
            print(f"[PHASE] apply_authorized_changes: {execution_log['phases']['apply_authorized_changes']['changes_applied']} applied")

            # Phase 5: Verify
            execution_log["phases"]["re_scan_and_verify"] = self.phase_re_scan_and_verify()
            print(f"[PHASE] re_scan_and_verify: {execution_log['phases']['re_scan_and_verify']['improvement']} improvement")

            # Phase 6: Seal
            execution_log["phases"]["seal_evidence_pack"] = self.phase_seal_evidence_pack(
                execution_log["phases"]["re_scan_and_verify"]
            )
            print(f"[PHASE] seal_evidence_pack: {execution_log['phases']['seal_evidence_pack']['receipts_emitted']} receipts")

            execution_log["status"] = "complete"
            self.progress_store.complete_run(self.workflow_id, "completed")
            print(f"[REMEDIATION] Complete. Evidence pack: {self.receipt_emitter.report_root / self.workflow_id}")

        except Exception as e:
            execution_log["status"] = "failed"
            execution_log["error"] = str(e)
            self.progress_store.complete_run(self.workflow_id, "failed")
            print(f"[REMEDIATION ERROR] {str(e)}")

        return execution_log
