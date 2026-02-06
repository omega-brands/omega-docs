# PT-003 Quick Start Guide

**Proof Campaign**: Agent Registry & Capability Routing  
**Status**: Ready to Execute  
**Time to Complete**: ~15 minutes  

---

## Prerequisites

- ✅ Federation Core running on port 9405
- ✅ Python 3.8+ with httpx (`pip install httpx`)
- ✅ .NET 8.0 SDK (for C# SDK)
- ✅ Valid passport/HMAC token
- ✅ Docker with federation_core container

---

## Step 1: Run Python SDK (Loose Mode)

```bash
cd D:\Repos\OMEGA\omega-core

python ops/proof/pt003/pt003_route_agent.py --mode loose \
  > REPORT/PROOFS/PT-003_agent_registry_capability_routing/python_loose.txt 2>&1
```

**Expected Output**:
- Registry status (total_servers, active_servers)
- Discovered agents (≥2 agents with scores)
- Selected agent with run_id and confidence score
- JSON output with full response

---

## Step 2: Run Python SDK (Strict Mode)

```bash
python ops/proof/pt003/pt003_route_agent.py --mode strict \
  > REPORT/PROOFS/PT-003_agent_registry_capability_routing/python_strict.txt 2>&1
```

**Expected Output**: Same as loose mode, but with strict policy enforcement

---

## Step 3: Run Python SDK (Negative Test)

```bash
python ops/proof/pt003/pt003_route_agent.py --mode loose --negative \
  > REPORT/PROOFS/PT-003_agent_registry_capability_routing/python_negative_capability.txt 2>&1
```

**Expected Output**:
- Error response (404/deny/no route)
- Run ID still present
- Fail-closed behavior demonstrated

---

## Step 4: Run C# SDK (Loose Mode)

```bash
cd ops/proof/pt003/Pt003.RouteAgent

dotnet run -- --mode loose \
  > ../../../REPORT/PROOFS/PT-003_agent_registry_capability_routing/csharp_loose.txt 2>&1
```

**Expected Output**: Same as Python SDK

---

## Step 5: Run C# SDK (Strict Mode)

```bash
dotnet run -- --mode strict \
  > ../../../REPORT/PROOFS/PT-003_agent_registry_capability_routing/csharp_strict.txt 2>&1
```

**Expected Output**: Same as Python SDK strict mode

---

## Step 6: Capture Federation Core Logs

```bash
# Before running tests, start log capture
docker logs -f federation_core > REPORT/PROOFS/PT-003_agent_registry_capability_routing/logs/logs_fc_all.txt &

# After running all tests, stop log capture
# Then split logs by test:
# logs_fc_python_loose.txt
# logs_fc_python_strict.txt
# logs_fc_csharp_loose.txt
# logs_fc_csharp_strict.txt
# logs_fc_negative_capability.txt
```

---

## Step 7: Verify Outputs

```bash
# Check all output files exist
ls -la REPORT/PROOFS/PT-003_agent_registry_capability_routing/

# Verify JSON output in each file
grep -l "routing_result" REPORT/PROOFS/PT-003_agent_registry_capability_routing/*.txt
```

---

## Step 8: Create Proof Report

Create: `REPORT/PROOFS/PT-003_agent_registry_capability_routing_PROOF_REPORT.md`

Include:
```markdown
# PT-003 Proof Report

## Execution Summary
- Timestamp: [ISO 8601]
- Git SHA: [git rev-parse HEAD]
- Image Digest: [docker inspect federation_core]

## Test Results

### Python Loose Mode
- Run ID: [from output]
- Selected Agent: [agent_id]
- Confidence Score: [score]
- Status: ✅ PASS

### Python Strict Mode
- Run ID: [from output]
- Selected Agent: [agent_id]
- Confidence Score: [score]
- Status: ✅ PASS

### C# Loose Mode
- Run ID: [from output]
- Selected Agent: [agent_id]
- Status: ✅ PASS

### C# Strict Mode
- Run ID: [from output]
- Selected Agent: [agent_id]
- Status: ✅ PASS

### Negative Test (Non-existent Capability)
- Run ID: [from output]
- Expected: Fail-closed (404/deny)
- Actual: [result]
- Status: ✅ PASS

## Log Analysis

### Join Keys Found
- Primary: run_id (UUID format)
- Secondary: request_id (from headers)

### FC Endpoints Hit
- GET /servers/status ✅
- GET /agents/discover ✅
- POST /route ✅

### Policy Enforcement
- Loose mode: [observations]
- Strict mode: [observations]
- Differences: [list any differences]

## Receipts & Evidence
- Receipt IDs: [list any receipt IDs]
- Evidence Packs: [paths if any]

## Verdict
✅ **PASS** - Agent registry & capability routing via FC proven
```

---

## Step 9: Commit & Tag

```bash
git add ops/proof/pt003/ REPORT/PROOFS/PT-003_*

git commit -m "proof(pt-003): agent registry + capability routing via fc (policy-variant, receipted)"

git tag omega-proof-campaign-pt003

git push origin main --tags
```

---

## Troubleshooting

### Python SDK Fails
```bash
# Install httpx
pip install httpx

# Check FC is running
curl http://federation_core:9405/health

# Check token format
echo "Token: $PASSPORT_TOKEN"
```

### C# SDK Fails
```bash
# Check .NET version
dotnet --version

# Restore packages
dotnet restore

# Run with verbose output
dotnet run -- --mode loose --verbose
```

### No Agents Found
```bash
# Query registry directly
curl -H "Authorization: Bearer $TOKEN" \
  http://federation_core:9405/servers/status

# Check if agents are registered
curl -H "Authorization: Bearer $TOKEN" \
  http://federation_core:9405/omega/directory/servers
```

---

## Success Criteria

✅ Python SDK runs in loose and strict modes  
✅ C# SDK runs in loose and strict modes  
✅ Negative test case returns fail-closed response  
✅ All outputs captured to correct locations  
✅ FC logs contain join keys and routing decisions  
✅ Proof report completed with all sections  
✅ Commit and tag created  

---

## Files Created

```
ops/proof/pt003/
├── pt003_route_agent.py
├── README.md
└── Pt003.RouteAgent/
    ├── Program.cs
    └── Pt003.RouteAgent.csproj

REPORT/PROOFS/
├── PT-003_agent_registry_capability_routing_directive.md
├── PT-003_IMPLEMENTATION_SUMMARY.md
├── PT-003_QUICK_START.md (this file)
├── PT-003_agent_registry_capability_routing_PROOF_REPORT.md (to create)
└── PT-003_agent_registry_capability_routing/
    ├── logs/
    ├── python_loose.txt
    ├── python_strict.txt
    ├── python_negative_capability.txt
    ├── csharp_loose.txt
    └── csharp_strict.txt
```

---

**Estimated Time**: 15 minutes  
**Difficulty**: Medium  
**Status**: Ready to Execute  

**This is the way.** 🔱

