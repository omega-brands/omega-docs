# PT-003 Index & Navigation Guide

**Campaign**: OMEGA Proof Campaign  
**Proof Target**: Agent Registry & Capability Routing  
**Status**: ✅ COMPLETE - Ready for Execution  

---

## 📋 Document Index

### 1. **Directive** (START HERE)
**File**: `PT-003_agent_registry_capability_routing_directive.md`

The authoritative specification document. Contains:
- Goal statement and proof objectives
- Exact Federation Core endpoints
- SDK implementation requirements
- Test data preconditions
- Policy variation requirements
- Log capture strategy
- Receipt/evidence requirements
- Negative test case specification
- Kill-switch requirements
- Proof report structure
- Commit & tag instructions

**Read Time**: 10 minutes  
**Purpose**: Understand what needs to be proven

---

### 2. **Quick Start Guide** (EXECUTE THIS)
**File**: `PT-003_QUICK_START.md`

Step-by-step execution guide. Contains:
- Prerequisites checklist
- 9 execution steps with commands
- Expected outputs for each step
- Log capture instructions
- Proof report template
- Commit & tag commands
- Troubleshooting guide
- Success criteria

**Read Time**: 5 minutes  
**Purpose**: Execute the proof campaign

---

### 3. **Implementation Summary** (TECHNICAL DETAILS)
**File**: `PT-003_IMPLEMENTATION_SUMMARY.md`

Technical documentation. Contains:
- What was delivered
- Federation Core endpoints identified
- SDK implementation details
- Documentation overview
- Directory structure
- Test capability specifications
- Policy mode definitions
- Next steps for execution
- Key design decisions
- Compliance checklist

**Read Time**: 10 minutes  
**Purpose**: Understand the technical implementation

---

### 4. **Delivery Summary** (OVERVIEW)
**File**: `PT-003_DELIVERY_SUMMARY.md`

High-level delivery overview. Contains:
- Executive summary
- Deliverables list
- Federation Core endpoints
- Directory structure
- Test specifications
- Execution checklist
- Key features
- Compliance verification
- Time estimates
- Next steps

**Read Time**: 5 minutes  
**Purpose**: Get an overview of what was delivered

---

### 5. **SDK Documentation** (REFERENCE)
**File**: `ops/proof/pt003/README.md`

SDK reference documentation. Contains:
- Overview of PT-003
- Quick start for Python SDK
- Quick start for C# SDK
- Federation Core endpoints
- Test data specifications
- Output capture locations
- Proof report requirements
- Commit & tag instructions
- Requirements and next steps

**Read Time**: 5 minutes  
**Purpose**: Reference for SDK usage

---

## 🚀 Quick Navigation

### I want to...

**...understand what PT-003 proves**
→ Read: `PT-003_agent_registry_capability_routing_directive.md` (Section 1)

**...execute the proof campaign**
→ Read: `PT-003_QUICK_START.md` (Follow all 9 steps)

**...understand the technical implementation**
→ Read: `PT-003_IMPLEMENTATION_SUMMARY.md`

**...get an overview of deliverables**
→ Read: `PT-003_DELIVERY_SUMMARY.md`

**...reference SDK usage**
→ Read: `ops/proof/pt003/README.md`

**...understand Federation Core endpoints**
→ Read: `PT-003_agent_registry_capability_routing_directive.md` (Section 2)

**...see the Python SDK code**
→ View: `ops/proof/pt003/pt003_route_agent.py`

**...see the C# SDK code**
→ View: `ops/proof/pt003/Pt003.RouteAgent/Program.cs`

---

## 📁 File Structure

```
REPORT/PROOFS/
├── PT-003_INDEX.md (this file)
├── PT-003_agent_registry_capability_routing_directive.md
├── PT-003_QUICK_START.md
├── PT-003_IMPLEMENTATION_SUMMARY.md
├── PT-003_DELIVERY_SUMMARY.md
├── PT-003_agent_registry_capability_routing_PROOF_REPORT.md (to create)
└── PT-003_agent_registry_capability_routing/
    ├── logs/
    ├── python_loose.txt
    ├── python_strict.txt
    ├── python_negative_capability.txt
    ├── csharp_loose.txt
    └── csharp_strict.txt

ops/proof/pt003/
├── pt003_route_agent.py
├── README.md
└── Pt003.RouteAgent/
    ├── Program.cs
    └── Pt003.RouteAgent.csproj
```

---

## 🎯 Execution Path

1. **Read Directive** (10 min)
   - Understand what needs to be proven
   - Review Federation Core endpoints
   - Review test specifications

2. **Review Quick Start** (5 min)
   - Understand execution steps
   - Check prerequisites
   - Plan execution timeline

3. **Execute SDKs** (15 min)
   - Run Python SDK (loose, strict, negative)
   - Run C# SDK (loose, strict)
   - Capture outputs

4. **Capture Logs** (5 min)
   - Extract federation_core logs
   - Organize by test run
   - Verify join keys present

5. **Create Proof Report** (10 min)
   - Use template from Quick Start
   - Fill in all sections
   - Include log excerpts

6. **Commit & Tag** (2 min)
   - Stage all files
   - Commit with specified message
   - Create git tag

**Total Time**: ~47 minutes

---

## 🔑 Key Concepts

### Federation Core
- Service discovery backbone
- Maintains agent/tool registry
- Provides capability-based routing
- Enforces policy governance
- Runs on port 9405

### Capability Routing
- Agents declare capabilities
- Requests specify required capability
- FC matches request to capable agents
- Selection based on capability + performance
- Policy mode affects selection criteria

### Policy Modes
- **Loose**: Permissive, minimal validation
- **Strict**: Strict validation, policy enforcement

### Join Keys
- **Primary**: run_id (UUID)
- **Secondary**: request_id (from headers)
- Used for log correlation and traceability

### Test Capabilities
- **Primary**: `llm.generate_response` (from PT-001)
- **Negative**: `capability.DOES_NOT_EXIST` (fail-closed test)

---

## ✅ Success Criteria

- [ ] All SDKs execute successfully
- [ ] Outputs captured to correct locations
- [ ] FC logs contain join keys
- [ ] Negative test returns fail-closed response
- [ ] Proof report completed
- [ ] Commit and tag created
- [ ] All files pushed to remote

---

## 📞 Support

### If SDKs fail to run
→ See: `PT-003_QUICK_START.md` (Troubleshooting section)

### If you need endpoint details
→ See: `PT-003_agent_registry_capability_routing_directive.md` (Section 2)

### If you need SDK usage examples
→ See: `ops/proof/pt003/README.md`

### If you need technical details
→ See: `PT-003_IMPLEMENTATION_SUMMARY.md`

---

## 🔱 The Way

This proof campaign demonstrates:
- ✅ Agent selection is real (not hardcoded)
- ✅ Selection is based on capabilities
- ✅ Policy governance is enforced
- ✅ Decisions are traceable via logs
- ✅ Receipts prove compliance

**Status**: Ready to execute  
**Difficulty**: Medium  
**Time**: ~47 minutes  

**This is the way.** 🔱

---

## Version History

| Date | Status | Changes |
|------|--------|---------|
| 2026-02-06 | ✅ COMPLETE | Initial delivery - all documents and SDKs created |

---

**Last Updated**: 2026-02-06  
**Next Review**: After execution completion

