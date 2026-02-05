"""
PRIORS MODULE - Elbow Interference Theory™
==========================================
Hard-coded behavioral defaults and adjustment rules for scoring.

This module implements Russell Barnett's behavioral priors that adjust
the raw M, E, F, B, K, C scores based on context, format, and market data.

Key Principles:
- Cognitive Interference (C) baseline is elevated by default
- Promo reliance increases effective C (purchased velocity vs structural)
- Familiarity (F) is protective under macro stress
- Self-managed formats (pints) incur stopping penalties
- Portion-bound formats reduce cognitive load

Author: Russell Barnett © 2026
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Union
from enum import Enum

# Optional import for hard_data integration
try:
    from hard_data import HardDataInputs, get_category_benchmark
    HARD_DATA_AVAILABLE = True
except ImportError:
    HARD_DATA_AVAILABLE = False
    HardDataInputs = None  # Type hint fallback


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class Cohort(Enum):
    YOUNGER = "younger"      # Gen Z, Millennials
    MIXED = "mixed"          # Broad demo
    OLDER = "older"          # Gen X, Boomers


class Occasion(Enum):
    LATE_NIGHT = "late_night"
    EVENING = "evening"
    DAYTIME = "daytime"
    ON_THE_GO = "on_the_go"


class ProductFormat(Enum):
    # Self-managed stopping (HIGH friction)
    PINT = "pint"
    TUB = "tub"
    BAG = "bag"
    BOX = "box"
    
    # Portion-bound (LOW friction)
    BAR = "bar"
    BITE = "bite"
    SINGLE = "single"
    NOVELTY = "novelty"
    CAN = "can"
    BOTTLE = "bottle"
    
    # Other
    SANDWICH = "sandwich"
    CHIPS = "chips"
    DRINK = "drink"
    OTHER = "other"


# Format categories for penalty/bonus logic
SELF_MANAGED_FORMATS = {ProductFormat.PINT, ProductFormat.TUB, ProductFormat.BAG, ProductFormat.BOX}
PORTION_BOUND_FORMATS = {ProductFormat.BAR, ProductFormat.BITE, ProductFormat.SINGLE, 
                         ProductFormat.NOVELTY, ProductFormat.CAN, ProductFormat.BOTTLE}


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScoringContext:
    """Context object threaded through the scoring pipeline."""
    cohort: str = "mixed"           # 'younger' | 'mixed' | 'older'
    occasion: str = "evening"       # 'late_night' | 'evening' | 'daytime' | 'on_the_go'
    macro_stress: bool = True       # Default TRUE - conservative assumption
    category: str = "ice_cream"     # e.g., 'ice_cream_pints', 'functional_soda', 'snacks'
    
    # Promo data (0..1 scale)
    promo_frequency: float = 0.0    # % weeks on deal
    promo_depth: float = 0.0        # avg % off base price
    
    # Velocity data for trend
    ups_pw_13: Optional[float] = None   # Units per store per week (13-week)
    ups_pw_26: Optional[float] = None   # Units per store per week (26-week)
    
    # Format
    format: str = "pint"            # Product format string
    
    # Feature flag
    use_priors: bool = True         # Allow disabling priors for sensitivity checks


@dataclass
class RawScores:
    """Raw M, E, F, B, K, C scores before prior adjustments."""
    M: float  # Mouthfeel (1-5)
    E: float  # Emotion (1-5)
    F: float  # Familiarity (1-5)
    B: float  # Bites (1-5)
    K: float  # Kinetic (1-5)
    C: float  # Cognitive (1-5)


@dataclass
class AdjustedScores:
    """Scores after prior adjustments with audit trail."""
    M: float
    E: float
    F: float
    B: float
    K: float
    C: float
    
    # Audit trail
    adjustments: List[str] = field(default_factory=list)
    repeat_momentum: Optional[int] = None  # 1-5 trend score
    promo_penalty: float = 0.0
    
    def get_adjustment_log(self) -> str:
        """Returns formatted adjustment log for report."""
        if not self.adjustments:
            return "No adjustments applied."
        return "\n".join(f"• {adj}" for adj in self.adjustments)


# ═══════════════════════════════════════════════════════════════════════════════
# PRIOR CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# 1. Cognitive Interference baseline elevation
C_MIN_DEFAULT = 2.5  # Elevated baseline unless justified lower

# 2. Velocity trend weighting
TREND_WEIGHT = 0.65   # Weight for trend (13→26 change)
LEVEL_WEIGHT = 0.35   # Weight for absolute level

# 3. Promo-to-friction coefficients
PROMO_FREQ_COEFF = 0.6
PROMO_DEPTH_COEFF = 0.4
PROMO_C_MULTIPLIER = 1.25

# 4. Macro stress F multiplier
MACRO_STRESS_F_MULTIPLIER = 1.15

# 5. Instructional messaging C increase for younger cohort
YOUNGER_MESSAGING_C_INCREASE = 0.30

# 6. Self-managed format penalties
SELF_MANAGED_C_PENALTY = 0.35
SELF_MANAGED_K_PENALTY = 0.20

# 7. Portion-bound format bonus
PORTION_BOUND_C_BONUS = -0.15  # Negative = reduction


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def clamp(value: float, min_val: float = 1.0, max_val: float = 5.0) -> float:
    """Clamp value to valid score range (default 1-5)."""
    return max(min_val, min(max_val, value))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division handling zero denominators."""
    if denominator == 0:
        return default
    return numerator / denominator


def get_format_enum(format_str: str) -> ProductFormat:
    """
    Convert format string to enum, defaulting to OTHER.

    IMPORTANT:
    - Do NOT let "multi-serve" collapse everything into PINT.
    - Detect specific formats first (bag/box/tub/pint), then portion-bound,
      then generic fallback.
    """
    format_lower = (format_str or "").lower().strip()

    # Specific multi-serve formats first (avoid misclassifying bags/boxes as pint)
    if "bag" in format_lower or "pouch" in format_lower:
        return ProductFormat.BAG
    if "box" in format_lower or "carton" in format_lower:
        return ProductFormat.BOX
    if "tub" in format_lower:
        return ProductFormat.TUB
    if "pint" in format_lower:
        return ProductFormat.PINT

    # Portion-bound formats
    if "bar" in format_lower:
        return ProductFormat.BAR
    if "bite" in format_lower:
        return ProductFormat.BITE
    if "single serve" in format_lower or "single-serve" in format_lower or "single" == format_lower:
        return ProductFormat.SINGLE
    if "novelty" in format_lower:
        return ProductFormat.NOVELTY
    if "can" in format_lower:
        return ProductFormat.CAN
    if "bottle" in format_lower:
        return ProductFormat.BOTTLE

    # Other
    if "sandwich" in format_lower:
        return ProductFormat.SANDWICH
    if "chips" in format_lower:
        return ProductFormat.CHIPS
    if "drink" in format_lower:
        return ProductFormat.DRINK

    # Generic fallback (only if nothing more specific is found)
    if "multi-serve" in format_lower:
        return ProductFormat.PINT

    return ProductFormat.OTHER


# ═══════════════════════════════════════════════════════════════════════════════
# REPEAT MOMENTUM CALCULATION
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_repeat_momentum(ups_pw_13: Optional[float], 
                               ups_pw_26: Optional[float]) -> Tuple[Optional[int], Optional[float]]:
    """
    Calculate RepeatMomentum score (1-5) from velocity trend.
    
    Returns:
        Tuple of (momentum_score, trend_pct)
    """
    if ups_pw_13 is None or ups_pw_26 is None:
        return None, None
    
    if ups_pw_26 <= 0:
        return 3, 0.0  # Neutral if no baseline
    
    trend_pct = (ups_pw_13 - ups_pw_26) / ups_pw_26
    
    # Piecewise mapping to 1-5 score
    if trend_pct <= -0.10:
        momentum = 1  # Strong decline
    elif trend_pct <= -0.03:
        momentum = 2  # Moderate decline
    elif trend_pct <= 0.03:
        momentum = 3  # Stable
    elif trend_pct <= 0.10:
        momentum = 4  # Moderate growth
    else:
        momentum = 5  # Strong growth
    
    return momentum, trend_pct


# ═══════════════════════════════════════════════════════════════════════════════
# PROMO PENALTY CALCULATION
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_promo_penalty(promo_frequency: float, promo_depth: float) -> float:
    """
    Calculate promo penalty (0-1 scale) from promo reliance metrics.
    
    Higher promo reliance = higher penalty = higher effective C.
    """
    # Validate inputs
    freq = clamp(promo_frequency, 0.0, 1.0)
    depth = clamp(promo_depth, 0.0, 1.0)
    
    # Weighted combination
    penalty = PROMO_FREQ_COEFF * freq + PROMO_DEPTH_COEFF * depth
    
    return clamp(penalty, 0.0, 1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PRIORS FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════

def apply_priors(raw: RawScores, context: ScoringContext) -> AdjustedScores:
    """
    Apply behavioral priors to raw scores based on context.
    
    Returns AdjustedScores with audit trail of all modifications.
    """
    adjustments: List[str] = []
    
    # Start with raw values
    M = raw.M
    E = raw.E
    F = raw.F
    B = raw.B
    K = raw.K
    C = raw.C
    
    # Feature flag check
    if not context.use_priors:
        adjustments.append("Priors disabled. Using raw inputs only.")
        return AdjustedScores(
            M=clamp(M), E=clamp(E), F=clamp(F),
            B=clamp(B), K=clamp(K), C=clamp(C),
            adjustments=adjustments
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # PRIOR 1: Cognitive Interference baseline elevation
    # ─────────────────────────────────────────────────────────────────────────
    if C < C_MIN_DEFAULT:
        old_C = C
        C = C_MIN_DEFAULT
        adjustments.append(f"C elevated from {old_C:.2f} to {C:.2f} (baseline minimum)")
    
    # ─────────────────────────────────────────────────────────────────────────
    # PRIOR 3: Promo reliance increases effective C
    # ─────────────────────────────────────────────────────────────────────────
    promo_penalty = calculate_promo_penalty(context.promo_frequency, context.promo_depth)
    
    if promo_penalty > 0.01:  # Only apply if meaningful
        c_increase = min(0.9, PROMO_C_MULTIPLIER * promo_penalty)
        old_C = C
        C = clamp(C + c_increase)
        adjustments.append(
            f"Promo reliance (freq={context.promo_frequency:.0%}, depth={context.promo_depth:.0%}) "
            f"increased C by {c_increase:.2f} ({old_C:.2f} → {C:.2f})"
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # PRIOR 4: Familiarity protection under macro stress
    # ─────────────────────────────────────────────────────────────────────────
    if context.macro_stress:
        old_F = F
        F = clamp(F * MACRO_STRESS_F_MULTIPLIER)
        if F != old_F:
            adjustments.append(
                f"Macro stress active: F multiplied by {MACRO_STRESS_F_MULTIPLIER} "
                f"({old_F:.2f} → {F:.2f})"
            )
    
    # ─────────────────────────────────────────────────────────────────────────
    # PRIOR 5: Instructional messaging increases C for younger cohort
    # ─────────────────────────────────────────────────────────────────────────
    if context.cohort == "younger":
        # Check for values-heavy categories (functional, wellness, etc.)
        values_categories = ["functional", "wellness", "probiotic", "keto", "plant"]
        if any(cat in context.category.lower() for cat in values_categories):
            old_C = C
            C = clamp(C + YOUNGER_MESSAGING_C_INCREASE)
            adjustments.append(
                f"Younger cohort + values-messaging category: C increased by "
                f"{YOUNGER_MESSAGING_C_INCREASE:.2f} ({old_C:.2f} → {C:.2f})"
            )
    
    # ─────────────────────────────────────────────────────────────────────────
    # PRIOR 6: Format-based penalties/bonuses
    # ─────────────────────────────────────────────────────────────────────────
    format_enum = get_format_enum(context.format)
    
    if format_enum in SELF_MANAGED_FORMATS:
        # Self-managed stopping penalty
        old_C, old_K = C, K
        C = clamp(C + SELF_MANAGED_C_PENALTY)
        K = clamp(K + SELF_MANAGED_K_PENALTY)
        adjustments.append(
            f"Self-managed format ({context.format}): "
            f"C +{SELF_MANAGED_C_PENALTY:.2f} ({old_C:.2f} → {C:.2f}), "
            f"K +{SELF_MANAGED_K_PENALTY:.2f} ({old_K:.2f} → {K:.2f})"
        )
    
    elif format_enum in PORTION_BOUND_FORMATS:
        # Portion-bound bonus (reduces C)
        old_C = C
        C = clamp(C + PORTION_BOUND_C_BONUS)
        adjustments.append(
            f"Portion-bound format ({context.format}): "
            f"C {PORTION_BOUND_C_BONUS:.2f} ({old_C:.2f} → {C:.2f})"
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # PRIOR 2: Calculate Repeat Momentum from velocity trend
    # ─────────────────────────────────────────────────────────────────────────
    repeat_momentum, trend_pct = calculate_repeat_momentum(
        context.ups_pw_13, context.ups_pw_26
    )
    
    if repeat_momentum is not None:
        adjustments.append(
            f"Repeat Momentum: {repeat_momentum}/5 (trend: {trend_pct:+.1%})"
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # Record context for transparency
    # ─────────────────────────────────────────────────────────────────────────
    context_summary = (
        f"Context: cohort={context.cohort}, occasion={context.occasion}, "
        f"macroStress={context.macro_stress}, category={context.category}"
    )
    adjustments.insert(0, context_summary)
    
    return AdjustedScores(
        M=clamp(M),
        E=clamp(E),
        F=clamp(F),
        B=clamp(B),
        K=clamp(K),
        C=clamp(C),
        adjustments=adjustments,
        repeat_momentum=repeat_momentum,
        promo_penalty=promo_penalty
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def apply_priors_dict(
    raw_scores: Dict[str, float],
    context_dict: Dict,
    hard_data: Optional["HardDataInputs"] = None
) -> Tuple[Dict[str, float], List[str]]:
    """
    Dictionary-based interface for apply_priors.

    FIXES INCLUDED:
    - Uses passed hard_data for benchmarks when available (guardrails only).
    - Does not alter scoring math beyond priors already defined.
    """
    raw = RawScores(
        M=raw_scores.get("M", 3),
        E=raw_scores.get("E", 3),
        F=raw_scores.get("F", 3),
        B=raw_scores.get("B", 3),
        K=raw_scores.get("K", 3),
        C=raw_scores.get("C", 3),
    )

    context = ScoringContext(
        cohort=context_dict.get("cohort", "mixed"),
        occasion=context_dict.get("occasion", "evening"),
        macro_stress=context_dict.get("macro_stress", True),
        category=context_dict.get("category", "ice_cream"),
        promo_frequency=context_dict.get("promo_frequency", 0.0),
        promo_depth=context_dict.get("promo_depth", 0.0),
        ups_pw_13=context_dict.get("ups_pw_13"),
        ups_pw_26=context_dict.get("ups_pw_26"),
        format=context_dict.get("format", "pint"),
        use_priors=context_dict.get("use_priors", True),
    )

    adjusted = apply_priors(raw, context)

    # ─────────────────────────────────────────────────────────
    # HARD DATA VALIDATION (guardrails and flags only)
    # ─────────────────────────────────────────────────────────
    hard_data_flags: List[str] = []

    def _get_benchmark_from_passed_hard_data(hd_obj, category_key: str) -> Optional[Dict]:
        """
        Best-effort benchmark extraction from passed hard_data.
        Supports a few common shapes without forcing a schema.
        """
        if hd_obj is None:
            return None

        # Case 1: dict-like hard_data with benchmarks
        if isinstance(hd_obj, dict):
            # common patterns: hd_obj["benchmarks"][category], hd_obj["category_benchmarks"][category]
            for top_key in ("benchmarks", "category_benchmarks", "categories"):
                if top_key in hd_obj and isinstance(hd_obj[top_key], dict):
                    if category_key in hd_obj[top_key]:
                        return hd_obj[top_key][category_key]
            # or direct category mapping
            if category_key in hd_obj and isinstance(hd_obj[category_key], dict):
                return hd_obj[category_key]
            return None

        # Case 2: object-like hard_data with attributes
        for attr in ("benchmarks", "category_benchmarks", "categories"):
            if hasattr(hd_obj, attr):
                container = getattr(hd_obj, attr)
                if isinstance(container, dict) and category_key in container:
                    return container[category_key]

        # Case 3: method-based access
        for method_name in ("get_category_benchmark", "benchmark_for_category", "get_benchmark"):
            if hasattr(hd_obj, method_name):
                try:
                    fn = getattr(hd_obj, method_name)
                    out = fn(category_key)
                    if isinstance(out, dict):
                        return out
                except Exception:
                    pass

        return None

    category = context_dict.get("category", "ice_cream")

    # We only validate if hard_data was actually passed in.
    # If none passed, we fall back to module benchmark (if available).
    try:
        benchmark: Optional[Dict] = None

        if hard_data is not None:
            benchmark = _get_benchmark_from_passed_hard_data(hard_data, category)

        if benchmark is None and HARD_DATA_AVAILABLE:
            # fallback to module-level benchmark if caller didn't pass hard_data,
            # or passed a structure we couldn't parse
            benchmark = get_category_benchmark(category)

        if isinstance(benchmark, dict) and benchmark:
            # Validate promo_frequency against benchmark
            promo_freq = context_dict.get("promo_frequency", 0.0)
            freq_min, freq_max = benchmark.get("typical_promo_frequency_range", (0.0, 1.0))

            if promo_freq > 0 and (promo_freq < freq_min or promo_freq > freq_max):
                if promo_freq < freq_min:
                    hard_data_flags.append(
                        f"Hard data flag: promo_frequency ({promo_freq:.0%}) below benchmark "
                        f"({freq_min:.0%}-{freq_max:.0%}) for {category}"
                    )
                else:
                    hard_data_flags.append(
                        f"Hard data flag: promo_frequency ({promo_freq:.0%}) above benchmark "
                        f"({freq_min:.0%}-{freq_max:.0%}) for {category}"
                    )

            # Validate promo_depth against benchmark
            promo_depth = context_dict.get("promo_depth", 0.0)
            depth_min, depth_max = benchmark.get("typical_promo_depth_range", (0.0, 1.0))

            if promo_depth > 0 and (promo_depth < depth_min or promo_depth > depth_max):
                if promo_depth < depth_min:
                    hard_data_flags.append(
                        f"Hard data flag: promo_depth ({promo_depth:.0%}) below benchmark "
                        f"({depth_min:.0%}-{depth_max:.0%}) for {category}"
                    )
                else:
                    hard_data_flags.append(
                        f"Hard data flag: promo_depth ({promo_depth:.0%}) above benchmark "
                        f"({depth_min:.0%}-{depth_max:.0%}) for {category}"
                    )

            # Validate velocity trend against benchmark (if available)
            ups_13 = context_dict.get("ups_pw_13")
            ups_26 = context_dict.get("ups_pw_26")

            if ups_13 is not None and ups_26 is not None and ups_26 > 0:
                trend = (ups_13 - ups_26) / ups_26
                benchmark_trend = benchmark.get("typical_velocity_13_26_trend_benchmark", 0.0)

                # Flag if trend significantly deviates from benchmark (>10 percentage points)
                trend_deviation = abs(trend - benchmark_trend)
                if trend_deviation > 0.10:
                    direction = "above" if trend > benchmark_trend else "below"
                    hard_data_flags.append(
                        f"Hard data flag: velocity trend ({trend:+.1%}) significantly {direction} "
                        f"category benchmark ({benchmark_trend:+.1%})"
                    )

            if hard_data_flags:
                hard_data_flags.insert(0, f"Hard data validation applied for category: {category}")

    except Exception as e:
        hard_data_flags.append(f"Hard data warning: Could not validate against benchmarks ({e})")

    # Combine adjusted score adjustments with hard data flags
    all_adjustments = adjusted.adjustments + hard_data_flags

    adjusted_dict = {
        "M": adjusted.M,
        "E": adjusted.E,
        "F": adjusted.F,
        "B": adjusted.B,
        "K": adjusted.K,
        "C": adjusted.C,
    }

    return adjusted_dict, all_adjustments


def get_default_context() -> ScoringContext:
    """Returns default context with conservative assumptions."""
    return ScoringContext(
        cohort="mixed",
        occasion="evening",
        macro_stress=True,
        category="ice_cream",
        promo_frequency=0.0,
        promo_depth=0.0,
        format="pint",
        use_priors=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT GENERATION HELPER
# ═══════════════════════════════════════════════════════════════════════════════

def generate_assumptions_section(adjusted: AdjustedScores, 
                                  context: ScoringContext) -> str:
    """
    Generate the 'Assumptions & Adjustments' section for the report.
    
    Output reads like an operator wrote it - short sentences, no marketing.
    """
    lines = [
        "═══════════════════════════════════════════",
        "ASSUMPTIONS & ADJUSTMENTS",
        "═══════════════════════════════════════════",
        "",
    ]
    
    if not context.use_priors:
        lines.append("Priors disabled. Raw scores used without adjustment.")
        lines.append("")
        return "\n".join(lines)
    
    # Context summary
    lines.append(f"Cohort: {context.cohort}")
    lines.append(f"Occasion: {context.occasion}")
    lines.append(f"Macro Stress: {'Active' if context.macro_stress else 'Inactive'}")
    lines.append(f"Category: {context.category}")
    lines.append(f"Format: {context.format}")
    lines.append("")
    
    # Adjustments applied
    lines.append("Adjustments Applied:")
    for adj in adjusted.adjustments[1:]:  # Skip context summary (first item)
        lines.append(f"  {adj}")
    
    if len(adjusted.adjustments) <= 1:
        lines.append("  None")
    
    lines.append("")
    
    # Final scores
    lines.append("Final Adjusted Scores:")
    lines.append(f"  M={adjusted.M:.2f}  E={adjusted.E:.2f}  F={adjusted.F:.2f}")
    lines.append(f"  B={adjusted.B:.2f}  K={adjusted.K:.2f}  C={adjusted.C:.2f}")
    
    if adjusted.repeat_momentum:
        lines.append(f"  Repeat Momentum: {adjusted.repeat_momentum}/5")
    
    lines.append("")
    
    return "\n".join(lines)
