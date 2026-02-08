# PT-016-B: Test Scenarios

---

## Scenario A: Revoke (Human-Gated)

**Goal:** Prove governed revocation path with explicit human approval.

### Steps

1. Create/ensure a birthed entity exists (use Genesis path from PT-014)
2. Call `revoke_entity` MCP tool (requires PT-005-style gate)
3. Approve gate (human decision)
4. Verify FC emits `FC_GENESIS_REVOKED` event
5. Verify ledger has death row with FK → birth row
6. Verify receipt chain: death receipt chains to birth receipt
7. Attempt to invoke the entity post-revocation → must fail

### Acceptance Criteria

- ✅ `revoke_entity` MCP tool called successfully
- ✅ Gate created with status `PENDING`
- ✅ Gate approved by human actor
- ✅ `FC_GENESIS_REVOKED` event emitted in FC logs
- ✅ Ledger shows: `death.birth_event_id = birth.birth_event_id`
- ✅ Receipt chain verified: `death.birth_receipt_hash = birth.receipt_hash`
- ✅ Post-revocation invocation blocked with error
- ✅ Evidence captured: FC logs, ledger extract, receipts, verification output

### Evidence Checklist

- [ ] `fc_logs_excerpt.txt` contains `FC_GENESIS_REVOKED`
- [ ] `ledger_extract.json` shows birth + death rows with FK linkage
- [ ] `receipts/birth_receipt.json` has `receipt_hash`
- [ ] `receipts/revoke_receipt.json` has `birth_receipt_hash` field
- [ ] `receipts/verification_output.json` shows chain verified
- [ ] `assertions/post_death_block.json` shows invocation blocked

---

## Scenario B: Terminate (System)

**Goal:** Prove system termination path (auto-approved authority).

### Steps

1. Create/ensure a birthed entity exists
2. Trigger `terminate_entity` MCP tool (auto-approved, system enforcement)
3. Verify FC emits `FC_GENESIS_TERMINATED` event
4. Verify ledger + FK linkage
5. Verify receipt chain to birth receipt
6. Attempt post-death invoke → must hard fail

### Acceptance Criteria

- ✅ `terminate_entity` MCP tool called successfully
- ✅ Gate created with status `APPROVED` (auto-approved)
- ✅ `FC_GENESIS_TERMINATED` event emitted in FC logs
- ✅ Ledger shows: `death.birth_event_id = birth.birth_event_id`
- ✅ Receipt chain verified: `death.birth_receipt_hash = birth.receipt_hash`
- ✅ Post-termination invocation blocked with hard error
- ✅ Evidence captured: FC logs, ledger extract, receipts, verification output

### Evidence Checklist

- [ ] `fc_logs_excerpt.txt` contains `FC_GENESIS_TERMINATED`
- [ ] `ledger_extract.json` shows birth + death rows with FK linkage
- [ ] `receipts/terminate_receipt.json` has `birth_receipt_hash` field
- [ ] `receipts/verification_output.json` shows chain verified
- [ ] `assertions/post_death_block.json` shows hard invocation failure

---

## Scenario C: Fail-Closed Receipt Integrity

**Goal:** Prove fail-closed behavior when birth receipt missing.

### Steps

1. Simulate missing birth receipt reference (without mutating history)
   - E.g., attempt verify with deliberately incomplete evidence set
2. Ensure verification fails **hard** (no recovery paths)
3. Capture verification output

### Acceptance Criteria

- ✅ Verification fails when birth receipt missing
- ✅ Error message indicates fail-closed behavior
- ✅ No recovery or bypass paths attempted
- ✅ Verification output captured

### Evidence Checklist

- [ ] `receipts/verification_output.json` shows failure reason
- [ ] Error message contains "fail-closed" or "integrity violation"
- [ ] No recovery attempts logged

---

## Scenario D: No Silent Deletion

**Goal:** Demonstrate that "death" always produces FC run + gate/event + ledger.

### Steps

1. Attempt any "delete-like" operation (if any exists)
2. Confirm it routes through governed flow OR is blocked
3. Confirm evidence shows:
   - FC event (FC_GENESIS_REVOKED or FC_GENESIS_TERMINATED)
   - Ledger record (death row with FK linkage)
   - Receipt chain (death receipt chained to birth)

### Acceptance Criteria

- ✅ No silent deletion paths exist
- ✅ All death routes through FC governance
- ✅ FC event emitted
- ✅ Ledger record created
- ✅ Receipt chain established

### Evidence Checklist

- [ ] `assertions/no_silent_delete.json` lists all checks performed
- [ ] FC event confirmed in logs
- [ ] Ledger record confirmed
- [ ] Receipt chain confirmed

---

## Evidence Bundle Structure

```
REPORT/PROOFS/PT-016-B-HARNESS/EVIDENCE/
  run_<timestamp>/
    manifest.json                    # Master manifest with hashes
    steps.jsonl                      # Action sequence (one per line)
    fc_logs_excerpt.txt              # Minimal FC log excerpt
    ledger_extract.json              # Birth + death + linkage rows
    receipts/
      birth_receipt.json             # Birth receipt from PT-014
      revoke_receipt.json            # Revocation receipt (Scenario A)
      terminate_receipt.json         # Termination receipt (Scenario B)
      verification_output.json       # Receipt chain verification
    assertions/
      post_death_block.json          # Post-death invocation block proof
      no_silent_delete.json          # No silent deletion checks
```

---

## Manifest Schema

```json
{
  "manifest_version": "1.0.0",
  "generated_at": "2026-02-07T...",
  "omega_core_repo": "https://github.com/m0r6aN/omega-core",
  "omega_core_tag": "omega-proof-campaign-pt016-runtime",
  "omega_core_commit": "46898b2...",
  "omega_docs_repo": "https://github.com/m0r6aN/omega-docs",
  "omega_docs_branch": "chore/proof-harness-pt016-b",
  "omega_docs_commit": "<commit_sha>",
  "fc_image_digest": "sha256:...",
  "scenarios": ["A", "B", "C", "D"],
  "file_hashes": {
    "steps.jsonl": "sha256:...",
    "fc_logs_excerpt.txt": "sha256:...",
    "ledger_extract.json": "sha256:...",
    "receipts/birth_receipt.json": "sha256:...",
    "receipts/revoke_receipt.json": "sha256:...",
    "receipts/terminate_receipt.json": "sha256:...",
    "receipts/verification_output.json": "sha256:...",
    "assertions/post_death_block.json": "sha256:...",
    "assertions/no_silent_delete.json": "sha256:..."
  }
}
```

---

**Family is forever. Death is governed. This is the way.** 🔱

