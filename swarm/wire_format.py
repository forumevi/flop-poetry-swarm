"""
Technocore WireFormatV3 Implementation
Yellowpaper v0.5.0 Protocol Compliant Protocol Settlement Payload
"""
import hashlib
import json
import time
from typing import Dict, Any, Optional, Tuple


class WireFormatV3:
    """
    FLOP Network Yellow Paper v0.5.0 Appendix F.3 & §12 compliant payload generator.
    Binds output_hash and decode_policy_hash for multi-agent poetry settlement.
    """

    VERSION: int = 3
    DEFAULT_CHANNEL: str = "pallet_compute_channel"

    def __init__(self, turn_index: int, agent_role: str, compute_channel: Optional[str] = None):
        self.turn_index = turn_index
        self.agent_role = agent_role
        self.compute_channel = compute_channel or self.DEFAULT_CHANNEL

    @staticmethod
    def compute_sha256(data: str) -> str:
        """
        Computes standard SHA-256 hex digest for any UTF-8 string input.
        """
        if not isinstance(data, str):
            raise TypeError("Data for SHA-256 computation must be a string.")
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_policy_hash(decode_params: Dict[str, Any]) -> str:
        """
        Generates deterministic SHA-256 hash for decoding parameters by sorting keys.
        """
        try:
            serialized_policy = json.dumps(decode_params, sort_keys=True)
            return WireFormatV3.compute_sha256(serialized_policy)
        except (TypeError, ValueError) as err:
            raise ValueError(f"Failed to serialize decode_params for policy hashing: {err}")

    @classmethod
    def build_verified_turn(
        cls,
        turn_index: int,
        agent_role: str,
        content: str,
        decode_params: Dict[str, Any],
        compute_channel: str = DEFAULT_CHANNEL
    ) -> Dict[str, Any]:
        """
        Constructs a complete verified turn payload compliant with WireFormat V3 specification.
        """
        content_hash = cls.compute_sha256(content)
        policy_hash = cls.generate_policy_hash(decode_params)
        timestamp = int(time.time())

        payload_body = {
            "content": content,
            "decode_params": decode_params,
            "created_at": timestamp
        }

        turn_structure = {
            "leaf_version": cls.VERSION,
            "turn_index": turn_index,
            "agent_role": agent_role,
            "compute_channel": compute_channel,
            "h_in": content_hash,
            "h_out": content_hash,
            "decode_policy_hash": policy_hash,
            "payload": payload_body
        }

        return turn_structure

    @classmethod
    def verify_turn_integrity(cls, turn_payload: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Verifies the internal cryptographic integrity of a turn payload.
        Returns a tuple of (is_valid: bool, reason: str).
        """
        if not isinstance(turn_payload, dict):
            return False, "Payload must be a dictionary."

        required_keys = ["leaf_version", "turn_index", "agent_role", "h_in", "h_out", "decode_policy_hash", "payload"]
        for key in required_keys:
            if key not in turn_payload:
                return False, f"Missing required top-level key: {key}"

        if turn_payload.get("leaf_version") != cls.VERSION:
            return False, f"Unsupported leaf_version: {turn_payload.get('leaf_version')}"

        try:
            content = turn_payload["payload"]["content"]
            expected_h_in = cls.compute_sha256(content)
            
            decode_params = turn_payload["payload"]["decode_params"]
            expected_policy_hash = cls.generate_policy_hash(decode_params)

            if turn_payload.get("h_in") != expected_h_in:
                return False, "Input content hash mismatch (h_in)."

            if turn_payload.get("decode_policy_hash") != expected_policy_hash:
                return False, "Decode policy hash mismatch."

            return True, "Payload integrity verified successfully."
        except KeyError as e:
            return False, f"Malformed payload body, missing key: {e}"
        except Exception as err:
            return False, f"Integrity check failed with error: {err}"

    @classmethod
    def to_json(cls, turn_payload: Dict[str, Any]) -> str:
        """Serializes payload dictionary to JSON string."""
        return json.dumps(turn_payload, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> Dict[str, Any]:
        """Deserializes JSON string back into payload dictionary."""
        return json.loads(json_str)


# Alias export for legacy imports compatibility
VerifiedTurn = WireFormatV3
VerifiedTurnPayload = WireFormatV3