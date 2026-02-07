# 🔱 PT-004 DIRECTIVE — Workflow Orchestration & Execution Spine

**Campaign**: OMEGA Proof Campaign  
**Proof Target**: PT-004  
**Status**: DIRECTIVE (Ready for Implementation)  
**Created**: 2026-02-06  

---

## 1) GOAL

Prove that **workflow execution** is:

* **Born inside Federation Core** — Workflows are created via FC API, not external runners
* **Lives inside Federation Core** — Every step executes under FC governance with policy evaluation
* **Dies inside Federation Core** — Completion/failure/pause recorded in FC storage with receipts
* **Step visibility** — Each step start/completion/failure is logged with timestamps and hashes
* **Policy gates** — Every step can be evaluated against governance policy (allow/deny/flag)
* **Pause/Resume/Retry** — First-class semantics for workflow control (not bolted-on)
* **Audit trail** — Immutable log of all state transitions with actor/timestamp/decision

**Proof Statement**: *Workflows are not routed through FC. They are governed by FC. Every step is a decision.*

---

## 2) FC ENDPOINTS TO HIT

All calls go to **Federation Core at `http://federation_core:9405`**.

### Workflow Lifecycle
- `POST /workflows/runs` — Create workflow run
- `GET /workflows/runs/{run_id}` — Get run status
- `PATCH /workflows/runs/{run_id}/status` — Update run status
- `POST /workflows/runs/{run_id}/steps` — Record step execution
- `GET /workflows/runs/{run_id}/logs` — Get audit trail

### Policy Gates
- `POST /workflows/runs/{run_id}/gates` — Request approval gate
- `PATCH /workflows/runs/{run_id}/gates/{gate_id}` — Resolve gate (approve/reject)

---

## 3) TEST WORKFLOW SPECIFICATION

**Workflow ID**: `pt004_execution_spine`  
**Steps**: 5 sequential steps with policy gates

1. **Step 1 (OBSERVE)**: Query registry for available agents
2. **Step 2 (DECIDE)**: Evaluate governance policy (allow/deny/flag)
3. **Step 3 (GATE)**: Request human approval (if flagged)
4. **Step 4 (ACT)**: Execute selected action
5. **Step 5 (TRANSFORM)**: Aggregate results

---

## 4) THREE VISIBILITY LAYERS (PROOF REQUIREMENTS)

### Layer 1: Step Visibility
- Each step has: `step_id`, `step_type`, `started_at`, `ended_at`, `status`
- Hashes: `input_hash`, `output_hash`, `receipt_hash`
- Logs show: "Step X started" → "Step X completed" with timestamps

### Layer 2: Policy Interaction
- Policy evaluation visible in logs (even if not blocking)
- Decision recorded: allow/deny/flag with reason
- Metadata shows policy_id, tier, rules_triggered

### Layer 3: Audit Trail
- Immutable log entries for every state change
- Actor ID, timestamp, decision, evidence_pack_ref
- Receipts chain: step_hash → workflow_hash

---

## 5) CONTROL FLOW TESTS (Minimum 3)

### Test A: Happy Path (All Allow)
- All steps execute successfully
- No gates triggered
- Workflow completes with COMPLETED status

### Test B: Policy Flag (Gate Required)
- Step 2 policy evaluation returns "flag"
- Workflow transitions to PAUSED
- Gate created and awaits approval
- Resume workflow after approval
- Workflow completes

### Test C: Policy Deny (Fail-Closed)
- Step 2 policy evaluation returns "deny"
- Workflow transitions to FAILED
- No further steps execute
- Audit trail shows denial reason

---

## 6) RECEIPT REQUIREMENTS

For each run:
- Workflow receipt (aggregated step hashes)
- Step receipts (input/output/decision hashes)
- Gate receipts (approval decision + actor)
- Audit log entries (immutable)

Store in: `REPORT/PROOFS/PT-004_workflow_orchestration/receipts/`

---

## 7) PROOF REPORT

Create: `REPORT/PROOFS/PT-004_workflow_orchestration_PROOF_REPORT.md`

Include:
- Timestamp, git SHA, image digest
- Test A/B/C results with run IDs
- Step visibility proof (log excerpts)
- Policy interaction proof (decision logs)
- Audit trail proof (immutable entries)
- Receipt chain validation
- Verdict

---

## 8) COMMIT + TAG

**Commit message**:
```
proof(pt-004): workflow orchestration + execution spine (step visibility, policy gates, audit trail)
```

**Tag**:
```
omega-proof-campaign-pt004
```

---

**This is the way.** 🔱

