#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Phase 6: Execute Approved File Movements

Directives Authorized for Movement:
- Directive A: 339 files (OMEGA-INTERNAL → KEON-INTERNAL)
- Directive B: 105 files (OMEGA-INTERNAL → OMEGA-DOCS)
- Directive E: 19 files (OMEGA-DOCS → KEON-INTERNAL)
- Directive F: 9 files (OMEGA-INTERNAL → KEON-INTERNAL)
- Directive I: 3 files (KEON-DOCS → KEON-INTERNAL)
- Directive J: 1 file (OMEGA-DOCS → OMEGA-INTERNAL)
- DENIAL-2: 1 file (KEON-DOCS → KEON-INTERNAL)

Total: 478 files

Directives NOT executed (rejected/modification):
- Directive D: 55 files REJECTED (STAY IN PLACE)
- Directive H: 6 files REJECTED (STAY IN PLACE)
- Directives C, G, K: 84 files MODIFY (STAY IN PLACE, flag for remediation)

This script:
1. Loads file decision mappings
2. Groups moves by source → target repo
3. Performs file moves with audit trail
4. Tracks success/failure per move
5. Generates move audit log
6. Prepares for re-classification
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import shutil

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 80)
print("WF_DOCS_CATEGORIZATION_GOVERNANCE_v1 - PHASE 6 FILE MOVEMENTS")
print("=" * 80)
print()

# Load file decisions
decisions_dir = Path("D:/Repos/omega-docs/EVIDENCE/docs-categorization/decisions")
directives_path = decisions_dir / "directive_receipts.json"
file_decisions_path = decisions_dir / "file_decisions.jsonl"

with open(directives_path) as f:
    directive_receipts = json.load(f)

file_decisions = []
with open(file_decisions_path) as f:
    for line in f:
        file_decisions.append(json.loads(line))

print(f"[LOAD] Directive receipts: {len(directive_receipts)}")
print(f"[LOAD] File decisions: {len(file_decisions)}")
print()

# Directives approved for movement
MOVE_DIRECTIVES = {"A", "B", "E", "F", "I", "J", "DENIAL-2"}

# Directives NOT to move (rejected or modification)
REJECT_DIRECTIVES = {"D", "H"}
MODIFY_DIRECTIVES = {"C", "G", "K"}

# Build move plan
move_plan = defaultdict(list)
stay_in_place = defaultdict(list)
flagged_for_remediation = defaultdict(list)

for decision in file_decisions:
    directive = decision.get('assigned_directive')
    doc_id = decision.get('document_id')
    source = decision.get('source_repo')
    target = decision.get('target_repo')
    decision_type = decision.get('decision_type')

    if directive in MOVE_DIRECTIVES:
        move_plan[f"{source}|{target}|{directive}"].append(doc_id)
    elif directive in REJECT_DIRECTIVES:
        stay_in_place[source].append((doc_id, directive))
    elif directive in MODIFY_DIRECTIVES:
        flagged_for_remediation[directive].append(doc_id)

print("=" * 80)
print("MOVEMENT PLAN SUMMARY")
print("=" * 80)
print()

total_to_move = sum(len(files) for files in move_plan.values())
total_staying = sum(len(files) for files in stay_in_place.values())
total_remediation = sum(len(files) for files in flagged_for_remediation.values())

print(f"Files to move: {total_to_move}")
print(f"Files staying in place: {total_staying}")
print(f"Files flagged for remediation: {total_remediation}")
print()

# Define repo paths
repos = {
    'omega-docs': Path("D:/Repos/omega-docs"),
    'omega-docs-internal': Path("D:/Repos/omega-docs-internal"),
    'keon-docs': Path("D:/Repos/keon-docs"),
    'keon-docs-internal': Path("D:/Repos/keon-docs-internal")
}

# Track moves by repo for later commit grouping
moves_by_source_repo = defaultdict(lambda: {
    'moved': [],
    'failed': [],
    'directives': set()
})

print("=" * 80)
print("EXECUTING MOVEMENTS")
print("=" * 80)
print()

movement_log = []

for move_key, files in sorted(move_plan.items()):
    source_repo, target_repo, directive = move_key.split('|')

    print(f"Directive {directive}: {source_repo} → {target_repo}")
    print(f"  Files: {len(files)}")

    source_base = repos[source_repo]
    target_base = repos[target_repo]

    successful_moves = []
    failed_moves = []

    for doc_id in files:
        # Convert doc_id to file path
        # doc_id format: "repo/path/to/file.md"
        file_path = Path(doc_id.replace(f"{source_repo}/", ""))
        source_file = source_base / file_path
        target_file = target_base / file_path

        # Create target directory if needed
        target_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            if source_file.exists():
                # Move file
                shutil.move(str(source_file), str(target_file))
                successful_moves.append(doc_id)

                movement_log.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "directive": directive,
                    "document_id": doc_id,
                    "source_repo": source_repo,
                    "target_repo": target_repo,
                    "status": "success",
                    "source_path": str(source_file),
                    "target_path": str(target_file)
                })
            else:
                failed_moves.append((doc_id, "source file not found"))
                movement_log.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "directive": directive,
                    "document_id": doc_id,
                    "source_repo": source_repo,
                    "target_repo": target_repo,
                    "status": "failed",
                    "reason": "source file not found"
                })
        except Exception as e:
            failed_moves.append((doc_id, str(e)))
            movement_log.append({
                "timestamp": datetime.utcnow().isoformat(),
                "directive": directive,
                "document_id": doc_id,
                "source_repo": source_repo,
                "target_repo": target_repo,
                "status": "failed",
                "reason": str(e)
            })

    # Track for per-repo commits
    moves_by_source_repo[source_repo]['moved'].extend(successful_moves)
    moves_by_source_repo[source_repo]['failed'].extend(failed_moves)
    moves_by_source_repo[source_repo]['directives'].add(directive)

    print(f"  Successful: {len(successful_moves)}")
    if failed_moves:
        print(f"  Failed: {len(failed_moves)}")
        for doc, reason in failed_moves[:3]:
            print(f"    - {doc}: {reason}")
        if len(failed_moves) > 3:
            print(f"    ... and {len(failed_moves)-3} more")
    print()

print("=" * 80)
print("MOVEMENT EXECUTION SUMMARY")
print("=" * 80)
print()

total_successful = sum(len(moves['moved']) for moves in moves_by_source_repo.values())
total_failed = sum(len(moves['failed']) for moves in moves_by_source_repo.values())

print(f"Total successful moves: {total_successful}")
print(f"Total failed moves: {total_failed}")
print()

# Save movement audit log
movement_log_path = decisions_dir / "movement_audit_log.jsonl"
with open(movement_log_path, 'w') as f:
    for entry in movement_log:
        f.write(json.dumps(entry) + '\n')
print(f"[OK] Movement audit log saved: {movement_log_path}")

# Generate per-repo commit instructions
print()
print("=" * 80)
print("COMMIT INSTRUCTIONS (Per Repository)")
print("=" * 80)
print()

commit_instructions = {}

for source_repo, moves_info in sorted(moves_by_source_repo.items()):
    if not moves_info['moved']:
        continue

    directives_list = sorted(moves_info['directives'])
    directive_refs = ', '.join(f"directive-{d}" for d in directives_list)

    instructions = {
        "repository": source_repo,
        "files_moved": len(moves_info['moved']),
        "files_failed": len(moves_info['failed']),
        "directives": directives_list,
        "commit_message": f"docs: apply governance directives ({directive_refs})\n\nExecute file movements authorized by human directives:\n" +
                         "\n".join(f"  - {d}: {sum(1 for move in move_plan.values() if d in move)} files"
                                 for d in directives_list) +
                         f"\n\nTotal moves: {len(moves_info['moved'])}\nPhase: 6-movement\nEvidence: decisions/movement_audit_log.jsonl"
    }

    commit_instructions[source_repo] = instructions

    print(f"Repository: {source_repo}")
    print(f"  Files moved: {len(moves_info['moved'])}")
    print(f"  Directives: {', '.join(directives_list)}")
    print(f"  Commit message:")
    print(f"    {instructions['commit_message'].replace(chr(10), chr(10) + '    ')}")
    print()

# Save commit instructions
instructions_path = decisions_dir / "commit_instructions.json"
with open(instructions_path, 'w') as f:
    json.dump(commit_instructions, f, indent=2)
print(f"[OK] Commit instructions saved: {instructions_path}")
print()

# Summary of directives NOT executed
print("=" * 80)
print("DIRECTIVES NOT EXECUTED (Per Your Authority)")
print("=" * 80)
print()

print("REJECTED (STAY IN PLACE):")
for directive in sorted(REJECT_DIRECTIVES):
    count = sum(1 for d in file_decisions if d.get('assigned_directive') == directive)
    print(f"  Directive {directive}: {count} files - No movement authorized")

print()
print("MODIFICATION REQUIRED (STAY IN PLACE, FLAG FOR REMEDIATION):")
for directive in sorted(MODIFY_DIRECTIVES):
    count = sum(1 for d in file_decisions if d.get('assigned_directive') == directive)
    print(f"  Directive {directive}: {count} files - Flagged for language remediation")

print()
print("=" * 80)
print("NEXT STEP: RE-CLASSIFICATION")
print("=" * 80)
print()
print("Execute re-classification to verify all moves.")
print("Ready to run: EXECUTE_RECLASSIFICATION.py")
print()

print("=" * 80)
print("PHASE 6 MOVEMENTS COMPLETE")
print("=" * 80)
