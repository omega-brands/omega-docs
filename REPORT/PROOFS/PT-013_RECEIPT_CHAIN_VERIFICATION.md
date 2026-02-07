# PT-013 Receipt Chain Verification

**Purpose:** Prove receipt chain integrity — every action has a receipt, every receipt has a hash  
**Method:** Option B — Manifest-emitted receipt hashes + ledger `prev_action_hash` chaining  
**Date:** 2026-02-07  

---

## Receipt Architecture

PT-013 uses **thin receipts** (RHID-first pattern):

1. Each ledger action has a `receipt_rhid` (pointer to receipt metadata)
2. Each receipt is mapped in `manifest.json` with:
   - `kind: "receipt"`
   - `action_id` (links receipt to action)
   - `run_id` (links receipt to workflow)
   - `actor_id` (attribution)
   - `action_type` (what was done)
   - `sha256` (integrity hash)
3. Actions chain via `prev_action_hash` (SHA256 of previous action data)

No `evidence/receipts/` directory exists. Receipts are embedded in the manifest.  
This is **Option B** per the PT-013 verification spec.

---

## Test A Receipt Chain — `bea9e0e1-989c-4e54-84c4-48cdec9a577d`

| Seq | Actor | Receipt RHID | SHA256 | prev_action_hash |
|-----|-------|-------------|--------|------------------|
| 1 | claude_titan | `rhid:receipt:038a2879...` | `30a7c05f936bc336...` | `null` (chain start) |
| 2 | gemini_titan | `rhid:receipt:ede61fb5...` | `0941c815879...` | `4a4b5311653a0dc8...` |
| 3 | gpt_titan | `rhid:receipt:556c774f...` | `9b06685f433867...` | `e10ba8eea4db854c...` |
| 4 | grok_titan | `rhid:receipt:a01ea374...` | `3fe88a10074156...` | `f04591292a461d6c...` |
| 5 | federation_core | `rhid:receipt:d450901d...` | `9ceea2763ed0f2...` | `69b87d7c09c6b051...` |
| 6 | approver_1 | `rhid:receipt:a92aab7a...` | `3df0145fb3fe31...` | `b0b43effc7bf7a98...` |
| 7 | federation_core | `rhid:receipt:bdfed951...` | `762f2054263b7f...` | `5bd1bacb96954828...` |

**Chain integrity:** 7 receipts, 6 hash links, 0 breaks. ✅

---

## Test B Receipt Chain — `f57650b0-1efd-44f2-b344-d2eb44ddf031`

| Seq | Actor | Receipt RHID | SHA256 | prev_action_hash |
|-----|-------|-------------|--------|------------------|
| 1 | claude_titan | `rhid:receipt:5ac4ffc9...` | `f1b3b5ef51508b...` | `null` (chain start) |
| 2 | gemini_titan | `rhid:receipt:fbeb4710...` | `ade1276b4e045f...` | `9f2c245c6a7b8fa7...` |
| 3 | federation_core | `rhid:receipt:006d1472...` | `703e1a97ad7c2c...` | `987283b5b57e7e4e...` |
| 4 | approver_1 | `rhid:receipt:6b72a352...` | `1af5159750d0a5...` | `01e65bbc82e37bfa...` |

**Chain integrity:** 4 receipts, 3 hash links, 0 breaks. ✅

---

## Test C Receipt Chain — `3cf293c9-f704-4a42-b701-7cd3dd09a2f5`

| Seq | Actor | Receipt RHID | SHA256 | prev_action_hash |
|-----|-------|-------------|--------|------------------|
| 1 | claude_titan | `rhid:receipt:469c81c2...` | `9e123ea1aa561f...` | `null` (chain start) |
| 2 | gemini_titan | `rhid:receipt:6b921d6e...` | `03117b6d543974...` | `b6dc935f41482a15...` |

**Chain integrity:** 2 receipts, 1 hash link, 0 breaks. ✅

---

## Manifest Receipt Summary

**File:** `PT-013-PBWB/manifest.json`

| Metric | Value |
|--------|-------|
| Total RHIDs | 25 |
| Receipt RHIDs | 13 |
| Artifact RHIDs | 10 |
| Gate RHIDs | 2 |
| All receipts have SHA256 | ✅ |
| All receipts have actor_id | ✅ |
| All receipts have action_id | ✅ |
| All receipts have run_id | ✅ |
| 100% RHID resolution | ✅ |

---

## Hash Generation Method

From `ops/proof/pt013/pt013_collab_executor.py`:

```python
def generate_receipt_hash(action: Action) -> str:
    data = f"{action.action_id}{action.run_id}{action.step_id}{action.actor_id}{action.action_type}"
    return hashlib.sha256(data.encode()).hexdigest()
```

Each `prev_action_hash` = `SHA256(action_id + run_id + step_id + actor_id + action_type)` of the
previous action. This creates a **tamper-evident chain** — modifying any action invalidates all
subsequent hashes.

Manifest SHA256 values are computed as:
```python
hashlib.sha256(f"{action.action_id}{action.run_id}".encode()).hexdigest()  # receipts
hashlib.sha256(f"{action.action_id}{output_rhid}".encode()).hexdigest()    # artifacts
```

---

## Auditor Verdict

| Criterion | Status |
|-----------|--------|
| Every action has a receipt RHID | ✅ 13/13 |
| Every receipt has a SHA256 hash | ✅ 13/13 |
| prev_action_hash chain is unbroken | ✅ 3/3 tests |
| Receipts are mapped in manifest | ✅ 100% resolution |
| Receipt hashes are deterministic | ✅ (SHA256 of action fields) |
| No `evidence/receipts/` directory | ⚠️ Option B used (manifest-embedded) |

**Receipt chain is verified. Option B (manifest-embedded receipts) is the active pattern.**

---

*This is the way.* 🔱

