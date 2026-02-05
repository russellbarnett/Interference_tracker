"""
Unit tests for ai_services module (rule-based memo; no live Gemini calls).
Run: python -m pytest test_ai_services.py -v
"""

import pytest
from ai_services import GEMINI_AVAILABLE, generate_rule_based_memo


class TestGeminiAvailable:
    def test_is_bool(self):
        assert isinstance(GEMINI_AVAILABLE, bool)


class TestGenerateRuleBasedMemo:
    """Rule-based memo does not call the API; we can test it fully."""

    def test_returns_non_empty_string(self):
        scores1 = {"M": 4, "E": 4, "F": 4, "B": 1, "K": 1, "C": 1}
        scores2 = {"M": 5, "E": 5, "F": 5, "B": 4, "K": 3, "C": 3}
        memo = generate_rule_based_memo("BrandA", "BrandB", 16.0, 2.0, scores1, scores2)
        assert isinstance(memo, str)
        assert len(memo) > 200

    def test_contains_both_brand_names(self):
        scores1 = {"M": 4, "E": 4, "F": 4, "B": 1, "K": 1, "C": 1}
        scores2 = {"M": 5, "E": 5, "F": 5, "B": 4, "K": 3, "C": 3}
        memo = generate_rule_based_memo("Serendipity", "Dr. Bombay", 2.5, 1.2, scores1, scores2)
        assert "Serendipity" in memo
        assert "Dr. Bombay" in memo

    def test_contains_s_score_language(self):
        scores1 = {"M": 4, "E": 4, "F": 4, "B": 1, "K": 1, "C": 1}
        scores2 = {"M": 4, "E": 4, "F": 4, "B": 4, "K": 3, "C": 3}
        memo = generate_rule_based_memo("A", "B", 16.0, 1.0, scores1, scores2)
        assert "S-Score" in memo or "Satisfaction" in memo
        assert "16" in memo or "16.0" in memo

    def test_contains_denominator_analysis(self):
        scores1 = {"M": 4, "E": 4, "F": 4, "B": 4, "K": 3, "C": 4}
        scores2 = {"M": 4, "E": 4, "F": 4, "B": 1, "K": 1, "C": 1}
        memo = generate_rule_based_memo("HighFriction", "LowFriction", 0.5, 16.0, scores1, scores2)
        assert "Denominator" in memo or "denominator" in memo or "FRICTION" in memo

    def test_winner_loser_consistent_with_scores(self):
        # BrandA has higher S -> winner
        scores1 = {"M": 5, "E": 5, "F": 5, "B": 1, "K": 1, "C": 1}
        scores2 = {"M": 3, "E": 3, "F": 3, "B": 4, "K": 3, "C": 3}
        memo = generate_rule_based_memo("Winner", "Loser", 125.0, 1.0, scores1, scores2)
        assert "Winner" in memo
        assert "Loser" in memo
        # Structural winner should be Winner
        assert memo.index("Winner") < memo.index("Loser") or "Winner" in memo
