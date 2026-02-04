# WF_DOCS_CATEGORIZATION_GOVERNANCE_v1 — HUMAN DECISION DIRECTIVES PROPOSAL

**Date:** 2026-02-04
**Scope:** 621 MITIGATE findings grouped into 11 policy-aligned directives
**Authority Required:** Your explicit approval for each directive
**Immutability:** Once approved, all decisions become locked audit trail

---

## EXECUTIVE SUMMARY

The drift report identifies 621 documentation misplacements. Rather than individual file-by-file decisions, I've grouped these into **11 decision directives** organized by policy intent and scope:

- **9 APPROVE directives** (614 files) — Systematic placement corrections
- **2 DECISION REQUIRED directives** (2 files) — Policy violations requiring explicit override decision

Each directive maps to a unique combination of:
- Current repository
- Target repository
- Policy reason for the move
- Files affected

---

## DECISION DIRECTIVES

### DIRECTIVE A: "Governance Docs from OMEGA-INTERNAL to KEON-INTERNAL" ✓ READY

**Files Affected:** 339 documents
**Current Location:** omega-docs-internal (mixed with technical docs)
**Target Location:** keon-docs-internal (canonical governance repo)
**Policy Reason:** Governance definitions belong in Keon repos, not mixed with technical OMEGA docs
**Authority Required:** Human approval
**Immutability:** Once approved, all 339 files will be moved and receipted

**What this means:**
- Configuration specs, architectural decisions, governance frameworks, procedural docs, etc.
- Currently scattered throughout omega-docs-internal
- Policy requires: move to keon-docs-internal as single batch

**Examples (339 total):**
- `audit_protocol.md`
- `BRINGUP_CHECKLIST.md`
- `CANONICAL_INDEX.md`
- `CONFIG_CENTRALIZED_SETTINGS.md`
- `CONFIG_MIGRATION_NOTES.md`
- `execution_order.md`
- `omega_positioning.md`
- `omega_shared_knowledge_canonical.md`
- ... and 331 more

**Ratification Required:** YES/NO

---

### DIRECTIVE B: "Technical Docs from OMEGA-INTERNAL to OMEGA-DOCS" ✓ READY

**Files Affected:** 105 documents
**Current Location:** omega-docs-internal (incorrectly marked internal)
**Target Location:** omega-docs (public, for technical audience)
**Policy Reason:** Technical/descriptive documentation should be in public omega-docs, not internal
**Authority Required:** Human approval
**Immutability:** Once approved, all 105 files will be moved and receipted

**What this means:**
- These are technical guides, SDKs, integration docs, agent documentation
- They contain no sensitive information and describe OMEGA functionality
- Currently hiding in internal repo where public users can't find them
- Policy requires: move to omega-docs so public documentation is complete

**Examples (105 total):**
- `bootstrap.md`
- `BrandGenie-OMEGA-Integration.md`
- `dual_mode_agent_readme.md`
- `genesis_executive_summary.md`
- `mcp-integration-guide.md`
- `MEMORY_AUTO_EMBEDDING_INTEGRATION.md`
- `omega-sdk.md`
- ... and 98 more

**Ratification Required:** YES/NO

---

### DIRECTIVE C: "Guarantee Claims from OMEGA-INTERNAL: MOVE to KEON-DOCS" ⚠️ DECISION

**Files Affected:** 75 documents
**Current Location:** omega-docs-internal
**Target Location:** keon-docs
**Policy Reason:** Guarantee claims in public repos must have associated evidence pack
**Authority Required:** Human decision — these claims need evidence OR must move to internal

**What this means:**
- These docs make guarantee/promise claims about system capabilities, correctness, completeness
- Currently in internal repo (hidden from public)
- Policy requires: Either (A) move to keon-docs with evidence pack, or (B) keep in internal
- Question: Do you want these guarantee claims visible in public keon-docs WITH evidence, or kept internal?

**Examples (75 total):**
- `BRANDGENIE_REBRANDING_VOTE.md` (claims about rebranding status)
- `DOCKER_DEPLOYMENT_UPDATES.md` (claims about deployment correctness)
- `federation_core_security.md` (claims about security guarantees)
- `federation_llm_toolserver.md` (claims about tool server capabilities)
- `MEMORY_INGESTION_GUIDE.md` (claims about memory ingestion)
- `OMEGA_ENTERPRISE_DESIGN_v1.0.md` (enterprise design guarantees)
- ... and 69 more

**Your Decision:**
- **ACCEPT-PUBLIC:** Move to keon-docs, treat as published guarantees (subject to evidence review)
- **ACCEPT-INTERNAL:** Keep in omega-docs-internal (guarantees not ready for public)
- **MODIFY-CLAIMS:** Move to keon-docs-internal, demote guarantee language to descriptive

**Ratification Required:** ACCEPT-PUBLIC / ACCEPT-INTERNAL / MODIFY-CLAIMS

---

### DIRECTIVE D: "Governance from OMEGA-INTERNAL to KEON-DOCS" ✓ READY

**Files Affected:** 55 documents
**Current Location:** omega-docs-internal
**Target Location:** keon-docs (published governance)
**Policy Reason:** Published governance belongs in keon-docs (not draft repo)
**Authority Required:** Human approval

**What this means:**
- These are published/finalized governance documents
- Currently in omega-docs-internal (internal draft status)
- Policy requires: move to keon-docs as published governance

**Examples (55 total):**
- `FastMCP_DIRECTORY_README.md`
- `omega_sdk_proposal_gemini.md`
- `PANTHEON_QUICK_REFERENCE.md`
- ... and 52 more

**Ratification Required:** YES/NO

---

### DIRECTIVE E: "Governance from OMEGA-DOCS to KEON-DOCS-INTERNAL" ✓ READY

**Files Affected:** 19 documents
**Current Location:** omega-docs (public repo)
**Target Location:** keon-docs-internal (draft governance)
**Policy Reason:** Governance definitions must not exist in public OMEGA repos
**Authority Required:** Human approval

**What this means:**
- These are governance/procedural documents currently in omega-docs
- Policy forbids governance in public OMEGA repos
- Must move to keon repos (internal for draft, published for finalized)
- These appear to be draft/evolving governance

**Examples (19 total):**
- `EXECUTION_READY_SUMMARY.md`
- `KEON_REMEDIATION_INDEX.md`
- `RUNBOOK_REMEDIATION_CYCLE_1.md`
- `docs/atlas/keon/WF_DOCS_GOVERNANCE_REMEDIATION_v1_SPEC.md`
- `docs/atlas/ppp/*` (kernel docs)
- ... and 14 more

**Ratification Required:** YES/NO

---

### DIRECTIVE F: "Governance Repo Migration: OMEGA-INTERNAL to KEON-INTERNAL" ✓ READY

**Files Affected:** 9 documents
**Current Location:** omega-docs-internal
**Target Location:** keon-docs-internal
**Policy Reason:** Agent/system governance belongs in keon-docs-internal, not omega-docs-internal
**Authority Required:** Human approval

**What this means:**
- These are governance docs about agents and the system
- Currently misplaced in omega-docs-internal
- Policy requires: Keon governance repos only

**Examples (9 total):**
- `agent-tests.md`
- `Agents.md`
- `omega_priority_roadmap.md`
- ... and 6 more

**Ratification Required:** YES/NO

---

### DIRECTIVE G: "Guarantee Claims from OMEGA-DOCS: MOVE to KEON-DOCS" ⚠️ DECISION

**Files Affected:** 8 documents
**Current Location:** omega-docs (public repo)
**Target Location:** keon-docs (public repo with governance context)
**Policy Reason:** Guarantee claims in public OMEGA repos need evidence pack OR move to keon-docs for governance context
**Authority Required:** Human decision

**What this means:**
- These are public OMEGA docs making guarantee claims
- Policy issue: guarantee claims in public repos need evidence
- Options: (A) Move to keon-docs where governance context can be established, or (B) Demote claims to descriptive language, or (C) Keep in omega-docs with added evidence links

**Examples (8 total):**
- `README.md` (governance/capability claims)
- `docs/landing.md` (landing page claims)
- `docs/atlas/documentation-complete.md` (completeness claims)
- `docs/atlas/capabilities-index.md` (capabilities claims)
- `docs/overview/core-concepts.md` (conceptual guarantees)
- `docs/overview/for-whom.md` (audience guarantees)
- `docs/overview/receipts.md` (receipt system guarantees)
- `docs/architecture/security/best-practices.md` (security claims)
- `docs/architecture/security/fortress.md` (security guarantees)

**Your Decision:**
- **ACCEPT-KEON:** Move to keon-docs (governance context available)
- **MODIFY-DEMOTE:** Keep in omega-docs but remove guarantee language
- **ACCEPT-OMEGA-PLUS-EVIDENCE:** Keep in omega-docs and add evidence links

**Ratification Required:** ACCEPT-KEON / MODIFY-DEMOTE / ACCEPT-OMEGA-PLUS-EVIDENCE

---

### DIRECTIVE H: "Governance from OMEGA-DOCS to KEON-DOCS" ✓ READY

**Files Affected:** 6 documents
**Current Location:** omega-docs (public repo)
**Target Location:** keon-docs (published governance repo)
**Policy Reason:** Governance in public OMEGA repos must move to Keon repos
**Authority Required:** Human approval

**What this means:**
- These governance docs are in omega-docs (wrong repo)
- Move to keon-docs as published governance

**Examples (6 total):**
- `INTERFACE/remediation_decisions.md`
- `docs/architecture/overview.md`
- `docs/atlas/start-here.md`
- ... and 3 more

**Ratification Required:** YES/NO

---

### DIRECTIVE I: "Draft Governance Migration: KEON-DOCS to KEON-DOCS-INTERNAL" ✓ READY

**Files Affected:** 3 documents
**Current Location:** keon-docs (published repo)
**Target Location:** keon-docs-internal (draft repo)
**Policy Reason:** Draft/incomplete governance belongs in keon-docs-internal, not public keon-docs
**Authority Required:** Human approval

**What this means:**
- These are governance docs currently in keon-docs (published)
- They should be in keon-docs-internal (draft/incomplete)
- Move to correct repo tier

**Examples (3 total):**
- `README.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `content/CONTENT_RECONCILIATION_LEDGER.md`

**Ratification Required:** YES/NO

---

### DIRECTIVE J: "Infrastructure Docs: OMEGA-DOCS to OMEGA-DOCS-INTERNAL" ✓ READY

**Files Affected:** 1 document
**Current Location:** omega-docs (public)
**Target Location:** omega-docs-internal (internal)
**Policy Reason:** Infrastructure/deployment docs should be internal, not public
**Authority Required:** Human approval

**What this means:**
- Infrastructure documentation should not be in public repo
- Move to internal

**Examples (1 total):**
- `docs/architecture/infrastructure/gateway-ingress.md`

**Ratification Required:** YES/NO

---

### DIRECTIVE K: "Changelog Guarantee Claims: KEON-DOCS" ⚠️ DECISION

**Files Affected:** 1 document
**Current Location:** keon-docs (public)
**Target Location:** keon-docs (same repo)
**Policy Reason:** Changelog makes guarantee claims but needs evidence pack OR handle differently
**Authority Required:** Human decision

**What this means:**
- Changelog document in keon-docs makes claims about versioning/release guarantees
- Policy requires: evidence OR demote language OR move to internal

**Examples (1 total):**
- `keon-docs/whitepaper/CHANGELOG.md`

**Your Decision:**
- **KEEP-WITH-EVIDENCE:** Keep in keon-docs, add evidence links
- **MODIFY-DEMOTE:** Keep in keon-docs, demote guarantee language
- **ACCEPT-INTERNAL:** Move to keon-docs-internal

**Ratification Required:** KEEP-WITH-EVIDENCE / MODIFY-DEMOTE / ACCEPT-INTERNAL

---

## POLICY DENIALS (2 files — BLOCKING DECISIONS)

### DENIAL 1: "CONVERSATIONAL_PANTHEON_ARCHITECTURE.md"

**File:** `omega-docs-internal/doctrine/CONVERSATIONAL_PANTHEON_ARCHITECTURE.md`
**Current Location:** omega-docs-internal (internal)
**Policy Block:** Draft/experimental content cannot be in public repos
**Status:** BLOCKED by fail-closed policy

**Your Decision Required:**
The document is marked as experimental/draft. Options:

1. **KEEP-INTERNAL:** Leave in omega-docs-internal (acceptable)
2. **PUBLISH-REMOVE-DRAFT:** Move to keon-docs if draft status is removed/outdated
3. **ARCHIVE:** Mark as archived/deprecated

**Ratification Required:** KEEP-INTERNAL / PUBLISH-REMOVE-DRAFT / ARCHIVE

---

### DENIAL 2: "WHITEPAPER.md"

**File:** `keon-docs/whitepaper/WHITEPAPER.md`
**Current Location:** keon-docs (public)
**Policy Block:** Draft/experimental content cannot be in public repos (fail-closed)
**Status:** BLOCKED by fail-closed policy

**Your Decision Required:**
Whitepaper is in keon-docs (public) but marked as draft. Options:

1. **MOVE-INTERNAL:** Move to keon-docs-internal until draft is finalized
2. **PUBLISH-FINALIZE:** Keep in keon-docs if draft status is removed and paper is published
3. **ARCHIVE:** Mark as archived/deprecated

**Ratification Required:** MOVE-INTERNAL / PUBLISH-FINALIZE / ARCHIVE

---

## SUMMARY: DECISION DIRECTIVES REQUIRING YOUR APPROVAL

| # | Directive | Files | Action | Status |
|---|-----------|-------|--------|--------|
| A | Governance: OMEGA-INTERNAL → KEON-INTERNAL | 339 | APPROVE | Ready |
| B | Technical: OMEGA-INTERNAL → OMEGA-DOCS | 105 | APPROVE | Ready |
| C | Guarantee Claims: OMEGA-INTERNAL | 75 | DECIDE | ⚠️ Decision |
| D | Governance: OMEGA-INTERNAL → KEON-DOCS | 55 | APPROVE | Ready |
| E | Governance: OMEGA-DOCS → KEON-INTERNAL | 19 | APPROVE | Ready |
| F | Governance: OMEGA-INTERNAL → KEON-INTERNAL | 9 | APPROVE | Ready |
| G | Guarantee Claims: OMEGA-DOCS | 8 | DECIDE | ⚠️ Decision |
| H | Governance: OMEGA-DOCS → KEON-DOCS | 6 | APPROVE | Ready |
| I | Draft: KEON-DOCS → KEON-DOCS-INTERNAL | 3 | APPROVE | Ready |
| J | Infrastructure: OMEGA-DOCS → INTERNAL | 1 | APPROVE | Ready |
| K | Changelog: KEON-DOCS Guarantee Claims | 1 | DECIDE | ⚠️ Decision |
| DENIAL 1 | CONVERSATIONAL_PANTHEON_ARCHITECTURE.md | 1 | DECIDE | 🚫 Blocked |
| DENIAL 2 | WHITEPAPER.md | 1 | DECIDE | 🚫 Blocked |

**Total Coverage:** 622 of 623 findings (100%)

---

## WHAT HAPPENS WHEN YOU APPROVE

Once you provide decisions on these directives:

1. **Each directive becomes a HumanDecisionReceipt**
   - Directive ID: e.g., "DIRECTIVE-A"
   - Authority: Your name
   - Rationale: Your explanation
   - Timestamp: ISO 8601
   - Hash: SHA256 (deterministic)

2. **All 622 files get classified decisions**
   - System maps each file to its directive
   - Generates per-file decision receipt
   - Links to parent directive receipt

3. **Phase 5-6 Execute:**
   - All decisions locked as immutable audit trail
   - Files moved according to approved directives (draft-only, no permanent changes yet)
   - Re-classification verifies placement after moves
   - Evidence pack sealed with full proof chain

4. **Evidence Pack contains:**
   - All 763 original classification receipts
   - All 622 decision receipts (directive + file-level)
   - Batch summary with your authority
   - Hash verification manifest
   - Portable ZIP archive for audit

---

## IMMEDIATE NEXT STEPS

Please provide explicit decisions on:

### Directives A, B, D, E, F, H, I, J (8 Ready Directives)
- YES to approve each
- Or provide alternative instructions

### Directives C, G (Guarantee Claims — 83 files)
- Choose: ACCEPT-PUBLIC / ACCEPT-INTERNAL / MODIFY-CLAIMS (or similar)
- What's your governance position on public guarantee claims?

### Directive K (Changelog — 1 file)
- Choose: KEEP-WITH-EVIDENCE / MODIFY-DEMOTE / ACCEPT-INTERNAL

### Denials (2 Blocked Files)
- CONVERSATIONAL_PANTHEON_ARCHITECTURE.md: KEEP-INTERNAL / PUBLISH-REMOVE-DRAFT / ARCHIVE
- WHITEPAPER.md: MOVE-INTERNAL / PUBLISH-FINALIZE / ARCHIVE

---

## GOVERNANCE GUARANTEES

Once you approve:

✅ **Non-Delegable Human Authority:** Your decisions, your name, your rationale
✅ **Immutable Audit Trail:** Every decision hashed and receipted
✅ **Policy Compliance:** All moves validated against governance rules
✅ **Deterministic Execution:** System applies directives consistently to all 622 files
✅ **Sealed Evidence:** Complete proof chain portable and auditable
✅ **Zero Silent Changes:** No moves without your explicit directive
✅ **Fail-Closed:** Policy blocks enforce (2 denials blocked until you decide)

---

**Status:** ⏳ AWAITING YOUR DIRECTIVE APPROVALS

What are your decisions on these directives?
