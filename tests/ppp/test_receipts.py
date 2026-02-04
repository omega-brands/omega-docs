"""Tests for receipt schema and canonicalization."""

import pytest
from src.ppp.receipts.schema import CanonicalSerializer, Receipt


def test_canonical_json_stable():
    """Canonical JSON should produce stable output."""
    obj1 = {"z": 1, "a": 2, "m": 3}
    obj2 = {"a": 2, "m": 3, "z": 1}
    
    json1 = CanonicalSerializer.canonical_json(obj1)
    json2 = CanonicalSerializer.canonical_json(obj2)
    
    assert json1 == json2


def test_canonical_json_sorts_keys():
    """Canonical JSON should sort keys."""
    obj = {"z": 1, "a": 2}
    json_str = CanonicalSerializer.canonical_json(obj)
    
    # Check that 'a' comes before 'z' in the string
    assert json_str.index('"a"') < json_str.index('"z"')


def test_canonical_json_preserves_list_order():
    """Canonical JSON should preserve list order (not sort)."""
    obj = {"items": [3, 1, 2]}
    json_str = CanonicalSerializer.canonical_json(obj)
    
    # Should preserve order: [3,1,2] not [1,2,3]
    assert json_str == '{"items":[3,1,2]}'


def test_hash_payload_deterministic():
    """Hash of same payload should be deterministic."""
    obj = {"x": 1, "y": 2}
    
    hash1 = CanonicalSerializer.hash_payload(obj)
    hash2 = CanonicalSerializer.hash_payload(obj)
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 hex digest length


def test_hash_payload_key_order_independent():
    """Hash should be independent of key order."""
    obj1 = {"z": 1, "a": 2}
    obj2 = {"a": 2, "z": 1}
    
    hash1 = CanonicalSerializer.hash_payload(obj1)
    hash2 = CanonicalSerializer.hash_payload(obj2)
    
    assert hash1 == hash2


def test_create_receipt_deterministic():
    """Creating identical receipts should produce identical hashes."""
    receipt1 = CanonicalSerializer.create_receipt(
        receipt_id="test-1",
        run_id="run-1",
        agent_id="agent-1",
        event="test_event",
        phase="test_phase",
        status="completed",
        policy={"policy_id": "policy.loose"},
        decision={"intent": "test", "chosen_action": "test", "confidence": 1.0},
        input_payload={"input": "data"},
        output_payload={"output": "data"},
    )
    
    receipt2 = CanonicalSerializer.create_receipt(
        receipt_id="test-1",
        run_id="run-1",
        agent_id="agent-1",
        event="test_event",
        phase="test_phase",
        status="completed",
        policy={"policy_id": "policy.loose"},
        decision={"intent": "test", "chosen_action": "test", "confidence": 1.0},
        input_payload={"input": "data"},
        output_payload={"output": "data"},
    )
    
    # Receipt hashes should be identical (excluding timestamp)
    assert receipt1.receipt_hash == receipt2.receipt_hash


def test_receipt_hash_stable_with_reordered_policy():
    """Receipt hash should be stable even if policy dict keys are reordered."""
    receipt1 = CanonicalSerializer.create_receipt(
        receipt_id="test-1",
        run_id="run-1",
        agent_id="agent-1",
        event="test_event",
        phase="test_phase",
        status="completed",
        policy={"policy_id": "p1", "allowed": True},
        decision={"intent": "test", "chosen_action": "test", "confidence": 1.0},
    )
    
    receipt2 = CanonicalSerializer.create_receipt(
        receipt_id="test-1",
        run_id="run-1",
        agent_id="agent-1",
        event="test_event",
        phase="test_phase",
        status="completed",
        policy={"allowed": True, "policy_id": "p1"},
        decision={"intent": "test", "chosen_action": "test", "confidence": 1.0},
    )
    
    assert receipt1.receipt_hash == receipt2.receipt_hash


def test_verify_receipt_hash_valid():
    """Valid receipt should pass hash verification."""
    receipt = CanonicalSerializer.create_receipt(
        receipt_id="test-1",
        run_id="run-1",
        agent_id="agent-1",
        event="test_event",
        phase="test_phase",
        status="completed",
        policy={"policy_id": "policy.loose"},
        decision={"intent": "test", "chosen_action": "test", "confidence": 1.0},
    )
    
    assert CanonicalSerializer.verify_receipt_hash(receipt)


def test_receipt_to_dict():
    """Receipt should convert to dict."""
    receipt = CanonicalSerializer.create_receipt(
        receipt_id="test-1",
        run_id="run-1",
        agent_id="agent-1",
        event="test_event",
        phase="test_phase",
        status="completed",
        policy={"policy_id": "policy.loose"},
        decision={"intent": "test", "chosen_action": "test", "confidence": 1.0},
    )
    
    receipt_dict = receipt.to_dict()
    
    assert receipt_dict["receipt_id"] == "test-1"
    assert receipt_dict["run_id"] == "run-1"
    assert receipt_dict["agent_id"] == "agent-1"
    assert receipt_dict["event"] == "test_event"
    assert "timestamp" in receipt_dict
    assert receipt_dict["receipt_hash"] == receipt.receipt_hash


def test_input_output_hash_different():
    """Different input/output payloads should have different hashes."""
    receipt1 = CanonicalSerializer.create_receipt(
        receipt_id="test-1",
        run_id="run-1",
        agent_id="agent-1",
        event="test",
        phase="test",
        status="completed",
        policy={},
        decision={},
        input_payload={"data": "input1"},
        output_payload={"data": "output1"},
    )
    
    receipt2 = CanonicalSerializer.create_receipt(
        receipt_id="test-1",
        run_id="run-1",
        agent_id="agent-1",
        event="test",
        phase="test",
        status="completed",
        policy={},
        decision={},
        input_payload={"data": "input2"},
        output_payload={"data": "output2"},
    )
    
    assert receipt1.input_hash != receipt2.input_hash
    assert receipt1.output_hash != receipt2.output_hash
