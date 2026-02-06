# PT-003: Agent Registry & Capability Routing Proof

**Status**: Ready for Implementation  
**Campaign**: OMEGA Proof Campaign  
**Proof Target**: Agent selection/routing via Federation Core  

---

## Overview

PT-003 proves that agent selection/routing is:
- ✅ Performed via **Federation Core** (port 9405)
- ✅ Based on **declared capabilities + registry state**
- ✅ **Policy-governed** (loose/strict modes)
- ✅ Observable via **container logs** with join keys
- ✅ Produces **receipts** and evidence packs

---

## Quick Start

### Python SDK

```bash
# Loose mode
python pt003_route_agent.py --mode loose

# Strict mode
python pt003_route_agent.py --mode strict

# Negative test (non-existent capability)
python pt003_route_agent.py --mode loose --negative
```

### C# SDK

```bash
cd Pt003.RouteAgent

# Loose mode
dotnet run -- --mode loose

# Strict mode
dotnet run -- --mode strict

# Negative test
dotnet run -- --mode loose --negative
```

---

## Federation Core Endpoints

### Registry Lookup
- **`GET /servers/status`** — Query registry status
  - Returns: total_servers, active_servers, stale_servers
  - Purpose: Prove ≥2 eligible agents exist

- **`GET /omega/directory/servers`** — List registered servers
  - Query params: tag, capability, q, page, limit
  - Returns: Server manifests with capabilities

### Routing Decision
- **`POST /route`** — Intelligent task routing
  - Request: {capability, preferred_tags, exclude_agents, tenant_id, run_id}
  - Response: Selected agent with rationale, confidence score

- **`GET /agents/discover`** — Capability-based discovery
  - Query params: capability, exclude_agents, include_performance, max_results
  - Returns: Ranked agents with scores and metrics

---

## Test Data

### Capability
- **Primary**: `llm.generate_response` (discovered in PT-001)
- **Negative**: `capability.DOES_NOT_EXIST` (fail-closed test)

### Policy Modes
- **Loose**: Permissive routing, minimal validation
- **Strict**: Strict validation, policy enforcement

---

## Output Capture

### Python Outputs
```
REPORT/PROOFS/PT-003_agent_registry_capability_routing/
  python_loose.txt
  python_strict.txt
  python_negative_capability.txt
```

### C# Outputs
```
REPORT/PROOFS/PT-003_agent_registry_capability_routing/
  csharp_loose.txt
  csharp_strict.txt
```

### Logs
```
REPORT/PROOFS/PT-003_agent_registry_capability_routing/logs/
  logs_fc_python_loose.txt
  logs_fc_python_strict.txt
  logs_fc_csharp_loose.txt
  logs_fc_csharp_strict.txt
  logs_fc_negative_capability.txt
```

---

## Proof Report

Create: `REPORT/PROOFS/PT-003_agent_registry_capability_routing_PROOF_REPORT.md`

Include:
- Timestamp, git SHA, image digest
- Policy mode per run
- Join keys (run_id/request_id)
- SDK commands used
- FC endpoints hit
- Routing outputs
- Negative-case result
- Log excerpts
- Receipt/evidence paths
- Verdict

---

## Commit & Tag

```bash
git add ops/proof/pt003/ REPORT/PROOFS/PT-003_*
git commit -m "proof(pt-003): agent registry + capability routing via fc (policy-variant, receipted)"
git tag omega-proof-campaign-pt003
```

---

## Requirements

- Python 3.8+ with httpx
- .NET 8.0 SDK (for C# SDK)
- Federation Core running on port 9405
- Valid passport/HMAC token for authentication

---

## Next Steps

1. ✅ Directive created
2. ✅ Python SDK created
3. ✅ C# SDK created
4. ⏳ Run both SDKs in loose and strict modes
5. ⏳ Capture logs from federation_core container
6. ⏳ Create negative test case
7. ⏳ Generate proof report
8. ⏳ Commit and tag

**This is the way.** 🔱

