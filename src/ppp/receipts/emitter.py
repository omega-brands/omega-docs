"""Receipt emission and evidence pack generation."""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Any
from .schema import Receipt, CanonicalSerializer


class ReceiptEmitter:
    """Emit receipts and create evidence packs."""

    def __init__(self, report_root: str = "REPORT/ppp"):
        self.report_root = Path(report_root)

    def emit_receipts(self, run_id: str, receipts: List[Receipt]) -> str:
        """Write receipts to JSONL file and return path."""
        run_dir = self.report_root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        receipts_file = run_dir / "receipts.jsonl"
        with open(receipts_file, 'w') as f:
            for receipt in receipts:
                receipt_dict = receipt.to_dict()
                f.write(json.dumps(receipt_dict) + '\n')
        
        return str(receipts_file)

    def create_summary(self, run_id: str, receipts: List[Receipt], metadata: Dict[str, Any]) -> str:
        """Create and write summary JSON."""
        run_dir = self.report_root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        # Count events and statuses
        event_counts = {}
        status_counts = {}
        rule_triggers = {}
        
        for receipt in receipts:
            event_counts[receipt.event] = event_counts.get(receipt.event, 0) + 1
            status_counts[receipt.status] = status_counts.get(receipt.status, 0) + 1
            
            # Count rule triggers
            if receipt.policy.get("rules_triggered"):
                for rule in receipt.policy["rules_triggered"]:
                    rule_id = rule.get("rule_id", "unknown")
                    if rule.get("matched"):
                        rule_triggers[rule_id] = rule_triggers.get(rule_id, 0) + 1
        
        summary = {
            "run_id": run_id,
            "timestamp": receipts[0].timestamp if receipts else None,
            "total_receipts": len(receipts),
            "event_counts": event_counts,
            "status_counts": status_counts,
            "rule_triggers": rule_triggers,
            "metadata": metadata,
        }
        
        summary_file = run_dir / "summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return str(summary_file)

    def create_evidence_pack(
        self,
        run_id: str,
        receipts: List[Receipt],
        policy_path: str,
        run_config_path: str,
        poml_path: str,
    ) -> str:
        """Create complete evidence pack structure."""
        evidence_dir = self.report_root / run_id / "evidence-pack"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy receipts
        receipts_src = self.report_root / run_id / "receipts.jsonl"
        if receipts_src.exists():
            shutil.copy(receipts_src, evidence_dir / "receipts.jsonl")
        
        # Copy summary
        summary_src = self.report_root / run_id / "summary.json"
        if summary_src.exists():
            shutil.copy(summary_src, evidence_dir / "summary.json")
        
        # Create drafts directory
        drafts_dir = evidence_dir / "drafts"
        drafts_dir.mkdir(exist_ok=True)
        
        # Store artifact texts
        for receipt in receipts:
            if receipt.artifacts and receipt.artifacts.get("outbound_text"):
                artifact_hash = receipt.artifacts.get("outbound_text_hash", "unknown")
                draft_file = drafts_dir / f"{artifact_hash}.txt"
                with open(draft_file, 'w') as f:
                    f.write(receipt.artifacts["outbound_text"])
        
        # Copy policy
        policies_dir = evidence_dir / "policies"
        policies_dir.mkdir(exist_ok=True)
        if Path(policy_path).exists():
            shutil.copy(policy_path, policies_dir / Path(policy_path).name)
        
        # Copy run config and POML
        config_dir = evidence_dir / "run-config"
        config_dir.mkdir(exist_ok=True)
        if Path(run_config_path).exists():
            shutil.copy(run_config_path, config_dir / Path(run_config_path).name)
        if Path(poml_path).exists():
            shutil.copy(poml_path, config_dir / Path(poml_path).name)
        
        # Create hashes manifest
        hashes = {}
        for receipt in receipts:
            hashes[receipt.receipt_id] = {
                "input_hash": receipt.input_hash,
                "output_hash": receipt.output_hash,
                "receipt_hash": receipt.receipt_hash,
            }
        
        hashes_file = evidence_dir / "hashes.json"
        with open(hashes_file, 'w') as f:
            json.dump(hashes, f, indent=2)
        
        return str(evidence_dir)
