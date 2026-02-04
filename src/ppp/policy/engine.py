"""Policy evaluation engine."""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from ..config.models import PolicyConfig


@dataclass
class PolicyDecision:
    """Result of policy evaluation."""
    allowed: bool
    rules_triggered: List[Dict[str, Any]] = field(default_factory=list)
    mitigations: List[Dict[str, Any]] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    uncertainty: List[str] = field(default_factory=list)


class PolicyEvaluator:
    """Deterministic policy evaluator."""

    def __init__(self, policy_config: PolicyConfig):
        self.policy = policy_config
        self.tier = policy_config.tier
        self.fail_on_ambiguity = policy_config.compliance.get("fail_on_ambiguity", False)

    def evaluate(
        self,
        context: Dict[str, Any],
        outbound_text: str = "",
    ) -> PolicyDecision:
        """
        Evaluate context against policy.
        
        Returns PolicyDecision with allowed/denied status and triggered rules.
        """
        decision = PolicyDecision(allowed=True)
        
        # Evaluate each rule
        for rule in self.policy.rules:
            rule_result = self._evaluate_rule(rule, context, outbound_text)
            decision.rules_triggered.append(rule_result)
            
            # Check if rule violation occurred
            if rule_result.get("violation"):
                if rule.get("action") == "deny":
                    decision.allowed = False
                    if self.fail_on_ambiguity:
                        decision.confidence = 0.0
                elif rule.get("action") == "deny_if_detected":
                    decision.allowed = False
                elif rule.get("action") == "deny_or_add_disclaimer":
                    # Add mitigation instead of denying
                    mitigation = {
                        "mitigation_id": f"add_disclaimer_{rule['id']}",
                        "description": f"Add disclaimer for rule {rule['id']}",
                        "applied": True,
                    }
                    decision.mitigations.append(mitigation)
                elif rule.get("action") == "deny_if_ambiguous" and self.fail_on_ambiguity:
                    decision.allowed = False

        return decision

    def _evaluate_rule(
        self,
        rule: Dict[str, Any],
        context: Dict[str, Any],
        outbound_text: str,
    ) -> Dict[str, Any]:
        """Evaluate a single rule."""
        rule_id = rule.get("id", "unknown")
        severity = rule.get("severity", "SHOULD")
        matched = False
        violation = False
        details = ""

        # Check rule type
        if rule_id == "disclosure_required":
            matched = True
            violation = "disclosure_template" not in rule.get("parameters", {})
            details = "Disclosure template check"

        elif rule_id == "no_pii":
            matched = True
            patterns = rule.get("parameters", {}).get("patterns", [])
            for pattern in patterns:
                if re.search(pattern, outbound_text, re.IGNORECASE):
                    violation = True
                    details = f"PII pattern detected: {pattern[:30]}..."
                    break

        elif rule_id == "no_deception":
            matched = True
            keywords = rule.get("parameters", {}).get("keywords", [])
            for keyword in keywords:
                if keyword.lower() in outbound_text.lower():
                    violation = True
                    details = f"Deceptive keyword detected: {keyword}"
                    break

        elif rule_id == "no_unauthorized_advice":
            matched = True
            prefixes = rule.get("parameters", {}).get("blocked_prefixes", [])
            for prefix in prefixes:
                if prefix.lower() in outbound_text.lower():
                    violation = True
                    details = f"Unauthorized advice pattern: {prefix}"
                    break

        elif rule_id == "factual_claims_sourced":
            matched = True
            keywords = rule.get("parameters", {}).get("detection_keywords", [])
            for keyword in keywords:
                if keyword.lower() in outbound_text.lower():
                    # Check for citation or uncertainty label
                    has_citation = "[citation:" in outbound_text.lower()
                    has_uncertainty = "[uncertain:" in outbound_text.lower()
                    if not (has_citation or has_uncertainty):
                        violation = True
                        details = f"Factual claim without citation: {keyword}"
                        break

        elif rule_id == "factual_claims_strict_sourcing":
            matched = True
            keywords = rule.get("parameters", {}).get("detection_keywords", [])
            for keyword in keywords:
                if keyword.lower() in outbound_text.lower():
                    has_citation = "[citation:" in outbound_text.lower()
                    if not has_citation:
                        violation = True
                        details = f"Strict: factual claim without citation: {keyword}"
                        break

        elif rule_id == "max_draft_length":
            matched = True
            max_chars = rule.get("parameters", {}).get("max_chars", 500)
            if len(outbound_text) > max_chars:
                violation = True
                details = f"Text length {len(outbound_text)} exceeds max {max_chars}"

        elif rule_id == "deny_on_ambiguity":
            # Check context for ambiguity signals
            confidence = context.get("confidence", 1.0)
            if confidence < 0.95:
                matched = True
                violation = True
                details = f"Low confidence decision: {confidence}"

        return {
            "rule_id": rule_id,
            "severity": severity,
            "matched": matched,
            "violation": violation,
            "details": details,
        }
