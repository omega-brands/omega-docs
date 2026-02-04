# PPP Policy Versioning & Lineage Tracking

**Version: v0.1.0+**

## Overview

Policy versioning enables:
- Tracking policy evolution over time
- Auditability: which policy was applied to which receipt
- Reproducibility: replay decisions using historical policy versions
- A/B testing: compare outcomes across policy versions

## Versioning Scheme

Policies follow **semantic versioning**: `MAJOR.MINOR.PATCH`

```yaml
policy:
  id: "policy.strict"
  version: "1.0.0"  # Semantic version
  parent: "policy.strict:0.9.0"  # Optional lineage
  created_at: "2026-02-03T12:00:00Z"
  modified_by: "audit-system"
```

### Version Semantics

| Change | Type | Example |
|--------|------|---------|
| New rule | MINOR | 1.0.0 → 1.1.0 |
| Rule modification (logic) | MINOR | 1.0.0 → 1.1.0 |
| Rule parameter change | PATCH | 1.0.0 → 1.0.1 |
| Documentation only | (no bump) | Stay at 1.0.0 |
| Breaking change (removed rule) | MAJOR | 1.0.0 → 2.0.0 |

## Lineage Tracking

Each policy can reference its parent:

```yaml
policy:
  id: "policy.strict"
  version: "1.1.0"
  parent: "policy.strict:1.0.0"
  changelog:
    - version: "1.1.0"
      date: "2026-02-10"
      changes:
        - "Added rule: strict_sourcing_for_claims"
        - "Updated rule parameters: confidence_threshold 0.95 → 0.98"
```

### Lineage Chain

```
policy.strict:0.9.0 (initial)
    ↓
policy.strict:1.0.0 (rule additions)
    ↓
policy.strict:1.0.1 (parameter tuning)
    ↓
policy.strict:1.1.0 (current)
```

## Receipt Tracking

Each receipt records the exact policy version used:

```json
{
  "receipt_id": "abc123",
  "policy": {
    "policy_id": "policy.strict",
    "policy_version": "1.1.0",
    "policy_hash": "f7a9e3b0c1d2e3f4...",
    "parent_policy": "policy.strict:1.0.1",
    "policy_lineage": [
      "policy.strict:0.9.0",
      "policy.strict:1.0.0",
      "policy.strict:1.0.1",
      "policy.strict:1.1.0"
    ]
  }
}
```

## Policy Archive Structure

```
ARCHIVE/policies/
├── policy.strict/
│   ├── 0.9.0/
│   │   ├── policy.strict_0.9.0.yaml
│   │   └── hash_manifest.json
│   ├── 1.0.0/
│   │   ├── policy.strict_1.0.0.yaml
│   │   └── hash_manifest.json
│   ├── 1.0.1/
│   ├── 1.1.0/
│   └── LINEAGE.json
├── policy.medium/
└── policy.loose/
```

## Hash Manifest

Each policy version is hashed for immutability:

```json
{
  "policy_id": "policy.strict",
  "version": "1.1.0",
  "hash": "f7a9e3b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "canonicalization_version": "1.0",
  "archived_at": "2026-02-10T12:00:00Z",
  "parent_hash": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
}
```

## Implementation: Policy Version Lookup

```python
class PolicyVersionManager:
    """Manage policy versions and lineage."""
    
    def __init__(self, archive_root: str = "ARCHIVE/policies"):
        self.archive_root = Path(archive_root)
    
    def get_policy_by_version(self, policy_id: str, version: str) -> PolicyConfig:
        """Retrieve a specific policy version from archive."""
        policy_path = self.archive_root / policy_id / version / f"{policy_id}_{version}.yaml"
        if not policy_path.exists():
            raise ValueError(f"Policy not found: {policy_id}:{version}")
        return ConfigLoader.load_policy_config(str(policy_path))
    
    def get_policy_lineage(self, policy_id: str) -> List[str]:
        """Get ordered lineage of policy versions."""
        lineage_file = self.archive_root / policy_id / "LINEAGE.json"
        if not lineage_file.exists():
            return []
        with open(lineage_file) as f:
            data = json.load(f)
        return data.get("versions", [])
    
    def archive_policy(self, policy: PolicyConfig):
        """Archive a policy version with hash verification."""
        version_dir = self.archive_root / policy.id / policy.version
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Save policy YAML
        policy_file = version_dir / f"{policy.id}_{policy.version}.yaml"
        with open(policy_file, 'w') as f:
            yaml.dump(asdict(policy), f)
        
        # Compute and store hash
        policy_hash = hashlib.sha256(
            CanonicalSerializer.canonical_json(asdict(policy)).encode()
        ).hexdigest()
        
        manifest = {
            "policy_id": policy.id,
            "version": policy.version,
            "hash": policy_hash,
            "archived_at": datetime.utcnow().isoformat() + "Z",
        }
        
        manifest_file = version_dir / "hash_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
```

## Comparing Policy Versions

```python
def compare_policies(policy_a: PolicyConfig, policy_b: PolicyConfig) -> Dict[str, Any]:
    """Compare two policy versions to identify changes."""
    diff = {
        "new_rules": [],
        "removed_rules": [],
        "modified_rules": [],
        "parameter_changes": [],
    }
    
    rules_a = {r["id"]: r for r in policy_a.rules}
    rules_b = {r["id"]: r for r in policy_b.rules}
    
    # New rules
    for rule_id in rules_b:
        if rule_id not in rules_a:
            diff["new_rules"].append(rule_id)
    
    # Removed rules
    for rule_id in rules_a:
        if rule_id not in rules_b:
            diff["removed_rules"].append(rule_id)
    
    # Modified rules
    for rule_id in rules_a:
        if rule_id in rules_b and rules_a[rule_id] != rules_b[rule_id]:
            diff["modified_rules"].append(rule_id)
            diff["parameter_changes"].append({
                "rule_id": rule_id,
                "from": rules_a[rule_id].get("parameters"),
                "to": rules_b[rule_id].get("parameters"),
            })
    
    return diff
```

## Audit Trail: Policy Impact Analysis

```python
def policy_impact_analysis(run_ids_a: List[str], run_ids_b: List[str]) -> Dict[str, Any]:
    """
    Compare receipt outcomes between two runs using different policy versions.
    
    Useful for: A/B testing, impact analysis, regression detection
    """
    decisions_a = load_decisions_from_runs(run_ids_a)
    decisions_b = load_decisions_from_runs(run_ids_b)
    
    return {
        "total_decisions_a": len(decisions_a),
        "total_decisions_b": len(decisions_b),
        "allowed_a": sum(1 for d in decisions_a if d["allowed"]),
        "allowed_b": sum(1 for d in decisions_b if d["allowed"]),
        "denied_a": sum(1 for d in decisions_a if not d["allowed"]),
        "denied_b": sum(1 for d in decisions_b if not d["allowed"]),
        "shift_from_allow_to_deny": [
            d for d in decisions_a
            if d["allowed"] and any(x["intent"] == d["intent"] and not x["allowed"] for x in decisions_b)
        ],
        "shift_from_deny_to_allow": [
            d for d in decisions_a
            if not d["allowed"] and any(x["intent"] == d["intent"] and x["allowed"] for x in decisions_b)
        ],
    }
```

## Backward Compatibility

v0.1.0 does NOT require versioning. If a policy lacks `version` field, it defaults to `"0.1.0"`.

When archiving or comparing policies:
- Missing `version` → treat as `"0.1.0"`
- Missing `parent` → treat as initial version (no lineage)
- Missing hash → compute on-demand

Versioning becomes mandatory in v0.2.0+.

## Best Practices

1. **Archive Every Policy Version** — Use `PolicyVersionManager.archive_policy()` immediately after policy creation/update

2. **Link Receipts to Policy Versions** — Receipt always includes `policy_version` and `policy_hash`

3. **Tag Policy Commits** — When policy changes go to production, tag the commit: `policy-strict-v1.1.0`

4. **Document Changes** — Every version bump should include a `changelog` entry explaining what changed and why

5. **Audit Impact** — Before deploying a new policy version, run `policy_impact_analysis()` on sample receipts to predict impact

---

**Policy versioning enables reproducibility and auditability across policy evolution.**
