"""Configuration data models for PPP."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class RunConfig:
    """Top-level run configuration."""
    version: str
    run_id_template: str
    agents: List[Dict[str, Any]]
    phases: List[Dict[str, Any]]
    target: Dict[str, Any]
    disclosure: Dict[str, Any]
    storage: Dict[str, Any]
    keon: Dict[str, Any]
    logging: Dict[str, Any]


@dataclass
class PolicyConfig:
    """Policy configuration."""
    id: str
    version: str
    description: str
    tier: str
    allowed_actions: List[str]
    denied_actions: List[str]
    rules: List[Dict[str, Any]]
    logging: Dict[str, Any]
    compliance: Dict[str, Any]


@dataclass
class TargetConfig:
    """Target configuration."""
    label: str
    description: Optional[str] = None
    url: Optional[str] = None


@dataclass
class PolicyRule:
    """A single policy rule."""
    id: str
    description: str
    severity: str  # MUST, SHOULD, MAY
    enforcement: str
    target: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Receipt:
    """PPP Receipt data structure."""
    receipt_id: str
    run_id: str
    agent_id: str
    timestamp: str
    event: str
    phase: str
    status: str
    input_hash: str
    output_hash: str
    receipt_hash: str
    policy: Dict[str, Any]
    decision: Dict[str, Any]
    artifacts: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    failure_stage: Optional[str] = None
