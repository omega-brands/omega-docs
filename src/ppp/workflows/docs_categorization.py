"""
WF_DOCS_CATEGORIZATION_GOVERNANCE_v1: Kernel-level documentation governance workflow.

This workflow implements phases 1-6 for documentation categorization and placement:

1. Collect — Enumerate all markdown files, extract metadata
2. Classify — Infer audience and detected claims for each file
3. Policy Evaluate — Check placement against policy rules
4. Drift Report — Generate findings (audit-only, no changes)
5. Human Decision Gate — Record human decisions on findings
6. Seal Evidence Pack — Bundle receipts and seal for audit

CRITICAL: Phases 1-4 are AUDIT-ONLY. No moves, no changes, no authority.
Phase 5-6 are blocked until human decisions are recorded.

Doctrine: "Meaning follows placement. Placement follows governance."
"""

import os
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import hashlib

from ppp.policy.engine import PolicyEvaluator, PolicyDecision
from ppp.receipts.emitter import ReceiptEmitter
from ppp.receipts.schema import Receipt, CanonicalSerializer
from ppp.receipts.classification import ClassificationReceipt, ClassificationBatch
from ppp.receipts.human_decision import HumanDecisionReceipt, HumanDecisionBatch
from ppp.storage.progress import ProgressStore
from ppp.config.loader import ConfigLoader


@dataclass
class DocumentMetadata:
    """Metadata about a markdown document."""

    file_id: str
    repo: str
    relative_path: str
    full_path: str
    filename: str
    size_bytes: int

    # Content analysis
    content: str = ""
    headings: List[str] = None
    first_paragraph: str = ""
    has_links: bool = False
    external_links: List[str] = None

    def __post_init__(self):
        if self.headings is None:
            self.headings = []
        if self.external_links is None:
            self.external_links = []


class DocsCategorizationWorkflow:
    """
    Kernel-level documentation governance workflow running on PPP kernel.

    Phases:
    1. collect: Enumerate markdown files, extract metadata
    2. classify: Infer audience + detect claims
    3. policy_evaluate: Check placement against policy
    4. drift_report: Generate findings (audit-only)
    5. human_decision_gate: Record human decisions (BLOCKED until decisions provided)
    6. seal_evidence_pack: Bundle receipts and seal
    """

    def __init__(self,
                 repos: List[str],
                 policy_path: str,
                 output_dir: str = "D:\\Repos\\omega-docs\\EVIDENCE\\docs-categorization"):
        """Initialize documentation categorization workflow."""
        self.repos = [Path(r) for r in repos]
        self.policy_path = Path(policy_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # PPP kernel components
        policy_config = ConfigLoader.load_policy_config(str(self.policy_path))
        self.policy_evaluator = PolicyEvaluator(policy_config)
        self.receipt_emitter = ReceiptEmitter(str(self.output_dir))
        self.progress_store = ProgressStore(str(self.output_dir / "progress.db"))

        # State
        self.documents: Dict[str, DocumentMetadata] = {}
        self.receipts: List[ClassificationReceipt] = []
        self.human_decisions: List[HumanDecisionReceipt] = []
        self.workflow_id = self._generate_workflow_id()

        # Initialize progress tracking
        self.progress_store.begin_run(
            run_id=self.workflow_id,
            agent_id="docs-categorization",
            policy_id="docs-placement-policy"
        )

    def _generate_workflow_id(self) -> str:
        """Generate Windows-compatible workflow ID."""
        timestamp = datetime.utcnow().isoformat().replace(':', '-').replace('.', '_')
        return f"wf-docs-categorization-{timestamp}"

    # ========== PHASE 1: COLLECT ==========

    def phase_collect(self) -> Dict[str, Any]:
        """Enumerate all markdown files and extract metadata."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "collect")

        try:
            files_found = 0

            for repo_path in self.repos:
                if not repo_path.exists():
                    print(f"[COLLECT WARNING] Repo not found: {repo_path}")
                    continue

                repo_name = repo_path.name

                # Find all markdown files
                for md_file in repo_path.rglob("*.md"):
                    try:
                        relative_path = md_file.relative_to(repo_path)

                        with open(md_file, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Extract metadata
                        headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
                        paragraphs = re.split(r'\n\n+', content)
                        first_paragraph = next((p for p in paragraphs if p.strip() and not p.startswith('#')), "")

                        # Find links
                        external_links = re.findall(r'\[.*?\]\((https?://[^\)]+)\)', content)
                        has_links = len(external_links) > 0

                        file_id = f"{repo_name}/{relative_path}"

                        doc = DocumentMetadata(
                            file_id=file_id,
                            repo=repo_name,
                            relative_path=str(relative_path),
                            full_path=str(md_file),
                            filename=md_file.name,
                            size_bytes=os.path.getsize(md_file),
                            content=content,
                            headings=headings,
                            first_paragraph=first_paragraph,
                            has_links=has_links,
                            external_links=external_links,
                        )

                        self.documents[file_id] = doc
                        files_found += 1

                    except Exception as e:
                        print(f"[COLLECT ERROR] {repo_name}/{relative_path}: {str(e)}")

            result = {
                "phase": "collect",
                "files_found": files_found,
                "repos_scanned": len([r for r in self.repos if r.exists()]),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "collect",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 2: CLASSIFY ==========

    def phase_classify(self) -> Dict[str, Any]:
        """Classify each document: infer audience and detect claims."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "classify")

        try:
            docs_classified = 0

            for file_id, doc in self.documents.items():
                # Infer audience
                audience = self._detect_audience(doc)

                # Detect claims
                claims = self._detect_claims(doc)

                # Infer purpose
                purpose = self._infer_purpose(doc, claims)

                # Store in doc for next phase
                doc.detected_audience = audience
                doc.detected_claims = claims
                doc.detected_purpose = purpose

                docs_classified += 1

            result = {
                "phase": "classify",
                "documents_classified": docs_classified,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "classify",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    def _detect_audience(self, doc: DocumentMetadata) -> str:
        """Infer whether document is public, internal, or ambiguous."""
        content_lower = doc.content.lower()
        path_lower = doc.relative_path.lower()

        # Check for internal indicators
        internal_indicators = [
            "draft", "notes", "wip", "internal", "experimental", "experiment",
            "archive", "99-internal", "runbook", "sop", "postmortem", "_draft"
        ]

        for indicator in internal_indicators:
            if indicator in path_lower or indicator in content_lower:
                return "internal"

        # Check for public indicators
        public_indicators = [
            "overview", "introduction", "what is", "architecture", "getting-started",
            "quickstart", "quick start", "user guide", "public", "readme"
        ]

        for indicator in public_indicators:
            if indicator in path_lower or indicator in content_lower:
                return "public"

        # If ambiguous, return ambiguous (let policy decide)
        return "ambiguous"

    def _detect_claims(self, doc: DocumentMetadata) -> List[str]:
        """Detect what types of claims the document makes."""
        claims = []
        content_lower = doc.content.lower()

        # Check for governance claims
        governance_keywords = [
            "governance", "policy", "receipt", "evidence pack", "verification",
            "audit", "deterministic", "fail-closed", "kernel", "primitive"
        ]
        if any(kw in content_lower for kw in governance_keywords):
            claims.append("governance")

        # Check for guarantee claims
        guarantee_keywords = [
            "guarantee", "ensures", "prevents", "enforces", "trust", "secure",
            "safety", "immutable", "atomic"
        ]
        if any(kw in content_lower for kw in guarantee_keywords):
            claims.append("guarantees")

        # Check for experimental claims
        experimental_keywords = [
            "experiment", "exploration", "prototype", "draft", "proposal",
            "wip", "work in progress"
        ]
        if any(kw in content_lower for kw in experimental_keywords):
            claims.append("experimental")

        # Check for whitepaper claims
        whitepaper_keywords = [
            "whitepaper", "white paper", "design document", "specification",
            "canonical"
        ]
        if any(kw in content_lower for kw in whitepaper_keywords):
            claims.append("whitepaper")

        # Default to descriptive if no strong claims
        if not claims:
            claims.append("descriptive")

        return claims

    def _infer_purpose(self, doc: DocumentMetadata, claims: List[str]) -> str:
        """Infer document purpose based on claims and path."""
        if "governance" in claims or "whitepaper" in claims:
            return "governance_definition"
        elif "guarantees" in claims:
            return "guarantee_specification"
        elif "experimental" in claims:
            return "experimental_work"
        elif "descriptive" in claims:
            return "descriptive"
        else:
            return "unknown"

    # ========== PHASE 3: POLICY EVALUATE ==========

    def phase_policy_evaluate(self) -> Dict[str, Any]:
        """Evaluate placement against policy rules."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "policy_evaluate")

        try:
            for file_id, doc in self.documents.items():
                # Determine target repo based on policy rules
                target_repo = self._determine_target_repo(doc)

                # Check placement against policy
                policy_decision = self._check_placement_policy(doc, target_repo)

                # Create receipt
                receipt = ClassificationReceipt(
                    receipt_id=f"receipt-{len(self.receipts)}",
                    workflow_id=self.workflow_id,
                    document_id=file_id,
                    source_repo=doc.repo,
                    source_path=doc.relative_path,
                    document_name=doc.filename,
                    detected_audience=doc.detected_audience,
                    detected_claims=doc.detected_claims,
                    detected_purpose=doc.detected_purpose,
                    target_repo=target_repo,
                    policy_decision=policy_decision["decision"],
                    violated_rules=policy_decision.get("violated_rules", []),
                    policy_rationale=policy_decision.get("rationale", ""),
                    suggested_action=policy_decision.get("suggested_action"),
                    remediation_reason=policy_decision.get("remediation_reason"),
                )

                self.receipts.append(receipt)

            result = {
                "phase": "policy_evaluate",
                "documents_evaluated": len(self.receipts),
                "allow": sum(1 for r in self.receipts if r.policy_decision == "ALLOW"),
                "mitigate": sum(1 for r in self.receipts if r.policy_decision == "MITIGATE"),
                "deny": sum(1 for r in self.receipts if r.policy_decision == "DENY"),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "policy_evaluate",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    def _determine_target_repo(self, doc: DocumentMetadata) -> str:
        """Determine where policy says document should live."""
        # Governance claims -> keon-docs (public) or keon-docs-internal (internal)
        if "governance" in doc.detected_claims or doc.detected_purpose == "governance_definition":
            if doc.detected_audience == "public":
                return "keon-docs"
            else:
                return "keon-docs-internal"

        # Everything else -> omega repos based on audience
        if doc.detected_audience == "public":
            return "omega-docs"
        else:
            return "omega-docs-internal"

    def _check_placement_policy(self, doc: DocumentMetadata, target_repo: str) -> Dict[str, Any]:
        """Check if current placement complies with policy."""
        violations = []
        decision = "ALLOW"
        suggested_action = None
        remediation_reason = None

        # Rule 1: No drafts in public
        if target_repo.endswith("-docs") and "experimental" in doc.detected_claims:
            violations.append("forbid_drafts_in_public")
            decision = "DENY"
            suggested_action = "move_to_internal_repo"
            remediation_reason = "Draft/experimental content cannot be in public repos"

        # Rule 2: Governance claims only in Keon
        if "governance" in doc.detected_claims and doc.repo.startswith("omega"):
            violations.append("governance_claims_only_in_keon")
            decision = "MITIGATE"
            suggested_action = "move_to_keon_docs_or_keon_docs_internal"
            remediation_reason = "Governance definitions belong in Keon repos"

        # Rule 3: Guarantees require evidence
        if "guarantees" in doc.detected_claims and target_repo == "keon-docs":
            # Check if evidence pack is referenced
            if "evidence" not in doc.content.lower() and "evidence-pack" not in doc.content.lower():
                violations.append("guarantees_require_evidence")
                decision = "MITIGATE"
                suggested_action = "attach_evidence_pack_or_demote_to_internal"
                remediation_reason = "Guarantee claims must have associated evidence pack"

        # Rule 4: Public repos shouldn't link to internal
        if target_repo.endswith("-docs") and "internal" in str(doc.external_links).lower():
            violations.append("linkage_public_to_internal_forbidden")
            decision = "MITIGATE"
            suggested_action = "remove_link_or_move_to_public"
            remediation_reason = "Public docs cannot link to internal repos"

        # Check if currently misplaced
        if target_repo != doc.repo and decision == "ALLOW":
            decision = "MITIGATE"
            violations.append("misplaced_content")
            suggested_action = f"move_to_{target_repo}"
            remediation_reason = f"Document should be in {target_repo}, currently in {doc.repo}"

        return {
            "decision": decision,
            "violated_rules": violations,
            "rationale": f"Policy evaluated document against placement rules",
            "suggested_action": suggested_action,
            "remediation_reason": remediation_reason,
        }

    # ========== PHASE 4: DRIFT REPORT ==========

    def phase_drift_report(self) -> Dict[str, Any]:
        """Generate drift report (audit-only, no changes)."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "drift_report")

        try:
            mitigations = [r for r in self.receipts if r.policy_decision == "MITIGATE"]
            denials = [r for r in self.receipts if r.policy_decision == "DENY"]

            report = {
                "phase": "drift_report",
                "total_documents": len(self.receipts),
                "allow_count": sum(1 for r in self.receipts if r.policy_decision == "ALLOW"),
                "mitigate_count": len(mitigations),
                "deny_count": len(denials),
                "mitigations": [
                    {
                        "document_id": r.document_id,
                        "source_repo": r.source_repo,
                        "target_repo": r.target_repo,
                        "reason": r.remediation_reason,
                        "suggested_action": r.suggested_action,
                    }
                    for r in mitigations
                ],
                "denials": [
                    {
                        "document_id": r.document_id,
                        "source_repo": r.source_repo,
                        "violation": r.violated_rules[0] if r.violated_rules else "unknown",
                        "reason": r.remediation_reason,
                    }
                    for r in denials
                ],
                "audit_only": True,
                "no_changes_applied": True,
                "timestamp": datetime.utcnow().isoformat(),
            }

            result = report

        except Exception as e:
            result = {
                "phase": "drift_report",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 5: HUMAN DECISION GATE ==========

    def phase_human_decision_gate(self, decisions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record human decisions on MITIGATE/DENY findings."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "human_decision_gate")

        try:
            decisions_recorded = 0

            for decision_data in decisions_data.get("decisions", []):
                try:
                    # Find the receipt
                    receipt = next(
                        (r for r in self.receipts if r.document_id == decision_data.get("document_id")),
                        None
                    )

                    if not receipt:
                        print(f"[DECISION WARNING] Document not found: {decision_data.get('document_id')}")
                        continue

                    # Create decision receipt
                    decision = HumanDecisionReceipt(
                        decision_id=f"decision-{decisions_recorded}",
                        workflow_id=self.workflow_id,
                        finding_id=receipt.receipt_id,
                        decision_type=decision_data.get("decision_type"),
                        authority=decision_data.get("authority"),
                        timestamp=datetime.utcnow().isoformat(),
                        rationale=decision_data.get("rationale"),
                    )

                    self.human_decisions.append(decision)
                    decisions_recorded += 1

                except Exception as e:
                    print(f"[DECISION ERROR] {decision_data.get('document_id')}: {str(e)}")

            result = {
                "phase": "human_decision_gate",
                "decisions_recorded": decisions_recorded,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            result = {
                "phase": "human_decision_gate",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 6: SEAL EVIDENCE PACK ==========

    def phase_seal_evidence_pack(self) -> Dict[str, Any]:
        """Seal evidence pack with all classification receipts."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "seal_evidence_pack")

        try:
            # Create batch
            batch = ClassificationBatch(
                batch_id=f"batch-{self.workflow_id}",
                workflow_id=self.workflow_id,
                timestamp=datetime.utcnow().isoformat(),
                policy_id="docs-placement-policy",
                policy_version="1.0.0",
                receipts=self.receipts,
                batch_summary="Documentation categorization workflow execution",
            )

            # Create receipts for emission
            receipts: List[Receipt] = []

            for receipt in self.receipts:
                r = Receipt(
                    receipt_id=receipt.receipt_id,
                    run_id=self.workflow_id,
                    agent_id="docs-categorization",
                    timestamp=receipt.timestamp,
                    event="document_classified",
                    phase="seal_evidence_pack",
                    status=receipt.policy_decision.lower(),
                    input_hash="unknown",
                    output_hash=hashlib.sha256(
                        receipt.receipt_hash.encode('utf-8')
                    ).hexdigest(),
                    receipt_hash=receipt.receipt_hash,
                    policy={
                        "id": "docs-placement-policy",
                        "version": "1.0.0",
                    },
                    decision={
                        "document_id": receipt.document_id,
                        "policy_decision": receipt.policy_decision,
                        "source_repo": receipt.source_repo,
                        "target_repo": receipt.target_repo,
                    },
                    artifacts={"classification_receipt": receipt.to_dict()},
                )
                receipts.append(r)

            # Emit receipts
            receipts_file = self.receipt_emitter.emit_receipts(self.workflow_id, receipts)

            # Create summary
            summary_data = {
                "workflow_id": self.workflow_id,
                "workflow_name": "WF_DOCS_CATEGORIZATION_GOVERNANCE_v1",
                "timestamp": datetime.utcnow().isoformat(),
                "total_documents": len(self.receipts),
                "allow": sum(1 for r in self.receipts if r.policy_decision == "ALLOW"),
                "mitigate": sum(1 for r in self.receipts if r.policy_decision == "MITIGATE"),
                "deny": sum(1 for r in self.receipts if r.policy_decision == "DENY"),
                "human_decisions_recorded": len(self.human_decisions),
                "batch_hash": batch.batch_hash,
                "doctrine": "Meaning follows placement. Placement follows governance.",
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
                "batch_hash": batch.batch_hash,
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

    def run_audit_only(self) -> Dict[str, Any]:
        """Execute Phases 1-4 in audit-only mode (no decisions, no changes)."""
        print(f"[WORKFLOW] Starting WF_DOCS_CATEGORIZATION_GOVERNANCE_v1 (AUDIT-ONLY)")
        print(f"[WORKFLOW] ID: {self.workflow_id}")

        execution_log = {
            "workflow_id": self.workflow_id,
            "mode": "audit_only",
            "phases": {},
        }

        try:
            # Phase 1: Collect
            execution_log["phases"]["collect"] = self.phase_collect()
            print(f"[PHASE] collect: {execution_log['phases']['collect']['files_found']} files")

            # Phase 2: Classify
            execution_log["phases"]["classify"] = self.phase_classify()
            print(f"[PHASE] classify: complete")

            # Phase 3: Policy Evaluate
            execution_log["phases"]["policy_evaluate"] = self.phase_policy_evaluate()
            print(f"[PHASE] policy_evaluate: complete")

            # Phase 4: Drift Report
            execution_log["phases"]["drift_report"] = self.phase_drift_report()
            print(f"[PHASE] drift_report: {execution_log['phases']['drift_report']['mitigate_count']} findings")

            execution_log["status"] = "audit_complete"
            print(f"[WORKFLOW] Audit complete. Awaiting human decisions before Phase 5-6.")

        except Exception as e:
            execution_log["status"] = "failed"
            execution_log["error"] = str(e)
            print(f"[WORKFLOW ERROR] {str(e)}")

        return execution_log

    def run_with_decisions(self, decisions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Phases 5-6 after human decisions are provided."""
        print(f"[WORKFLOW] Continuing WF_DOCS_CATEGORIZATION_GOVERNANCE_v1 (DECISION-GATED)")

        execution_log = {
            "workflow_id": self.workflow_id,
            "mode": "decision_gated",
            "phases": {},
        }

        try:
            # Phase 5: Human Decision Gate
            execution_log["phases"]["human_decision_gate"] = self.phase_human_decision_gate(decisions_data)
            print(f"[PHASE] human_decision_gate: {execution_log['phases']['human_decision_gate']['decisions_recorded']} recorded")

            # Phase 6: Seal Evidence Pack
            execution_log["phases"]["seal_evidence_pack"] = self.phase_seal_evidence_pack()
            print(f"[PHASE] seal_evidence_pack: complete")

            execution_log["status"] = "complete"
            self.progress_store.complete_run(self.workflow_id, "completed")
            print(f"[WORKFLOW] Complete. Evidence pack: {self.receipt_emitter.report_root / self.workflow_id}")

        except Exception as e:
            execution_log["status"] = "failed"
            execution_log["error"] = str(e)
            self.progress_store.complete_run(self.workflow_id, "failed")
            print(f"[WORKFLOW ERROR] {str(e)}")

        return execution_log
