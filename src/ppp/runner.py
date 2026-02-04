"""PPP runner orchestration."""

import uuid
from datetime import datetime
from typing import List
from pathlib import Path

from .config.loader import ConfigLoader
from .policy.engine import PolicyEvaluator
from .receipts.schema import CanonicalSerializer, Receipt
from .receipts.emitter import ReceiptEmitter
from .storage.progress import ProgressStore
from .targets.mock import MockTarget
from .targets.moltbook import MoltbookTarget
from .keon.seal import NoopSealer


class PPPRunner:
    """Main PPP orchestrator."""

    def __init__(self, run_config_path: str = "configs/ppp/ppp.run.yaml"):
        self.config = ConfigLoader.load_run_config(run_config_path)
        self.run_config_path = run_config_path
        self.emitter = ReceiptEmitter(self.config.storage.get("report_root", "REPORT/ppp"))
        self.store = ProgressStore(self.config.storage.get("progress_db", "data/ppp_progress.db"))
        self.receipts: List[Receipt] = []
        self.sealer = NoopSealer()

    def run_all(self) -> int:
        """Run all agents through all phases."""
        try:
            for agent_config in self.config.agents:
                agent_id = agent_config.get("id")
                policy_id = agent_config.get("policy")
                
                self._run_agent(agent_id, policy_id)
            
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1

    def _run_agent(self, agent_id: str, policy_id: str) -> None:
        """Run a single agent through all phases."""
        # Generate run ID
        run_id = f"ppp_{agent_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize run
        self.store.begin_run(run_id, agent_id, policy_id)
        
        # Load policy
        policy_path = ConfigLoader.resolve_policy_path(policy_id)
        policy_config = ConfigLoader.load_policy_config(policy_path)
        evaluator = PolicyEvaluator(policy_config)
        
        # Initialize target
        target_config = self.config.target.get("label", "moltbook")
        if target_config == "moltbook.com" or target_config == "moltbook":
            target = MoltbookTarget(self.config.__dict__.get("targets", {}).get("moltbook", {}))
        else:
            target = MockTarget(self.config.__dict__.get("targets", {}).get("moltbook", {}))
        
        # Run phases
        for phase_config in self.config.phases:
            phase_name = phase_config.get("name")
            if not phase_config.get("enabled", True):
                continue
            
            phase_id = self.store.start_phase(run_id, phase_name)
            
            try:
                if phase_name == "discover":
                    self._phase_discover(run_id, agent_id, policy_id, target, evaluator)
                elif phase_name == "observe":
                    self._phase_observe(run_id, agent_id, policy_id, target, evaluator)
                elif phase_name == "participate":
                    self._phase_participate(run_id, agent_id, policy_id, target, evaluator)
                elif phase_name == "emit_receipts":
                    self._phase_emit_receipts(run_id, agent_id, policy_id, policy_path)
                
                self.store.complete_phase(phase_id, "completed")
            except Exception as e:
                self.store.complete_phase(phase_id, "failed")
                receipt = CanonicalSerializer.create_receipt(
                    receipt_id=str(uuid.uuid4()),
                    run_id=run_id,
                    agent_id=agent_id,
                    event="error_occurred",
                    phase=phase_name,
                    status="failed",
                    policy={"policy_id": policy_id, "rules_triggered": []},
                    decision={"intent": phase_name, "chosen_action": "error", "confidence": 0.0},
                    failure_stage=phase_name,
                )
                self.receipts.append(receipt)
        
        self.store.complete_run(run_id, "completed")

    def _phase_discover(self, run_id: str, agent_id: str, policy_id: str, target, evaluator) -> None:
        """Discovery phase."""
        receipt_id = str(uuid.uuid4())
        
        try:
            targets = target.discover()
            
            receipt = CanonicalSerializer.create_receipt(
                receipt_id=receipt_id,
                run_id=run_id,
                agent_id=agent_id,
                event="phase_completed",
                phase="discover",
                status="completed",
                policy={"policy_id": policy_id, "rules_triggered": []},
                decision={
                    "intent": "discover targets",
                    "chosen_action": "discovered",
                    "confidence": 1.0,
                },
                artifacts={"targets_discovered": len(targets)},
            )
            self.receipts.append(receipt)
        except Exception as e:
            receipt = CanonicalSerializer.create_receipt(
                receipt_id=receipt_id,
                run_id=run_id,
                agent_id=agent_id,
                event="error_occurred",
                phase="discover",
                status="failed",
                policy={"policy_id": policy_id, "rules_triggered": []},
                decision={"intent": "discover", "chosen_action": "error", "confidence": 0.0},
            )
            self.receipts.append(receipt)

    def _phase_observe(self, run_id: str, agent_id: str, policy_id: str, target, evaluator) -> None:
        """Observation phase."""
        receipt_id = str(uuid.uuid4())
        
        try:
            targets = target.discover()
            if targets:
                observation = target.observe(targets[0]["id"])
            
            receipt = CanonicalSerializer.create_receipt(
                receipt_id=receipt_id,
                run_id=run_id,
                agent_id=agent_id,
                event="phase_completed",
                phase="observe",
                status="completed",
                policy={"policy_id": policy_id, "rules_triggered": []},
                decision={
                    "intent": "observe targets",
                    "chosen_action": "observed",
                    "confidence": 1.0,
                },
            )
            self.receipts.append(receipt)
        except Exception as e:
            receipt = CanonicalSerializer.create_receipt(
                receipt_id=receipt_id,
                run_id=run_id,
                agent_id=agent_id,
                event="error_occurred",
                phase="observe",
                status="failed",
                policy={"policy_id": policy_id, "rules_triggered": []},
                decision={"intent": "observe", "chosen_action": "error", "confidence": 0.0},
            )
            self.receipts.append(receipt)

    def _phase_participate(self, run_id: str, agent_id: str, policy_id: str, target, evaluator) -> None:
        """Participation (draft) phase."""
        receipt_id = str(uuid.uuid4())
        
        try:
            targets = target.discover()
            if targets:
                draft_text = f"[Autonomous agent disclosure: This content was generated by a policy-governed autonomous agent and has not been reviewed by a human. Replies to this message are not monitored.]\n\nThis is a test draft response from {agent_id}."
                
                decision = evaluator.evaluate({"phase": "participate"}, draft_text)
                
                draft_artifact = target.participate(targets[0]["id"], "thread_0", draft_text)
                
                receipt = CanonicalSerializer.create_receipt(
                    receipt_id=receipt_id,
                    run_id=run_id,
                    agent_id=agent_id,
                    event="phase_completed" if decision.allowed else "action_denied",
                    phase="participate",
                    status="completed" if decision.allowed else "denied",
                    policy={
                        "policy_id": policy_id,
                        "rules_triggered": decision.rules_triggered,
                        "allowed": decision.allowed,
                    },
                    decision={
                        "intent": "generate draft reply",
                        "chosen_action": "draft" if decision.allowed else "deny",
                        "confidence": decision.confidence,
                        "uncertainty": decision.uncertainty,
                    },
                    output_payload={"text": draft_text},
                    artifacts={
                        "outbound_text": draft_text,
                        "outbound_text_hash": CanonicalSerializer.hash_payload({"text": draft_text}),
                    },
                )
                self.receipts.append(receipt)
        except Exception as e:
            receipt = CanonicalSerializer.create_receipt(
                receipt_id=receipt_id,
                run_id=run_id,
                agent_id=agent_id,
                event="error_occurred",
                phase="participate",
                status="failed",
                policy={"policy_id": policy_id, "rules_triggered": []},
                decision={"intent": "participate", "chosen_action": "error", "confidence": 0.0},
            )
            self.receipts.append(receipt)

    def _phase_emit_receipts(self, run_id: str, agent_id: str, policy_id: str, policy_path: str) -> None:
        """Receipt emission phase."""
        try:
            receipts_file = self.emitter.emit_receipts(run_id, self.receipts)
            summary_file = self.emitter.create_summary(
                run_id,
                self.receipts,
                {"agent_id": agent_id, "policy_id": policy_id},
            )
            
            poml_path = "docs/atlas/ppp/poml.public-participation-probe.yaml"
            evidence_pack_dir = self.emitter.create_evidence_pack(
                run_id,
                self.receipts,
                policy_path,
                self.run_config_path,
                poml_path,
            )
            
            receipt_id = str(uuid.uuid4())
            receipt = CanonicalSerializer.create_receipt(
                receipt_id=receipt_id,
                run_id=run_id,
                agent_id=agent_id,
                event="phase_completed",
                phase="emit_receipts",
                status="completed",
                policy={"policy_id": policy_id, "rules_triggered": []},
                decision={
                    "intent": "emit receipts and create evidence pack",
                    "chosen_action": "receipts_emitted",
                    "confidence": 1.0,
                },
                artifacts={
                    "receipts_file": receipts_file,
                    "summary_file": summary_file,
                    "evidence_pack": evidence_pack_dir,
                },
            )
            self.receipts.append(receipt)
        except Exception as e:
            receipt_id = str(uuid.uuid4())
            receipt = CanonicalSerializer.create_receipt(
                receipt_id=receipt_id,
                run_id=run_id,
                agent_id=agent_id,
                event="error_occurred",
                phase="emit_receipts",
                status="failed",
                policy={"policy_id": policy_id, "rules_triggered": []},
                decision={"intent": "emit_receipts", "chosen_action": "error", "confidence": 0.0},
            )
            self.receipts.append(receipt)
