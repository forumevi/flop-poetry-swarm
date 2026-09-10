"""
Fallback Engine for Flop Poetry Swarm Generator Agent.
Ensures zero-downtime stanza generation with graceful degradation.
"""
import time
from typing import Callable, List, Any

class SwarmFallbackEngine:
    def __init__(self, timeout_seconds: float = 2.0):
        self.timeout_seconds = timeout_seconds

    def execute_with_fallback(self, primary_provider: Callable, fallback_providers: List[Callable], *args, **kwargs) -> Any:
        """
        Birincil üretim metodunu dener. Başarısız olursa sırayla yedek sağlayıcılara geçer.
        """
        providers = [primary_provider] + fallback_providers

        for idx, provider in enumerate(providers):
            try:
                start_time = time.time()
                result = provider(*args, **kwargs)
                elapsed = time.time() - start_time

                if result and elapsed <= self.timeout_seconds:
                    return {
                        "content": result,
                        "provider_index": idx,
                        "latency_ms": round(elapsed * 1000, 2),
                        "status": "SUCCESS"
                    }
            except Exception as e:
                # İlgili sağlayıcı hata verirse bir sonrakine yumuşak geçiş yap
                continue

        # Tüm sağlayıcılar başarısız olursa güvenli varsayılan metni üret
        return {
            "content": "Algoritmik akış kesintisiz sürer,\nKripto ağlar yanıtı yeniden üretir.",
            "provider_index": -1,
            "latency_ms": 0.0,
            "status": "SAFE_FALLBACK"
        }

if __name__ == "__main__":
    engine = SwarmFallbackEngine()

    def slow_primary():
        time.sleep(0.1)
        return "Birincil LLM üretimi yapıldı."

    def backup():
        return "Yedek LLM üretimi yapıldı."

    res = engine.execute_with_fallback(slow_primary, [backup])
    print("Test Fallback Engine Result:", res)