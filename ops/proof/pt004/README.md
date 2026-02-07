# PT-004 Workflow Orchestration Test Harness

**Proof Campaign**: PT-004  
**Target**: Workflow Orchestration & Execution Spine  
**Status**: Ready for Execution  

---

## Overview

This test harness demonstrates that OMEGA workflows are:
1. **Born inside Federation Core** — Created via FC API
2. **Live inside Federation Core** — Every step governed by FC
3. **Die inside Federation Core** — Completion recorded with receipts
4. **Auditable** — Full immutable audit trail

---

## What It Tests

### Test A: Happy Path
All steps execute successfully without policy intervention.

```
PENDING → RUNNING (step_1) → RUNNING (step_2) → ... → COMPLETED
```

**Proves**: Step visibility, normal execution flow

### Test B: Policy Flag
Step 2 policy evaluation returns "flag", triggering pause/resume.

```
PENDING → RUNNING (step_1) → RUNNING (step_2) → PAUSED (gate) → RUNNING (step_3) → COMPLETED
```

**Proves**: Policy gates, pause/resume semantics, audit trail

### Test C: Policy Deny
Step 2 policy evaluation returns "deny", failing workflow.

```
PENDING → RUNNING (step_1) → RUNNING (step_2) → FAILED
```

**Proves**: Fail-closed behavior, policy enforcement

---

## Usage

### Prerequisites
```bash
pip install httpx
```

### Run All Tests
```bash
python pt004_workflow_executor.py
```

### Expected Output
```
🔱 PT-004 WORKFLOW ORCHESTRATION TEST HARNESS
Federation Core: http://federation_core:9405
Timestamp: 2026-02-06T...Z

============================================================
TEST A: HAPPY PATH (All Allow)
============================================================
✓ Created workflow run: <run_id>
✓ Step 1 started: step_1
✓ Step 1 executed
...
✓ Workflow completed

============================================================
TEST B: POLICY FLAG (Gate Required)
============================================================
✓ Created workflow run: <run_id>
✓ Step 1 executed
✓ Step 2 executed
✓ Workflow paused (policy flag)
✓ Workflow resumed after approval
✓ Workflow completed

============================================================
TEST C: POLICY DENY (Fail-Closed)
============================================================
✓ Created workflow run: <run_id>
✓ Step 1 executed
✓ Workflow failed (policy deny)

============================================================
SUMMARY
============================================================
✓ happy_path: <run_id>
✓ policy_flag: <run_id>
✓ policy_deny: <run_id>

✅ All tests completed successfully
```

---

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/workflows/runs` | POST | Create workflow run |
| `/workflows/runs/{run_id}/status` | PATCH | Update run status |
| `/workflows/runs/{run_id}` | GET | Get run with logs/gates |

---

## Configuration

Edit these constants in the script:

```python
FC_BASE_URL = "http://federation_core:9405"
TENANT_ID = "tenant_omega"
ACTOR_ID = "pt004_test_harness"
```

---

## Output Artifacts

The test harness produces:
- Run IDs for each test
- Audit trail entries (FC logs)
- Receipt hashes (in FC storage)

Capture these for the proof report:
```bash
# Get run details with audit trail
curl -s http://federation_core:9405/workflows/runs/{run_id}?include_logs=true | jq .

# Get FC logs
docker logs federation_core > fc_logs.txt
```

---

## Proof Report Integration

Use the run IDs and logs from this harness to populate:
`REPORT/PROOFS/PT-004_workflow_orchestration_PROOF_REPORT.md`

Include:
- Run IDs from each test
- Step visibility proof (log excerpts)
- Policy interaction proof (decision logs)
- Audit trail proof (immutable entries)

---

**This is the way.** 🔱

