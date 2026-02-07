# PT-013 Index

**Proof:** Multi-Titan Collaboration (Proof-Backed Workflow Policy Pack)  
**Status:** ✅ COMPLETE  
**Date:** 2026-02-07  

## Documentation Files

### Core Proof Documents

1. **PT-013_MULTI_TITAN_COLLAB_DIRECTIVE.md**
   - Original mission statement
   - Required artifacts and success criteria
   - Rule of law (no mocks, no emulators)

2. **PT-013_IMPLEMENTATION_SUMMARY.md**
   - Implementation approach
   - Test harness design
   - Data structures and RHID format
   - Success criteria met

3. **PT-013_EXECUTION_SUMMARY.md**
   - Test results (all 3 tests passed)
   - Metrics and observations
   - Bundle output files

4. **PT-013_EXECUTION_PROOF_REPORT.md**
   - Thesis statement
   - Evidence for each requirement
   - Success criteria table
   - Conclusion

5. **PT-013_QUICK_START.md**
   - How to run the tests
   - Expected output
   - How to view results

### Verification & Seal Documents (Added for audit-grade closure)

6. **PT-013_FC_LOG_EXCERPTS.md**
   - Live FC container log lines per run_id
   - Status transitions, gate create/resolve, HTTP evidence
   - Container image digest

7. **PT-013_TITAN_LOG_EXCERPTS.md**
   - Titan invocation proof (harness → FC architecture)
   - Per-test action tables with receipt RHIDs
   - FC HTTP timestamp evidence

8. **PT-013_RECEIPT_CHAIN_VERIFICATION.md**
   - Receipt chain integrity per test
   - SHA256 hash verification
   - Manifest receipt summary

9. **PT-013_CAMPAIGN_COMPLETE.md**
   - Campaign status, git binding, FC container info

### Output Artifacts

**Location:** `PT-013-PBWB/`

- `collaboration_ledger.jsonl` - Test A (7 actions)
- `collaboration_ledger_test_b.jsonl` - Test B (4 actions)
- `collaboration_ledger_test_c.jsonl` - Test C (2 actions)
- `manifest.json` - RHID manifest (25 RHIDs)
- `final_artifact.md` - Evidence pack

### Test Harness

**Location:** `ops/proof/pt013/pt013_collab_executor.py`

- 700+ lines
- 3 test functions (happy path, gate deny, titan failure)
- Bundle generation functions
- Real FC API integration

## Key Concepts

### RHID (Resource Hash ID)
Format: `rhid:<kind>:<uuid>`

Kinds:
- `receipt` - Action receipt
- `artifact` - Output artifact
- `gate` - Approval gate
- `llm` - LLM invocation
- `toolio` - Tool I/O
- `policy` - Policy decision
- `logslice` - Log slice

### Action Types
- `execute` - Titan execution
- `gate_request` - FC requests approval
- `gate_resolve` - Human approves/rejects
- `seal` - FC seals bundle
- `propose`, `transform`, `decide`, `validate` - Other action types

### Actor Types
- `titan` - Claude, Gemini, GPT, Grok
- `human` - Human approver
- `fc` - Federation Core
- `tool`, `service`, `agent` - Other actors

## Success Metrics

✅ 4 distinct Titan actor_ids (required: ≥3)  
✅ 8 tool invocation actions (required: ≥1)  
✅ 2 gate_request + 2 gate_resolve (required: ≥1 pair)  
✅ 25 RHIDs mapped (100% resolution)  
✅ Receipt chain integrity verified  
✅ final_artifact.md generated  

## Related Proofs

- **PT-004:** Workflow Orchestration Execution Spine
- **PT-005:** Explicit GATE_REQUIRED Ergonomics
- **PT-013:** Multi-Titan Collaboration (this proof)
- **PT-014:** Genesis Spawning (future)

---

**This is the way.** 🔱

