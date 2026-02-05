#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Language Remediation Evaluator

PolicyEvaluator for language-based remediation of guarantee claims.
Detects guarantee language patterns, assigns confidence scores, applies fail-closed logic.

Part of WF_DOCS_REMEDIATION_GOVERNANCE_v1.
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
import yaml


@dataclass
class GuaranteeClaim:
    """Detected guarantee claim with context."""
    text: str
    claim_type: str  # Type A, B, C, D
    line_number: int
    context_before: str
    context_after: str
    pattern_matched: str
    confidence: float  # 0.0-1.0


class LanguageRemediationEvaluator:
    """Evaluator for guarantee language detection and remediation rules."""

    def __init__(self, policy_path: str):
        """
        Initialize evaluator with policy rules.

        Args:
            policy_path: Path to policy.language-remediation.yaml
        """
        self.policy_path = policy_path
        self.policy = self._load_policy()
        self.pattern_cache = {}

    def _load_policy(self) -> dict:
        """Load remediation policy from YAML."""
        with open(self.policy_path) as f:
            return yaml.safe_load(f)

    def detect_guarantee_claims(self, file_content: str, directive_id: str) -> List[GuaranteeClaim]:
        """
        Detect all guarantee language claims in file content.

        Args:
            file_content: Full file content (multiline string)
            directive_id: Directive ID (C, G, K) for directive-specific patterns

        Returns:
            List of GuaranteeClaim objects with line numbers, context, confidence
        """
        if directive_id not in self.policy['directives']:
            return []

        directive_rules = self.policy['directives'][directive_id]['rules']
        lines = file_content.split('\n')
        claims = []

        for line_num, line in enumerate(lines, 1):
            for rule in directive_rules:
                pattern = rule['pattern']
                replacement_conf = rule.get('replacement_confidence', 0.85)

                # Compile regex pattern
                try:
                    regex = re.compile(pattern, re.IGNORECASE)
                except re.error:
                    continue

                # Find all matches in line
                for match in regex.finditer(line):
                    matched_text = match.group(0)

                    # Determine claim type based on pattern
                    claim_type = self._determine_claim_type(matched_text)

                    # Extract context (lines before/after)
                    context_before = lines[max(0, line_num-2):line_num-1]
                    context_after = lines[line_num:min(len(lines), line_num+2)]

                    # Confidence based on match strength + rule confidence
                    confidence = min(1.0, replacement_conf * 0.95)  # Slightly discounted for pattern matching

                    claim = GuaranteeClaim(
                        text=line.strip(),
                        claim_type=claim_type,
                        line_number=line_num,
                        context_before=' '.join(context_before),
                        context_after=' '.join(context_after),
                        pattern_matched=matched_text,
                        confidence=confidence
                    )
                    claims.append(claim)

        return claims

    def _determine_claim_type(self, text: str) -> str:
        """Determine claim type (A/B/C/D) based on language."""
        text_lower = text.lower()

        # Type A: Strong guarantees
        if re.search(r'\b(guarantee|ensures|prevent|enforce)\b', text_lower):
            return "Type A"

        # Type B: Weak guarantees
        elif re.search(r'\b(provides?|offers|includes)\b', text_lower):
            return "Type B"

        # Type C: Promise language
        elif re.search(r'\b(will|shall|must)\b', text_lower):
            return "Type C"

        # Type D: Superlative claims
        elif re.search(r'\b(complete|perfect|ultimate|best|always|never)\b', text_lower):
            return "Type D"

        return "Type B"  # Default

    def classify_claims(self, claims: List[GuaranteeClaim]) -> Dict:
        """
        Classify claims by type and confidence distribution.

        Returns:
            {
                "claim_count": int,
                "by_type": {"Type A": 5, "Type B": 3, ...},
                "confidence_distribution": {"0.95-1.0": 3, "0.70-0.94": 4, "<0.70": 1}
            }
        """
        by_type = {}
        confidence_dist = {"0.95-1.0": 0, "0.70-0.94": 0, "<0.70": 0}

        for claim in claims:
            # Count by type
            by_type[claim.claim_type] = by_type.get(claim.claim_type, 0) + 1

            # Count confidence distribution
            if claim.confidence >= 0.95:
                confidence_dist["0.95-1.0"] += 1
            elif claim.confidence >= 0.70:
                confidence_dist["0.70-0.94"] += 1
            else:
                confidence_dist["<0.70"] += 1

        return {
            "claim_count": len(claims),
            "by_type": by_type,
            "confidence_distribution": confidence_dist
        }

    def evaluate_policy(self, claims: List[GuaranteeClaim], directive_id: str) -> Dict:
        """
        Apply policy rules and determine PROCEED / REVIEW / BLOCK decision.

        Returns:
            {
                "policy_decision": "PROCEED" | "REVIEW" | "BLOCK",
                "claims_proceeding": int,      # 0.95+
                "claims_requiring_review": int, # 0.70-0.94
                "claims_blocked": int,         # <0.70
                "applicable_rules": [...],
                "violation_reasons": [...]
            }
        """
        thresholds = self.policy['confidence_thresholds']

        claims_proceeding = sum(1 for c in claims if c.confidence >= thresholds['proceed_auto_approve'])
        claims_review = sum(1 for c in claims if thresholds['review_human_required'] <= c.confidence < thresholds['proceed_auto_approve'])
        claims_blocked = sum(1 for c in claims if c.confidence < thresholds['block_explicit_override'])

        # Determine overall policy decision
        if claims_blocked > 0:
            policy_decision = "BLOCK"
        elif claims_review > 0:
            policy_decision = "REVIEW"
        else:
            policy_decision = "PROCEED"

        return {
            "policy_decision": policy_decision,
            "claims_proceeding": claims_proceeding,
            "claims_requiring_review": claims_review,
            "claims_blocked": claims_blocked,
            "applicable_rules": [rule['pattern'] for rule in self.policy['directives'][directive_id]['rules']],
            "violation_reasons": [] if policy_decision == "PROCEED" else ["Low confidence claims require human review" if policy_decision == "REVIEW" else "Blocked claims require explicit override"]
        }

    def suggest_replacements(self, claims: List[GuaranteeClaim], directive_id: str) -> List[Dict]:
        """
        Generate suggested replacements for claims based on policy rules.

        Returns:
            List of {
                "claim_text": str,
                "claim_type": str,
                "confidence": float,
                "suggested_replacement": str,
                "replacement_confidence": float
            }
        """
        suggestions = []
        directive_rules = self.policy['directives'][directive_id]['rules']

        for claim in claims:
            for rule in directive_rules:
                pattern = rule['pattern']
                if re.search(pattern, claim.text, re.IGNORECASE):
                    suggestion = {
                        "claim_text": claim.text,
                        "claim_type": claim.claim_type,
                        "confidence": claim.confidence,
                        "suggested_replacement": rule['replacement'],
                        "replacement_confidence": rule.get('replacement_confidence', 0.85),
                        "line_number": claim.line_number,
                        "context": claim.context_before
                    }
                    suggestions.append(suggestion)
                    break  # One replacement per claim

        return suggestions
