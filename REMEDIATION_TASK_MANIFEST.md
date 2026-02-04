# Remediation Task Manifest

**Generated:** 2026-02-04 (Post-Movement Phase 6)
**Source Workflow:** WF_DOCS_CATEGORIZATION_GOVERNANCE_v1
**Authority:** User (Non-delegable)
**Status:** Ready for Separate Governed Remediation Workflow

---

## OVERVIEW

**84 files** flagged during documentation governance audit require remediation:
- **75 files** (Directive C): Guarantee language → Demote to descriptive language
- **8 files** (Directive G): Guarantee language → Demote to descriptive language
- **1 file** (Directive K): Changelog guarantee claims → Demote to descriptive language

**Key Principle:** Files remain in current location during remediation. Language modifications are non-movement changes.

---

## REMEDIATION DIRECTIVES

### Directive C: Guarantee Claims Language Remediation (OMEGA-INTERNAL)

**Files:** 75 documents
**Current Location:** omega-docs-internal (internal repo)
**Issue:** Files contain guarantee/promise language without evidence pack
**Remediation Action:** Demote guarantee language to descriptive language

**Decision Principle:**
- Files stay in omega-docs-internal (no movement)
- Language modified from guarantee/promise to descriptive/factual
- No evidence pack attachment required at this stage
- Separate workflow needed if files later promoted to public repos with guarantees

**Examples (75 total):**
1. `omega-docs-internal/BRANDGENIE_REBRANDING_VOTE.md`
2. `omega-docs-internal/DOCKER_DEPLOYMENT_UPDATES.md`
3. `omega-docs-internal/federation_core_security.md`
4. `omega-docs-internal/federation_llm_toolserver.md`
5. `omega-docs-internal/MEMORY_INGESTION_GUIDE.md`
6. `omega-docs-internal/OMEGA_ENTERPRISE_DESIGN_v1.0.md`
... and 69 more

**Sample Language Changes:**
```
BEFORE: "This system guarantees end-to-end encryption"
AFTER:  "This system provides end-to-end encryption"

BEFORE: "Federation ensures cross-agent consistency"
AFTER:  "Federation provides cross-agent consistency"

BEFORE: "The memory system guarantees immutability"
AFTER:  "The memory system maintains immutability properties"
```

**Acceptance Criteria:**
- All guarantee/promise language removed
- Replaced with factual, descriptive language
- No claims about future behavior or guarantees
- File functionality/purpose preserved
- No file structure changes

**Estimated Effort:** 30-60 minutes (75 files × 30-60 sec per file)

---

### Directive G: Guarantee Claims Language Remediation (OMEGA-DOCS)

**Files:** 8 documents
**Current Location:** omega-docs (public repo)
**Issue:** Public files contain guarantee/promise language without evidence
**Remediation Action:** Demote guarantee language to descriptive language

**Decision Principle:**
- Files stay in omega-docs (public location)
- Language modified from guarantee to descriptive
- Makes public documentation safer (no unsubstantiated claims)
- Future evidence-pack attachment can restore guarantee language if validated

**Files (8 total):**
1. `omega-docs/README.md`
2. `omega-docs/docs/landing.md`
3. `omega-docs/docs/atlas/documentation-complete.md`
4. `omega-docs/docs/atlas/capabilities-index.md`
5. `omega-docs/docs/overview/core-concepts.md`
6. `omega-docs/docs/overview/for-whom.md`
7. `omega-docs/docs/overview/receipts.md`
8. `omega-docs/docs/architecture/security/best-practices.md`
9. `omega-docs/docs/architecture/security/fortress.md`

**Impact:** These are high-visibility public documents. Language changes ensure public-facing content is factual.

**Sample Language Changes:**
```
BEFORE: "The system ensures security at every layer"
AFTER:  "The system provides security features at multiple layers"

BEFORE: "Documentation is complete and up-to-date"
AFTER:  "Documentation covers core functionality and key features"

BEFORE: "Receipt system guarantees auditability"
AFTER:  "Receipt system provides audit trail capabilities"
```

**Acceptance Criteria:**
- All guarantee/promise claims removed
- Replaced with evidence-backed or descriptive language
- Maintains professional tone
- Preserves document structure and accessibility
- Verified readable/comprehensible

**Estimated Effort:** 15-30 minutes (8 files × 2-4 min per file)

---

### Directive K: Changelog Guarantee Claims Remediation (KEON-DOCS)

**Files:** 1 document
**Current Location:** keon-docs (public governance repo)
**Issue:** Changelog contains version/release guarantee language
**Remediation Action:** Demote guarantee language to descriptive

**File (1 total):**
1. `keon-docs/whitepaper/CHANGELOG.md`

**Decision Principle:**
- File stays in keon-docs (published governance location)
- Language modified to reflect actual release/version history
- Separates aspirational from factual claims

**Sample Language Changes:**
```
BEFORE: "v2.0 guarantees backward compatibility"
AFTER:  "v2.0 maintains backward compatibility with v1.9"

BEFORE: "All breaking changes documented and enforced"
AFTER:  "Breaking changes documented in migration guide"
```

**Acceptance Criteria:**
- Version history remains accurate
- Removed language is replaced with factual statements
- Linked to actual release notes/migration guides where applicable
- Maintains historical context

**Estimated Effort:** 5-10 minutes (1 file)

---

## REMEDIATION WORKFLOW PATTERN

This manifest describes work suitable for a **separate, governed remediation workflow** that should:

1. **Accept This Manifest** as input
2. **Parse Directive References** (C, G, K) and file lists
3. **Execute Language Audits** (verify current state)
4. **Apply Modifications** (demote guarantee → descriptive)
5. **Verify Accuracy** (proof-read each change)
6. **Record Decisions** (immutable remediation receipts)
7. **Seal Evidence** (remediation outcome pack)

**Example Remediation Workflow:**
```
WF_LANGUAGE_REMEDIATION_v1:
  Phases:
    1. Audit — Read each file, identify guarantee language
    2. Classify — Tag guarantee claims by type/severity
    3. Modify — Demote language per directive principles
    4. Verify — Human review of each modification
    5. Record — Create RemediationReceipt per file
    6. Seal — Evidence pack with before/after diffs
```

---

## TASK QUEUE (Per Directive)

### Directive C: 75 Files (OMEGA-INTERNAL)

**By Repository Section:**

**category: federation/**
- `federation_core_security.md`
- `federation_llm_toolserver.md`
- `FEDERATION-CORE-SECURITY-COMPLETE.md`
... (3 files)

**category: memory/**
- `MEMORY_AUTO_EMBEDDING_INTEGRATION.md`
- `MEMORY_INGESTION_GUIDE.md`
... (2 files)

**category: configuration/**
- `CONFIG_CENTRALIZED_SETTINGS.md`
- `CONFIG_MIGRATION_NOTES.md`
... (2 files)

**category: design/**
- `OMEGA_ENTERPRISE_DESIGN_v1.0.md`
- `DOCKER_DEPLOYMENT_UPDATES.md`
- `BRANDGENIE_REBRANDING_VOTE.md`
... (3 files)

**category: other/**
- (64 remaining files)

**[Complete list available in file_decisions.jsonl under Directive C]**

---

### Directive G: 8 Files (OMEGA-DOCS)

**By Document:**
1. `README.md` — Primary entry point, claims about guarantees
2. `docs/landing.md` — Landing page, marketing language
3. `docs/atlas/documentation-complete.md` — Completeness claims
4. `docs/atlas/capabilities-index.md` — Capability promises
5. `docs/overview/core-concepts.md` — Conceptual guarantees
6. `docs/overview/for-whom.md` — Audience/use-case guarantees
7. `docs/overview/receipts.md` — Receipt system promises
8. `docs/architecture/security/best-practices.md` — Security guarantees
9. `docs/architecture/security/fortress.md` — Fort metaphor, strength claims

---

### Directive K: 1 File (KEON-DOCS)

**File:**
1. `keon-docs/whitepaper/CHANGELOG.md` — Release version claims

---

## AUTHORITY & GOVERNANCE

**This manifest represents:**
- ✅ User's explicit decision (Directives C, G, K approved)
- ✅ Non-delegable authority (language remediation scope)
- ✅ Separate workflow authorization (governed independently)
- ✅ Constitutional baseline (remediation pattern for future use)

**No remediation work** should proceed without:
- Acceptance of this manifest
- Creation of governance workflow (WF_LANGUAGE_REMEDIATION_v1 or similar)
- Separate human decision gate for each modification
- Immutable remediation receipts for all changes
- Final sealed evidence pack

---

## EVIDENCE REFERENCES

**Classification Phase Evidence:**
- `drift_report_2026-02-04T13-42-32.json` — Original 84 files identified

**Decision Phase Evidence:**
- `decisions/directive_receipts.json` — Directives C, G, K details
- `decisions/file_decisions.jsonl` — Per-file directive mapping

**Movement Phase Evidence:**
- `decisions/movement_audit_log.jsonl` — Proves 478 moves completed
- Non-remediation files proven to stay in place

---

## ACCEPTANCE CHECKLIST

Before remediation workflow begins:

- [ ] Manifest reviewed and understood
- [ ] Remediation scope confirmed (84 files total)
- [ ] Authority acknowledged (User directives)
- [ ] File list verified against source manifest
- [ ] Separate governed workflow planned
- [ ] Evidence preservation plan established
- [ ] Human decision gate designed for remediation
- [ ] Rollback plan prepared (before/after diffs preserved)

---

## NEXT STEPS

1. **This Manifest** created and ready
2. **File Movements** completed (469 files moved, verified)
3. **Re-Classification** pending (verify all moves correct)
4. **Evidence Pack Seal** pending (post-movement proof)
5. **Remediation Workflow Launch** (separate, governed process)

---

**Status:** Manifest complete. Ready for remediation workflow design/execution.

**Authority:** User
**Date:** 2026-02-04
**Evidence Location:** `D:\Repos\omega-docs\EVIDENCE\docs-categorization\`
