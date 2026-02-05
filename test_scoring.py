"""
Unit tests for scoring module (S-Score and rationale validation).
Run: python -m pytest test_scoring.py -v
"""

import pytest
from scoring import calculate_s_score, validate_rationale


class TestCalculateSScore:
    """S = (M×E×F) / (B×K×C); denominator clamped to min 1.0."""

    def test_my_mochi_style_denominator_collapse(self):
        # B=1, K=1, C=1 -> den=1, num=4*4*4=64 -> S=64
        assert calculate_s_score(4, 4, 4, 1, 1, 1) == 64.0

    def test_pint_style_high_denominator(self):
        # 5*5*5 / (4*3*3) = 125/36 ≈ 3.47
        assert calculate_s_score(5, 5, 5, 4, 3, 3) == pytest.approx(125 / 36, rel=0.01)

    def test_accepts_ints(self):
        assert calculate_s_score(4, 4, 4, 1, 1, 1) == 64.0

    def test_accepts_floats(self):
        assert calculate_s_score(4.0, 4.0, 4.0, 1.0, 1.0, 1.0) == 64.0

    def test_denominator_clamped_min_one(self):
        # Even with B=0, K=0, C=0 we clamp den to 1.0
        assert calculate_s_score(1, 1, 1, 0, 0, 0) == 1.0

    def test_negative_numerator_returns_zero(self):
        assert calculate_s_score(-1, 1, 1, 1, 1, 1) == 0.0

    def test_zero_result_safe(self):
        assert calculate_s_score(0, 0, 0, 1, 1, 1) == 0.0

    def test_large_scores_no_inf(self):
        # 5*5*5 / 1 = 125
        assert calculate_s_score(5, 5, 5, 1, 1, 1) == 125.0
        assert calculate_s_score(5, 5, 5, 1, 1, 1) != float("inf")


class TestValidateRationale:
    def test_empty_fails(self):
        assert validate_rationale("") is False
        assert validate_rationale("   ") is False

    def test_short_fails(self):
        assert validate_rationale("Too short") is False
        assert validate_rationale("123456789012345678901234") is False  # 24 alnum

    def test_25_alnum_passes(self):
        assert validate_rationale("a" * 25) is True
        assert validate_rationale("This is a reasonable override rationale for the score.") is True

    def test_strip_whitespace(self):
        assert validate_rationale("  " + "a" * 25 + "  ") is True
