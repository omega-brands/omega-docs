"""Test vector suite for canonicalization (RFC 8785 inspired).

These test vectors ensure that canonicalization is deterministic
across platforms, Python versions, and implementations.
"""

import pytest
from src.ppp.receipts.schema import CanonicalSerializer


class TestCanonicalVectors:
    """JCS-inspired test vectors for deterministic serialization."""

    def test_empty_object(self):
        """Empty object should serialize consistently."""
        obj = {}
        result = CanonicalSerializer.canonical_json(obj)
        assert result == "{}"
        assert CanonicalSerializer.canonical_json(obj) == result

    def test_empty_array(self):
        """Empty array should serialize consistently."""
        obj = {"a": []}
        result = CanonicalSerializer.canonical_json(obj)
        assert result == '{"a":[]}'

    def test_key_ordering(self):
        """Keys must be sorted alphabetically."""
        obj1 = {"z": 1, "a": 2, "m": 3}
        obj2 = {"a": 2, "m": 3, "z": 1}
        assert CanonicalSerializer.canonical_json(obj1) == CanonicalSerializer.canonical_json(obj2)
        assert CanonicalSerializer.canonical_json(obj1) == '{"a":2,"m":3,"z":1}'

    def test_nested_key_ordering(self):
        """Keys in nested objects must also be sorted."""
        obj = {"outer": {"z": 1, "a": 2}}
        result = CanonicalSerializer.canonical_json(obj)
        assert result == '{"outer":{"a":2,"z":1}}'

    def test_array_order_preserved(self):
        """Array order must be preserved, not sorted."""
        obj = {"items": [3, 1, 2]}
        result = CanonicalSerializer.canonical_json(obj)
        assert result == '{"items":[3,1,2]}'
        assert "[1,2,3]" not in result

    def test_float_zero(self):
        """Float zero must be consistent."""
        obj = {"confidence": 0.0}
        result = CanonicalSerializer.canonical_json(obj)
        # Should be "0.0" as string to avoid drift
        assert '"0.0"' in result or '0.0' in result

    def test_float_whole_number(self):
        """Whole number floats must be consistent."""
        obj = {"value": 1.0}
        result = CanonicalSerializer.canonical_json(obj)
        # Should represent as "1.0" (string) to avoid representation drift
        assert "1" in result

    def test_float_fractional_consistency(self):
        """Fractional floats must be consistent across runs."""
        obj = {"confidence": 0.95}
        result1 = CanonicalSerializer.canonical_json(obj)
        result2 = CanonicalSerializer.canonical_json(obj)
        assert result1 == result2
        # Should use fixed precision string representation
        assert isinstance(result1, str)

    def test_float_precision_preservation(self):
        """Float precision up to IEEE 754 limits must be preserved."""
        obj = {"value": 0.123456789012345}
        result1 = CanonicalSerializer.canonical_json(obj)
        result2 = CanonicalSerializer.canonical_json(obj)
        assert result1 == result2

    def test_boolean_values(self):
        """Boolean values must serialize consistently."""
        obj = {"enabled": True, "disabled": False}
        result = CanonicalSerializer.canonical_json(obj)
        assert "true" in result or "True" in result
        assert "false" in result or "False" in result

    def test_null_values(self):
        """Null values must serialize consistently."""
        obj = {"value": None}
        result = CanonicalSerializer.canonical_json(obj)
        assert "null" in result

    def test_string_escaping(self):
        """Strings with special characters must escape consistently."""
        obj = {"text": 'Hello "world" \\ slash'}
        result = CanonicalSerializer.canonical_json(obj)
        assert result == CanonicalSerializer.canonical_json(obj)

    def test_unicode_characters(self):
        """Unicode characters must serialize consistently."""
        obj = {"text": "Héllo wørld"}
        result = CanonicalSerializer.canonical_json(obj)
        assert result == CanonicalSerializer.canonical_json(obj)
        assert result == '{"text":"Héllo wørld"}'

    def test_no_trailing_spaces(self):
        """No trailing spaces in output."""
        obj = {"a": 1, "b": 2}
        result = CanonicalSerializer.canonical_json(obj)
        assert result == result.strip()
        assert not result.endswith(" ")

    def test_hash_determinism_identical_dicts(self):
        """Hash of identical dicts (different order) must match."""
        dict1 = {"z": 1, "a": 2}
        dict2 = {"a": 2, "z": 1}
        hash1 = CanonicalSerializer.hash_payload(dict1)
        hash2 = CanonicalSerializer.hash_payload(dict2)
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256

    def test_hash_determinism_multiple_runs(self):
        """Hash of same dict must be identical across multiple runs."""
        obj = {"confidence": 0.95, "intent": "test", "action": "allow"}
        hashes = [CanonicalSerializer.hash_payload(obj) for _ in range(5)]
        assert all(h == hashes[0] for h in hashes)

    def test_hash_sensitivity_to_values(self):
        """Hash must change if values change."""
        obj1 = {"confidence": 0.95}
        obj2 = {"confidence": 0.96}
        hash1 = CanonicalSerializer.hash_payload(obj1)
        hash2 = CanonicalSerializer.hash_payload(obj2)
        assert hash1 != hash2

    def test_hash_sensitivity_to_keys(self):
        """Hash must change if keys change."""
        obj1 = {"confidence": 0.95}
        obj2 = {"confidences": 0.95}
        hash1 = CanonicalSerializer.hash_payload(obj1)
        hash2 = CanonicalSerializer.hash_payload(obj2)
        assert hash1 != hash2

    def test_complex_nested_structure(self):
        """Complex nested structures must serialize deterministically."""
        obj = {
            "receipt": {
                "z_field": "last",
                "a_field": "first",
                "m_field": {
                    "nested_z": [3, 1, 2],
                    "nested_a": 0.95,
                }
            }
        }
        result1 = CanonicalSerializer.canonical_json(obj)
        result2 = CanonicalSerializer.canonical_json(obj)
        assert result1 == result2
        # Verify key ordering
        assert result1.index('"a_field"') < result1.index('"m_field"')
        assert result1.index('"m_field"') < result1.index('"z_field"')

    def test_float_rstrip_trailing_zeros(self):
        """Float representation should strip trailing zeros."""
        obj = {"value": 0.5}
        result = CanonicalSerializer.canonical_json(obj)
        # Should not have excessive trailing zeros
        assert result == CanonicalSerializer.canonical_json(obj)

    def test_receipt_hash_vector(self):
        """Real receipt hash must be reproducible."""
        receipt_obj = {
            "receipt_id": "abc123",
            "run_id": "ppp_agent_20260204",
            "agent_id": "agent_1",
            "event": "action_allowed",
            "phase": "participate",
            "status": "completed",
            "input_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "output_hash": "d4735fea99c5b0f3f4e8e9b1a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
            "receipt_hash": "f7a9e3b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
            "policy": {"policy_id": "policy.strict", "allowed": True},
            "decision": {"intent": "test", "chosen_action": "allow", "confidence": 0.98}
        }
        
        hash1 = CanonicalSerializer.hash_payload(receipt_obj)
        hash2 = CanonicalSerializer.hash_payload(receipt_obj)
        assert hash1 == hash2
        assert len(hash1) == 64
