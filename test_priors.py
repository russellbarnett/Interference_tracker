"""
Unit Tests for Priors Module
=============================
Tests for behavioral priors, adjustments, and edge cases.

Run with: python -m pytest test_priors.py -v
"""

import pytest
from priors import (
    apply_priors, apply_priors_dict,
    RawScores, ScoringContext, AdjustedScores,
    calculate_promo_penalty, calculate_repeat_momentum,
    get_format_enum, ProductFormat, clamp,
    C_MIN_DEFAULT, PROMO_C_MULTIPLIER,
    SELF_MANAGED_C_PENALTY, SELF_MANAGED_K_PENALTY,
    PORTION_BOUND_C_BONUS, MACRO_STRESS_F_MULTIPLIER,
)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestClamp:
    def test_clamp_within_range(self):
        assert clamp(3.0) == 3.0
    
    def test_clamp_below_min(self):
        assert clamp(0.5) == 1.0
    
    def test_clamp_above_max(self):
        assert clamp(6.0) == 5.0
    
    def test_clamp_custom_range(self):
        assert clamp(0.5, 0.0, 1.0) == 0.5
        assert clamp(-0.5, 0.0, 1.0) == 0.0
        assert clamp(1.5, 0.0, 1.0) == 1.0


class TestGetFormatEnum:
    def test_exact_match(self):
        assert get_format_enum("pint") == ProductFormat.PINT
        assert get_format_enum("bar") == ProductFormat.BAR
        assert get_format_enum("can") == ProductFormat.CAN
    
    def test_fuzzy_match(self):
        # "Pint / Tub (multi-serve)" may resolve to PINT or TUB depending on enum order
        assert get_format_enum("Pint / Tub (multi-serve)") in (ProductFormat.PINT, ProductFormat.TUB)
        assert get_format_enum("Single-Serve Bar") == ProductFormat.BAR
        assert get_format_enum("novelty ice cream") == ProductFormat.NOVELTY
    
    def test_unknown_format(self):
        assert get_format_enum("unknown_xyz") == ProductFormat.OTHER


# ═══════════════════════════════════════════════════════════════════════════════
# PROMO PENALTY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPromoPenalty:
    def test_zero_promo_no_penalty(self):
        """No promo activity = no penalty."""
        penalty = calculate_promo_penalty(0.0, 0.0)
        assert penalty == 0.0
    
    def test_heavy_promo_meaningful_penalty(self):
        """Heavy promo reliance = significant penalty."""
        # 80% weeks on deal, 40% avg discount
        penalty = calculate_promo_penalty(0.8, 0.4)
        # 0.6 * 0.8 + 0.4 * 0.4 = 0.48 + 0.16 = 0.64
        assert penalty == pytest.approx(0.64, rel=0.01)
    
    def test_max_promo_capped(self):
        """Penalty capped at 1.0."""
        penalty = calculate_promo_penalty(1.0, 1.0)
        assert penalty == 1.0
    
    def test_promo_frequency_weighted_higher(self):
        """Frequency weighted 0.6 vs depth 0.4."""
        freq_heavy = calculate_promo_penalty(1.0, 0.0)  # 0.6 * 1 + 0.4 * 0 = 0.6
        depth_heavy = calculate_promo_penalty(0.0, 1.0)  # 0.6 * 0 + 0.4 * 1 = 0.4
        assert freq_heavy > depth_heavy


# ═══════════════════════════════════════════════════════════════════════════════
# REPEAT MOMENTUM TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRepeatMomentum:
    def test_strong_decline(self):
        """Greater than 10% decline = 1."""
        momentum, trend = calculate_repeat_momentum(0.85, 1.0)
        assert momentum == 1
        assert trend == pytest.approx(-0.15, rel=0.01)
    
    def test_moderate_decline(self):
        """3-10% decline = 2."""
        momentum, trend = calculate_repeat_momentum(0.95, 1.0)
        assert momentum == 2
    
    def test_stable(self):
        """Within ±3% = 3."""
        momentum, trend = calculate_repeat_momentum(1.0, 1.0)
        assert momentum == 3
        assert trend == pytest.approx(0.0, abs=0.01)
    
    def test_moderate_growth(self):
        """3-10% growth = 4."""
        momentum, trend = calculate_repeat_momentum(1.05, 1.0)
        assert momentum == 4
    
    def test_strong_growth(self):
        """Greater than 10% growth = 5."""
        momentum, trend = calculate_repeat_momentum(1.15, 1.0)
        assert momentum == 5
    
    def test_missing_data_returns_none(self):
        """Missing velocity data returns None."""
        momentum, trend = calculate_repeat_momentum(None, 1.0)
        assert momentum is None
        assert trend is None
    
    def test_zero_baseline_handled(self):
        """Zero baseline returns neutral score."""
        momentum, trend = calculate_repeat_momentum(1.0, 0.0)
        assert momentum == 3
        assert trend == 0.0
    
    def test_boundary_conditions(self):
        """Test values at typical thresholds."""
        # Clear strong decline (below -10%)
        m1, _ = calculate_repeat_momentum(0.88, 1.0)
        assert m1 == 1  # -12% -> strong decline
        
        # Clear moderate decline (between -10% and -3%)
        m2, _ = calculate_repeat_momentum(0.94, 1.0)
        assert m2 == 2  # -6% -> moderate decline
        
        # Clear stable (between -3% and +3%)
        m3, _ = calculate_repeat_momentum(1.01, 1.0)
        assert m3 == 3  # +1% -> stable
        
        # Clear moderate growth (between +3% and +10%)
        m4, _ = calculate_repeat_momentum(1.06, 1.0)
        assert m4 == 4  # +6% -> moderate growth


# ═══════════════════════════════════════════════════════════════════════════════
# APPLY PRIORS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestApplyPriors:
    def test_priors_disabled(self):
        """When use_priors=False, raw scores pass through unchanged."""
        raw = RawScores(M=4, E=4, F=5, B=4, K=3, C=2)
        context = ScoringContext(use_priors=False)
        
        adjusted = apply_priors(raw, context)
        
        assert adjusted.M == 4
        assert adjusted.E == 4
        assert adjusted.F == 5
        assert adjusted.B == 4
        assert adjusted.K == 3
        assert adjusted.C == 2
        assert "Priors disabled" in adjusted.adjustments[0]
    
    def test_c_baseline_elevation(self):
        """C below minimum gets elevated to C_MIN_DEFAULT."""
        raw = RawScores(M=4, E=4, F=5, B=4, K=3, C=1.5)
        context = ScoringContext(use_priors=True, promo_frequency=0, promo_depth=0)
        
        adjusted = apply_priors(raw, context)
        
        assert adjusted.C >= C_MIN_DEFAULT
    
    def test_promo_increases_c(self):
        """Promo reliance increases effective C."""
        raw = RawScores(M=4, E=4, F=5, B=4, K=3, C=2.5)
        
        # No promo
        context_no_promo = ScoringContext(promo_frequency=0.0, promo_depth=0.0)
        adj_no_promo = apply_priors(raw, context_no_promo)
        
        # Heavy promo
        context_promo = ScoringContext(promo_frequency=0.7, promo_depth=0.3)
        adj_promo = apply_priors(raw, context_promo)
        
        assert adj_promo.C > adj_no_promo.C
        assert adj_promo.promo_penalty > 0
    
    def test_macro_stress_increases_f(self):
        """Macro stress multiplies F by 1.15."""
        raw = RawScores(M=4, E=4, F=4.0, B=4, K=3, C=3)
        
        context_stress = ScoringContext(macro_stress=True, format="bar")
        context_no_stress = ScoringContext(macro_stress=False, format="bar")
        
        adj_stress = apply_priors(raw, context_stress)
        adj_no_stress = apply_priors(raw, context_no_stress)
        
        # F should be higher with macro stress
        assert adj_stress.F > adj_no_stress.F
        assert adj_stress.F == pytest.approx(4.0 * MACRO_STRESS_F_MULTIPLIER, rel=0.01)
    
    def test_pint_format_penalty(self):
        """Pints get C and K penalties."""
        raw = RawScores(M=4, E=4, F=5, B=4, K=3, C=3)
        
        context_pint = ScoringContext(format="pint", promo_frequency=0, macro_stress=False)
        context_bar = ScoringContext(format="bar", promo_frequency=0, macro_stress=False)
        
        adj_pint = apply_priors(raw, context_pint)
        adj_bar = apply_priors(raw, context_bar)
        
        # Pint should have higher C and K
        assert adj_pint.C > adj_bar.C
        assert adj_pint.K > adj_bar.K
    
    def test_portion_bound_bonus(self):
        """Portion-bound formats get C reduction."""
        raw = RawScores(M=4, E=4, F=5, B=4, K=3, C=3)
        
        context_bar = ScoringContext(format="bar", promo_frequency=0, macro_stress=False)
        
        adj = apply_priors(raw, context_bar)
        
        # C should be reduced (bonus is negative)
        # Note: C starts at 3, but baseline elevation to 2.5 doesn't apply since 3 > 2.5
        # So C = 3 + PORTION_BOUND_C_BONUS (-0.15) = 2.85
        assert adj.C == pytest.approx(3 + PORTION_BOUND_C_BONUS, rel=0.01)
    
    def test_adjustments_logged(self):
        """All adjustments are logged transparently."""
        raw = RawScores(M=4, E=4, F=4, B=4, K=3, C=2)
        context = ScoringContext(
            promo_frequency=0.5,
            promo_depth=0.3,
            macro_stress=True,
            format="pint"
        )
        
        adjusted = apply_priors(raw, context)
        
        # Should have multiple adjustments logged
        assert len(adjusted.adjustments) > 1
        
        # Check specific adjustment types are mentioned
        log_text = "\n".join(adjusted.adjustments)
        assert "Promo reliance" in log_text
        assert "Macro stress" in log_text
        assert "Self-managed format" in log_text


# ═══════════════════════════════════════════════════════════════════════════════
# DICTIONARY INTERFACE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestDictInterface:
    def test_apply_priors_dict(self):
        """Test dictionary-based interface."""
        raw_scores = {"M": 4, "E": 4, "F": 5, "B": 4, "K": 3, "C": 3}
        context = {
            "cohort": "mixed",
            "macro_stress": True,
            "promo_frequency": 0.3,
            "promo_depth": 0.2,
            "format": "pint"
        }
        
        adjusted, adjustments = apply_priors_dict(raw_scores, context)
        
        assert "M" in adjusted
        assert "C" in adjusted
        assert len(adjustments) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# REGRESSION TEST: ICE CREAM PINTS FIXTURE
# ═══════════════════════════════════════════════════════════════════════════════

class TestIceCreamPintsRegression:
    """
    Regression tests for ice cream pints using mock data.
    Tests Serendipity, Ben & Jerry's, Häagen-Dazs scenarios.
    """
    
    @pytest.fixture
    def serendipity_context(self):
        """Serendipity: legacy brand, low promo reliance, positive trend."""
        return {
            "cohort": "younger",
            "occasion": "evening",
            "macro_stress": True,
            "category": "ice_cream_pints",
            "promo_frequency": 0.15,  # Low promo
            "promo_depth": 0.10,
            "ups_pw_13": 2.8,  # Growing
            "ups_pw_26": 2.5,
            "format": "pint",
            "use_priors": True,
        }
    
    @pytest.fixture
    def serendipity_scores(self):
        """Serendipity raw scores: high F due to legacy."""
        return {"M": 5, "E": 5, "F": 5, "B": 4, "K": 3, "C": 2}
    
    @pytest.fixture
    def ben_jerrys_context(self):
        """Ben & Jerry's: legacy brand, moderate promo, stable trend."""
        return {
            "cohort": "mixed",
            "occasion": "evening",
            "macro_stress": True,
            "category": "ice_cream_pints",
            "promo_frequency": 0.45,  # Moderate promo
            "promo_depth": 0.25,
            "ups_pw_13": 3.0,
            "ups_pw_26": 3.0,  # Stable
            "format": "pint",
            "use_priors": True,
        }
    
    @pytest.fixture
    def ben_jerrys_scores(self):
        return {"M": 5, "E": 4, "F": 5, "B": 4, "K": 3, "C": 2}
    
    @pytest.fixture
    def haagen_dazs_context(self):
        """Häagen-Dazs: premium legacy, high promo (distribution push), declining."""
        return {
            "cohort": "older",
            "occasion": "evening",
            "macro_stress": True,
            "category": "ice_cream_pints",
            "promo_frequency": 0.60,  # High promo
            "promo_depth": 0.35,
            "ups_pw_13": 2.2,  # Declining
            "ups_pw_26": 2.6,
            "format": "pint",
            "use_priors": True,
        }
    
    @pytest.fixture
    def haagen_dazs_scores(self):
        return {"M": 5, "E": 4, "F": 5, "B": 4, "K": 3, "C": 3}
    
    def test_serendipity_lower_promo_penalty(self, serendipity_context, serendipity_scores,
                                              ben_jerrys_context, ben_jerrys_scores):
        """Serendipity gets lower promo penalty than Ben & Jerry's."""
        ser_adj, ser_log = apply_priors_dict(serendipity_scores, serendipity_context)
        bj_adj, bj_log = apply_priors_dict(ben_jerrys_scores, ben_jerrys_context)
        
        # Serendipity has lower promo reliance, so should have lower C increase from promo
        # Note: Both get baseline elevation and format penalty, but promo component differs
        ser_promo_penalty = calculate_promo_penalty(
            serendipity_context["promo_frequency"],
            serendipity_context["promo_depth"]
        )
        bj_promo_penalty = calculate_promo_penalty(
            ben_jerrys_context["promo_frequency"],
            ben_jerrys_context["promo_depth"]
        )
        
        assert ser_promo_penalty < bj_promo_penalty
    
    def test_heavy_promo_increases_c_more(self, haagen_dazs_context, haagen_dazs_scores,
                                           serendipity_context, serendipity_scores):
        """Promo-heavy brand gets higher effective C."""
        hd_adj, hd_log = apply_priors_dict(haagen_dazs_scores, haagen_dazs_context)
        ser_adj, ser_log = apply_priors_dict(serendipity_scores, serendipity_context)
        
        # Häagen-Dazs has higher promo reliance
        assert hd_adj["C"] > ser_adj["C"]
    
    def test_repeat_momentum_higher_for_growing_brand(self, serendipity_context, serendipity_scores,
                                                       haagen_dazs_context, haagen_dazs_scores):
        """Serendipity (growing) has higher RepeatMomentum than Häagen-Dazs (declining)."""
        ser_momentum, ser_trend = calculate_repeat_momentum(
            serendipity_context["ups_pw_13"],
            serendipity_context["ups_pw_26"]
        )
        hd_momentum, hd_trend = calculate_repeat_momentum(
            haagen_dazs_context["ups_pw_13"],
            haagen_dazs_context["ups_pw_26"]
        )
        
        assert ser_momentum > hd_momentum
        assert ser_trend > 0  # Serendipity growing
        assert hd_trend < 0   # Häagen-Dazs declining
    
    def test_report_includes_adjustments(self, serendipity_context, serendipity_scores):
        """Report includes the adjustments log."""
        adj, adjustments = apply_priors_dict(serendipity_scores, serendipity_context)
        
        assert len(adjustments) > 0
        log_text = "\n".join(adjustments)
        
        # Should mention key context
        assert "cohort" in log_text.lower() or "Context" in log_text


# ═══════════════════════════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
