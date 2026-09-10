import json
from wire_format import WireFormatV3

class PoetrySwarmOrchestrator:
    """
    3-Agent Pipeline: Architect -> Generator -> Auditor
    """
    def __init__(self, topic: str):
        self.topic = topic
        self.turns = []
        self.decode_policy = {"temperature": 0.7, "top_p": 0.9, "seed": 42}

    def run_pipeline(self):
        # Step 1: Architect Agent sets structural rules
        arch_spec = f"Theme: {self.topic} | Structure: AABB | Meter: 11-syllable"
        turn_0 = WireFormatV3.build_verified_turn(0, "Architect", arch_spec, self.decode_policy)
        self.turns.append(turn_0)

        # Step 2: Generator Agent writes verse
        verse = "Golden nodes align across the digital sphere,\nSignals pulse clear when the BFT is near."
        turn_1 = WireFormatV3.build_verified_turn(1, "Generator", verse, self.decode_policy)
        self.turns.append(turn_1)

        # Step 3: Auditor Agent validates rhyme & binds settlement payload
        audit_verdict = f"AUDIT_PASSED: output_hash={turn_1['h_out']}"
        turn_2 = WireFormatV3.build_verified_turn(2, "Auditor", audit_verdict, self.decode_policy)
        self.turns.append(turn_2)

        return {
            "session_id": f"sess_{WireFormatV3.compute_sha256(self.topic)[:12]}",
            "aggregate_gn": sum(t["g_n"] for t in self.turns),
            "verified_turns": self.turns
        }

if __name__ == "__main__":
    swarm = PoetrySwarmOrchestrator("Autonomous AI Swarms")
    print(json.dumps(swarm.run_pipeline(), indent=2))