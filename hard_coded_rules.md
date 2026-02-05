# Hard-Coded Rules: What Goes Where

This document defines the data governance for the Elbow Interference Theory™ scoring system.

---

## ✅ HARD-CODED (in `hard_data.py`)

These values are **deterministic constants** that do not change based on brand, analyst input, or AI inference. They represent structural truths about categories and cohorts.

### 1. Category Benchmark Ranges

Promo frequency and promo depth benchmarks by category. Used for **guardrails only** (flagging outliers), not for scoring.

| Category | Promo Frequency Range | Promo Depth Range | Source |
|----------|----------------------|-------------------|--------|
| ice_cream | 30-55% | 15-30% | TODO: Industry report |
| ice_cream_pints | 35-55% | 18-28% | TODO: Industry report |
| ice_cream_novelties | 25-45% | 12-22% | TODO: Industry report |
| functional_beverages | 15-35% | 8-18% | TODO: Industry report |
| energy_drinks | 20-40% | 10-22% | TODO: Industry report |
| carbonated_soft_drinks | 40-60% | 20-35% | TODO: Industry report |
| salty_snacks | 40-60% | 18-32% | TODO: Industry report |
| bars_snacks | 25-45% | 12-25% | TODO: Industry report |

**Rule**: If analyst-entered promo values fall outside these ranges, log a flag. Do not auto-correct.

---

### 2. Cohort Sensitivity Multipliers

These adjust how much Familiarity (F) and Cognitive Interference (C) matter by demographic cohort.

| Cohort | F Sensitivity | C Sensitivity | Promo Response | Notes |
|--------|--------------|---------------|----------------|-------|
| younger | 0.7 | 1.3 | 1.2 | Less brand-loyal, more price-sensitive |
| mixed | 1.0 | 1.0 | 1.0 | Baseline |
| older | 1.4 | 0.8 | 0.7 | Habitual, brand-loyal |

**Rule**: These multipliers inform priors adjustments. They do not directly change raw scores.

---

### 3. Category-Level Behavioral Truths

Short bullets (max 12 words) that appear in the Investor Memo as "External Support." These are **structural observations** about categories, not brand-specific claims.

**Format**: Timeless truths about format/category behavior. No brand names. No time-bound claims.

Examples:
- ✅ "Pint velocity declining vs portioned alternatives."
- ✅ "Portion-bound formats reduce decision friction."
- ✅ "Celebrity brands face cognitive entry barriers."
- ❌ "Serendipity outperforming Dr. Bombay" (brand-specific)
- ❌ "Q4 2025 showed 15% decline" (time-bound)
- ❌ "Kroger seeing strong novelty sales" (retailer-specific)

---

## ✏️ ANALYST-ENTERED (via UI)

These values must be entered by the analyst for each analysis. They are **not inferred or auto-populated**.

| Field | Description | Where Entered |
|-------|-------------|---------------|
| Brand Name | The brand being analyzed | Main UI - Brand 1/2 inputs |
| Product Format | Physical format (pint, bar, can, etc.) | Main UI - Format dropdown |
| Promo Frequency | % weeks on deal (0-100%) | Sidebar - Advanced Settings |
| Promo Depth | Avg % off base price (0-100%) | Sidebar - Advanced Settings |
| Velocity 13-week | UPS/PW for recent period | Sidebar (if available) |
| Velocity 26-week | UPS/PW for baseline period | Sidebar (if available) |
| Occasion | Primary consumption occasion | Main UI - Occasion field |
| Override Justifications | Rationale for manual score changes | Inline with each metric |

**Rule**: If analyst does not enter promo data, assume 0 (no promo penalty applied).

---

## 🤖 AI-INFERRED (via Gemini)

These values are suggested by the AI based on brand/format context. Analyst can override.

| Field | Description | Override Allowed? |
|-------|-------------|-------------------|
| M (Mouthfeel) | Sensory experience score | Yes, with justification |
| E (Emotion) | Emotional satisfaction score | Yes, with justification |
| F (Familiarity) | Brand recognition/ritual score | Yes, with justification |
| B (Bites) | Decision count score | Yes, with justification |
| K (Kinetic) | Physical effort score | Yes, with justification |
| C (Cognitive) | Mental interference score | Yes, with justification |
| Investment Memo | Strategic synthesis narrative | No (regenerate if needed) |

**Rule**: AI suggestions are starting points. The Justification Gate requires rationale for any deviation from AI baseline.

---

## ❌ DO NOT HARD-CODE

The following should **never** be hard-coded:

| Item | Reason |
|------|--------|
| Brand-specific M/E/F/B/K/C values | Brands change; AI should infer from current context |
| Competitor comparison claims | Legal risk; depends on current performance |
| Retailer-specific performance | Changes by period; requires fresh data |
| Time-bound metrics | Stale data worse than no data |
| New launch assessments | Requires real-time market intelligence |
| Price points | Changes frequently |
| Distribution/ACV claims | Requires syndicated data feed |

---

## Data Flow Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                        HARD DATA                                │
│  (Category benchmarks, Cohort multipliers, Behavioral truths)   │
│                    ↓ guardrails only                            │
├─────────────────────────────────────────────────────────────────┤
│                      ANALYST INPUT                              │
│  (Brand, Format, Promo %, Velocity, Occasion, Justifications)   │
│                    ↓ primary inputs                             │
├─────────────────────────────────────────────────────────────────┤
│                      AI INFERENCE                               │
│  (M, E, F, B, K, C suggestions + Investment Memo synthesis)     │
│                    ↓ suggestions only                           │
├─────────────────────────────────────────────────────────────────┤
│                      PRIORS LAYER                               │
│  (Applies behavioral adjustments based on context)              │
│                    ↓ transparent log                            │
├─────────────────────────────────────────────────────────────────┤
│                      FINAL SCORE                                │
│  S = Satisfaction (Value Delivered ÷ Cost Extracted)            │
│  S = (M × E × F) ÷ (B × K × C)                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Maintenance Notes

- **Quarterly**: Review category benchmarks against latest industry reports
- **Annually**: Validate cohort sensitivity assumptions
- **Never**: Hard-code brand-specific claims without expiration dates

---

*Document version: 1.0 | Last updated: February 2026*
