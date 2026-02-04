# PPP Policy Merge Strategy

**Version: v0.1.0**

## Overview

When multiple policies are applied (chained policies, policy inheritance, or multi-tier evaluation), the merge strategy determines how conflicts are resolved.

## Core Strategy: Restrictive Override

**Principle:** If any policy component rejects an action, the entire decision is rejection.

```
Policy A: ALLOW with mitigations
Policy B: DENY
─────────────────────────────
Result: DENY
```

## Decision Matrix

| Policy A | Policy B | Result | Rationale |
|----------|----------|--------|-----------|
| ALLOW | ALLOW | ALLOW | No conflict |
| ALLOW | MITIGATE | MITIGATE | Apply both mitigations |
| ALLOW | DENY | DENY | Conservative (most restrictive wins) |
| MITIGATE | MITIGATE | MITIGATE | Combine all mitigations |
| MITIGATE | DENY | DENY | Conservative |
| DENY | DENY | DENY | Denied by either rule |

## Implementation Pattern

```python
def merge_policy_decisions(decision_a: PolicyDecision, decision_b: PolicyDecision) -> PolicyDecision:
    """Merge two policy decisions using restrictive override."""
    
    # If either disallows, the result is deny
    if not decision_a.allowed or not decision_b.allowed:
        return PolicyDecision(
            allowed=False,
            rules_triggered=decision_a.rules_triggered + decision_b.rules_triggered,
            mitigations=decision_a.mitigations + decision_b.mitigations,
            confidence=min(decision_a.confidence, decision_b.confidence),
            uncertainty=decision_a.uncertainty + decision_b.uncertainty,
        )
    
    # If both allow, combine mitigations
    return PolicyDecision(
        allowed=True,
        rules_triggered=decision_a.rules_triggered + decision_b.rules_triggered,
        mitigations=decision_a.mitigations + decision_b.mitigations,
        confidence=min(decision_a.confidence, decision_b.confidence),
        uncertainty=decision_a.uncertainty + decision_b.uncertainty,
    )
```

## Conflict Resolution Examples

### Example 1: Loose + Strict Chaining

**Scenario:** Run agent through loose policy, then strict policy on same draft.

```
Loose Policy:
  - Disclosure required: ALLOW (with prepend)
  - No PII: ALLOW

Strict Policy:
  - Disclosure required: ALLOW
  - Deny on confidence < 0.95: DENY (confidence=0.80)

Result: DENY
Rationale: Strict policy is more conservative; applies override
```

### Example 2: Factual Claims Medium + Strict

**Scenario:** Same draft evaluated by medium and strict policies.

**Draft:** "Studies show [uncertain: limited evidence] that X is true."

```
Medium Policy:
  - Factual claims sourced: ALLOW (uncertainty label provided)

Strict Policy:
  - Factual claims strict sourcing: DENY (no citation, only uncertainty)

Result: DENY
Rationale: Strict requires citation; uncertainty label insufficient
```

### Example 3: Multiple Mitigations

**Scenario:** Two policies both require mitigations.

```
Policy A:
  - Disclosure required: ALLOW (add prefix)

Policy B:
  - Content length limit: ALLOW (truncate to 500 chars)

Result: ALLOW
Mitigations Applied:
  1. Add disclosure prefix
  2. Truncate to 500 chars

Final Output: Disclosure prefix + content (truncated) + suffix
```

## When to Use Merge Strategy

### Use Merge When:

✅ Chaining policies through phases  
✅ A/B testing policy variants  
✅ Policy inheritance (base + override)  
✅ Multi-tier evaluation (quick + deep)

### Don't Merge When:

❌ Single policy per run (current v0.1.0 pattern)  
❌ Policies applied sequentially without combining results  
❌ Exclusive policy selection (use one, not both)

## Future Extensions (v0.2.0+)

### Weighted Policy Merge

Allow policies to have "authority weights":

```yaml
policy:
  id: "policy.strict"
  weight: 2  # Strict policies weight 2x more
  merge_strategy: "weighted"
```

### Custom Merge Functions

Allow policies to define merge behavior:

```yaml
policy:
  merge_strategy: "custom"
  merge_function: "custom_resolvers.resolve_factual_conflicts"
```

### Policy Precedence Chain

Define explicit ordering:

```yaml
run:
  policy_chain:
    - policy: "policy.quick_check"
      order: 1
    - policy: "policy.deep_audit"
      order: 2
    - policy: "policy.governance_check"
      order: 3
  merge_strategy: "ordered_restrictive"
```

## Receipt Impact

When policies are merged, the receipt records all:

```json
{
  "policy": {
    "policies_evaluated": [
      {"policy_id": "policy.loose", "allowed": true},
      {"policy_id": "policy.strict", "allowed": false}
    ],
    "merge_strategy": "restrictive_override",
    "final_allowed": false,
    "merge_rationale": "Strict policy denied on confidence < 0.95"
  },
  "decision": {
    "intent": "...",
    "chosen_action": "deny",
    "confidence": 0.80
  }
}
```

## Backward Compatibility

v0.1.0 (current) does NOT merge policies. Each agent runs under exactly one policy.

Merge strategy is optional and activated only when explicitly configured in run YAML:

```yaml
run:
  agents:
    - id: "agent_1"
      policies:  # NEW: list of policies instead of single policy
        - "policy.loose"
        - "policy.strict"
      merge_strategy: "restrictive_override"  # NEW
```

If `policies` is a list, merge strategy applies. If `policy` is a string, single-policy mode (v0.1.0 compatible).

---

**Merge Strategy is optional in v0.1.0, required for v0.2.0+**
