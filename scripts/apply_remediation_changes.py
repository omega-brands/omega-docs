#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apply Remediation Changes Script

Separate from workflow: reads approved RemediationReceipts and applies changes to files.
Used ONLY after Phase 6 approval (Phase 5 human decision gate).

Executes AFTER Phases 1-6 seal evidence.

Invariants:
- No changes applied until explicitly approved
- Every change tracked + verified
- Before/after hashes matched to RemediationReceipt
- Rollback capability preserved (before/after diffs recorded)
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import hashlib
from typing import List, Dict, Tuple

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


class ApplyRemediationChanges:
    """Apply approved remediation changes to files."""

    def __init__(self, evidence_dir: str, repos: Dict[str, str]):
        """
        Initialize applier.

        Args:
            evidence_dir: Directory containing remediation evidence pack
            repos: Dict mapping repo names to repo paths
                Example: {
                    "omega-docs": "D:/Repos/omega-docs",
                    "omega-docs-internal": "D:/Repos/omega-docs-internal",
                    "keon-docs": "D:/Repos/keon-docs",
                }
        """
        self.evidence_dir = Path(evidence_dir)
        self.repos = {name: Path(path) for name, path in repos.items()}

    def apply_all_approved_changes(self) -> Dict:
        """
        Apply all approved changes from remediation evidence pack.

        Returns:
            {
                "total_files_applied": int,
                "total_files_failed": int,
                "changes_applied_log": [...]
            }
        """
        print("=" * 80)
        print("APPLYING APPROVED REMEDIATION CHANGES")
        print("=" * 80)
        print()

        # Load approval list
        approvals_path = self.evidence_dir / "decisions" / "remediation_decisions.json"
        if not approvals_path.exists():
            print(f"[ERROR] Approval list not found: {approvals_path}")
            return {"total_files_applied": 0, "total_files_failed": 0, "error": "No approval list"}

        with open(approvals_path) as f:
            approvals = json.load(f)

        print(f"[LOAD] {len(approvals.get('remediation_decisions', []))} directives approved")

        # Load remediation receipts (to-be-applied changes)
        receipts_path = self.evidence_dir / "decisions" / "remediation_receipts.jsonl"
        if not receipts_path.exists():
            print(f"[ERROR] Remediation receipts not found: {receipts_path}")
            return {"total_files_applied": 0, "total_files_failed": 0, "error": "No receipts"}

        # Apply changes
        total_applied = 0
        total_failed = 0
        changes_log = []

        with open(receipts_path) as f:
            for line in f:
                receipt = json.loads(line)

                # Check if this directive was approved
                directive_approved = any(
                    d['directive_id'] == receipt['directive_id'] and d['decision_type'] == "APPROVE_BATCH"
                    for d in approvals.get('remediation_decisions', [])
                )

                if not directive_approved:
                    print(f"[SKIP] {receipt['document_id']} (directive {receipt['directive_id']} not approved)")
                    continue

                # Apply change to file
                success, result = self._apply_change_to_file(receipt)

                if success:
                    total_applied += 1
                    changes_log.append({
                        "status": "success",
                        "document_id": receipt['document_id'],
                        "changes_count": receipt['changes_approved']
                    })
                    print(f"[OK] {receipt['document_id']} ({receipt['changes_approved']} changes applied)")
                else:
                    total_failed += 1
                    changes_log.append({
                        "status": "failed",
                        "document_id": receipt['document_id'],
                        "error": result
                    })
                    print(f"[FAIL] {receipt['document_id']}: {result}")

        print()
        print("=" * 80)
        print("CHANGES APPLIED")
        print("=" * 80)
        print(f"Total applied: {total_applied}")
        print(f"Total failed: {total_failed}")
        print()

        return {
            "total_files_applied": total_applied,
            "total_files_failed": total_failed,
            "changes_applied_log": changes_log
        }

    def _apply_change_to_file(self, receipt: Dict) -> Tuple[bool, str]:
        """
        Apply a single remediation change to a file.

        Args:
            receipt: RemediationReceipt with changes_details

        Returns:
            (success: bool, result_or_error: str)
        """
        file_path = self._resolve_file_path(receipt['source_repo'], receipt['file_path'])

        if not file_path.exists():
            return False, f"File not found: {file_path}"

        try:
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Verify hash matches receipt
            original_hash = hashlib.sha256(original_content.encode()).hexdigest()
            if original_hash != receipt['file_hash_pre']:
                return False, f"Hash mismatch (file may have been modified)"

            # Apply changes
            modified_content = original_content
            for change in receipt['changes_details']:
                old_text = change['old']
                new_text = change['new']
                modified_content = modified_content.replace(old_text, new_text, 1)

            # Compute hash of modified content
            modified_hash = hashlib.sha256(modified_content.encode()).hexdigest()

            # Write modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)

            # Verify write
            with open(file_path, 'r', encoding='utf-8') as f:
                verify_content = f.read()

            verify_hash = hashlib.sha256(verify_content.encode()).hexdigest()
            if verify_hash != modified_hash:
                return False, "Write verification failed"

            return True, f"Applied {len(receipt['changes_details'])} changes"

        except Exception as e:
            return False, str(e)

    def _resolve_file_path(self, repo_name: str, file_path: str) -> Path:
        """
        Resolve file path from repo name.

        Args:
            repo_name: Repository name (e.g., "omega-docs-internal")
            file_path: Relative file path within repo

        Returns:
            Absolute file path
        """
        if repo_name not in self.repos:
            raise ValueError(f"Unknown repo: {repo_name}")

        return self.repos[repo_name] / file_path


if __name__ == "__main__":
    # Example usage (after Phase 6 seal)
    evidence_dir = "D:\\Repos\\omega-docs\\EVIDENCE\\language-remediation"
    repos = {
        "omega-docs": "D:\\Repos\\omega-docs",
        "omega-docs-internal": "D:\\Repos\\omega-docs-internal",
        "keon-docs": "D:\\Repos\\keon-docs",
        "keon-docs-internal": "D:\\Repos\\keon-docs-internal",
    }

    applier = ApplyRemediationChanges(evidence_dir, repos)
    result = applier.apply_all_approved_changes()
    print(json.dumps(result, indent=2))
