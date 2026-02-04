"""Tests for progress storage."""

import pytest
import tempfile
from pathlib import Path
from src.ppp.storage.progress import ProgressStore


@pytest.fixture
def temp_db():
    """Create a temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        yield str(db_path)


def test_progress_store_init(temp_db):
    """Progress store should initialize database."""
    store = ProgressStore(temp_db)
    assert Path(temp_db).exists()


def test_begin_run(temp_db):
    """Should be able to begin a run."""
    store = ProgressStore(temp_db)
    result = store.begin_run("run-1", "agent-1", "policy.loose", "config_hash_1")
    assert result is True


def test_begin_run_duplicate(temp_db):
    """Should not allow duplicate run IDs."""
    store = ProgressStore(temp_db)
    store.begin_run("run-1", "agent-1", "policy.loose")
    result = store.begin_run("run-1", "agent-1", "policy.loose")
    assert result is False


def test_start_phase(temp_db):
    """Should be able to start a phase."""
    store = ProgressStore(temp_db)
    store.begin_run("run-1", "agent-1", "policy.loose")
    phase_id = store.start_phase("run-1", "discover")
    assert phase_id is not None
    assert "discover" in phase_id


def test_complete_phase(temp_db):
    """Should be able to complete a phase."""
    store = ProgressStore(temp_db)
    store.begin_run("run-1", "agent-1", "policy.loose")
    phase_id = store.start_phase("run-1", "discover")
    result = store.complete_phase(phase_id, "completed")
    assert result is True


def test_checkpoint(temp_db):
    """Should be able to create a checkpoint."""
    store = ProgressStore(temp_db)
    store.begin_run("run-1", "agent-1", "policy.loose")
    checkpoint_id = store.checkpoint("run-1", "discover", "checkpoint_data_1")
    assert checkpoint_id is not None


def test_get_last_checkpoint(temp_db):
    """Should be able to retrieve last checkpoint."""
    store = ProgressStore(temp_db)
    store.begin_run("run-1", "agent-1", "policy.loose")
    store.checkpoint("run-1", "discover", "checkpoint_1")
    store.checkpoint("run-1", "discover", "checkpoint_2")
    
    checkpoint = store.get_last_checkpoint("run-1", "discover")
    assert checkpoint is not None
    assert checkpoint["data"] == "checkpoint_2"


def test_get_run_status(temp_db):
    """Should be able to get run status."""
    store = ProgressStore(temp_db)
    store.begin_run("run-1", "agent-1", "policy.loose", "config_hash_1")
    
    status = store.get_run_status("run-1")
    assert status is not None
    assert status["run_id"] == "run-1"
    assert status["agent_id"] == "agent-1"
    assert status["policy_id"] == "policy.loose"
    assert status["status"] == "in_progress"


def test_complete_run(temp_db):
    """Should be able to complete a run."""
    store = ProgressStore(temp_db)
    store.begin_run("run-1", "agent-1", "policy.loose")
    result = store.complete_run("run-1", "completed")
    assert result is True
    
    status = store.get_run_status("run-1")
    assert status["status"] == "completed"
    assert status["completed_at"] is not None


def test_list_runs(temp_db):
    """Should be able to list runs."""
    store = ProgressStore(temp_db)
    store.begin_run("run-1", "agent-1", "policy.loose")
    store.begin_run("run-2", "agent-2", "policy.medium")
    
    runs = store.list_runs()
    assert len(runs) >= 2
    assert any(r["run_id"] == "run-1" for r in runs)
    assert any(r["run_id"] == "run-2" for r in runs)


def test_run_lifecycle(temp_db):
    """Test full run lifecycle."""
    store = ProgressStore(temp_db)
    
    # Begin run
    store.begin_run("run-1", "agent-1", "policy.loose")
    
    # Start phases
    discover_phase = store.start_phase("run-1", "discover")
    store.complete_phase(discover_phase, "completed")
    
    observe_phase = store.start_phase("run-1", "observe")
    store.checkpoint("run-1", "observe", "observation_data")
    store.complete_phase(observe_phase, "completed")
    
    # Complete run
    store.complete_run("run-1", "completed")
    
    # Verify final state
    status = store.get_run_status("run-1")
    assert status["status"] == "completed"
    
    checkpoint = store.get_last_checkpoint("run-1", "observe")
    assert checkpoint["data"] == "observation_data"
