"""
HARD DATA MODULE - Elbow Interference Theory™
=============================================
Deterministic, human-entered constants and lookups.
NO AI CALLS. NO BUSINESS LOGIC. DATA CONTAINER ONLY.

This module provides:
- Cohort elasticity coefficients (F/C sensitivity multipliers)
- Category-level benchmarks (promo frequency/depth ranges)
- External support snippets (behavioral truths for investor memos)

WHAT IS HARD-CODED HERE (see hard_coded_rules.md):
✅ Category benchmark ranges for promo frequency and promo depth
✅ Cohort sensitivity multipliers (younger/mixed/older)
✅ Category-level behavioral truths (short bullets)

WHAT IS NOT HARD-CODED HERE:
❌ Brand-specific M/E/F/B/K/C values (AI-inferred)
❌ Competitor claims (legal risk)
❌ Retailer-specific performance (requires fresh data)
❌ Time-bound metrics (stale data risk)

All values below are PLACEHOLDER DEFAULTS with TODO tags.
Replace with proprietary data from industry reports.

Author: Russell Barnett © 2026
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CategoryBenchmark:
    """Benchmark data for a product category."""
    typical_promo_frequency_range: tuple  # (min, max) as 0-1 scale
    typical_promo_depth_range: tuple       # (min, max) as 0-1 scale
    typical_velocity_13_26_trend_benchmark: float  # Expected trend % (-0.05 = -5%)
    price_tier_notes: str                  # Human-readable pricing context


@dataclass
class CohortElasticity:
    """Elasticity coefficients by cohort segment."""
    f_sensitivity: float      # How much F (Familiarity) matters
    c_sensitivity: float      # How much C (Cognitive) penalizes
    promo_response: float     # How reactive to promotions
    trend_weight: float       # How much trend vs level matters
    notes: str                # Human-readable context


@dataclass
class HardDataInputs:
    """
    Container for all deterministic, human-entered data.
    No AI calls. No computed values. Pure data.
    """
    cohort_elasticity: Dict[str, CohortElasticity] = field(default_factory=dict)
    category_benchmarks: Dict[str, CategoryBenchmark] = field(default_factory=dict)
    retailer_belief_support: Dict[str, List[str]] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# COHORT ELASTICITY DATA
# ═══════════════════════════════════════════════════════════════════════════════
# These multipliers adjust how much Familiarity (F) and Cognitive (C) matter
# by demographic cohort. Used in priors adjustments, not direct scoring.
#
# TODO: Validate these coefficients against proprietary research annually.
# TODO: Consider adding income-based or geographic cohort variants.

_COHORT_ELASTICITY = {
    "younger": CohortElasticity(
        f_sensitivity=0.7,      # TODO: Validate - Less anchored to legacy brands
        c_sensitivity=1.3,      # TODO: Validate - More sensitive to cognitive friction
        promo_response=1.2,     # TODO: Validate - Higher promo responsiveness
        trend_weight=0.7,       # TODO: Validate - Trend-followers
        notes="Gen Z/Millennials: value-seeking, trend-sensitive, lower brand loyalty"
    ),
    "mixed": CohortElasticity(
        f_sensitivity=1.0,      # Baseline (no adjustment)
        c_sensitivity=1.0,      # Baseline (no adjustment)
        promo_response=1.0,     # Baseline (no adjustment)
        trend_weight=0.5,       # Balanced
        notes="Broad demographic: balanced sensitivities across dimensions"
    ),
    "older": CohortElasticity(
        f_sensitivity=1.4,      # TODO: Validate - Strong legacy brand preference
        c_sensitivity=0.8,      # TODO: Validate - Less bothered by complexity
        promo_response=0.7,     # TODO: Validate - Lower promo chase
        trend_weight=0.3,       # TODO: Validate - Habit-driven
        notes="Gen X/Boomers: habitual, brand-loyal, less price-sensitive"
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORY BENCHMARKS
# ═══════════════════════════════════════════════════════════════════════════════
# Promo frequency and depth benchmarks by category.
# Used for GUARDRAILS ONLY (flagging outliers), not for scoring.
#
# TODO: Update quarterly with latest industry report data (Circana, Nielsen, etc.)
# TODO: Add source citations for each category benchmark.
#
# FORMAT:
#   typical_promo_frequency_range: (min, max) as 0-1 scale (e.g., 0.30 = 30%)
#   typical_promo_depth_range: (min, max) as 0-1 scale
#   typical_velocity_13_26_trend_benchmark: Expected trend % (-0.05 = -5% decline)

_CATEGORY_BENCHMARKS = {
    # ───────────────────────────────────────────────────────────────────────────
    # FROZEN
    # TODO: Source - Industry report Q1 2026
    # ───────────────────────────────────────────────────────────────────────────
    "ice_cream": CategoryBenchmark(
        typical_promo_frequency_range=(0.30, 0.55),  # TODO: Verify with Circana
        typical_promo_depth_range=(0.15, 0.30),      # TODO: Verify with Circana
        typical_velocity_13_26_trend_benchmark=-0.02,  # TODO: Update quarterly
        price_tier_notes="Premium pints: $5-7. Super-premium: $7-10. Value: $3-5."
    ),
    "ice_cream_pints": CategoryBenchmark(
        typical_promo_frequency_range=(0.35, 0.55),  # TODO: Verify with Circana
        typical_promo_depth_range=(0.18, 0.28),      # TODO: Verify with Circana
        typical_velocity_13_26_trend_benchmark=-0.03,  # TODO: Update quarterly
        price_tier_notes="Pint format under pressure. Premium positioning required."
    ),
    "ice_cream_novelties": CategoryBenchmark(
        typical_promo_frequency_range=(0.25, 0.45),  # TODO: Verify with Circana
        typical_promo_depth_range=(0.12, 0.22),      # TODO: Verify with Circana
        typical_velocity_13_26_trend_benchmark=0.02,   # TODO: Update quarterly
        price_tier_notes="Novelties growing. Portion control drives repeat."
    ),
    "frozen_snacks": CategoryBenchmark(
        typical_promo_frequency_range=(0.20, 0.40),  # TODO: Verify with Circana
        typical_promo_depth_range=(0.10, 0.20),      # TODO: Verify with Circana
        typical_velocity_13_26_trend_benchmark=0.03,   # TODO: Update quarterly
        price_tier_notes="Handheld formats outperforming multi-serve."
    ),
    
    # ───────────────────────────────────────────────────────────────────────────
    # BEVERAGES
    # TODO: Source - Industry report Q1 2026
    # ───────────────────────────────────────────────────────────────────────────
    "carbonated_soft_drinks": CategoryBenchmark(
        typical_promo_frequency_range=(0.40, 0.60),  # TODO: Verify with Nielsen
        typical_promo_depth_range=(0.20, 0.35),      # TODO: Verify with Nielsen
        typical_velocity_13_26_trend_benchmark=-0.01,  # TODO: Update quarterly
        price_tier_notes="Highly commoditized. Promo-driven category."
    ),
    "functional_beverages": CategoryBenchmark(
        typical_promo_frequency_range=(0.15, 0.35),  # TODO: Verify with Nielsen
        typical_promo_depth_range=(0.08, 0.18),      # TODO: Verify with Nielsen
        typical_velocity_13_26_trend_benchmark=0.05,   # TODO: Update quarterly
        price_tier_notes="Premium pricing accepted. Health claims drive purchase."
    ),
    "energy_drinks": CategoryBenchmark(
        typical_promo_frequency_range=(0.20, 0.40),  # TODO: Verify with Nielsen
        typical_promo_depth_range=(0.10, 0.22),      # TODO: Verify with Nielsen
        typical_velocity_13_26_trend_benchmark=0.04,   # TODO: Update quarterly
        price_tier_notes="Brand-loyal category. Ritual-driven consumption."
    ),
    "water": CategoryBenchmark(
        typical_promo_frequency_range=(0.35, 0.55),  # TODO: Verify with Nielsen
        typical_promo_depth_range=(0.15, 0.30),      # TODO: Verify with Nielsen
        typical_velocity_13_26_trend_benchmark=0.01,   # TODO: Update quarterly
        price_tier_notes="Commoditized. Differentiation via branding/function."
    ),
    
    # ───────────────────────────────────────────────────────────────────────────
    # SNACKS
    # TODO: Source - Industry report Q1 2026
    # ───────────────────────────────────────────────────────────────────────────
    "salty_snacks": CategoryBenchmark(
        typical_promo_frequency_range=(0.40, 0.60),  # TODO: Verify with Circana
        typical_promo_depth_range=(0.18, 0.32),      # TODO: Verify with Circana
        typical_velocity_13_26_trend_benchmark=0.01,   # TODO: Update quarterly
        price_tier_notes="Scale matters. Private label pressure increasing."
    ),
    "bars_snacks": CategoryBenchmark(
        typical_promo_frequency_range=(0.25, 0.45),  # TODO: Verify with Circana
        typical_promo_depth_range=(0.12, 0.25),      # TODO: Verify with Circana
        typical_velocity_13_26_trend_benchmark=0.02,   # TODO: Update quarterly
        price_tier_notes="Portion-bound format. Functional claims add premium."
    ),
    "cookies_crackers": CategoryBenchmark(
        typical_promo_frequency_range=(0.35, 0.55),
        typical_promo_depth_range=(0.15, 0.28),
        typical_velocity_13_26_trend_benchmark=-0.01,
        price_tier_notes="Legacy brands dominate. Innovation in portion control."
    ),
    "confectionery": CategoryBenchmark(
        typical_promo_frequency_range=(0.30, 0.50),
        typical_promo_depth_range=(0.12, 0.25),
        typical_velocity_13_26_trend_benchmark=0.00,
        price_tier_notes="Impulse-driven. Seasonal spikes significant."
    ),
    
    # ───────────────────────────────────────────────────────────────────────────
    # DAIRY & ALTERNATIVES
    # TODO: Source - Industry report Q1 2026
    # ───────────────────────────────────────────────────────────────────────────
    "yogurt": CategoryBenchmark(
        typical_promo_frequency_range=(0.35, 0.55),  # TODO: Verify with Circana
        typical_promo_depth_range=(0.15, 0.28),      # TODO: Verify with Circana
        typical_velocity_13_26_trend_benchmark=-0.02,  # TODO: Update quarterly
        price_tier_notes="Greek dominates. Plant-based growing but niche."
    ),
    "milk_alternatives": CategoryBenchmark(
        typical_promo_frequency_range=(0.20, 0.40),  # TODO: Verify with Nielsen
        typical_promo_depth_range=(0.10, 0.20),      # TODO: Verify with Nielsen
        typical_velocity_13_26_trend_benchmark=0.03,   # TODO: Update quarterly
        price_tier_notes="Oat milk leading. Almond mature. Emerging: potato, hemp."
    ),
    
    # ───────────────────────────────────────────────────────────────────────────
    # DEFAULT FALLBACK
    # ───────────────────────────────────────────────────────────────────────────
    "default": CategoryBenchmark(
        typical_promo_frequency_range=(0.25, 0.45),
        typical_promo_depth_range=(0.12, 0.25),
        typical_velocity_13_26_trend_benchmark=0.00,
        price_tier_notes="Category-specific data not available."
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# EXTERNAL SUPPORT SNIPPETS
# ═══════════════════════════════════════════════════════════════════════════════
# Category-level behavioral truths for Investor Memo "External Support" section.
# Max 12 words each. Must be TIMELESS STRUCTURAL OBSERVATIONS.
#
# RULES (see hard_coded_rules.md):
# ✅ Format/category behavior observations (no brand names)
# ✅ Structural truths about consumption patterns
# ❌ Brand-specific claims (e.g., "Serendipity outperforming...")
# ❌ Time-bound claims (e.g., "Q4 2025 showed...")
# ❌ Retailer-specific claims (e.g., "Kroger seeing...")
# ❌ Competitor comparisons
#
# TODO: Review annually for continued accuracy.
# TODO: Add source citations where available.

_RETAILER_BELIEF_SUPPORT = {
    "ice_cream": [
        # TODO: Verify these remain accurate structural observations
        "Pint category flat; novelties outpacing traditional formats.",
        "Portion control driving premium ice cream growth.",
        "Legacy brands retain shelf but lose share to innovation.",
        "Price-per-ounce scrutiny increasing across frozen desserts.",
        "Handheld frozen snacks showing strongest velocity gains.",
    ],
    "ice_cream_pints": [
        # TODO: Verify these remain accurate structural observations
        "Pint velocity declining vs portioned alternatives.",
        "Premium pint segment requires brand story to sustain.",
        "Celebrity brands struggling with repeat after trial.",
        "Legacy pint brands maintain habitual buyer base.",
        "Self-managed stopping formats face cognitive headwinds.",
    ],
    "ice_cream_novelties": [
        # TODO: Verify these remain accurate structural observations
        "Novelties growing faster than total frozen dessert.",
        "Single-serve formats reduce decision friction.",
        "Mochi and bites leading innovation pipeline.",
        "Impulse positioning outperforms destination trips.",
        "Portion-bound formats showing superior repeat rates.",
    ],
    "frozen_snacks": [
        "Handheld frozen growing at 2x category average.",
        "Convenience formats winning on-the-go occasions.",
        "Portion control reduces guilt-driven purchase friction.",
    ],
    "carbonated_soft_drinks": [
        "CSD flat; growth in mini-can and zero-sugar variants.",
        "Ritual preservation drives Coca-Cola repeat dominance.",
        "Private label gaining in value-conscious segments.",
        "Functional soda disrupting traditional cola occasions.",
    ],
    "functional_beverages": [
        "Functional claims justify premium pricing.",
        "Gut health and energy leading benefit platforms.",
        "Younger cohorts over-index on functional beverages.",
        "Probiotic drinks showing strong repeat metrics.",
    ],
    "energy_drinks": [
        "Energy drinks showing ritual-like consumption patterns.",
        "Brand loyalty highest among all beverage segments.",
        "Monster and Red Bull dominate despite premium pricing.",
        "Emerging brands face high cognitive entry barriers.",
    ],
    "salty_snacks": [
        "Salty snacks stable; innovation in better-for-you.",
        "Portion packs growing faster than share bags.",
        "Private label pressure on mainstream salty snacks.",
    ],
    "bars_snacks": [
        "Bars category mature but protein segment growing.",
        "Portion-bound format supports repeat behavior.",
        "Functional claims drive premium acceptance.",
    ],
    "default": [
        "Category data being compiled.",
        "Structural analysis based on format characteristics.",
        "Consult category manager for specific insights.",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_hard_data() -> HardDataInputs:
    """
    Returns a fully populated HardDataInputs object with safe placeholder defaults.
    
    Usage:
        data = get_hard_data()
        cohort = data.cohort_elasticity["younger"]
        benchmark = data.category_benchmarks["ice_cream"]
    """
    return HardDataInputs(
        cohort_elasticity=_COHORT_ELASTICITY.copy(),
        category_benchmarks=_CATEGORY_BENCHMARKS.copy(),
        retailer_belief_support=_RETAILER_BELIEF_SUPPORT.copy(),
    )


def get_category_benchmark(category: str) -> dict:
    """
    Get benchmark data for a specific category.
    Falls back to "default" if category not found.
    
    Args:
        category: Category key (e.g., "ice_cream", "energy_drinks")
    
    Returns:
        Dict with benchmark fields:
        - typical_promo_frequency_range: tuple
        - typical_promo_depth_range: tuple
        - typical_velocity_13_26_trend_benchmark: float
        - price_tier_notes: str
    """
    # Normalize category key
    cat_key = category.lower().replace(" ", "_").replace("-", "_")
    
    # Try exact match first
    if cat_key in _CATEGORY_BENCHMARKS:
        benchmark = _CATEGORY_BENCHMARKS[cat_key]
    else:
        # Try partial matching
        for key in _CATEGORY_BENCHMARKS:
            if cat_key in key or key in cat_key:
                benchmark = _CATEGORY_BENCHMARKS[key]
                break
        else:
            benchmark = _CATEGORY_BENCHMARKS["default"]
    
    return {
        "typical_promo_frequency_range": benchmark.typical_promo_frequency_range,
        "typical_promo_depth_range": benchmark.typical_promo_depth_range,
        "typical_velocity_13_26_trend_benchmark": benchmark.typical_velocity_13_26_trend_benchmark,
        "price_tier_notes": benchmark.price_tier_notes,
    }


def get_external_support_snippets(category: str) -> List[str]:
    """
    Get external support snippets for a specific category.
    Falls back to "default" if category not found.
    
    Args:
        category: Category key (e.g., "ice_cream", "functional_beverages")
    
    Returns:
        List of short bullet strings (max 12 words each)
    """
    # Normalize category key
    cat_key = category.lower().replace(" ", "_").replace("-", "_")
    
    # Try exact match first
    if cat_key in _RETAILER_BELIEF_SUPPORT:
        return _RETAILER_BELIEF_SUPPORT[cat_key].copy()
    
    # Try partial matching
    for key in _RETAILER_BELIEF_SUPPORT:
        if cat_key in key or key in cat_key:
            return _RETAILER_BELIEF_SUPPORT[key].copy()
    
    return _RETAILER_BELIEF_SUPPORT["default"].copy()


def get_cohort_elasticity(cohort: str) -> dict:
    """
    Get elasticity coefficients for a specific cohort.
    Falls back to "mixed" if cohort not found.
    
    Args:
        cohort: Cohort key ("younger", "mixed", "older")
    
    Returns:
        Dict with elasticity fields
    """
    cohort_key = cohort.lower().strip()
    
    if cohort_key in _COHORT_ELASTICITY:
        e = _COHORT_ELASTICITY[cohort_key]
    else:
        e = _COHORT_ELASTICITY["mixed"]
    
    return {
        "f_sensitivity": e.f_sensitivity,
        "c_sensitivity": e.c_sensitivity,
        "promo_response": e.promo_response,
        "trend_weight": e.trend_weight,
        "notes": e.notes,
    }


def list_categories() -> List[str]:
    """Returns list of all available category keys."""
    return [k for k in _CATEGORY_BENCHMARKS.keys() if k != "default"]


def list_cohorts() -> List[str]:
    """Returns list of all available cohort keys."""
    return list(_COHORT_ELASTICITY.keys())
