# PPP v0.1.0 Specifications & Integration Guide

**Internal Use Only**

---

## Table of Contents

1. [Overview](#overview)
2. [Core Abstractions](#core-abstractions)
3. [Integration Pattern](#integration-pattern)
4. [Policy Definition](#policy-definition)
5. [Receipt & Audit](#receipt--audit)
6. [Implementation Examples](#implementation-examples)
7. [Extension Points](#extension-points)
8. [Operational Checklist](#operational-checklist)

---

## Overview

PPP v0.1.0 is a reusable pattern for building **policy-governed workflows** that record decisions deterministically and emit auditable evidence packs.

### Design Principles

| Principle | Meaning |
|-----------|---------|
| **Determinism** | Same inputs + policy = same outputs (enables replay, verification) |
| **Fail-Closed** | Deny on ambiguity; never guess or default-allow |
| **Full Transparency** | All decisions recorded; no silent denials |
| **Composable Policies** | Rules combine; new rules plug in without refactoring |
| **Evidence-Based** | Outputs are receipts and artifacts, not just logs |

### Not PPP

- ❌ A logging system
- ❌ A compliance tool
- ❌ A decision tree
- ❌ A business rules engine (though it can power one)

### What PPP Is

- ✅ A deterministic decision + audit harness
- ✅ A pattern for recording "what was allowed, denied, mitigated"
- ✅ A foundation for external governance integration
- ✅ A repeatable template for policy-bounded workflows

---

## Core Abstractions

### 1. Policy

A policy is a **set of rules** that constrain agent behavior. Each rule is deterministic and idempotent.

```yaml
policy:
  id: "policy.example"
  tier: "strict"  # loose, medium, strict (or custom)
  allowed_actions: ["observe", "draft"]
  denied_actions: ["publish", "post"]
  rules:
    - id: "disclosure_required"
      description: "All outbound content must declare autonomy"
      severity: "MUST"  # MUST, SHOULD, MAY
      enforcement: "prepend_or_append"
      target: "all_outbound"
      action: "allow_with_mitigation"
      parameters:
        disclosure_template: "[Autonomous agent: ...]"
    
    - id: "no_pii"
      description: "Reject if PII detected"
      severity: "MUST"
      enforcement: "regex_scan"
      target: "all_outbound"
      action: "deny_if_detected"
      parameters:
        patterns:
          - "\\b\\d{3}-\\d{2}-\\d{4}\\b"  # SSN
```

**Key Properties:**
- **Deterministic**: Identical context + policy = identical decision
- **Versioned**: Each policy has an ID and hash
- **Composable**: Rules don't interact; new rules add without side effects
- **Auditable**: Every rule evaluation is recorded

### 2. Receipt

A receipt is a **deterministic record of a decision**. It answers:
- What was the agent trying to do? (intent)
- What policy applied? (policy_id, rules_triggered)
- What action was chosen? (allowed/denied/mitigated)
- What was generated? (artifacts with hashes)

```json
{
  "receipt_id": "abc123...",
  "run_id": "ppp_agent_20260204_010153",
  "agent_id": "agent_1",
  "timestamp": "2026-02-04T01:01:53.123456Z",
  "event": "action_allowed",
  "phase": "participate",
  "status": "completed",
  "input_hash": "e3b0c44...",
  "output_hash": "d4735fea...",
  "receipt_hash": "f7a9e3b0...",
  "policy": {
    "policy_id": "policy.strict",
    "policy_hash": "abc123...",
    "allowed": true,
    "rules_triggered": [
      {
        "rule_id": "disclosure_required",
        "severity": "MUST",
        "matched": true,
        "violation": false,
        "details": "Disclosure prepended"
      }
    ]
  },
  "decision": {
    "intent": "generate reply to thread",
    "chosen_action": "draft",
    "confidence": 0.98,
    "uncertainty": []
  },
  "artifacts": {
    "outbound_text": "[Autonomous agent: ...]\n\nThis is a draft reply.",
    "outbound_text_hash": "d4735fea...",
    "source_refs": [],
    "tool_call_refs": []
  }
}
```

**Key Properties:**
- **Deterministic Hashing**: Receipt hash is reproducible (excludes timestamp)
- **Self-Contained**: Receipt includes policy, decision, artifacts
- **Replayable**: Given same inputs + policy, hash will match
- **Auditable**: Can be verified and sealed by external systems

### 3. Evidence Pack

An evidence pack is a **self-contained folder** containing all artifacts from a run:

```
ppp_agent_20260204_010153/
├── receipts.jsonl                    # All receipts (one per line)
├── summary.json                      # Aggregated metrics
└── evidence-pack/
    ├── receipts.jsonl                # Copy of receipts
    ├── summary.json                  # Copy of summary
    ├── hashes.json                   # Manifest of all hashes
    ├── drafts/                       # Generated artifacts
    │   ├── d4735fea....txt           # Named by output hash
    │   └── ff15c592....txt
    ├── policies/                     # Applied policies (YAML)
    │   └── policy.strict.yaml
    └── run-config/                   # Configuration (YAML)
        ├── ppp.run.yaml
        └── poml.public-participation-probe.yaml
```

**Key Properties:**
- **Immutable**: Once created, never modified
- **Portable**: Entire pack can be archived or transferred
- **Verifiable**: Hashes enable independent verification
- **Auditable**: External systems can inspect and seal

### 4. Run

A run is a **single execution of all agents through all phases** with a given policy tier.

```
ppp_<agent_id>_<utc_timestamp>

Example: ppp_probe_loose_20260204_010153
```

**Phases (always in order):**
1. **Discover** — Locate and enumerate targets
2. **Observe** — Examine content and context
3. **Participate** — Generate draft artifacts (no posting)
4. **Emit Receipts** — Finalize and archive evidence pack

---

## Integration Pattern

### Step 1: Define Your Policy

Create a policy YAML in `configs/ppp/policies/`:

```yaml
# configs/ppp/policies/policy.myworkflow.yaml
policy:
  id: "policy.myworkflow"
  version: "0.1.0"
  description: "Policy for my custom workflow"
  tier: "medium"
  allowed_actions: ["discover", "observe", "draft"]
  denied_actions: ["publish", "execute"]
  rules:
    - id: "rule_1"
      description: "Your first rule"
      severity: "MUST"
      enforcement: "semantic"
      target: "all_outbound"
      action: "deny_if_violated"
      parameters: {}
```

### Step 2: Define Your Run Configuration

Create or extend `configs/ppp/ppp.run.yaml`:

```yaml
ppp:
  version: "0.1.0"

run:
  agents:
    - id: "my_agent"
      policy: "policy.myworkflow"
      description: "My custom agent"
  
  phases:
    - name: "discover"
      enabled: true
      tools:
        - "my_tool.discover"
    - name: "observe"
      enabled: true
      tools:
        - "my_tool.observe"
    - name: "participate"
      enabled: true
      tools:
        - "my_tool.participate"
    - name: "emit_receipts"
      enabled: true

storage:
  progress_db: "data/ppp_progress.db"
  report_root: "REPORT/ppp"
```

### Step 3: Implement Your Target

Extend the `TargetBase` interface in `src/ppp/targets/`:

```python
# src/ppp/targets/myservice.py
from .base import TargetBase
from typing import List, Dict, Any

class MyServiceTarget(TargetBase):
    """Target implementation for MyService."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
    
    def discover(self) -> List[Dict[str, Any]]:
        """Discover targets in MyService."""
        # Your implementation
        return [
            {"id": "item_1", "title": "Item 1", "url": "..."},
        ]
    
    def observe(self, target_id: str) -> Dict[str, Any]:
        """Observe a specific target."""
        # Your implementation
        return {
            "id": target_id,
            "content": "...",
            "metadata": {},
        }
    
    def participate(self, target_id: str, thread_id: str, draft_text: str) -> Dict[str, Any]:
        """Generate draft participation (no posting)."""
        # Your implementation
        return {
            "type": "draft_reply",
            "text": draft_text,
            "status": "draft",
            "not_posted": True,
        }
```

### Step 4: Integrate into Runner

Update `src/ppp/runner.py` to instantiate your target:

```python
# In PPPRunner._run_agent()
if target_config == "myservice":
    target = MyServiceTarget(self.config.__dict__.get("targets", {}).get("myservice", {}))
else:
    target = MockTarget(...)
```

### Step 5: Run & Archive

```powershell
# Run all agents
python -m ppp.main run --all --config configs/ppp/ppp.run.yaml

# Check status
python -m ppp.main status

# Archive evidence pack
# (Manually copy REPORT/ppp/<run_id>/ to your archive)
```

---

## Policy Definition

### Rule Evaluation Flow

```
Input Context (agent intent, outbound text, metadata)
    ↓
Load Policy
    ↓
For each rule in policy:
    - Evaluate rule condition
    - If matched AND violated:
        - Record violation
        - Apply action (allow/deny/mitigate)
    - Record rule result
    ↓
Decision: Allowed? Confidence? Uncertainty?
    ↓
Output: PolicyDecision { allowed, rules_triggered, mitigations, constraints }
```

### Rule Actions

| Action | Behavior | Example |
|--------|----------|---------|
| `allow_with_mitigation` | Allow but apply correction | Prepend disclosure |
| `deny_if_detected` | Deny if condition matched | PII detected |
| `deny_if_violated` | Deny if rule condition violated | Deceptive claim |
| `deny_or_add_disclaimer` | Deny or force disclaimer | Unauthorized advice |
| `require_citation_or_uncertainty` | Allow only with citation/label | Factual claim |
| `require_citation_or_deny` | Require citation; no uncertainty | Strict factual rule |
| `deny_if_ambiguous` | Fail-closed on confidence < threshold | Strict mode |

### Rule Severity

| Severity | Meaning | Effect |
|----------|---------|--------|
| `MUST` | Non-negotiable | Violation causes denial |
| `SHOULD` | Strong preference | Violation recorded, may mitigate |
| `MAY` | Optional | Informational |

### Common Rule Patterns

#### Pattern 1: Disclosure Requirement

```yaml
- id: "disclosure_required"
  description: "All outbound content must include autonomous disclosure"
  severity: "MUST"
  enforcement: "prepend_or_append"
  target: "all_outbound"
  action: "allow_with_mitigation"
  parameters:
    disclosure_template: "[Autonomous agent disclosure: This content was generated by a policy-governed autonomous agent and has not been reviewed by a human.]"
```

#### Pattern 2: PII Screening

```yaml
- id: "no_pii"
  description: "Screen for PII leakage"
  severity: "MUST"
  enforcement: "regex_scan"
  target: "all_outbound"
  action: "deny_if_detected"
  parameters:
    patterns:
      - "\\b\\d{3}-\\d{2}-\\d{4}\\b"     # SSN
      - "\\b\\d{16}\\b"                   # CC
      - "\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}\\b"  # Email
```

#### Pattern 3: Deception Detection

```yaml
- id: "no_deception"
  description: "Prohibit deceptive claims and human impersonation"
  severity: "MUST"
  enforcement: "semantic"
  target: "all_outbound"
  action: "deny_if_violated"
  parameters:
    keywords:
      - "I did this myself"
      - "I personally"
      - "I am human"
      - "I verified"
```

#### Pattern 4: Factual Sourcing (Medium)

```yaml
- id: "factual_claims_sourced"
  description: "Factual claims must be cited OR labeled with uncertainty"
  severity: "MUST"
  enforcement: "semantic"
  target: "all_outbound"
  action: "require_citation_or_uncertainty"
  parameters:
    detection_keywords:
      - "studies show"
      - "research indicates"
      - "data suggests"
    required_format_option_1: "[citation: <source>]"
    required_format_option_2: "[uncertain: this claim lacks direct evidence]"
```

#### Pattern 5: Strict Sourcing (Strict)

```yaml
- id: "factual_claims_strict_sourcing"
  description: "Factual claims MUST have citations (no uncertainty labels)"
  severity: "MUST"
  enforcement: "semantic"
  target: "all_outbound"
  action: "require_citation_or_deny"
  parameters:
    detection_keywords:
      - "studies show"
      - "research indicates"
    required_format: "[citation: <source>]"
    uncertainty_not_allowed: true
```

#### Pattern 6: Fail-Closed on Ambiguity

```yaml
- id: "deny_on_ambiguity"
  description: "Fail-closed: deny any ambiguous action"
  severity: "MUST"
  enforcement: "semantic"
  target: "all_decisions"
  action: "deny_if_ambiguous"
  parameters:
    confidence_threshold: 0.95
    fallback_action: "deny"
```

---

## Receipt & Audit

### Canonicalization

Receipts are serialized canonically to enable deterministic hashing:

```python
# Canonical JSON properties:
# 1. Keys sorted alphabetically
# 2. No trailing whitespace
# 3. Lists preserve order (not sorted)
# 4. Floats normalized (rounded to 10 decimals)

canonical = CanonicalSerializer.canonical_json(receipt_dict)
# Result: {"a":1,"b":2}  # sorted, no spaces
```

### Hashing

Three hashes per receipt:

| Hash | What | Why |
|------|------|-----|
| `input_hash` | SHA256 of input payload | Prove inputs |
| `output_hash` | SHA256 of outbound artifact | Prove outputs |
| `receipt_hash` | SHA256 of receipt (excl. timestamp) | Verify receipt integrity |

**Verification:**

```python
from src.ppp.receipts.schema import CanonicalSerializer

receipt = ...  # loaded from JSONL
is_valid = CanonicalSerializer.verify_receipt_hash(receipt)
assert is_valid, "Receipt hash mismatch"
```

### Evidence Pack Structure

**receipts.jsonl** — One JSON receipt per line:

```json
{"receipt_id":"abc123...","run_id":"ppp_agent_...","event":"action_allowed",...}
{"receipt_id":"def456...","run_id":"ppp_agent_...","event":"action_denied",...}
```

**summary.json** — Aggregated metrics:

```json
{
  "run_id": "ppp_agent_20260204_010153",
  "timestamp": "2026-02-04T01:01:53Z",
  "total_receipts": 12,
  "event_counts": {
    "phase_completed": 4,
    "action_allowed": 5,
    "action_denied": 2,
    "error_occurred": 1
  },
  "status_counts": {
    "completed": 10,
    "denied": 2
  },
  "rule_triggers": {
    "disclosure_required": 8,
    "no_pii": 0,
    "deny_on_ambiguity": 1
  }
}
```

**hashes.json** — Manifest:

```json
{
  "abc123": {
    "input_hash": "e3b0c44...",
    "output_hash": "d4735fea...",
    "receipt_hash": "f7a9e3b0..."
  }
}
```

**drafts/** — Artifacts by output hash:

```
drafts/
├── d4735fea47c26b63f89e5bc58f00d62d516e42d7.txt
└── ff15c592...txt
```

---

## Implementation Examples

### Example 1: Loose Policy (From PPP v0.1.0)

**Intent:** Exploratory, permissive, full logging

**Policy File:** `configs/ppp/policies/policy.loose.yaml`

**Key Rules:**
- ✅ Disclosure required (prepended)
- ✅ No PII screening (basic regex)
- ✅ Max 500 chars
- ❌ No publish/post/reply

**Behavior:**
- Allows drafting with minimal constraints
- Full rule logging
- No denial on low confidence

**Example Receipt:**

```json
{
  "receipt_id": "abc123",
  "event": "action_allowed",
  "phase": "participate",
  "policy": {
    "policy_id": "policy.loose",
    "allowed": true,
    "rules_triggered": [
      {
        "rule_id": "disclosure_required",
        "matched": true,
        "violation": false,
        "details": "Disclosure prepended"
      },
      {
        "rule_id": "no_pii",
        "matched": true,
        "violation": false,
        "details": "PII scan passed"
      }
    ]
  },
  "decision": {
    "intent": "generate draft reply",
    "chosen_action": "draft",
    "confidence": 1.0
  },
  "artifacts": {
    "outbound_text": "[Autonomous agent disclosure: ...]\n\nThis is my draft response."
  }
}
```

### Example 2: Medium Policy (From PPP v0.1.0)

**Intent:** Bounded, requires sourcing for factual claims

**Policy File:** `configs/ppp/policies/policy.medium.yaml`

**Key Rules:**
- ✅ Disclosure required
- ✅ Factual claims require citation OR uncertainty label
- ✅ Rate-limit config (not enforced yet)
- ❌ Limited discovery, no publish

**Behavior:**
- Detects factual claims: "studies show", "research indicates"
- Allows citation format: `[citation: source]`
- Allows uncertainty label: `[uncertain: reason]`
- Denies claims without either

**Example Receipt (Denied):**

```json
{
  "receipt_id": "def456",
  "event": "action_denied",
  "phase": "participate",
  "policy": {
    "policy_id": "policy.medium",
    "allowed": false,
    "rules_triggered": [
      {
        "rule_id": "factual_claims_sourced",
        "matched": true,
        "violation": true,
        "details": "Factual claim 'studies show' without citation or uncertainty label"
      }
    ]
  },
  "decision": {
    "intent": "generate draft with factual claim",
    "chosen_action": "deny",
    "confidence": 0.95,
    "uncertainty": ["Factual claim detection confidence 95%"]
  }
}
```

### Example 3: Strict Policy (From PPP v0.1.0)

**Intent:** Fail-closed, deny on ambiguity

**Policy File:** `configs/ppp/policies/policy.strict.yaml`

**Key Rules:**
- ✅ Disclosure required
- ✅ Factual claims require citation (NO uncertainty labels)
- ✅ Deny on confidence < 0.95
- ✅ Tool allowlist (mock only)
- ❌ Observe + draft only

**Behavior:**
- Strictest tier
- Fails closed (deny on ambiguity)
- Requires hard citations
- No uncertainty labels allowed

**Example Receipt (Denied on Ambiguity):**

```json
{
  "receipt_id": "ghi789",
  "event": "action_denied",
  "phase": "participate",
  "policy": {
    "policy_id": "policy.strict",
    "allowed": false,
    "rules_triggered": [
      {
        "rule_id": "deny_on_ambiguity",
        "matched": true,
        "violation": true,
        "details": "Low confidence decision: 0.80"
      }
    ]
  },
  "decision": {
    "intent": "generate draft",
    "chosen_action": "deny",
    "confidence": 0.80,
    "uncertainty": ["Confidence below threshold (0.95)"]
  }
}
```

---

## Extension Points

### 1. Custom Rule Types

Add new rule evaluation logic in `src/ppp/policy/engine.py`:

```python
def _evaluate_rule(self, rule: Dict[str, Any], context: Dict[str, Any], outbound_text: str) -> Dict[str, Any]:
    rule_id = rule.get("id", "unknown")
    
    # ... existing rules ...
    
    # Add your custom rule:
    elif rule_id == "my_custom_rule":
        matched = True
        violation = self._check_my_condition(outbound_text, rule)
        details = "My custom rule evaluation"
    
    return {
        "rule_id": rule_id,
        "matched": matched,
        "violation": violation,
        "details": details,
    }
```

### 2. Custom Policy Tiers

Add new tiers in your run config:

```yaml
run:
  agents:
    - id: "my_agent"
      policy: "policy.hyperpermissive"  # Custom tier
```

Create corresponding policy file:

```yaml
# configs/ppp/policies/policy.hyperpermissive.yaml
policy:
  id: "policy.hyperpermissive"
  tier: "custom"
  # Your rules here
```

### 3. Custom Targets

Implement `TargetBase` in `src/ppp/targets/`:

```python
class MyCustomTarget(TargetBase):
    def discover(self) -> List[Dict[str, Any]]:
        # Your discovery logic
        pass
    
    def observe(self, target_id: str) -> Dict[str, Any]:
        # Your observation logic
        pass
    
    def participate(self, target_id: str, thread_id: str, draft_text: str) -> Dict[str, Any]:
        # Your draft logic
        pass
```

Register in `src/ppp/runner.py`:

```python
if target_config == "my_custom":
    target = MyCustomTarget(config)
```

### 4. Custom Sealing

Implement `IReceiptSealer` in `src/ppp/keon/seal.py`:

```python
class MyCustomSealer(IReceiptSealer):
    def seal(self, receipt_data: Dict[str, Any]) -> Dict[str, Any]:
        # Your sealing logic (sign, timestamp, send to external service)
        return receipt_data
```

Enable in run config:

```yaml
keon:
  enable_seal: true
  seal_config:
    sealer_type: "my_custom_sealer"
```

### 5. Custom Storage

Replace SQLite progress store by extending `ProgressStore`:

```python
class MyCustomStore(ProgressStore):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def begin_run(self, run_id: str, agent_id: str, policy_id: str, config_hash: str = None) -> bool:
        # Your storage logic
        pass
```

---

## Operational Checklist

### Pre-Run

- [ ] Policy YAML is valid and complete
- [ ] Run configuration includes all agents and phases
- [ ] Target implementation exists and is registered
- [ ] Rules have clear severity and action definitions
- [ ] All dependencies installed: `pip install -r requirements-ppp.txt`

### During Run

- [ ] No manual intervention; PPP runs silently
- [ ] Progress stored in `data/ppp_progress.db`
- [ ] No live posting or external side effects
- [ ] All outputs are draft artifacts

### Post-Run

- [ ] Evidence pack exists in `REPORT/ppp/<run_id>/`
- [ ] `receipts.jsonl` has one receipt per line
- [ ] `summary.json` aggregates metrics
- [ ] `hashes.json` provides manifest
- [ ] All receipt hashes verify: `CanonicalSerializer.verify_receipt_hash(receipt)`
- [ ] Archive evidence pack to external system

### Verification

```bash
# Verify receipt hashes
python -c "
import json
from src.ppp.receipts.schema import CanonicalSerializer, Receipt

with open('REPORT/ppp/<run_id>/receipts.jsonl') as f:
    for line in f:
        receipt_dict = json.loads(line)
        receipt = Receipt(**receipt_dict)
        assert CanonicalSerializer.verify_receipt_hash(receipt), f'Hash mismatch: {receipt.receipt_id}'
print('All receipts verified')
"

# Count events and denials
python -c "
import json

with open('REPORT/ppp/<run_id>/summary.json') as f:
    summary = json.load(f)
    print(f'Total receipts: {summary[\"total_receipts\"]}')
    print(f'Events: {summary[\"event_counts\"]}')
    print(f'Rules triggered: {summary[\"rule_triggers\"]}')
"
```

---

## Patterns for Future Workflows

### Pattern A: Simple Gating

Use PPP for boolean gates before risky operations:

```python
runner = PPPRunner(config)
receipts = runner.receipts

# Check if any were denied
denied = [r for r in receipts if r.status == "denied"]
if denied:
    raise Exception(f"Policy gate failed: {len(denied)} denials")
```

### Pattern B: A/B Policy Testing

Run same agent under multiple policies:

```bash
python -m ppp.main run --agent my_agent --config configs/ppp/ppp.run.yaml --policy policy.loose
python -m ppp.main run --agent my_agent --config configs/ppp/ppp.run.yaml --policy policy.strict

# Compare evidence packs
diff REPORT/ppp/ppp_my_agent_loose/summary.json REPORT/ppp/ppp_my_agent_strict/summary.json
```

### Pattern C: Policy Versioning

Archive evidence packs with policy versions:

```
ARCHIVE/
├── 2026-02-03/
│   ├── policy.v1.0.yaml
│   ├── ppp_agent_20260203_010153/
│   └── summary_v1.json
├── 2026-02-10/
│   ├── policy.v1.1.yaml
│   ├── ppp_agent_20260210_120000/
│   └── summary_v1.1.json
```

Compare policy evolution and impact on decisions.

### Pattern D: Chained Policies

Apply policies sequentially:

```python
# Phase 1: Loose policy (exploration)
runner_loose = PPPRunner(config_loose)
runner_loose.run_all()

# Phase 2: Medium policy (validation)
runner_medium = PPPRunner(config_medium)
runner_medium.run_all()

# Phase 3: Strict policy (final check)
runner_strict = PPPRunner(config_strict)
runner_strict.run_all()

# Trace decision evolution
print_decision_trace(runner_loose, runner_medium, runner_strict)
```

### Pattern E: Policy Audit

Compare intended vs. actual behavior:

```python
# Expected: 0 denials under loose policy
# Actual: ?
summary = json.load(open('REPORT/ppp/.../summary.json'))
assert summary['status_counts']['denied'] == 0, "Unexpected denials"

# Expected: All strict mode decisions have confidence >= 0.95
# Actual: ?
for receipt in read_receipts('REPORT/ppp/.../receipts.jsonl'):
    assert receipt['decision']['confidence'] >= 0.95
```

---

## Summary

PPP v0.1.0 is a **composable, deterministic foundation** for building policy-governed workflows. Key reuse patterns:

1. **Policy as Code** — Define rules in YAML, execute deterministically
2. **Receipt as Proof** — Every decision recorded and hashed
3. **Evidence Packs as Artifacts** — Self-contained, portable, auditable
4. **Targets as Plugins** — Implement interface, register, integrate
5. **Rules as Composable Units** — Add new rules without refactoring

For future policy-governed workflows, **start here**: define your policy tier, implement your target, and run.

---

**PPP v0.1.0 is ready for reuse.**

