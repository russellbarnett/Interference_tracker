"""
Elbow Interference Evaluator™ — Configuration and copy.
TOOLTIPS, White Paper context for AI, and default category.
CONFIDENTIAL: Russell Barnett © 2026.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TOOLTIPS (help text for Streamlit widgets)
# ═══════════════════════════════════════════════════════════════════════════════

TOOLTIPS = {
    "equation": "S = Satisfaction. Value Delivered ÷ Cost Extracted = Satisfaction. Satisfaction enables persistence over time, but persistence is not the equation itself.",
    "brand_name": "Enter the brand as a consumer recognizes it (typos are fine).",
    "format": "Format sets baseline friction. Portion-bound ends the occasion. Self-managed requires stopping decisions.",
    "occasion_free_text": "Optional. Adds context to the memo. Does not change math unless you use Priors.",

    "M": "Mouthfeel: texture and physical experience while consuming.",
    "E": "Emotion: the payoff during consumption (comfort, indulgence, relief).",
    "F": "Familiarity: how established the brand is in real life (habit, ritual, legacy).",
    "B": "Bites: how many stop/continue decisions happen before the occasion ends.",
    "K": "Kinetic: physical effort to keep consuming (prep, tools, cleanup, handling).",
    "C": "Cognitive: how much thinking, evaluation, or self-control the product triggers.",

    "override_rationale": "If you override a score, explain why. Keeps assumptions explicit and audit-able.",

    "priors_toggle": "Applies behavioral priors (context adjustments). Turn off for sensitivity checks.",
    "cohort": "Who is the buyer? Younger cohorts often carry higher messaging friction in values-heavy categories.",
    "priors_occasion": "Primary usage context. Occasion changes how friction and familiarity land.",
    "macro_stress": "When stress is active, Familiarity gets more weight (people default to known choices).",
    "promo_frequency": "Share of weeks on deal. High reliance implies velocity is being purchased.",
    "promo_depth": "Average discount depth. Deeper discount implies more purchased velocity risk.",
    "ups_13": "Units per store per week (last 13 weeks). Used for Repeat Momentum signal.",
    "ups_26": "Units per store per week (last 26 weeks). Used for Repeat Momentum signal.",

    "upload": "Upload CSV/Excel/PDF/Word/PPT/Text. Used for reference, context, and (optionally) priors inputs.",
}


def tip(key: str) -> str:
    """Return tooltip text for a widget key."""
    return TOOLTIPS.get(key, "")


# Default category when none selected (e.g. for priors/benchmarks).
DEFAULT_CATEGORY = "ice_cream"


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYST PERSONA (for all data analysis and research outputs)
# ═══════════════════════════════════════════════════════════════════════════════

ANALYST_PERSONA = """
You are a world-class analyst and a world-class market research expert and strategist.
- Treat all data with the rigor and insight of top-tier institutional research.
- Draw clear, evidence-based conclusions; call out uncertainty where it exists.
- Frame findings in terms of strategy, implications, and actionable recommendations.
- Use precise language and avoid vague or generic statements.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# WHITE PAPER CONTEXT (for Gemini prompts)
# ═══════════════════════════════════════════════════════════════════════════════

WHITE_PAPER_CONTEXT = """
THE ELBOW INTERFERENCE THEORY™ - FULL WHITE PAPER BY RUSSELL BARNETT

CORE CONCEPT:
Most products fail not because they lack quality, but because they ask too much of the consumer at the wrong moment.
Consumption begins in the elbow - the body acting without deliberation. Reaching, opening, tasting. The head is not involved.
But at some point, the head arrives. The consumer becomes aware they are consuming. They evaluate. They decide whether to continue.
The transition from elbow to head is the interference point. The longer the elbow runs uninterrupted, the more consumption compounds quietly.

KEY INSIGHT: Products do not compete on taste alone. They compete on how long they delay the head.

THE SATISFACTION EQUATION:
S = (M × E × F) ÷ (B × K × C)

VALUE DELIVERED (Numerator):
- M (Mouthfeel): How the product feels in the mouth during consumption
- E (Emotion): The feeling the product creates while being consumed  
- F (Familiarity): How recognizable and comfortable the experience is

COST EXTRACTED (Denominator):
- B (Bites): How many decisions the consumer makes before the occasion ends
- K (Kinetic Effort): The physical work required to continue consuming
- C (Cognitive Interference): How much the product asks the consumer to think

INTERPRETATION: S = Satisfaction. The option with higher S (Satisfaction) repeats more easily. The gap between scores tells you how large the behavioral advantage is.

CRITICAL INSIGHT ON FRICTION:
Friction compounds. Pleasure does not. A product rarely fails because of one flaw. It fails because multiple small frictions stack until the head interrupts the elbow.

CASE STUDY - MY/MOCHI (Structural Compounder):
- Handheld, portion-bound, no spoon, no stick, one motion from freezer to mouth
- Did NOT replace pints - served a different job (frozen snacking vs ice cream eating)
- Scores: M=4 (differentiated chew), E=4 (novel/surprising), F=3 (moderate initially)
- Denominator: B=1 (portion-bound), K=1 (single motion), C=1 (occasion ends automatically)
- S-Score: 16.0 - DENOMINATOR COLLAPSE achieved
- Key: "My/Mochi delays the head by ending the event"

CASE STUDY - PINT ICE CREAM (High Interference):
- Multiple bites, self-managed stopping, spoon/bowl ritual
- Scores: M=5 (category benchmark), E=5 (high indulgence), F=5 (very familiar)
- Denominator: B=4-5 (many decision points), K=3 (spoon/thaw/cleanup), C=3-4 (guilt, stopping decisions)
- S-Score: ~1.6-2.2
- Key: "The head arrives when stopping becomes self-managed"

THE CRITICAL DISTINCTION - FAMILIARITY (F):
- Legacy brands with decades of presence = F=5 (e.g., Serendipity has NYC ritual since 1954)
- New entrants/startups = F=2-3 (consumers must learn the product)
- Celebrity launches = F=3 (novelty, not ritual - the celebrity is familiar but the PRODUCT is not)

THE CRITICAL DISTINCTION - COGNITIVE INTERFERENCE (C):
- Legacy brands you buy on autopilot = C=1-2
- Premium pricing requiring justification = C=3-4  
- Celebrity brands = C=4-5 because "celebrity branding invites the Head Zone to audit the purchase"
- The Snoop Dogg hook is CONCEPTUAL (requires thinking). My/Mochi's success was EMBODIED (resolved in the mouth)
- "Conceptual hooks are harder and more expensive to defend over time"

THE "YEAR 5 SWING" RISK:
For high-interference brands, once novelty fades, the Head Zone must manually "authorize" the purchase. This creates a "Behavioral Margin Call" where velocity must be purchased through sustained spend rather than quiet compounding.

PRESENCE VS PERSISTENCE:
- TAM (Total Addressable Market) measures PRESENCE - how many consumers might consider a product
- S-Score = Satisfaction. Higher Satisfaction supports persistence (whether they will return without being reminded)
- "A $10 billion TAM means nothing if the product invites the head in too early"

ENTERPRISE VALUE INSIGHT:
"Products do not create behavior. They align with it. Capital can extend momentum, but it cannot change structure. Enterprise value compounds where the elbow finishes before the head arrives."
"""
