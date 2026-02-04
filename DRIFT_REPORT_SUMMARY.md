# WF_DOCS_CATEGORIZATION_GOVERNANCE_v1 — DRIFT REPORT SUMMARY

**Execution Date:** 2026-02-04
**Workflow Mode:** Phase 1-4 Audit-Only (No Changes Applied)
**Status:** AWAITING HUMAN DECISIONS

---

## EXECUTIVE SUMMARY

The documentation categorization governance workflow has **classified 763 markdown files** across four repositories against the **docs-placement policy** (canonical governance rules).

### Classification Results

| Decision | Count | Meaning |
|----------|-------|---------|
| **ALLOW** | 140 | Correctly placed, policy satisfied |
| **MITIGATE** | 621 | Placement violation detected, requires decision |
| **DENY** | 2 | Policy violation, cannot auto-remediate |
| **TOTAL** | 763 | All markdown files across 4 repos |

### Key Finding

**95 files (12% of total) are currently misplaced** and require human decision before they can be moved.

---

## FINDINGS BY CATEGORY

### 1. GOVERNANCE DEFINITIONS BELONG IN KEON REPOS (419 files)

**Policy Rule:** Governance definitions must not live in public OMEGA repos

**Examples:**
- `omega-docs/EXECUTION_READY_SUMMARY.md`
- `omega-docs/KEON_REMEDIATION_INDEX.md`
- `omega-docs/RUNBOOK_REMEDIATION_CYCLE_1.md`
- `omega-docs/INTERFACE/remediation_decisions.md`
- `omega-docs/docs/atlas/keon/**` (48 governance docs)
- `omega-docs/docs/atlas/ppp/**` (32 kernel docs)

**Distribution:**
- From omega-docs → keon-docs-internal: 362 files
- From omega-docs → keon-docs: 57 files

**Decision Required:**
- Move all governance definitions out of omega-docs
- Target: keon-docs-internal (for draft/internal) OR keon-docs (for published policy)

---

### 2. TECHNICAL DOCS SHOULD BE IN OMEGA-DOCS (105 files)

**Policy Rule:** Technical/descriptive documentation belongs in public omega-docs

**Current State:** 105 files currently in omega-docs-internal but are descriptive/technical

**Examples:**
- `omega-docs-internal/bootstrap.md`
- `omega-docs-internal/BrandGenie-OMEGA-Integration.md`
- `omega-docs-internal/dual_mode_agent_readme.md`
- All files in `omega-docs-internal/docs/**` (98 technical docs)

**Decision Required:**
- Move these technical docs to omega-docs
- They are not sensitive/internal, just currently in wrong repo

---

### 3. GUARANTEE CLAIMS WITHOUT EVIDENCE (84 files)

**Policy Rule:** Public documents making guarantee claims must have associated evidence pack

**Examples:**
- `omega-docs/README.md` (makes guarantees about governance)
- `omega-docs/docs/landing.md` (promotional claims)
- `omega-docs/docs/atlas/documentation-complete.md`
- `omega-docs/docs/atlas/capabilities-index.md`

**Issue:** These files are in public repos and make claims ("system guarantees X", "document is complete") but have no evidence pack attached

**Decision Options:**
1. **Move to internal** — If claims are not ready to defend with evidence
2. **Keep in public + add evidence** — If claims are valid and provable
3. **Modify claims** — Demote from guarantee language to descriptive language

---

### 4. GOVERNANCE DOCS IN WRONG KEON REPO (12 files)

**Policy Rule:** Draft governance belongs in keon-docs-internal; published policy in keon-docs

**Examples (should move to keon-docs-internal):**
- `keon-docs/README.md`
- `keon-docs/.github/PULL_REQUEST_TEMPLATE.md`
- `keon-docs/content/CONTENT_RECONCILIATION_LEDGER.md`

**Examples (currently in omega-docs-internal, should be in keon-docs-internal):**
- `omega-docs-internal/agent-tests.md`
- `omega-docs-internal/Agents.md`
- `omega-docs-internal/omega_priority_roadmap.md`

---

### 5. DRAFT/EXPERIMENTAL CONTENT IN PUBLIC REPOS (2 files - DENY)

**Policy Rule:** Draft and experimental content CANNOT be in public repos (fail-closed)

**Files (BLOCKED from public):**
1. `keon-docs/whitepaper/WHITEPAPER.md`
   - Status: Draft, but currently in keon-docs (public)
   - Policy: DENY — move to internal or remove draft status

2. `omega-docs-internal/doctrine/CONVERSATIONAL_PANTHEON_ARCHITECTURE.md`
   - Status: Experimental, contains "draft" language
   - Policy: DENY — keep in internal until published

---

## REMEDIATION TARGETS

### Target Repo Distribution

| Repo | Documents Needing Movement | Reason |
|------|---------------------------|--------|
| **keon-docs-internal** | 370 | Governance + draft docs belong here |
| **keon-docs** | 145 | Published governance + guarantees |
| **omega-docs** | 105 | Technical docs misplaced to internal |
| **omega-docs-internal** | 1 | Infrastructure docs should stay internal |

---

## DECISION WORKFLOW (YOUR NEXT STEPS)

### Phase 5: Human Decision Gate (Awaiting You)

You must provide decisions on the 621 MITIGATE findings:

**Decision Format:**

```json
{
  "decisions": [
    {
      "document_id": "omega-docs/EXECUTION_READY_SUMMARY.md",
      "decision_type": "ACCEPT",
      "authority": "Your Name",
      "target_repo_approval": "keon-docs-internal",
      "rationale": "This is governance documentation and belongs in internal Keon repo"
    },
    {
      "document_id": "omega-docs-internal/bootstrap.md",
      "decision_type": "ACCEPT",
      "authority": "Your Name",
      "target_repo_approval": "omega-docs",
      "rationale": "Technical documentation, no sensitive content, belongs in public docs"
    },
    {
      "document_id": "omega-docs/README.md",
      "decision_type": "MODIFY",
      "authority": "Your Name",
      "modified_rationale": "Demote guarantee claims to descriptive language to keep in public",
      "rationale": "Can stay in omega-docs if claims are rewritten"
    },
    {
      "document_id": "keon-docs/whitepaper/WHITEPAPER.md",
      "decision_type": "ACCEPT",
      "authority": "Your Name",
      "target_repo_approval": "keon-docs-internal",
      "rationale": "DENY policy prevents draft content in public; must move to internal"
    }
  ]
}
```

### Decision Types

| Type | Meaning | Use When |
|------|---------|----------|
| **ACCEPT** | Approve suggested placement | You agree with target repo |
| **MODIFY** | Different target or different action | You have alternative placement |
| **REJECT** | Do not move this document | You want to keep it where it is |

---

## CRITICAL NOTES

### NO CHANGES ARE PERMANENT YET

- Phase 1-4 is **audit-only** — no files were moved
- All decisions are **immutable once recorded** — they become part of the audit trail
- Phase 5-6 will only execute after you approve all decisions
- Evidence pack will seal proof of your decisions

### POLICY IS FAIL-CLOSED

Two files (**keon-docs/whitepaper** and **one experimental doc**) are DENY status because policy forbids draft content in public repos. These CANNOT be auto-moved — they require either:
1. Moving to internal
2. Removing draft/experimental status

### GUARANTEE CLAIMS REQUIRE EVIDENCE

84 files in omega-docs make guarantee claims (about completeness, correctness, etc.) but have no attached evidence pack. Policy requires evidence for public guarantees. You must decide:
- Move to internal (claims not ready)
- Keep in public + provide evidence
- Modify claims to remove guarantee language

---

## NEXT STEPS

### Option 1: Full Decision Set
Provide all 621 decisions at once in JSON format

### Option 2: Batch Decision
Provide decisions for each category separately:
1. Governance docs (419 files) → keon-docs-internal
2. Technical docs (105 files) → omega-docs
3. Guarantee docs (84 files) → internal or modify
4. Misplaced governance (12 files) → correct repos
5. Draft content (2 files) → decision on remediation

### Option 3: Auto-Fill with Review
Tell me:
- "Auto-ACCEPT all governance moves to keon-docs-internal"
- "I'll decide on the guarantee claims separately"
- "Auto-ACCEPT technical docs to omega-docs"

Then provide specific decisions for files you want to handle differently

### Option 4: Conversational
Ask me questions or walk through findings one category at a time

---

## PHASE 6 EXECUTION (After Decisions)

Once you provide decisions, Phase 6 will:

1. **Record all decisions** as immutable HumanDecisionReceipt objects
2. **Apply approved moves** (draft-only, no permanent changes yet)
3. **Re-classify** moved documents to verify placement
4. **Create evidence pack** containing:
   - 763 original classification receipts
   - 621 human decision receipts (your decisions)
   - Batch summary with your authority attribution
   - Verification proof
   - Sealed ZIP archive

---

## FILES READY FOR REVIEW

**Drift Report (Full):**
- `D:\Repos\omega-docs\EVIDENCE\docs-categorization\drift_report_2026-02-04T13-42-32.json`

**This Summary:**
- `D:\Repos\omega-docs\DRIFT_REPORT_SUMMARY.md`

---

## DOCTRINE

**"Meaning follows placement. Placement follows governance."**

This workflow proves:
- Governance detects drift (✓ 621 misplacements found)
- Humans decide placement (⏳ Awaiting your decisions)
- Policy enforces rules (✓ 2 DENY findings blocked by policy)
- Evidence proves accountability (📦 To be sealed after Phase 6)

**Status:** ⏳ AWAITING YOUR DECISIONS
**Constitutional:** This cycle establishes baseline for all future documentation governance
**Immutable:** All decisions will be receipted and sealed

---

Ready for your direction. How would you like to provide decisions?
