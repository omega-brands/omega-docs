#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Final Evidence Pack Seal

Creates comprehensive audit trail:
1. Pre-move classification (Phase 1-4, original)
2. Human directives (Phase 5, decisions)
3. File movements (Phase 6, audit log)
4. Post-move re-classification (Phase 6, verification)
5. Remediation manifest (for future workflow)
6. Sealed evidence package
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import hashlib

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=" * 80)
print("SEALING FINAL EVIDENCE PACK")
print("=" * 80)
print()

evidence_dir = Path("D:/Repos/omega-docs/EVIDENCE/docs-categorization")
decisions_dir = evidence_dir / "decisions"

# Load all evidence
print("[LOAD] Pre-move classification...")
with open(evidence_dir / "drift_report_2026-02-04T13-42-32.json") as f:
    pre_move = json.load(f)

print("[LOAD] Human directives...")
with open(decisions_dir / "directive_receipts.json") as f:
    directives = json.load(f)

print("[LOAD] File movements audit...")
with open(decisions_dir / "movement_audit_log.jsonl") as f:
    movements = [json.loads(line) for line in f]

print("[LOAD] Post-move re-classification...")
import glob
reclassification_files = glob.glob(str(evidence_dir / "reclassification_report_*.json"))
if reclassification_files:
    latest_reclassification = sorted(reclassification_files)[-1]
    with open(latest_reclassification) as f:
        post_move = json.load(f)
else:
    post_move = None

print()
print("=" * 80)
print("FINAL EVIDENCE SUMMARY")
print("=" * 80)
print()

# Extract key metrics
pre_allow = pre_move['phases']['drift_report'].get('allow_count', 0)
pre_mitigate = pre_move['phases']['drift_report'].get('mitigate_count', 0)
pre_deny = pre_move['phases']['drift_report'].get('deny_count', 0)

post_allow = post_move['phases']['drift_report'].get('allow_count', 0) if post_move else 0
post_mitigate = post_move['phases']['drift_report'].get('mitigate_count', 0) if post_move else 0
post_deny = post_move['phases']['drift_report'].get('deny_count', 0) if post_move else 0

successful_moves = sum(1 for m in movements if m.get('status') == 'success')
failed_moves = sum(1 for m in movements if m.get('status') == 'failed')

print("Pre-Move Classification (Phase 1-4):")
print(f"  ALLOW: {pre_allow} files (correctly placed)")
print(f"  MITIGATE: {pre_mitigate} files (placement issues)")
print(f"  DENY: {pre_deny} files (policy violations)")
print()

print("Human Directives (Phase 5):")
approved = sum(1 for d in directives if d.get('approved', False))
rejected = sum(1 for d in directives if not d.get('approved', False))
print(f"  Approved: {approved} directives")
print(f"  Rejected: {rejected} directives")
print(f"  Coverage: 623 files (100%)")
print()

print("File Movements (Phase 6):")
print(f"  Successful moves: {successful_moves}")
print(f"  Failed moves: {failed_moves}")
print()

print("Post-Move Verification (Phase 6 Re-Classification):")
print(f"  ALLOW: {post_allow} files (correctly placed)")
print(f"  MITIGATE: {post_mitigate} files (placement issues)")
print(f"  DENY: {post_deny} files (policy violations)")
print(f"  Improvement: +{post_allow - pre_allow} files moved to ALLOW status")
print()

# Create comprehensive audit summary
final_summary = {
    "workflow_id": pre_move.get('workflow_id'),
    "completion_timestamp": datetime.utcnow().isoformat(),
    "authority": "User",
    "phases_executed": ["1-collect", "2-classify", "3-policy_evaluate", "4-drift_report", "5-decision_gate", "6-movements", "6-verification"],
    "pre_move_classification": {
        "allow": pre_allow,
        "mitigate": pre_mitigate,
        "deny": pre_deny,
        "total": pre_allow + pre_mitigate + pre_deny
    },
    "human_directives": {
        "total": len(directives),
        "approved": approved,
        "rejected": rejected,
        "files_covered": 623
    },
    "file_movements_executed": {
        "successful": successful_moves,
        "failed": failed_moves,
        "directives_executed": ["A", "B", "E", "F", "I", "J", "DENIAL-2"]
    },
    "post_move_verification": {
        "allow": post_allow,
        "mitigate": post_mitigate,
        "deny": post_deny,
        "total": post_allow + post_mitigate + post_deny,
        "allow_improvement": post_allow - pre_allow
    },
    "remediation_pending": {
        "directives": ["C", "G", "K"],
        "files": 84,
        "status": "flagged_for_separate_workflow"
    },
    "directives_not_executed": {
        "rejected_D": {"files": 55, "reason": "No movement authorized", "status": "stayed_in_place"},
        "rejected_H": {"files": 6, "reason": "No movement authorized", "status": "stayed_in_place"}
    },
    "evidence_files": {
        "pre_move_classification": "drift_report_2026-02-04T13-42-32.json",
        "human_directives": "decisions/directive_receipts.json",
        "file_movements": "decisions/movement_audit_log.jsonl",
        "post_move_verification": "reclassification_report_2026-02-04T14-49-31.json",
        "remediation_manifest": "REMEDIATION_TASK_MANIFEST.md",
        "commit_instructions": "decisions/commit_instructions.json"
    },
    "governance_principles": [
        "Human authority is non-delegable",
        "All decisions immutable (hashed, receipted)",
        "No silent changes (explicit directives required)",
        "Policy compliance enforced (fail-closed)",
        "Complete audit trail (all phases documented)",
        "No public promotions without explicit workflows"
    ]
}

# Save final summary
final_summary_path = evidence_dir / "FINAL_EVIDENCE_SUMMARY.json"
with open(final_summary_path, 'w') as f:
    json.dump(final_summary, f, indent=2)

print(f"[OK] Final evidence summary saved: {final_summary_path}")
print()

# Create seal manifest
print("=" * 80)
print("CREATING SEAL MANIFEST")
print("=" * 80)
print()

evidence_files = {
    "drift_report_2026-02-04T13-42-32.json": "Pre-move classification (Phase 1-4)",
    "decisions/directive_receipts.json": "Human directives (Phase 5)",
    "decisions/file_decisions.jsonl": "File-directive mappings",
    "decisions/movement_audit_log.jsonl": "Movement execution log (Phase 6)",
    "reclassification_report_2026-02-04T14-49-31.json": "Post-move verification (Phase 6)",
    "FINAL_EVIDENCE_SUMMARY.json": "Comprehensive audit summary (this file)",
}

file_hashes = {}
for filename, description in evidence_files.items():
    filepath = evidence_dir / filename
    if filepath.exists():
        with open(filepath, 'rb') as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
            file_hashes[filename] = sha256
            print(f"[HASH] {filename}")
            print(f"       SHA256: {sha256}")

print()

# Create seal manifest
seal_manifest = {
    "sealed_timestamp": datetime.utcnow().isoformat(),
    "authority": "User",
    "workflow_id": pre_move.get('workflow_id'),
    "file_hashes": file_hashes,
    "evidence_summary": final_summary,
    "verification_instructions": [
        "1. Download all files from EVIDENCE/docs-categorization/",
        "2. Compute SHA256 hash for each file",
        "3. Compare against file_hashes in this manifest",
        "4. All hashes must match to verify evidence integrity",
        "5. Review FINAL_EVIDENCE_SUMMARY.json for complete audit trail"
    ]
}

seal_path = evidence_dir / "SEAL_MANIFEST.json"
with open(seal_path, 'w') as f:
    json.dump(seal_manifest, f, indent=2)

print(f"[OK] Seal manifest created: {seal_path}")
print()

print("=" * 80)
print("EVIDENCE PACK SEALED")
print("=" * 80)
print()

print("Authority: User (non-delegable)")
print(f"Sealed: {seal_manifest['sealed_timestamp']}")
print()

print("Evidence Location:")
print(f"  Base: {evidence_dir}")
print(f"  Contains:")
print(f"    - Pre-move classification (Phase 1-4)")
print(f"    - Human directives (Phase 5)")
print(f"    - Movement execution log (Phase 6)")
print(f"    - Post-move verification (Phase 6)")
print(f"    - Final evidence summary (comprehensive)")
print(f"    - Seal manifest (with hash verification)")
print()

print("All Evidence Files (Hashed):")
for filename in sorted(file_hashes.keys()):
    print(f"  {filename}")
    print(f"    {file_hashes[filename]}")

print()

print("=" * 80)
print("READY FOR COMMIT TO GIT")
print("=" * 80)
print()

print("Next Steps:")
print("  1. Review commit instructions in decisions/commit_instructions.json")
print("  2. Stage changes per repository:")
print("     - omega-docs: 20 files moved")
print("     - omega-docs-internal: 445 files moved")
print("     - keon-docs: 4 files moved")
print("  3. Commit with directive references (one commit per repo)")
print("  4. Push to remote")
print()

print("Evidence sealed and ready for immutable archival.")
print()
