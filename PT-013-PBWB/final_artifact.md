# PT-013 Multi-Titan Collaboration — Evidence Pack

**Generated:** 2026-02-07T13:43:04.838767+00:00Z

## Executive Summary

This evidence pack proves **multi-Titan collaboration under FC-governed workflows** with:
- ✅ Action-level attribution ("who did what")
- ✅ Thin receipts (RHID-first, heavy payloads in objects)
- ✅ RHID pointers (Resource Hash IDs mapping to storage locations)
- ✅ Sealed bundle output (manifest + receipts + immutable objects)

## Collaboration Ledger

**Total Actions:** 13
**Unique Titans:** 4
**Gate Actions:** 4
**Seal Actions:** 1

### Action Sequence


#### Action 1: EXECUTE
- **Actor:** titan / claude_titan
- **Step:** step_1
- **Capabilities:** claude
- **Inputs:** 0 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:038a2879-030e-4355-b37b-713326e83851`
- **Prev Hash:** None

#### Action 2: EXECUTE
- **Actor:** titan / gemini_titan
- **Step:** step_2
- **Capabilities:** gemini
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:ede61fb5-a830-4661-a671-1376e1ef7199`
- **Prev Hash:** 4a4b5311653a0dc8...

#### Action 3: EXECUTE
- **Actor:** titan / gpt_titan
- **Step:** step_3
- **Capabilities:** gpt
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:556c774f-83f7-49a4-9665-4d06d9dd8cbf`
- **Prev Hash:** e10ba8eea4db854c...

#### Action 4: EXECUTE
- **Actor:** titan / grok_titan
- **Step:** step_4
- **Capabilities:** grok
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:a01ea374-f9d5-4b28-adf0-614eae5f64b3`
- **Prev Hash:** f04591292a461d6c...

#### Action 5: GATE_REQUEST
- **Actor:** fc / federation_core
- **Step:** step_5
- **Capabilities:** gate_management
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:d450901d-0193-4f75-9e0e-fa373f788572`
- **Prev Hash:** 69b87d7c09c6b051...

#### Action 6: GATE_RESOLVE
- **Actor:** human / approver_1
- **Step:** step_5
- **Capabilities:** approve
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:a92aab7a-4eca-4254-afc4-5b4ddaeaf4e8`
- **Prev Hash:** b0b43effc7bf7a98...
- **Policy Decision:** {"policy_id": "collab_approval", "tier": "human", "decision": "allow"}

#### Action 7: SEAL
- **Actor:** fc / federation_core
- **Step:** step_6
- **Capabilities:** seal
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:bdfed951-931e-4bc6-80a0-1b92aea95fb7`
- **Prev Hash:** 5bd1bacb96954828...

#### Action 1: EXECUTE
- **Actor:** titan / claude_titan
- **Step:** step_1
- **Capabilities:** claude
- **Inputs:** 0 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:5ac4ffc9-1dcb-4fee-a40b-4ae82ab0a3f1`
- **Prev Hash:** None

#### Action 2: EXECUTE
- **Actor:** titan / gemini_titan
- **Step:** step_2
- **Capabilities:** gemini
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:fbeb4710-8e75-46cb-abbe-a7b9f4a3a75d`
- **Prev Hash:** 9f2c245c6a7b8fa7...

#### Action 3: GATE_REQUEST
- **Actor:** fc / federation_core
- **Step:** step_3
- **Capabilities:** gate_management
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:006d1472-24ae-4ae6-8e9d-65203395dafe`
- **Prev Hash:** 987283b5b57e7e4e...

#### Action 4: GATE_RESOLVE
- **Actor:** human / approver_1
- **Step:** step_3
- **Capabilities:** approve
- **Inputs:** 1 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:6b72a352-c9de-434c-8eef-38b4fffa7195`
- **Prev Hash:** 01e65bbc82e37bfa...
- **Policy Decision:** {"policy_id": "security_gate", "tier": "human", "decision": "deny", "reason": "Security policy violation detected"}

#### Action 1: EXECUTE
- **Actor:** titan / claude_titan
- **Step:** step_1
- **Capabilities:** claude
- **Inputs:** 0 artifact(s)
- **Outputs:** 1 artifact(s)
- **Receipt RHID:** `rhid:receipt:469c81c2-daeb-4ac7-a029-06a112ccf213`
- **Prev Hash:** None

#### Action 2: EXECUTE
- **Actor:** titan / gemini_titan
- **Step:** step_2
- **Capabilities:** gemini
- **Inputs:** 1 artifact(s)
- **Outputs:** 0 artifact(s)
- **Receipt RHID:** `rhid:receipt:6b921d6e-b3da-4c6d-b5bb-1321fe62a87e`
- **Prev Hash:** b6dc935f41482a15...
- **Policy Decision:** {"error": "timeout", "reason": "Gemini execution exceeded 30s timeout"}


## RHID Manifest

**Total RHIDs:** 25

All RHIDs are resolvable via the manifest. Each RHID maps to:
- Content kind (receipt, artifact, gate, etc.)
- Creator actor ID
- Creation timestamp
- SHA256 hash for integrity verification

### Manifest Structure

```json
{
  "manifest_version": "1.0.0",
  "generated_at": "2026-02-07T13:43:04.834186+00:00",
  "rhid_count": 25,
  "rhids": {
    "rhid:receipt:...": {"kind": "receipt", "action_id": "...", ...},
    "rhid:artifact:...": {"kind": "artifact", "action_id": "...", ...},
    ...
  }
}
```

## Success Criteria

✅ **≥3 distinct Titan actor_ids in ledger:** 4 Titans
✅ **≥1 tool invocation action in ledger:** 8 execute actions
✅ **gate_request + gate_resolve actions exist:** 2 gate_request, 2 gate_resolve
✅ **100% RHID resolution via manifest:** 25 RHIDs mapped
✅ **Receipt chain integrity verified:** prev_action_hash chaining enabled
✅ **final_artifact.md exists and is referenced by RHID:** This document

## Fail-Closed Semantics

This evidence pack demonstrates **fail-closed semantics** across three test scenarios:

1. **Test A (Happy Path):** Multi-Titan collaboration with human gate approval → COMPLETED
2. **Test B (Gate Deny):** Human rejection stops workflow → FAILED (fail-closed)
3. **Test C (Titan Failure):** Titan timeout halts execution → FAILED (fail-closed)

All workflows default to denial/pause, not permission.

## Audit Trail

- **Workflow Runs:** 3 unique runs
- **Request IDs:** 3 unique requests
- **Actor Types:** fc, human, titan
- **Action Types:** execute, gate_request, gate_resolve, seal

---

**This is the way.** 🔱
