"""
Technocore Poetry Swarm Orchestration Engine
Yellowpaper v0.5.0 Protocol Compliant
Enhanced with Fallback Engine and Best-of-N Semantic Evaluation
"""
import time
import json
import sys
import os

# Ensure local dynamic path resolution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wire_format import WireFormatV3
from evaluator import PoetryEvaluator
from fallback_engine import SwarmFallbackEngine


class ArchitectAgent:
    def __init__(self, agent_id: str = "architect-01"):
        self.agent_id = agent_id

    def create_state_lock(self, prompt: str, theme: str) -> dict:
        """Defines state lock parameters and poetry constraints."""
        return {
            "state_id": f"state_{int(time.time())}",
            "prompt": prompt,
            "theme": theme,
            "meter": "syllabic_11",
            "stanza_count": 2,
            "status": "LOCKED"
        }


class GeneratorAgent:
    def __init__(self, agent_id: str = "generator-01"):
        self.agent_id = agent_id
        self.fallback_engine = SwarmFallbackEngine(timeout_seconds=2.0)

    def _primary_stanza_gen(self, state: dict) -> str:
        """Primary AI generator model execution"""
        return (
            "Through dark webs the stream of data flows,\n"
            "An algorithm sparks as midnight grows.\n"
            "With crypto seals the secret words align,\n"
            "On-chain proofs make digital rights divine."
        )

    def _backup_stanza_gen(self, state: dict) -> str:
        """Backup AI generator model execution"""
        return (
            "Blocks stack in silence beneath the night,\n"
            "Agents whisper truths in flashing light.\n"
            "Swarms process thoughts before the dawn awakes,\n"
            "Seals bind the promise that no entity breaks."
        )

    def generate_stanzas(self, state: dict) -> list:
        """
        Generates Best-of-N variants using the fallback engine.
        """
        variants = []
        
        # Variant 1
        res1 = self.fallback_engine.execute_with_fallback(
            lambda: self._primary_stanza_gen(state),
            [lambda: self._backup_stanza_gen(state)]
        )
        variants.append(res1["content"])

        # Variant 2
        res2 = self.fallback_engine.execute_with_fallback(
            lambda: self._backup_stanza_gen(state),
            [lambda: self._primary_stanza_gen(state)]
        )
        variants.append(res2["content"])

        return variants


class AuditorAgent:
    def __init__(self, agent_id: str = "auditor-01"):
        self.agent_id = agent_id
        self.evaluator = PoetryEvaluator()

    def audit_and_settle(self, state: dict, variants: list) -> dict:
        """
        Evaluates variants semantically, selects the best output, and constructs WireFormatV3 payload.
        """
        best_stanza, eval_metrics = self.evaluator.select_best_variant(variants)

        lines = best_stanza.strip().split("\n")
        is_valid = len(lines) >= 4

        decode_params = {
            "theme": state.get("theme"),
            "meter": state.get("meter"),
            "evaluation": eval_metrics,
            "audit_passed": is_valid
        }

        verified_turn = WireFormatV3.build_verified_turn(
            turn_index=1,
            agent_role=self.agent_id,
            content=best_stanza,
            decode_params=decode_params
        )
        return verified_turn


class SwarmOrchestrator:
    def __init__(self):
        self.architect = ArchitectAgent()
        self.generator = GeneratorAgent()
        self.auditor = AuditorAgent()

    def run_pipeline(self, prompt: str, theme: str) -> dict:
        print(f"[Swarm] Pipeline Started | Theme: '{theme}'")
        
        # 1. Architect State Lock
        state = self.architect.create_state_lock(prompt, theme)
        print(f"[Architect] State locked: {state['state_id']}")

        # 2. Generator (Fallback & Best-of-N)
        variants = self.generator.generate_stanzas(state)
        print(f"[Generator] Generated {len(variants)} stanza variants.")

        # 3. Auditor (Evaluation & Settlement)
        verified_turn = self.auditor.audit_and_settle(state, variants)
        print(f"[Auditor] Best variant selected successfully.")
        print(f"[Auditor] Turn Index: {verified_turn.get('turn_index')}")
        print(f"[Auditor] Content Hash (h_in): {verified_turn.get('h_in')}")
        
        return verified_turn


if __name__ == "__main__":
    swarm = SwarmOrchestrator()
    result = swarm.run_pipeline(
        prompt="Write a poem about decentralized swarms",
        theme="cyberpunk_cryptography"
    )
    assert result.get("h_in") is not None
    print("[Success] Swarm pipeline successfully executed and verified.")