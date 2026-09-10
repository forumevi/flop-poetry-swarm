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
            except Exception:
                continue

        return {
            "content": "Algorithmic flows continuously stream,\nCrypto networks recreate the dream.",
            "provider_index": -1,
            "latency_ms": 0.0,
            "status": "SAFE_FALLBACK"
        }