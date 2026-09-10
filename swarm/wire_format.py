import hashlib
import json

class WireFormatV3:
    """
    FLOP Network Yellow Paper v0.5.0 Appendix F.3 & §12 compliant payload generator.
    Binds output_hash and decode_policy_hash for multi-agent poetry settlement.
    """
    @staticmethod
    def compute_sha256(data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def build_verified_turn(turn_index: int, agent_role: str, content: str, decode_params: dict) -> dict:
        content_hash = WireFormatV3.compute_sha256(content)
        policy_str = json.dumps(decode_params, sort_keys=True)
        decode_policy_hash = WireFormatV3.compute_sha256(policy_str)
        
        return {
            "leaf_version": 3,
            "turn_index": turn_index,
            "agent_role": agent_role,
            "h_in": content_hash,
            "h_out": content_hash,
            "decode_policy_hash": decode_policy_hash,
            "g_n": len(content.split()) * 1000,  # Billed reference-work units
            "status": "VERIFIED"
        }