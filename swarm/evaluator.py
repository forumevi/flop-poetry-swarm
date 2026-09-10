"""
Semantic & Rhythmic Evaluator for Flop Poetry Swarm.
Evaluates generated stanzas using multi-criteria scoring to select the optimal payload.
"""
import re

class PoetryEvaluator:
    def __init__(self):
        # Ağırlıklandırılmış jüri metrikleri
        self.weights = {
            "rhythm_score": 0.35,
            "imagery_density": 0.35,
            "cohesion_score": 0.30
        }

    def evaluate_stanza(self, stanza: str) -> dict:
        """
        Gelen kıtayı hece ritmi, imge zenginliği ve yapısal bütünlük açısından skorlar.
        """
        lines = [line.strip() for line in stanza.strip().split("\n") if line.strip()]
        if not lines:
            return {"total_score": 0.0, "metrics": {}}

        # 1. Ritim / Hece Dengesi Kontrolü
        syllable_counts = [self._count_syllables(line) for line in lines]
        avg_syllables = sum(syllable_counts) / len(syllable_counts)
        variance = sum((s - avg_syllables) ** 2 for s in syllable_counts) / len(syllable_counts)
        rhythm_score = max(0.0, 1.0 - (variance / 20.0))

        # 2. Kelime Çeşitliliği / İmge Yoğunluğu
        words = re.findall(r'\b\w+\b', stanza.lower())
        unique_words = set(words)
        imagery_density = len(unique_words) / max(len(words), 1)

        # 3. Yapısal Bütünlük
        cohesion_score = 1.0 if len(lines) in [4, 8, 12] else 0.7

        total_score = (
            rhythm_score * self.weights["rhythm_score"] +
            imagery_density * self.weights["imagery_density"] +
            cohesion_score * self.weights["cohesion_score"]
        )

        return {
            "total_score": round(total_score, 4),
            "metrics": {
                "rhythm_score": round(rhythm_score, 4),
                "imagery_density": round(imagery_density, 4),
                "cohesion_score": round(cohesion_score, 4)
            }
        }

    def select_best_variant(self, variants: list) -> tuple:
        """
        Best-of-N sampling: Üretilen varyasyonlar arasından en yüksek skora sahip olanı seçer.
        """
        best_stanza = None
        best_score = -1.0
        best_eval = {}

        for stanza in variants:
            res = self.evaluate_stanza(stanza)
            if res["total_score"] > best_score:
                best_score = res["total_score"]
                best_stanza = stanza
                best_eval = res

        return best_stanza, best_eval

    def _count_syllables(self, text: str) -> int:
        """Türkçe / İngilizce sesli harf hece sayım mantığı"""
        text = text.lower()
        vowels = "aeıioöuü"
        return sum(1 for char in text if char in vowels)

if __name__ == "__main__":
    evaluator = PoetryEvaluator()
    sample = "Karanlık teknoloji derinlerde yankılanır\nAlgoritmalar gece boyu akıp taranır"
    print("Test Evaluation Result:", evaluator.evaluate_stanza(sample))