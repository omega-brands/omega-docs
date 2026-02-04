#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Execute Phase 1-4 audit-only run of WF_DOCS_CATEGORIZATION_GOVERNANCE_v1.

This script:
1. Instantiates the workflow
2. Runs Phases 1-4 (collect, classify, evaluate, drift report)
3. Generates drift report
4. Blocks before Phase 5-6 (awaiting human decisions)
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Set UTF-8 output encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 80)
print("WF_DOCS_CATEGORIZATION_GOVERNANCE_v1 - PHASE 1-4 AUDIT-ONLY RUN")
print("=" * 80)
print()

try:
    from ppp.workflows.docs_categorization import DocsCategorizationWorkflow

    print("[OK] Workflow module imported successfully")
    print()

    # Define repos
    repos = [
        Path("D:/Repos/omega-docs"),
        Path("D:/Repos/omega-docs-internal"),
        Path("D:/Repos/keon-docs"),
        Path("D:/Repos/keon-docs-internal"),
    ]

    # Create workflow instance
    policy_path = Path("D:/Repos/omega-docs/configs/ppp/policies/policy.docs-placement.yaml")
    output_dir = Path("D:/Repos/omega-docs/EVIDENCE/docs-categorization")

    print(f"Repos: {[str(r) for r in repos]}")
    print(f"Policy: {policy_path}")
    print(f"Output: {output_dir}")
    print()

    # Create evidence directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    workflow = DocsCategorizationWorkflow(
        repos=repos,
        policy_path=policy_path,
        output_dir=output_dir
    )

    print("[OK] Workflow instantiated")
    print()

    # Execute Phase 1-4 audit-only
    print("=" * 80)
    print("EXECUTING PHASES 1-4 (AUDIT-ONLY)")
    print("=" * 80)
    print()

    result = workflow.run_audit_only()

    print()
    print("=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)
    print()

    # Display summary
    summary = result.get("summary", {})
    print(f"Total files collected: {summary.get('total_files', 0)}")
    print(f"Files classified: {summary.get('classified_count', 0)}")
    print(f"ALLOW decisions: {summary.get('allow_count', 0)}")
    print(f"MITIGATE decisions: {summary.get('mitigate_count', 0)}")
    print(f"DENY decisions: {summary.get('deny_count', 0)}")
    print()

    if summary.get('mitigate_count', 0) > 0:
        print("[!] FINDINGS REQUIRING REVIEW (MITIGATE):")
        mitigations = result.get("mitigations", [])
        for i, m in enumerate(mitigations[:5], 1):  # Show first 5
            print(f"  {i}. {m.get('document_id')} -> {m.get('target_repo')}")
            print(f"     Violated rules: {', '.join(m.get('violated_rules', []))}")
        if len(mitigations) > 5:
            print(f"  ... and {len(mitigations) - 5} more")
        print()

    if summary.get('deny_count', 0) > 0:
        print("[X] FINDINGS DENIED (DENY):")
        denials = result.get("denials", [])
        for i, d in enumerate(denials[:5], 1):  # Show first 5
            print(f"  {i}. {d.get('document_id')} (currently in {d.get('source_repo')})")
            print(f"     Reason: {', '.join(d.get('violated_rules', []))}")
        if len(denials) > 5:
            print(f"  ... and {len(denials) - 5} more")
        print()

    # Save full report
    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    report_path = output_dir / f"drift_report_{timestamp}.json"
    with open(report_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"[OK] Full drift report saved: {report_path}")
    print()

    print("=" * 80)
    print("AWAITING HUMAN DECISIONS")
    print("=" * 80)
    print()
    print("Phase 1-4 (audit-only) execution complete.")
    print("Phases 5-6 are BLOCKED until human decisions are recorded.")
    print()
    print("Next step: Review findings and provide decisions in JSON format:")
    print("""
    {
      "decisions": [
        {
          "finding_id": "finding-0",
          "document_id": "docs/path/file.md",
          "decision_type": "ACCEPT|MODIFY|REJECT",
          "authority": "Your Name",
          "suggested_target_repo": "target-repo-name",
          "rationale": "Why you chose this decision"
        }
      ]
    }
    """)
    print()

except Exception as e:
    print(f"[ERROR] {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
