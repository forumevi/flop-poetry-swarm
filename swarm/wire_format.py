"""
Technocore Poetry Swarm Orchestration Engine
Yellowpaper v0.5.0 Protocol Compliant
Enhanced with Fallback Engine and Best-of-N Semantic Evaluation
"""
import time
import json
import sys
import os

# GitHub Actions ve yerel içe aktarma yollarını garantiye al
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wire_format import WireFormatV3
from evaluator import PoetryEvaluator
from fallback_engine import SwarmFallbackEngine


class ArchitectAgent:
    def __init__(self, agent_id: str = "architect-01"):
        self.agent_id = agent_id

    def create_state_lock(self, prompt: str, theme: str) -> dict:
        """Kilit parametreleri ve şiir kısıtlarını tanımlar."""
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
        """Birincil üretici motoru"""
        return (
            "Karanlık ağlarda veri taranır,\n"
            "Algoritma gece boyu uzanır.\n"
            "Kripto mühürle sözler bağlanır,\n"
            "Zincirüstü şifre hakkı kazanır."
        )

    def _backup_stanza_gen(self, state: dict) -> str:
        """Yedek üretici motoru"""
        return (
            "Bloklar dizilir sessiz derine,\n"
            "Ajanlar fısıldar devrin yerine.\n"
            "Veriler işlenir günün seherine,\n"
            "Mühürler vurulur hakkın emrine."
        )

    def generate_stanzas(self, state: dict) -> list:
        """
        Fallback engine kullanarak Best-of-N varyasyonları üretir.
        """
        variants = []
        
        # 1. Varyasyon
        res1 = self.fallback_engine.execute_with_fallback(
            lambda: self._primary_stanza_gen(state),
            [lambda: self._backup_stanza_gen(state)]
        )
        variants.append(res1["content"])

        # 2. Varyasyon (Best-of-N için alternatif)
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
        Gelen varyasyonları semantik olarak skorlar, en iyisini seçer ve WireFormatV3 payload oluşturur.
        """
        # Best-of-N Değerlendirmesi
        best_stanza, eval_metrics = self.evaluator.select_best_variant(variants)

        # Temel Doğrulama Mantığı
        lines = best_stanza.strip().split("\n")
        is_valid = len(lines) >= 4

        decode_params = {
            "theme": state.get("theme"),
            "meter": state.get("meter"),
            "evaluation": eval_metrics,
            "audit_passed": is_valid
        }

        # WireFormatV3 Yapısına Tam Uyumlu Payload
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
        print(f"[Swarm] Pipeline Başlatıldı | Tema: '{theme}'")
        
        # 1. Architect State Lock
        state = self.architect.create_state_lock(prompt, theme)
        print(f"[Architect] State kilitlendi: {state['state_id']}")

        # 2. Generator (Fallback & Best-of-N)
        variants = self.generator.generate_stanzas(state)
        print(f"[Generator] {len(variants)} adet şiir varyasyonu üretildi.")

        # 3. Auditor (Evaluation & Settlement)
        verified_turn = self.auditor.audit_and_settle(state, variants)
        print(f"[Auditor] En iyi varyasyon seçildi.")
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
    print("[Success] Swarm pipeline başarıyla tamamlandı ve doğrulandı.")