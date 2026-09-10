"""
Semantic & Rhythmic Evaluator for Flop Poetry Swarm.
Evaluates generated stanzas using multi-criteria scoring to select the optimal payload.
"""
import re

class PoetryEvaluator:
    def __init__(self):
        # Weighted metric distribution
        self.weights = {
            "rhythm_score": 0.35,
            "imagery_density": 0.35,
            "cohesion_score": 0.30
        }

    def evaluate_stanza(self, stanza: str) -> dict:
        """
        Scores input stanza based on syllabic rhythm, imagery density, and structural cohesion.
        """
        lines = [line.strip() for line in stanza.strip().split("\n") if line.strip()]
        if not lines:
            return {"total_score": 0.0, "metrics": {}}

        # 1. Rhythm / Syllabic Balance Check
        syllable_counts = [self._count_syllables(line) for line in lines]
        avg_syllables = sum(syllable_counts) / len(syllable_counts)
        variance = sum((s - avg_syllables) ** 2 for s in syllable_counts) / len(syllable_counts)
        rhythm_score = max(0.0, 1.0 - (variance / 20.0))

        # 2. Vocabulary Diversity / Imagery Density
        words = re.findall(r'\b\w+\b', stanza.lower())
        unique_words = set(words)
        imagery_density = len(unique_words) / max(len(words), 1)

        # 3. Structural Cohesion
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
        Best-of-N sampling: Selects the variant with the highest total evaluation score.
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
        """Standard English vowel syllable counter with basic silent 'e' heuristic."""
        text = text.lower()
        words = re.findall(r'\b[a-z]+\b', text)
        total_syllables = 0
        for word in words:
            # Count vowel groups
            syllables = len(re.findall(r'[aeiouy]+', word))
            # Subtract silent 'e' at the end of word if applicable
            if word.endswith('e') and not word.endswith('le') and syllables > 1:
                syllables -= 1
            total_syllables += max(1, syllables)
        return total_syllables

if __name__ == "__main__":
    evaluator = PoetryEvaluator()
    sample = "Through dark webs the stream of data flows,\nAn algorithm sparks as midnight grows."
    print("Test Evaluation Result:", evaluator.evaluate_stanza(sample))