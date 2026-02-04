"""
Public Participation Probe (PPP) v0.1.0

An internal execution harness for evaluating policy-governed autonomous agent behavior
in public or semi-public digital environments.

Core principles:
  - Deterministic: same inputs + policy = same result
  - Audit-safe: all decisions recorded with hashes
  - Fail-closed: deny on ambiguity
  - Draft-only: no live posting
  - Disclosure-required: all outbound content marked autonomous
"""

__version__ = "0.1.0"
__author__ = "Anthropic"

from .runner import PPPRunner
from .policy.engine import PolicyEvaluator

__all__ = ["PPPRunner", "PolicyEvaluator"]
