# PT-017-B: Test Scenarios for Policy Automation

---

## Scenario 1: VERIFY_FAIL Trigger

**Goal:** Prove policy auto-revokes on receipt verification failure.

### Steps

1. Create entity with invalid/missing birth receipt
2. Trigger policy evaluation with VERIFY_FAIL condition
3. Verify PolicyEvaluator returns REVOCATION_RECOMMENDED
4. Verify AutomationGuardrails pass (human gate, cooldown, entity state)
5. Call revoke_entity through PolicyAutomationOrchestrator
6. Verify FC_GENESIS_REVOKED event includes policy_version + automation flag
7. Verify ledger shows policy attribution

### Acceptance Criteria

- ✅ Policy evaluation triggered on verify-fail
- ✅ REVOCATION_RECOMMENDED result
- ✅ Guardrails enforced (human gate required)
- ✅ FC event includes policy_version, automation=true, trigger_events
- ✅ Ledger shows policy_id and policy_version
- ✅ Receipt chain verified

---

## Scenario 2: POST_DEATH_ACTION Trigger

**Goal:** Prove policy auto-terminates on dead entity invocation.

### Steps

1. Create and revoke entity (Scenario 1 result)
2. Attempt to invoke revoked entity
3. Trigger policy evaluation with POST_DEATH_ACTION condition
4. Verify PolicyEvaluator returns REVOCATION_INITIATED (AUTO_TERMINATE severity)
5. Call terminate_entity through PolicyAutomationOrchestrator
6. Verify FC_GENESIS_TERMINATED event includes policy attribution
7. Verify ledger shows automation=true

### Acceptance Criteria

- ✅ Policy evaluation triggered on post-death-action
- ✅ REVOCATION_INITIATED result (AUTO_TERMINATE)
- ✅ Guardrails enforced
- ✅ FC event includes policy context
- ✅ Ledger shows policy attribution
- ✅ Entity fully terminated

---

## Scenario 3: INVALID_MANIFEST Trigger

**Goal:** Prove policy auto-revokes on manifest integrity violation.

### Steps

1. Create entity with valid manifest
2. Simulate manifest drift (hash mismatch)
3. Trigger policy evaluation with INVALID_MANIFEST condition
4. Verify PolicyEvaluator returns REVOCATION_RECOMMENDED
5. Verify guardrails pass
6. Call revoke_entity
7. Verify FC event includes trigger_events array

### Acceptance Criteria

- ✅ Policy evaluation triggered on invalid-manifest
- ✅ REVOCATION_RECOMMENDED result
- ✅ FC event includes trigger_events with manifest violation details
- ✅ Ledger shows policy attribution
- ✅ Receipt chain verified

---

## Scenario 4: DRIFT Trigger

**Goal:** Prove policy auto-revokes on state divergence.

### Steps

1. Create entity with known state
2. Simulate state divergence (detected via ledger audit)
3. Trigger policy evaluation with DRIFT condition
4. Verify PolicyEvaluator returns REVOCATION_RECOMMENDED
5. Verify guardrails enforce cooldown (prevent flapping)
6. Call revoke_entity
7. Verify cooldown prevents immediate re-evaluation

### Acceptance Criteria

- ✅ Policy evaluation triggered on drift
- ✅ REVOCATION_RECOMMENDED result
- ✅ Cooldown enforced (no flapping)
- ✅ FC event includes policy context
- ✅ Ledger shows policy attribution
- ✅ Cooldown prevents re-trigger within period

---

## Scenario 5: LIFECYCLE_EVENT Trigger

**Goal:** Prove policy auto-revokes on specific FC event types.

### Steps

1. Create entity
2. Emit specific FC event (e.g., FC_GENESIS_BIRTH_FAILED)
3. Trigger policy evaluation with LIFECYCLE_EVENT condition
4. Verify PolicyEvaluator returns REVOCATION_RECOMMENDED
5. Verify human gate requirement enforced
6. Call revoke_entity
7. Verify FC event includes trigger_events with lifecycle event ID

### Acceptance Criteria

- ✅ Policy evaluation triggered on lifecycle-event
- ✅ REVOCATION_RECOMMENDED result
- ✅ Human gate requirement enforced
- ✅ FC event includes trigger_events array
- ✅ Ledger shows policy attribution
- ✅ Receipt chain verified

---

## Scenario 6: Fail-Closed Ambiguity Cases

**Goal:** Prove fail-closed behavior on ambiguous conditions.

### Case 6a: Missing Birth Receipt

- Create entity without birth receipt in ledger
- Trigger policy evaluation
- Verify PolicyEvaluator returns NO_ACTION (fail-closed)
- Verify no revocation initiated

### Case 6b: Incomplete Ledger

- Create entity with incomplete ledger state
- Trigger policy evaluation
- Verify PolicyEvaluator returns NO_ACTION (fail-closed)
- Verify no revocation initiated

### Case 6c: Already-Dead Entity

- Create and revoke entity
- Trigger policy evaluation on dead entity
- Verify AutomationGuardrails.check_entity_state() returns failed
- Verify no revocation initiated

### Case 6d: Cooldown Violation

- Create entity and trigger revocation
- Immediately trigger policy evaluation again
- Verify AutomationGuardrails.check_cooldown() returns failed
- Verify NO_ACTION (fail-closed on cooldown)

### Acceptance Criteria (All Cases)

- ✅ PolicyEvaluator returns NO_ACTION
- ✅ No revocation initiated
- ✅ No FC event emitted
- ✅ Ledger unchanged
- ✅ Fail-closed behavior confirmed

---

## Evidence Checklist

- [ ] `fc_logs_excerpt.txt` contains all FC_GENESIS_* events with policy attribution
- [ ] `policy_evaluations.json` shows all 5 trigger types + 4 fail-closed cases
- [ ] `ledger_extract.json` shows policy_version, automation flag in death events
- [ ] `receipts/` contains birth + revoke/terminate receipts with chains
- [ ] `assertions/policy_attribution.json` verifies FC event fields
- [ ] `assertions/fail_closed_cases.json` verifies NO_ACTION on ambiguity
- [ ] `assertions/guardrail_enforcement.json` verifies human gate + cooldown
- [ ] `manifest.json` contains SHA256 hashes of all evidence files

---

**This is the way. 🔱**

