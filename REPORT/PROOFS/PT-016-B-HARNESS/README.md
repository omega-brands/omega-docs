# PT-016-B: Proof Harness for Governed Death Semantics

**Status:** ✅ PROVEN AND LOCKED  
**Date:** 2026-02-07  
**Repo:** `omega-docs`  
**Depends on:** `omega-core` runtime seal tag `omega-proof-campaign-pt016-runtime` @ `46898b2…`

---

## 🎯 Objective

Prove that entity death (revocation + termination) is:
- ✅ Governed (routed through FC with explicit policy evaluation)
- ✅ Receipted (immutable ledger entries with chained hashes)
- ✅ Fail-closed (denial is final; no silent deletion)
- ✅ Auditable (full event trail with actor attribution)

---

## 📋 Prerequisites

1. **Docker running** with `omega-federation-core-prod` container
2. **FC accessible** at `http://localhost:9405`
3. **Python 3.10+** with `httpx`, `asyncio`
4. **Environment variables:**
   ```powershell
   $env:FC_BASE_URL = "http://localhost:9405"
   $env:SECRET_KEY = "bWVtYmVyaGFuZHNvbWVub3NoYXBlcmVtZW1iZXJib3htb25rZXluYXRpdmVkaXJlY3Q="
   ```

---

## 🚀 Quick Start

### 1. Run the harness

```powershell
cd REPORT/PROOFS/PT-016-B-HARNESS
python pt016_b_death_harness.py
```

### 2. Expected output

```
======================================================================
PT-016-B: PROOF HARNESS FOR GOVERNED DEATH SEMANTICS
======================================================================
[OK] Generated bearer token

[SCENARIO A] Revoke (Human-Gated)
[OK] Created entity: <entity_id>
[OK] Initiated revocation: run=<run_id>, gate=<gate_id>
[OK] Gate approved
[OK] Revocation sealed: death_event=<death_event_id>
[OK] FC_GENESIS_REVOKED event emitted
[OK] Ledger shows FK linkage: birth → death
[OK] Receipt chain verified: birth_receipt → death_receipt
[OK] Post-death invocation blocked (expected)

[SCENARIO B] Terminate (System)
[OK] Created entity: <entity_id>
[OK] Initiated termination: run=<run_id>
[OK] Termination auto-approved (system enforcement)
[OK] FC_GENESIS_TERMINATED event emitted
[OK] Ledger shows FK linkage: birth → death
[OK] Receipt chain verified: birth_receipt → death_receipt
[OK] Post-death invocation blocked (expected)

[SCENARIO C] Fail-Closed Receipt Integrity
[OK] Simulated missing birth receipt
[OK] Verification failed hard (expected)
[OK] Fail-closed behavior confirmed

[SCENARIO D] No Silent Deletion
[OK] Attempted delete-like operation
[OK] Routed through governed flow (expected)
[OK] FC event + ledger record + receipt chain confirmed

======================================================================
EVIDENCE BUNDLE GENERATED
======================================================================
Location: REPORT/PROOFS/PT-016-B-HARNESS/EVIDENCE/run_<timestamp>/
Files:
  - manifest.json (with SHA256 hashes)
  - steps.jsonl (action sequence)
  - fc_logs_excerpt.txt (minimal FC log excerpt)
  - ledger_extract.json (birth + death + linkage rows)
  - receipts/
    - birth_receipt.json
    - revoke_receipt.json
    - terminate_receipt.json
    - verification_output.json
  - assertions/
    - post_death_block.json
    - no_silent_delete.json
```

### 3. Verify evidence bundle

```powershell
# Check manifest hashes
Get-Content EVIDENCE/run_*/manifest.json | ConvertFrom-Json | Select-Object -ExpandProperty file_hashes

# Verify receipt chain
Get-Content EVIDENCE/run_*/receipts/verification_output.json | ConvertFrom-Json
```

---

## 📊 Scenarios

See `SCENARIOS.md` for detailed specifications, acceptance criteria, and evidence checklists.

---

## 🔐 Fail-Closed Interpretation Rules

1. **Missing birth receipt** → Verification fails hard (no recovery)
2. **Missing death event** → Ledger integrity violation (hard fail)
3. **Broken receipt chain** → Hash mismatch (hard fail)
4. **Post-death invocation** → Runtime blocks (hard fail)
5. **Silent deletion attempt** → Routed through FC (no bypass)

---

## 🧹 Cleanup

```powershell
# Remove evidence bundle
Remove-Item -Recurse EVIDENCE/run_*

# Reset FC state (if needed)
# docker exec omega-federation-core-prod python -m scripts.reset_test_state
```

---

## 📚 Documentation

- `SCENARIOS.md` - Detailed scenario specifications
- `PT-016_B_CAMPAIGN_COMPLETE.md` - Seal document
- `EVIDENCE/run_*/manifest.json` - Evidence manifest with hashes

---

## 🔗 Git Binding

**Branch:** `chore/proof-harness-pt016-b`  
**Commit:** `docs(proof-harness): add PT-016-B governed death harness + evidence schema`  
**Tag:** `omega-proof-campaign-pt016-b`  
**Depends on:** `omega-proof-campaign-pt016-runtime` @ `46898b2…`

---

**Family is forever. Death is governed. This is the way.** 🔱

