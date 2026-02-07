# PT-004 Quick Start Guide

**Estimated Time**: 20 minutes  
**Difficulty**: Medium  
**Status**: Ready to Execute  

---

## Prerequisites

- [ ] Federation Core running at `http://federation_core:9405`
- [ ] Python 3.9+ with `httpx` installed
- [ ] Access to FC logs (docker logs federation_core)
- [ ] Git repository ready for commit

---

## Step 1: Review Directive (5 min)

Read: `REPORT/PROOFS/PT-004_workflow_orchestration_directive.md`

Key points:
- Workflows are born/live/die in FC
- Three visibility layers: step, policy, audit
- Three tests: happy path, policy flag, policy deny

---

## Step 2: Verify FC is Running (2 min)

```bash
curl -s http://federation_core:9405/health | jq .
```

Expected: `{"status": "healthy"}`

---

## Step 3: Run Test Harness (10 min)

```bash
cd ops/proof/pt004
python pt004_workflow_executor.py
```

Expected output:
```
✓ Created workflow run: <run_id>
✓ Step 1 started: step_1
✓ Step 1 executed
...
✓ Workflow completed
✓ All tests completed successfully
```

---

## Step 4: Capture Logs (3 min)

```bash
docker logs federation_core > REPORT/PROOFS/PT-004_workflow_orchestration/logs/fc_logs.txt
```

Verify logs contain:
- "FC-RUN-001" (run created)
- "FC-RUN-002" (status changed)
- "FC-STEP-001" (step started)
- "FC-STEP-002" (step completed)

---

## Step 5: Verify Receipts (2 min)

Check storage for receipts:
```bash
ls -la artifacts/receipts/pt004_execution_spine/
```

Expected: Receipt files with hashes

---

## Step 6: Create Proof Report (5 min)

Create: `REPORT/PROOFS/PT-004_workflow_orchestration_PROOF_REPORT.md`

Include:
```markdown
# PT-004 Proof Report

## Execution Summary
- Timestamp: [ISO 8601]
- Git SHA: [git rev-parse HEAD]

## Test Results

### Test A: Happy Path
- Run ID: [from output]
- Status: ✅ PASS
- Steps executed: 5
- Audit entries: [count]

### Test B: Policy Flag
- Run ID: [from output]
- Status: ✅ PASS
- Pause/resume: ✓
- Gate created: ✓

### Test C: Policy Deny
- Run ID: [from output]
- Status: ✅ PASS
- Fail-closed: ✓

## Visibility Proof

### Layer 1: Step Visibility
[Log excerpts showing step start/end]

### Layer 2: Policy Interaction
[Log excerpts showing policy evaluation]

### Layer 3: Audit Trail
[Log excerpts showing immutable entries]

## Verdict
✅ PT-004 PASS
```

---

## Step 7: Commit & Tag (2 min)

```bash
git add REPORT/PROOFS/PT-004_*
git add ops/proof/pt004/
git commit -m "proof(pt-004): workflow orchestration + execution spine (step visibility, policy gates, audit trail)"
git tag omega-proof-campaign-pt004
git push origin main --tags
```

---

## Troubleshooting

### FC not responding
```bash
docker-compose logs federation_core | tail -50
```

### Test harness fails
- Check FC is running: `curl http://federation_core:9405/health`
- Check network: `docker network ls`
- Check logs: `docker logs federation_core`

### Receipts not found
- Check storage path: `ls -la artifacts/receipts/`
- Check FC logs for errors

---

## Success Criteria

- [ ] All three tests execute successfully
- [ ] FC logs contain FC-RUN-* and FC-STEP-* events
- [ ] Receipts created in storage
- [ ] Proof report completed
- [ ] Commit and tag created
- [ ] All files pushed to remote

---

**This is the way.** 🔱

