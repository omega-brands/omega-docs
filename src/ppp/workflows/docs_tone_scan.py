"""
WF_DOCS_GOVERNANCE_TONE_SCAN_v1: Autonomous scanning of documentation for governance tone.

This workflow scans markdown documentation for:
1. Ungoverned autonomy claims (autonomous, self-evolving, etc.)
2. Orchestration-as-trust assumptions (execution implies safety)
3. Omission drift (decisions/execution language missing governance context)
4. Anthropomorphic framing without governance context
5. Vocabulary canon alignment (suggested replacements for governance concepts)

The workflow runs on the PPP kernel:
- All decisions are policy-governed (docs-governance-tone.yaml)
- All findings emit receipts (deterministic, auditable)
- Evidence packs prove compliance with governance rules

Doctrine: "Execution proposes. Governance decides. Receipts prove."
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime
import hashlib

from ppp.policy.engine import PolicyEvaluator, PolicyDecision
from ppp.receipts.emitter import ReceiptEmitter
from ppp.receipts.schema import Receipt, CanonicalSerializer
from ppp.storage.progress import ProgressStore
from ppp.config.loader import ConfigLoader
from ppp.keon.seal import TemporalSealer


@dataclass
class DocsFinding:
    """Represents a single governance tone finding in documentation."""
    finding_id: str
    rule_id: str
    severity: str  # P0 (MUST), P1 (SHOULD), P2 (polish)
    finding_type: str  # ungoverned_autonomy, orchestration_as_trust, omission_drift, etc.
    location: str  # file:line_start:line_end
    text_snippet: str
    message: str
    suggested_fix: Optional[str] = None
    policy_decision: Optional[PolicyDecision] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert finding to dictionary for JSON serialization."""
        d = asdict(self)
        # PolicyDecision is complex; just keep decision status
        if self.policy_decision:
            rule_ids = [r.get('id', 'unknown') for r in self.policy_decision.rules_triggered]
            d['policy_decision'] = {
                'allowed': self.policy_decision.allowed,
                'rule_ids': rule_ids,
                'mitigations': self.policy_decision.mitigations,
                'confidence': self.policy_decision.confidence,
            }
        return d


class DocsToneScanWorkflow:
    """
    Autonomous governance tone scanning workflow running on PPP kernel.

    Phases:
    1. collect: Enumerate markdown files in docs/
    2. scan: Apply regex patterns for ungoverned autonomy claims
    3. classify: Categorize findings by type and severity
    4. rewrite: Draft suggested rewrites per vocabulary canon
    5. verify: Run each finding through policy engine (fail-closed)
    6. emit_receipts: Generate deterministic evidence pack with receipts
    """

    def __init__(self,
                 docs_root: str = "D:\\Repos\\omega-docs\\docs",
                 policy_path: str = "D:\\Repos\\omega-docs\\configs\\ppp\\policies\\policy.docs-governance-tone.yaml",
                 output_dir: str = "D:\\Repos\\omega-docs\\EVIDENCE\\docs-governance-tone"):
        """Initialize workflow with PPP kernel integration."""
        self.docs_root = Path(docs_root)
        self.policy_path = Path(policy_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # PPP kernel components
        policy_config = ConfigLoader.load_policy_config(str(self.policy_path))
        self.policy_evaluator = PolicyEvaluator(policy_config)
        self.receipt_emitter = ReceiptEmitter(str(self.output_dir))
        self.progress_store = ProgressStore(str(self.output_dir / "progress.db"))
        self.sealer = TemporalSealer({})

        # State
        self.findings: List[DocsFinding] = []
        self.scanned_files: List[str] = []
        # Generate workflow_id without colons (Windows-compatible)
        timestamp = datetime.utcnow().isoformat().replace(':', '-').replace('.', '_')
        self.workflow_id = f"wf-docs-tone-scan-{timestamp}"

        # Initialize progress tracking
        self.progress_store.begin_run(
            run_id=self.workflow_id,
            agent_id="docs-governance-tone-scan",
            policy_id="docs-governance-tone"
        )

    # ========== PHASE 1: COLLECT ==========

    def phase_collect(self) -> Dict[str, Any]:
        """Enumerate markdown files in docs/ directory."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "collect")

        # Collect all .md files recursively
        md_files = list(self.docs_root.rglob("*.md"))
        self.scanned_files = [str(f.relative_to(self.docs_root)) for f in md_files]

        result = {
            "phase": "collect",
            "files_found": len(self.scanned_files),
            "files": self.scanned_files[:10],  # First 10 for preview
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 2: SCAN ==========

    def _scan_ungoverned_autonomy(self, text: str, filename: str, line_num: int) -> List[DocsFinding]:
        """Detect ungoverned autonomy claims."""
        patterns = [
            (r"\b(autonomous|self-evolving?|self-improving?|self-directed)\b", "Autonomy claim"),
            (r"\bwithout human (assistance|intervention|review)\b", "No human involvement"),
            (r"\bno manual intervention\b", "No manual intervention"),
            (r"\bevolves? indefinitely\b", "Indefinite evolution"),
            (r"\b(digital organisms?|living systems?|artificial life)\b", "Organism metaphor"),
        ]

        findings = []
        for pattern, message in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                finding = DocsFinding(
                    finding_id=f"finding-{len(self.findings)}",
                    rule_id="no_ungoverned_autonomy_claims",
                    severity="P0",
                    finding_type="ungoverned_autonomy",
                    location=f"{filename}:{line_num}",
                    text_snippet=text[max(0, match.start()-20):match.end()+20],
                    message=f"{message}: '{match.group()}'",
                )
                findings.append(finding)

        return findings

    def _scan_orchestration_as_trust(self, text: str, filename: str, line_num: int) -> List[DocsFinding]:
        """Detect orchestration-as-trust assumptions."""
        patterns = [
            (r"orchestrat.*ensures safety", "Orchestration ensures safety"),
            (r"execution.*guarantees correctness", "Execution guarantees"),
            (r"automat.*provides trust", "Automation provides trust"),
            (r"distributed.*without governance", "Distribution without governance"),
        ]

        findings = []
        for pattern, message in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                finding = DocsFinding(
                    finding_id=f"finding-{len(self.findings)}",
                    rule_id="no_orchestration_as_trust",
                    severity="P0",
                    finding_type="orchestration_as_trust",
                    location=f"{filename}:{line_num}",
                    text_snippet=text[max(0, match.start()-20):match.end()+20],
                    message=f"{message}: '{match.group()}'",
                )
                findings.append(finding)

        return findings

    def _scan_omission_drift(self, text: str, filename: str, line_num: int) -> List[DocsFinding]:
        """Detect omission drift: decision/execution language missing governance context."""
        trigger_keywords = [
            "decision", "execution", "publish", "invoke", "tool",
            "federation", "workflow", "orchestrat"
        ]
        required_governance = [
            "policy", "governance", "receipt", "audit", "verify",
            "fail-closed", "deterministic"
        ]

        findings = []

        # Check if text contains trigger keywords but NOT governance keywords
        has_trigger = any(re.search(rf"\b{kw}\b", text, re.IGNORECASE) for kw in trigger_keywords)
        has_governance = any(re.search(rf"\b{kw}\b", text, re.IGNORECASE) for kw in required_governance)

        if has_trigger and not has_governance:
            # Extract trigger words for the message
            triggered = [kw for kw in trigger_keywords
                        if re.search(rf"\b{kw}\b", text, re.IGNORECASE)]

            finding = DocsFinding(
                finding_id=f"finding-{len(self.findings)}",
                rule_id="omission_drift_detection",
                severity="P1",
                finding_type="omission_drift",
                location=f"{filename}:{line_num}",
                text_snippet=text[:100],
                message=f"Section discusses {', '.join(triggered[:2])} without governance context",
            )
            findings.append(finding)

        return findings

    def _scan_anthropomorphic_framing(self, text: str, filename: str, line_num: int) -> List[DocsFinding]:
        """Detect anthropomorphic framing without governance context."""
        patterns = [
            (r"\bagent[s]?\s+(think|decide|evolve|spawn)\b", "Agent action"),
            (r"\bdigital (organism|entity|creature|being)\b", "Digital entity"),
            (r"\b(civilization|ecosystem|organism)\b", "Ecosystem metaphor"),
        ]

        # Context keywords that would justify anthropomorphic language
        governance_context = ["governed", "policy", "receipt", "audit", "bounded"]
        has_context = any(re.search(rf"\b{kw}\b", text, re.IGNORECASE) for kw in governance_context)

        findings = []
        for pattern, message in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                if not has_context:
                    finding = DocsFinding(
                        finding_id=f"finding-{len(self.findings)}",
                        rule_id="anthropomorphic_framing_without_context",
                        severity="P1",
                        finding_type="anthropomorphic_framing",
                        location=f"{filename}:{line_num}",
                        text_snippet=text[max(0, match.start()-20):match.end()+20],
                        message=f"{message} without governance context: '{match.group()}'",
                    )
                    findings.append(finding)

        return findings

    def phase_scan(self) -> Dict[str, Any]:
        """Scan markdown files for governance tone issues."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "scan")

        files_scanned = 0
        sections_with_findings = 0

        for file_rel in self.scanned_files:
            file_path = self.docs_root / file_rel

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Split by sections (lines starting with #)
                lines = content.split('\n')
                current_section = ""
                section_start = 0

                for line_num, line in enumerate(lines, 1):
                    # Accumulate section text
                    current_section += line + "\n"

                    # On new heading or end of file, scan accumulated section
                    if (line.startswith('#') and current_section) or line_num == len(lines):
                        if len(current_section) > 10:  # Ignore empty sections
                            # Run all scan functions
                            findings = []
                            findings.extend(self._scan_ungoverned_autonomy(current_section, file_rel, section_start))
                            findings.extend(self._scan_orchestration_as_trust(current_section, file_rel, section_start))
                            findings.extend(self._scan_omission_drift(current_section, file_rel, section_start))
                            findings.extend(self._scan_anthropomorphic_framing(current_section, file_rel, section_start))

                            if findings:
                                sections_with_findings += len(findings)
                                self.findings.extend(findings)

                        current_section = ""
                        section_start = line_num

                files_scanned += 1

            except Exception as e:
                # Log error but continue
                print(f"[SCAN ERROR] {file_rel}: {str(e)}")

        result = {
            "phase": "scan",
            "files_scanned": files_scanned,
            "findings_detected": len(self.findings),
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 3: CLASSIFY ==========

    def phase_classify(self) -> Dict[str, Any]:
        """Classify findings by type and severity."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "classify")

        # Already classified during scan; just summarize
        by_type = {}
        by_severity = {}

        for finding in self.findings:
            by_type[finding.finding_type] = by_type.get(finding.finding_type, 0) + 1
            by_severity[finding.severity] = by_severity.get(finding.severity, 0) + 1

        result = {
            "phase": "classify",
            "findings_by_type": by_type,
            "findings_by_severity": by_severity,
            "total_findings": len(self.findings),
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 4: REWRITE ==========

    def phase_rewrite(self) -> Dict[str, Any]:
        """Draft suggested rewrites per vocabulary canon."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "rewrite")

        # Vocabulary canon replacements from policy
        replacements = {
            "autonomous agent": "policy-governed agent",
            "self-evolving": "parameterized evolution via versioned policies",
            "automated execution": "deterministic, receipted execution",
            "orchestrated": "orchestrated and verified with evidence packs",
            "distributed system": "distributed governance system with deterministic receipts",
            "intelligent": "governed and verifiable",
        }

        rewrites_suggested = 0

        for finding in self.findings:
            # Try to find and suggest replacements
            for old_phrase, new_phrase in replacements.items():
                if old_phrase.lower() in finding.text_snippet.lower():
                    finding.suggested_fix = f"Replace '{old_phrase}' with '{new_phrase}'"
                    rewrites_suggested += 1
                    break

        result = {
            "phase": "rewrite",
            "rewrites_suggested": rewrites_suggested,
            "vocabulary_canon_applied": list(replacements.keys()),
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 5: VERIFY (POLICY) ==========

    def phase_verify(self) -> Dict[str, Any]:
        """Run each finding through policy engine (fail-closed governance)."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "verify")

        findings_approved = 0
        findings_rejected = 0

        for finding in self.findings:
            # Create finding text for policy evaluation
            finding_text = f"{finding.message}\n{finding.text_snippet}"

            # Run through policy engine with the finding text
            decision = self.policy_evaluator.evaluate(
                context={
                    "finding": finding,
                    "location": finding.location,
                },
                outbound_text=finding_text
            )

            finding.policy_decision = decision

            if decision.allowed:
                findings_approved += 1
            else:
                findings_rejected += 1

        result = {
            "phase": "verify",
            "findings_evaluated": len(self.findings),
            "findings_approved": findings_approved,
            "findings_rejected": findings_rejected,
            "policy_enforced": "docs-governance-tone.yaml v1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== PHASE 6: EMIT RECEIPTS ==========

    def phase_emit_receipts(self) -> Dict[str, Any]:
        """Generate deterministic evidence pack with receipts."""
        phase_id = self.progress_store.start_phase(self.workflow_id, "emit_receipts")

        # Collect receipts for each finding
        receipts: List[Receipt] = []

        for finding in self.findings:
            # Create canonical JSON for finding to get deterministic hash
            finding_dict = finding.to_dict()
            finding_json = CanonicalSerializer.canonical_json(finding_dict)
            output_hash = hashlib.sha256(finding_json.encode('utf-8')).hexdigest()

            # Create receipt
            receipt = Receipt(
                receipt_id=finding.finding_id,
                run_id=self.workflow_id,
                agent_id="docs-governance-tone-scan",
                timestamp=datetime.utcnow().isoformat(),
                event="governance_finding_detected",
                phase="emit_receipts",
                status="approved" if (finding.policy_decision and finding.policy_decision.allowed) else "flagged",
                input_hash="unknown",
                output_hash=output_hash,
                receipt_hash="",  # Will be computed
                policy={
                    "id": "docs-governance-tone",
                    "version": "1.0.0",
                    "tier": "strict",
                },
                decision={
                    "allowed": finding.policy_decision.allowed if finding.policy_decision else False,
                    "rule_id": finding.rule_id,
                    "severity": finding.severity,
                },
                artifacts={
                    "finding": finding_dict,
                    "suggested_fix": finding.suggested_fix,
                },
            )

            receipts.append(receipt)

        # Emit all receipts
        receipts_file = self.receipt_emitter.emit_receipts(self.workflow_id, receipts)

        # Create summary
        summary_data = {
            "workflow_id": self.workflow_id,
            "workflow_name": "WF_DOCS_GOVERNANCE_TONE_SCAN_v1",
            "timestamp": datetime.utcnow().isoformat(),
            "phases_executed": ["collect", "scan", "classify", "rewrite", "verify", "emit_receipts"],
            "total_findings": len(self.findings),
            "findings_by_severity": {
                "P0": sum(1 for f in self.findings if f.severity == "P0"),
                "P1": sum(1 for f in self.findings if f.severity == "P1"),
                "P2": sum(1 for f in self.findings if f.severity == "P2"),
            },
            "findings_by_type": {finding_type: sum(1 for f in self.findings if f.finding_type == finding_type)
                                for finding_type in set(f.finding_type for f in self.findings)},
            "files_scanned": len(self.scanned_files),
            "policy_applied": "docs-governance-tone.yaml v1.0.0",
            "doctrine": "Execution proposes. Governance decides. Receipts prove.",
            "receipts_emitted": len(receipts),
            "receipts_file": receipts_file,
        }

        # Create evidence pack
        summary_file = self.receipt_emitter.create_summary(
            self.workflow_id,
            receipts,
            summary_data
        )

        # Create evidence pack structure
        try:
            evidence_pack_dir = self.receipt_emitter.create_evidence_pack(
                run_id=self.workflow_id,
                receipts=receipts,
                policy_path=str(self.policy_path),
                run_config_path=str(self.docs_root / ".."),  # Dummy path
                poml_path=str(self.docs_root / ".."),  # Dummy path
            )
        except Exception as e:
            # If create_evidence_pack fails, try sealing anyway
            evidence_pack_dir = str(self.receipt_emitter.report_root / self.workflow_id / "evidence-pack")
            print(f"[WARNING] Evidence pack creation partial: {str(e)}")

        # Seal evidence pack
        try:
            sealed_pack = self.receipt_emitter.seal_evidence_pack(self.workflow_id)
            evidence_pack_hash = sealed_pack
        except Exception as e:
            evidence_pack_hash = "unsealed"
            print(f"[WARNING] Evidence pack sealing failed: {str(e)}")

        result = {
            "phase": "emit_receipts",
            "receipts_emitted": len(receipts),
            "summary_file": summary_file,
            "evidence_pack_hash": evidence_pack_hash,
            "evidence_pack_location": str(self.receipt_emitter.report_root / self.workflow_id),
            "summary": summary_data,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.progress_store.complete_phase(phase_id, "completed")
        return result

    # ========== EXECUTION ==========

    def run(self) -> Dict[str, Any]:
        """Execute all phases of the workflow."""
        print(f"[WORKFLOW] Starting WF_DOCS_GOVERNANCE_TONE_SCAN_v1")
        print(f"[WORKFLOW] ID: {self.workflow_id}")
        print(f"[WORKFLOW] Docs root: {self.docs_root}")
        print(f"[WORKFLOW] Output: {self.output_dir}")

        execution_log = {
            "workflow_id": self.workflow_id,
            "phases": {},
        }

        try:
            # Execute phases in sequence
            execution_log["phases"]["collect"] = self.phase_collect()
            print(f"[PHASE] collect: {execution_log['phases']['collect']['files_found']} files")

            execution_log["phases"]["scan"] = self.phase_scan()
            print(f"[PHASE] scan: {execution_log['phases']['scan']['findings_detected']} findings")

            execution_log["phases"]["classify"] = self.phase_classify()
            print(f"[PHASE] classify: complete")

            execution_log["phases"]["rewrite"] = self.phase_rewrite()
            print(f"[PHASE] rewrite: {execution_log['phases']['rewrite']['rewrites_suggested']} suggestions")

            execution_log["phases"]["verify"] = self.phase_verify()
            print(f"[PHASE] verify: {execution_log['phases']['verify']['findings_approved']} approved")

            execution_log["phases"]["emit_receipts"] = self.phase_emit_receipts()
            print(f"[PHASE] emit_receipts: {execution_log['phases']['emit_receipts']['receipts_emitted']} emitted")

            execution_log["status"] = "complete"
            self.progress_store.complete_run(self.workflow_id, "completed")
            print(f"[WORKFLOW] Complete. Evidence pack: {self.output_dir}")

        except Exception as e:
            execution_log["status"] = "failed"
            execution_log["error"] = str(e)
            self.progress_store.complete_run(self.workflow_id, "failed")
            print(f"[WORKFLOW ERROR] {str(e)}")

        return execution_log


def main():
    """Entry point for workflow execution."""
    workflow = DocsToneScanWorkflow()
    result = workflow.run()

    # Save execution log
    log_path = workflow.output_dir / "execution_log.json"
    with open(log_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"[COMPLETE] Execution log saved to {log_path}")
    return result


if __name__ == "__main__":
    main()
