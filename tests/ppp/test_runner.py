"""Tests for PPP runner."""

import pytest
import tempfile
from pathlib import Path
from src.ppp.runner import PPPRunner


def test_runner_init():
    """Runner should initialize with config."""
    runner = PPPRunner("configs/ppp/ppp.run.yaml")
    assert runner.config is not None
    assert runner.config.agents is not None


def test_runner_run_all():
    """Runner should execute run_all without errors."""
    runner = PPPRunner("configs/ppp/ppp.run.yaml")
    exit_code = runner.run_all()
    assert exit_code == 0


def test_runner_generates_receipts():
    """Runner should generate receipts."""
    runner = PPPRunner("configs/ppp/ppp.run.yaml")
    runner.run_all()
    assert len(runner.receipts) > 0


def test_runner_receipts_have_required_fields():
    """Receipts should have required fields."""
    runner = PPPRunner("configs/ppp/ppp.run.yaml")
    runner.run_all()
    
    for receipt in runner.receipts:
        assert receipt.receipt_id is not None
        assert receipt.run_id is not None
        assert receipt.agent_id is not None
        assert receipt.event is not None
        assert receipt.phase is not None
        assert receipt.status is not None
        assert receipt.receipt_hash is not None


def test_runner_produces_output_files():
    """Runner should produce output files."""
    runner = PPPRunner("configs/ppp/ppp.run.yaml")
    runner.run_all()
    
    # Check that REPORT directory has content
    report_root = Path("REPORT/ppp")
    assert report_root.exists()
    
    # Should have at least one run directory
    run_dirs = list(report_root.glob("ppp_*"))
    assert len(run_dirs) > 0


def test_runner_with_mock_target():
    """Runner should work with mock target."""
    runner = PPPRunner("configs/ppp/ppp.run.yaml")
    # Mock should be the default target
    assert runner.config.target.get("label") == "moltbook.com"
    
    exit_code = runner.run_all()
    assert exit_code == 0
