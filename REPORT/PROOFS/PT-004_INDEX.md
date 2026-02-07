# PT-004 Index & Navigation Guide

**Campaign**: OMEGA Proof Campaign  
**Proof Target**: Workflow Orchestration & Execution Spine  
**Status**: ✅ COMPLETE - Ready for Execution  

---

## 📋 Document Index

### 1. **Directive** (START HERE)
**File**: `PT-004_workflow_orchestration_directive.md`

The authoritative specification. Contains:
- Goal: Prove workflows are born/live/die in FC
- FC endpoints to hit
- Test workflow specification (5 steps)
- Three visibility layers (step, policy, audit)
- Three control flow tests (happy path, flag, deny)
- Receipt requirements
- Proof report structure
- Commit & tag instructions

**Read Time**: 10 minutes  
**Purpose**: Understand what needs to be proven

---

### 2. **Implementation Summary** (OVERVIEW)
**File**: `PT-004_IMPLEMENTATION_SUMMARY.md`

Technical documentation. Contains:
- What was delivered
- FC endpoints identified
- Test harness implementation
- Three visibility layers explained
- Directory structure
- Execution checklist

**Read Time**: 5 minutes  
**Purpose**: Understand the technical implementation

---

### 3. **Quick Start** (EXECUTION GUIDE)
**File**: `PT-004_QUICK_START.md`

Step-by-step execution guide. Contains:
- Prerequisites checklist
- 7 execution steps
- Expected outputs
- Log capture instructions
- Proof report template
- Commit & tag commands
- Troubleshooting guide

**Read Time**: 5 minutes  
**Purpose**: Execute the tests and capture results

---

### 4. **Test Harness README** (SDK REFERENCE)
**File**: `ops/proof/pt004/README.md`

SDK documentation. Contains:
- Overview of what's tested
- Test A/B/C descriptions
- Usage instructions
- API endpoints used
- Configuration options
- Output artifacts
- Proof report integration

**Read Time**: 5 minutes  
**Purpose**: Understand the test harness

---

### 5. **Test Harness Code** (IMPLEMENTATION)
**File**: `ops/proof/pt004/pt004_workflow_executor.py`

Python test harness (150 lines). Implements:
- Async HTTP client for FC API
- Workflow run creation
- Status updates
- Audit trail retrieval
- Test A: Happy path
- Test B: Policy flag
- Test C: Policy deny

**Read Time**: 10 minutes  
**Purpose**: Understand the test implementation

---

### 6. **Proof Report** (TO CREATE)
**File**: `PT-004_workflow_orchestration_PROOF_REPORT.md`

Proof report (to be created after execution). Will contain:
- Execution summary (timestamp, git SHA)
- Test results (A/B/C with run IDs)
- Step visibility proof (log excerpts)
- Policy interaction proof (decision logs)
- Audit trail proof (immutable entries)
- Receipt chain validation
- Verdict

**Read Time**: 10 minutes  
**Purpose**: Prove the campaign succeeded

---

## 🎯 Execution Path

1. **Read Directive** (10 min)
   - Understand what needs to be proven
   - Review FC endpoints
   - Review test specifications

2. **Review Implementation Summary** (5 min)
   - Understand what was delivered
   - Review directory structure
   - Check execution checklist

3. **Review Quick Start** (5 min)
   - Understand execution steps
   - Check prerequisites
   - Plan execution timeline

4. **Execute Test Harness** (10 min)
   - Run happy path test
   - Run policy flag test
   - Run policy deny test
   - Capture outputs

5. **Capture Logs** (5 min)
   - Extract FC logs
   - Verify join keys present
   - Organize by test run

6. **Create Proof Report** (10 min)
   - Use template from Quick Start
   - Fill in all sections
   - Include log excerpts

7. **Commit & Tag** (2 min)
   - Stage all files
   - Commit with specified message
   - Create git tag
   - Push to remote

---

## 📁 Directory Structure

```
ops/proof/pt004/
├── pt004_workflow_executor.py    (Test harness)
└── README.md                      (SDK documentation)

REPORT/PROOFS/
├── PT-004_INDEX.md (this file)
├── PT-004_workflow_orchestration_directive.md
├── PT-004_IMPLEMENTATION_SUMMARY.md
├── PT-004_QUICK_START.md
├── PT-004_workflow_orchestration_PROOF_REPORT.md (to create)
└── PT-004_workflow_orchestration/
    ├── receipts/
    ├── happy_path.txt
    ├── policy_flag.txt
    └── policy_deny.txt
```

---

## ✅ Success Criteria

- [ ] All three tests execute successfully
- [ ] FC logs contain FC-RUN-* and FC-STEP-* events
- [ ] Receipts created in storage
- [ ] Proof report completed
- [ ] Commit and tag created
- [ ] All files pushed to remote

---

## 📞 Support

### If test harness fails
→ See: `PT-004_QUICK_START.md` (Troubleshooting section)

### If you need endpoint details
→ See: `PT-004_workflow_orchestration_directive.md` (Section 2)

### If you need SDK usage examples
→ See: `ops/proof/pt004/README.md`

---

## 🔗 Related Campaigns

- **PT-003**: Agent Registry & Capability Routing (foundation)
- **PT-005**: GATE_REQUIRED / human resume points (next)
- **PT-013**: Multi-Titan Collaboration (depends on PT-004)
- **PT-014**: Genesis Spawn (depends on PT-004)

---

**Estimated Time**: 60 minutes  
**Difficulty**: Medium  
**Status**: Ready to Execute  

**This is the way.** 🔱

