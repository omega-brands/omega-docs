"""Tests for policy evaluator."""

import pytest
from src.ppp.config.models import PolicyConfig
from src.ppp.policy.engine import PolicyEvaluator


@pytest.fixture
def loose_policy():
    """Create loose policy config."""
    return PolicyConfig(
        id="policy.loose",
        version="0.1.0",
        description="Loose policy",
        tier="loose",
        allowed_actions=["discover", "observe", "draft"],
        denied_actions=["publish", "post"],
        rules=[
            {
                "id": "disclosure_required",
                "description": "Disclosure required",
                "severity": "MUST",
                "enforcement": "prepend_or_append",
                "target": "all_outbound",
                "action": "allow_with_mitigation",
                "parameters": {},
            }
        ],
        logging={},
        compliance={"fail_on_ambiguity": False},
    )


@pytest.fixture
def medium_policy():
    """Create medium policy config."""
    return PolicyConfig(
        id="policy.medium",
        version="0.1.0",
        description="Medium policy",
        tier="medium",
        allowed_actions=["discover_limited", "observe", "draft"],
        denied_actions=["publish", "post"],
        rules=[
            {
                "id": "factual_claims_sourced",
                "description": "Factual claims sourced",
                "severity": "MUST",
                "enforcement": "semantic",
                "target": "all_outbound",
                "action": "require_citation_or_uncertainty",
                "parameters": {
                    "detection_keywords": ["studies show", "research indicates"],
                },
            }
        ],
        logging={},
        compliance={"fail_on_ambiguity": False},
    )


@pytest.fixture
def strict_policy():
    """Create strict policy config."""
    return PolicyConfig(
        id="policy.strict",
        version="0.1.0",
        description="Strict policy",
        tier="strict",
        allowed_actions=["observe", "draft"],
        denied_actions=["discover_open", "publish", "post"],
        rules=[
            {
                "id": "deny_on_ambiguity",
                "description": "Deny on ambiguity",
                "severity": "MUST",
                "enforcement": "semantic",
                "target": "all_decisions",
                "action": "deny_if_ambiguous",
                "parameters": {"confidence_threshold": 0.95},
            }
        ],
        logging={},
        compliance={"fail_on_ambiguity": True},
    )


def test_loose_policy_allows_draft(loose_policy):
    """Loose policy should allow draft content."""
    evaluator = PolicyEvaluator(loose_policy)
    decision = evaluator.evaluate({"phase": "participate"}, "Test draft content")
    assert decision.allowed


def test_loose_policy_disclosure_required(loose_policy):
    """Loose policy should enforce disclosure rule."""
    evaluator = PolicyEvaluator(loose_policy)
    context = {"phase": "participate"}
    outbound = "Some content without disclosure"
    decision = evaluator.evaluate(context, outbound)
    # Should still allow but may have triggered disclosure rule
    assert decision.allowed


def test_medium_policy_factual_claim_without_citation(medium_policy):
    """Medium policy should catch factual claims without citation."""
    evaluator = PolicyEvaluator(medium_policy)
    context = {"phase": "participate"}
    outbound = "Studies show that autonomous agents are beneficial."
    decision = evaluator.evaluate(context, outbound)
    # Check if rule was triggered
    triggered_rules = [r for r in decision.rules_triggered if r["rule_id"] == "factual_claims_sourced"]
    assert len(triggered_rules) > 0


def test_medium_policy_factual_claim_with_citation(medium_policy):
    """Medium policy should allow factual claims with citation."""
    evaluator = PolicyEvaluator(medium_policy)
    context = {"phase": "participate"}
    outbound = "Studies show [citation: source.com] that autonomous agents are beneficial."
    decision = evaluator.evaluate(context, outbound)
    assert decision.allowed


def test_medium_policy_factual_claim_with_uncertainty_label(medium_policy):
    """Medium policy should allow factual claims with uncertainty label."""
    evaluator = PolicyEvaluator(medium_policy)
    context = {"phase": "participate"}
    outbound = "Research indicates [uncertain: limited evidence] that this is true."
    decision = evaluator.evaluate(context, outbound)
    assert decision.allowed


def test_strict_policy_deny_on_ambiguity(strict_policy):
    """Strict policy should deny on low confidence."""
    evaluator = PolicyEvaluator(strict_policy)
    context = {"phase": "participate", "confidence": 0.80}
    decision = evaluator.evaluate(context, "Test")
    # Should trigger ambiguity rule
    triggered_rules = [r for r in decision.rules_triggered if r["rule_id"] == "deny_on_ambiguity"]
    assert len(triggered_rules) > 0


def test_no_pii_detection(loose_policy):
    """Policy should detect PII patterns."""
    loose_policy.rules.append(
        {
            "id": "no_pii",
            "description": "No PII",
            "severity": "MUST",
            "enforcement": "regex_scan",
            "target": "all_outbound",
            "action": "deny_if_detected",
            "parameters": {
                "patterns": ["\\b\\d{3}-\\d{2}-\\d{4}\\b"]  # SSN pattern
            },
        }
    )
    evaluator = PolicyEvaluator(loose_policy)
    context = {"phase": "participate"}
    outbound = "My SSN is 123-45-6789"
    decision = evaluator.evaluate(context, outbound)
    # Check if no_pii rule was triggered
    triggered_rules = [r for r in decision.rules_triggered if r["rule_id"] == "no_pii"]
    assert len(triggered_rules) > 0


def test_no_deception_detection(loose_policy):
    """Policy should detect deceptive claims."""
    loose_policy.rules.append(
        {
            "id": "no_deception",
            "description": "No deception",
            "severity": "MUST",
            "enforcement": "semantic",
            "target": "all_outbound",
            "action": "deny_if_violated",
            "parameters": {
                "keywords": ["I did this myself", "I am human"]
            },
        }
    )
    evaluator = PolicyEvaluator(loose_policy)
    context = {"phase": "participate"}
    outbound = "I personally did this myself"
    decision = evaluator.evaluate(context, outbound)
    # Check if no_deception rule was triggered
    triggered_rules = [r for r in decision.rules_triggered if r["rule_id"] == "no_deception"]
    assert len(triggered_rules) > 0
