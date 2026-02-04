"""Configuration loader for PPP."""

import yaml
from pathlib import Path
from typing import Dict, Any
from .models import RunConfig, PolicyConfig


class ConfigLoader:
    """Load and validate PPP configuration files."""

    @staticmethod
    def load_run_config(path: str) -> RunConfig:
        """Load run configuration from YAML."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        ppp_config = data.get('ppp', {})
        run_config = ppp_config.get('run', {})
        
        return RunConfig(
            version=ppp_config.get('version', '0.1.0'),
            run_id_template=run_config.get('id_template', 'ppp_{{agent_id}}_{{utc_timestamp}}'),
            agents=run_config.get('agents', []),
            phases=run_config.get('phases', []),
            target=run_config.get('target', {}),
            disclosure=ppp_config.get('disclosure', {}),
            storage=ppp_config.get('storage', {}),
            keon=ppp_config.get('keon', {}),
            logging=ppp_config.get('logging', {}),
        )

    @staticmethod
    def load_policy_config(path: str) -> PolicyConfig:
        """Load policy configuration from YAML."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        policy_data = data.get('policy', {})
        
        return PolicyConfig(
            id=policy_data.get('id', 'unknown'),
            version=policy_data.get('version', '0.1.0'),
            description=policy_data.get('description', ''),
            tier=policy_data.get('tier', 'loose'),
            allowed_actions=policy_data.get('allowed_actions', []),
            denied_actions=policy_data.get('denied_actions', []),
            rules=policy_data.get('rules', []),
            logging=policy_data.get('logging', {}),
            compliance=policy_data.get('compliance', {}),
        )

    @staticmethod
    def resolve_policy_path(policy_id: str, base_path: str = 'configs/ppp/policies') -> str:
        """Resolve policy file path from policy ID."""
        return str(Path(base_path) / f"{policy_id}.yaml")
