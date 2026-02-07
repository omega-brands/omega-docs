# PT-013 Quick Start

## Prerequisites

1. **Federation Core running** at `http://localhost:9405`
2. **Python 3.9+** with httpx and asyncio
3. **omega-docs repository** cloned

## Running the Tests

```bash
cd d:\Repos\omega-docs
python ops/proof/pt013/pt013_collab_executor.py
```

## Expected Output

```
[PANTHEON] PT-013 MULTI-TITAN COLLABORATION TEST HARNESS
Federation Core: http://localhost:9405
Timestamp: 2026-02-07T13:43:04.037512+00:00Z

============================================================
TEST A: HAPPY PATH (Multi-Titan Collab -> Gate Approve -> Sealed Bundle)
============================================================
[OK] Generated bearer token
[OK] Created workflow run: bea9e0e1-989c-4e54-84c4-48cdec9a577d
...
[OK] Test A passed: bea9e0e1-989c-4e54-84c4-48cdec9a577d

============================================================
TEST B: GATE DENY (Fail-Closed Semantics)
============================================================
...
[OK] Test B passed: f57650b0-1efd-44f2-b344-d2eb44ddf031

============================================================
TEST C: TITAN FAILURE (Timeout/Invalid Output)
============================================================
...
[OK] Test C passed: 3cf293c9-f704-4a42-b701-7cd3dd09a2f5

============================================================
GENERATING BUNDLE OUTPUT
============================================================
[OK] Manifest generated: PT-013-PBWB\manifest.json
[OK] Final artifact generated: PT-013-PBWB\final_artifact.md

============================================================
SUMMARY
============================================================
[OK] All tests completed
[OK] Total actions: 13
[OK] Bundle output: PT-013-PBWB
```

## Viewing Results

**Collaboration Ledgers:**
```bash
cat PT-013-PBWB/collaboration_ledger.jsonl
cat PT-013-PBWB/collaboration_ledger_test_b.jsonl
cat PT-013-PBWB/collaboration_ledger_test_c.jsonl
```

**RHID Manifest:**
```bash
cat PT-013-PBWB/manifest.json
```

**Evidence Pack:**
```bash
cat PT-013-PBWB/final_artifact.md
```

## Key Files

- **Test Harness:** `ops/proof/pt013/pt013_collab_executor.py`
- **Output:** `PT-013-PBWB/`
- **Documentation:** `REPORT/PROOFS/PT-013_*.md`

---


