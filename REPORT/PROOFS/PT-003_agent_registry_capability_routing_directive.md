# 🔱 PT-003 DIRECTIVE — Agent Registry & Capability Routing

**Campaign**: OMEGA Proof Campaign  
**Proof Target**: PT-003  
**Status**: DIRECTIVE (Ready for Implementation)  
**Created**: 2026-02-06  

---

## 1) GOAL

Prove that **agent selection/routing** is:

* Performed via **Federation Core** (port 9405)
* Based on **declared capabilities + registry state**
* **Policy-governed** (loose/strict modes)
* Observable via **container logs** with join keys (`run_id` or `request_id`)
* Produces **receipts** (and evidence packs if supported)

**Proof Statement**: *The chooser is real. The choice is traceable. The policy is enforced.*

---

## 2) FC ENDPOINTS TO HIT

All calls go to **Federation Core at `http://federation_core:9405`**.

### Registry Lookup Endpoints
- **`GET /servers/status`** — Query registry status and eligible agents/servers
  - Returns: `total_servers`, `active_servers`, `stale_servers`, `timestamp`
  - Purpose: Prove at least 2 eligible agents exist for tested capability

- **`GET /omega/directory/servers`** — List all registered servers with filtering
  - Query params: `tag`, `capability`, `q`, `page`, `limit`
  - Returns: Server manifests with capabilities, tags, endpoints
  - Purpose: Discover servers matching capability

### Routing Decision Endpoints
- **`POST /route`** — Intelligent task routing (documented in diagrams)
  - Request: `{task, requirements, capability, preferred_tags?, exclude_agents?, tenant_id?}`
  - Response: Selected agent/server with rationale, confidence score, registry snapshot
  - Purpose: Perform capability-based agent selection

- **`GET /agents/discover`** — Capability-based agent discovery
  - Query params: `capability`, `exclude_agents`, `include_performance`, `max_results`
  - Returns: Ranked list of agents with scores, capabilities, performance metrics
  - Purpose: Discover agents matching capability

---

## 3) SDK PATHS (Both Required)

### Python SDK
**Path**: `ops/proof/pt003/pt003_route_agent.py`

Must:
- Authenticate via real passport/HMAC (use PT-000 passport strategy)
- Query `/servers/status` to prove ≥2 eligible agents
- Submit routing request to `/route` with:
  - `capability`: `"llm.generate_response"` (from PT-001 discovered tools)
  - `preferred_tags`: `["llm_routing", "core_service"]` (optional)
  - `exclude_agents`: `[]` (optional)
  - `tenant_id`: `"omega"` (if required)
- Print: `run_id`, selected `agent_id`/`server_id`, selection rationale, registry snapshot
- Run in **loose** and **strict** policy modes

### C# SDK
**Path**: `ops/proof/pt003/Pt003.RouteAgent/Program.cs`

Same outputs as Python. Capture stdout to:
```
REPORT/PROOFS/PT-003_agent_registry_capability_routing/
  python_loose.txt
  python_strict.txt
  csharp_loose.txt
  csharp_strict.txt
```

---

## 4) TEST DATA / REGISTRY PRECONDITIONS

Before routing:
- Query `/servers/status` via FC
- Prove **≥2 eligible agents** exist for tested capability
- OR prove only 1 exists and **explicitly record limitation**

PT-003 passes with 1 agent, but limitation must be noted for PT-003-R1 (Genesis spawn).

---

## 5) POLICY VARIATIONS (Minimum 2)

Run routing under:
- **Loose** mode
- **Strict** mode

Policy must affect something:
- Selection changes, OR
- Metadata differs (redaction/justification), OR
- Strict introduces deny/mitigate behavior

If no differences: acceptable only if receipts show policy-mode and report explains why.

---

## 6) LOG REQUIREMENTS

**Join Keys**:
- Primary: `run_id` (if returned)
- Secondary: `request_id` (from FC SecurityEvents)

**Containers**:
- `federation_core` (mandatory)
- Registry service (if separate)
- Router/planner/orchestrator (if in path)

**Save logs to**:
```
REPORT/PROOFS/PT-003_agent_registry_capability_routing/logs/
  logs_fc_python_loose.txt
  logs_fc_python_strict.txt
  logs_fc_csharp_loose.txt
  logs_fc_csharp_strict.txt
```

**Required excerpts**:
- Request accepted by FC
- Auth passed
- Registry consulted / candidates enumerated
- Routing decision produced
- Receipt persisted

---

## 7) RECEIPT / EVIDENCE REQUIREMENTS

For each run:
- Capture `ReceiptId` / audit reference
- Store paths in proof report

If evidence pack produced:
```
REPORT/EVIDENCE_PACKS/PT-003/<timestamp>/...
```

No evidence pack? Still must have receipts + FC logs.

---

## 8) NEGATIVE ROUTING CASE (Fail-Closed Proof)

Request non-existent capability: `"capability.DOES_NOT_EXIST"`

Expected:
- FC returns governed failure (404/deny/structured "no route")
- Receipt still written
- Logs show decision and fail-closed behavior

Save:
```
REPORT/PROOFS/PT-003_agent_registry_capability_routing/python_negative_capability.txt
REPORT/PROOFS/PT-003_agent_registry_capability_routing/logs/logs_fc_negative_capability.txt
```

---

## 9) KILL-SWITCH REQUIREMENT

Kill-switch family: **ROUTING_REGISTRY**

PT-000 already proved global FC kill-switch. **Do not repeat** unless routing hits non-FC ports.

---

## 10) PROOF REPORT

Create: `REPORT/PROOFS/PT-003_agent_registry_capability_routing_PROOF_REPORT.md`

Include:
- Timestamp, git SHA, image digest
- Policy mode per run
- Join keys (`run_id`/`request_id`)
- SDK commands used
- FC endpoints hit
- Routing outputs (agent selected + rationale)
- Negative-case result
- Log excerpts
- Receipt/evidence paths
- Verdict

---

## 11) COMMIT + TAG

**Commit message**:
```
proof(pt-003): agent registry + capability routing via fc (policy-variant, receipted)
```

**Tag**:
```
omega-proof-campaign-pt003
```

---

## NEXT STEPS

1. ✅ Directive created (this file)
2. Create Python SDK at `ops/proof/pt003/pt003_route_agent.py`
3. Create C# SDK at `ops/proof/pt003/Pt003.RouteAgent/Program.cs`
4. Run both SDKs in loose and strict modes
5. Capture logs from federation_core container
6. Create negative test case
7. Generate proof report
8. Commit and tag

**This is the way.** 🔱

