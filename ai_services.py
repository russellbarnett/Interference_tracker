"""
Elbow Interference Evaluator™ — Gemini AI and memo generation.
Brand analysis, strategic synthesis, and rule-based memo.
CONFIDENTIAL: Russell Barnett © 2026.
"""

import json
from typing import Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    genai = None
    GEMINI_AVAILABLE = False

from config import WHITE_PAPER_CONTEXT, ANALYST_PERSONA
from brands import normalize_brand_name


def get_gemini_model():
    """Initialize Gemini model with API key from Streamlit secrets."""
    import streamlit as st
    if not GEMINI_AVAILABLE:
        print("[GEMINI] Library not available")
        return None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key or api_key == "YOUR_KEY_HERE":
            print("[GEMINI] No API key configured")
            return None
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("[GEMINI] ✓ Model initialized (gemini-2.0-flash)")
        return model
    except Exception as e:
        print(f"[GEMINI] ✗ Error: {e}")
        return None


def analyze_brand_with_ai(brand_name: str) -> Optional[dict]:
    """
    Use Gemini to analyze a brand using the complete Elbow Interference Theory™.
    Returns dict with archetype, description, and BRAND-SPECIFIC scores.
    """
    model = get_gemini_model()
    if not model or not brand_name:
        return None
    normalized_name = normalize_brand_name(brand_name)
    prompt = f"""{WHITE_PAPER_CONTEXT}

{ANALYST_PERSONA}

=== YOUR TASK ===

Analyze this CPG GROCERY brand using the Elbow Interference Theory: "{normalized_name}"

NOTE: The user entered "{brand_name}" - recognize common spelling variations:
- "dr bombay", "Dr. Bombay", "Dr Bombay" = Snoop Dogg's ice cream brand
- "mymochi", "My/Mochi", "my mochi" = the mochi ice cream brand
- Treat typos and variations as the intended brand

This applies to ANY orally consumed CPG grocery item - anything you eat or drink:
- Snacks (chips, crackers, cookies, bars, nuts, popcorn, jerky)
- Frozen (ice cream, novelties, pizza, meals, appetizers)
- Dairy (yogurt, cheese, milk, butter, cream)
- Beverages (soda, water, juice, coffee, tea, energy drinks, alcohol, kombucha)
- Confectionery (candy, chocolate, gum, mints)
- Bakery (bread, pastries, muffins, cakes)
- Deli/Prepared (sandwiches, salads, ready meals)
- Breakfast (cereal, oatmeal, pancake mix, syrup)
- Condiments (sauces, dressings, spreads)
- Baby food, supplements, protein powders - anything consumed orally

FOCUS ON F (Familiarity) and C (Cognitive) - these are BRAND-SPECIFIC:

F (Familiarity) - "How established is this brand in the consumer's mind?"

CRITICAL EXAMPLES FROM THE WHITE PAPER:
- **Serendipity** = F=5 (iconic NYC brand since 1954, decades of cultural presence, restaurant institution)
- **Dr. Bombay** = F=3 (launched 2023, celebrity-driven, consumers don't have RITUAL with it yet)
- **Häagen-Dazs** = F=5 (legacy premium brand, decades of presence)
- **My/Mochi** = F=3 (novel format, growing but not yet ritual)

General guidance:
- F=5: Iconic legacy brands - household names for DECADES (Coca-Cola, Oreo, Lay's, Serendipity, Ben & Jerry's)
- F=4: Well-known established brands (Kind, Chobani, Talenti)
- F=3: Growing/emerging brands OR celebrity launches (Poppi, Dr. Bombay, Feastables)
- F=2: New market entrants, niche brands
- F=1: Unknown/brand new launches

C (Cognitive) - "Does this brand make consumers THINK before buying?"

CRITICAL EXAMPLES FROM THE WHITE PAPER:
- **Serendipity** = C=3 (familiar legacy, some premium consideration but mostly autopilot)
- **Dr. Bombay** = C=5 (celebrity noise FORCES evaluation - "is this worth it because of Snoop?")
- **Coca-Cola** = C=1 (pure autopilot, decades of habit)
- **Häagen-Dazs** = C=3 (premium but familiar)

THE CELEBRITY TRAP: Celebrity brands get C=4-5 because:
> "Celebrity branding invites the Head Zone to audit the purchase"
> The consumer evaluates the CELEBRITY, not just the food

General guidance:
- C=1-2: Autopilot purchases - grab without thinking (Coke, Oreo, legacy brands)
- C=3: Some consideration - premium positioning (Häagen-Dazs, Serendipity)
- C=4-5: High cognitive load - CELEBRITY BRANDS, unfamiliar concepts (Dr. Bombay, Feastables)

CELEBRITY BRANDS ARE SPECIAL:
- Celebrity association INCREASES cognitive load (C=4-5) because consumers evaluate the celebrity, not just the food
- Celebrity does NOT increase familiarity (F) - the celebrity is familiar, but the PRODUCT is new
- Examples: Dr. Bombay (Snoop Dogg), Feastables (MrBeast), Prime (Logan Paul) = F=2-3, C=4-5

ALSO PROVIDE M AND E (but these matter less - focus on F and C):
- M (Mouthfeel): Quality of sensory experience (1-5)
- E (Emotion): Satisfaction/indulgence delivered (1-5)

For B and K, estimate based on typical format (user will override with their format selection):

UNITIZED formats (B=1, K=1) - The package ends the occasion:
- Single-serve packs, bars, sticks, individual portions
- Single cans/bottles of beverages
- Individually wrapped items
- Single-serve cups, pouches, squeeze tubes

BULK formats (B=4, K=3) - Consumer decides when to stop:
- Bags, pouches (chips, crackers, cookies, candy)
- Tubs, pints, containers (ice cream, yogurt, dips)
- Boxes, cartons (cereal, crackers, snack mixes)
- Multi-use jars/bottles (peanut butter, sauces, condiments)
- Anything where you reach in multiple times

Return ONLY valid JSON:
{{"archetype": "unitized|bulk|ritual", "description": "brief description", "M": 4, "E": 4, "F": 3, "B": 4, "K": 3, "C": 4, "reasoning": "Explain your F and C scores - what makes this brand familiar or unfamiliar? What creates cognitive load?"}}

If you cannot identify the brand, return: {{"error": "unknown"}}"""
    try:
        print(f"\n{'='*60}")
        print(f"🔍 ANALYZING BRAND: {brand_name} (normalized: {normalized_name})")
        print(f"{'='*60}")
        response = model.generate_content(prompt)
        text = response.text.strip()
        print(f"\n📥 RAW AI RESPONSE:")
        print(text)
        print(f"\n{'='*60}")
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        result = json.loads(text.strip())
        print(f"\n✅ PARSED SCORES FOR {brand_name}:")
        print(f"   M (Mouthfeel)  = {result.get('M')}")
        print(f"   E (Emotion)    = {result.get('E')}")
        print(f"   F (Familiarity)= {result.get('F')} ⭐")
        print(f"   B (Bites)      = {result.get('B')}")
        print(f"   K (Kinetic)    = {result.get('K')}")
        print(f"   C (Cognitive)  = {result.get('C')} ⭐")
        print(f"   Reasoning: {result.get('reasoning', 'none')[:100]}...")
        print(f"{'='*60}\n")
        return result
    except Exception as e:
        print(f"\n❌ AI ANALYSIS ERROR for {brand_name}: {e}")
        print(f"{'='*60}\n")
        return None


def generate_strategic_synthesis(
    brand1_name: str, brand2_name: str,
    s1: float, s2: float,
    scores1: dict, scores2: dict,
    rationale1: str, rationale2: str,
    data_context: str = "",
) -> Optional[str]:
    """
    Use Gemini to generate an institutional-grade investment memo.
    data_context: optional summary of uploaded file for the memo.
    """
    print("[SYNTHESIS] Getting Gemini model...")
    model = get_gemini_model()
    if not model:
        print("[SYNTHESIS] ✗ Model is None!")
        return None
    print("[SYNTHESIS] ✓ Model acquired")
    num1 = scores1.get('M', 1) * scores1.get('E', 1) * scores1.get('F', 1)
    den1 = scores1.get('B', 1) * scores1.get('K', 1) * scores1.get('C', 1)
    num2 = scores2.get('M', 1) * scores2.get('E', 1) * scores2.get('F', 1)
    den2 = scores2.get('B', 1) * scores2.get('K', 1) * scores2.get('C', 1)
    winner = brand1_name if s1 > s2 else brand2_name
    loser = brand2_name if s1 > s2 else brand1_name
    winner_score = max(s1, s2)
    loser_score = min(s1, s2)
    winner_scores = scores1 if s1 > s2 else scores2
    loser_scores = scores2 if s1 > s2 else scores1
    ratio = winner_score / loser_score if loser_score > 0 else float('inf')
    b1_warnings = []
    if scores1.get('B', 1) >= 4:
        b1_warnings.append(f"B={scores1.get('B')} (high decision count)")
    if scores1.get('K', 1) >= 4:
        b1_warnings.append(f"K={scores1.get('K')} (high effort)")
    if scores1.get('C', 1) >= 4:
        b1_warnings.append(f"C={scores1.get('C')} (head arrives early)")
    b2_warnings = []
    if scores2.get('B', 1) >= 4:
        b2_warnings.append(f"B={scores2.get('B')} (high decision count)")
    if scores2.get('K', 1) >= 4:
        b2_warnings.append(f"K={scores2.get('K')} (high effort)")
    if scores2.get('C', 1) >= 4:
        b2_warnings.append(f"C={scores2.get('C')} (head arrives early)")
    prompt = f"""{WHITE_PAPER_CONTEXT}

{ANALYST_PERSONA}

=== YOUR TASK ===

Generate a COMPREHENSIVE ELBOW INTERFERENCE ANALYSIS for Matt Leeds at Forward Consumer Partners.

Write as a world-class analyst and market research strategist: institutional-grade analysis that breaks down EACH brand individually, with clear strategic implications and evidence-based conclusions.

=== BRAND DATA ===

**{brand1_name}**
- S-Score™: {s1:.2f}
- M={scores1.get('M', 0)}, E={scores1.get('E', 0)}, F={scores1.get('F', 0)} (Numerator: {num1})
- B={scores1.get('B', 0)}, K={scores1.get('K', 0)}, C={scores1.get('C', 0)} (Denominator: {den1})
- Format/Archetype: {scores1.get('archetype', 'unknown')}
{f"- ⚠️ Critical Weaknesses: {', '.join(b1_warnings)}" if b1_warnings else "- ✅ No critical denominator weaknesses"}
{f"- Analyst Note: {rationale1}" if rationale1 else ""}

**{brand2_name}**
- S-Score™: {s2:.2f}
- M={scores2.get('M', 0)}, E={scores2.get('E', 0)}, F={scores2.get('F', 0)} (Numerator: {num2})
- B={scores2.get('B', 0)}, K={scores2.get('K', 0)}, C={scores2.get('C', 0)} (Denominator: {den2})
- Format/Archetype: {scores2.get('archetype', 'unknown')}
{f"- ⚠️ Critical Weaknesses: {', '.join(b2_warnings)}" if b2_warnings else "- ✅ No critical denominator weaknesses"}
{f"- Analyst Note: {rationale2}" if rationale2 else ""}

**Structural Winner: {winner}** with {ratio:.2f}x behavioral advantage
{f'''

=== UPLOADED CONTEXT: SALES DATA AND/OR BRAND/CONSUMER DOCUMENTS ===
The following data/documents have been uploaded. You MUST take this into context when writing the final report. As a world-class analyst, use this material rigorously.
- Cite specific figures, trends, or quotes from the sales data or document where they support your analysis.
- Weave in brand or consumer insights from the document where relevant.
- If the upload is sales/tabular data, reference column names and sample values where they inform the narrative.

{data_context}
''' if data_context else ""}

=== OUTPUT FORMAT (FOLLOW THIS EXACTLY) ===

---

# ELBOW INTERFERENCE ANALYSIS: {brand1_name} vs {brand2_name}

## Product Structure Overview

Create a brief table comparing the two brands:
| Dimension | {brand1_name} | {brand2_name} |
|-----------|--------------|---------------|
| Format | ? | ? |
| Category | ? | ? |
| Consumption | ? | ? |

---

## {brand1_name}: DETAILED ANALYSIS

### Value Delivered (Numerator)

**M (Mouthfeel): {scores1.get('M', 0)}/5**
- Explain what this score means for THIS specific brand
- Is it category-defining or merely acceptable?

**E (Emotion): {scores1.get('E', 0)}/5**
- What emotional payoff does this brand provide?
- Is it immediate pleasure or delayed gratification?

**F (Familiarity): {scores1.get('F', 0)}/5** {"⭐" if scores1.get('F', 0) >= 4 else "⚠️" if scores1.get('F', 0) <= 2 else ""}
- Is this anchored to existing ritual or requiring new behavior?
- Legacy vs new entrant assessment

### Cost Extracted (Denominator)

**B (Bites/Decisions): {scores1.get('B', 0)}/5** {"⚠️ HIGH FRICTION" if scores1.get('B', 0) >= 4 else ""}
- How many decisions before occasion ends?
- Does occasion end automatically or require self-management?

**K (Kinetic Effort): {scores1.get('K', 0)}/5** {"⚠️ HIGH FRICTION" if scores1.get('K', 0) >= 4 else ""}
- Physical effort to continue consuming
- Format-driven assessment

**C (Cognitive Interference): {scores1.get('C', 0)}/5** {"⚠️ CRITICAL WEAKNESS" if scores1.get('C', 0) >= 4 else ""}
- When does the head arrive?
- Celebrity noise? Premium justification? Conceptual hooks?

---

## {brand2_name}: DETAILED ANALYSIS

(Same structure as above for the second brand)

---

## The Core Problem: Head vs Elbow

Using the White Paper framework, identify the critical structural difference between these brands. Quote the relevant passage:

> "Consumption begins in the elbow. The elbow is the body acting without deliberation..."

For the LOWER scoring brand ({loser}), explain:
- Does it pass the "automatic consumption" test?
- At what point does the head arrive?
- Is the brand hook Conceptual (requires thinking) or Embodied (resolved in the body)?

---

## Comparative Scorecard

| Dimension | {brand1_name} | {brand2_name} | Advantage |
|-----------|--------------|---------------|-----------|
| Ritual Preservation | Yes/No | Yes/No | ? |
| Elbow Entry | How? | How? | ? |
| Cognitive Load | Low/Med/High | Low/Med/High | ? |
| Head Arrival | When? | When? | ? |
| Repeat Mechanism | How? | How? | ? |

Key Quote: *"Products do not compete on taste alone. They compete on how long they delay the head."*

---

## Why This Matters for Enterprise Value

The White Paper states: *"TAM is the size of the door. Elbow Interference tells you whether consumers walk through it once or every week."*

For {loser} (S-Score: {loser_score:.2f}):
- High interference = velocity must be purchased, not compounded
- Repeat depends on ______, not automatic behavior
- Marketing must continuously reactivate
- Churn risk assessment

For {winner} (S-Score: {winner_score:.2f}):
- Lower interference = repeat compounds naturally
- Behavioral advantage creates moat

Compare to benchmark acquisitions (Poppi at $1.95B captured low-friction soda moment).

---

## Where {loser} Could Improve (Through EIT Lens)

Provide 3-5 specific, actionable recommendations using the framework:
1. How to lower B (decisions)?
2. How to lower K (effort)?
3. How to lower C (cognitive friction)?
4. How to increase F (familiarity)?
5. What format change would collapse the denominator?

---

## Final Assessment

Using the framework's language:

> "Repeat behavior is not created by marketing. It is allowed or blocked by product structure."

**{winner}**: [Structural Compounder / Low-Friction Asset]
- Why repeat is structurally enabled

**{loser}**: [High-Interference Asset / Growth Trap / Purchased Velocity]
- Why repeat requires continued investment

**Investment Verdict:**
- Clear recommendation for Matt Leeds
- S-Score ratio ({ratio:.2f}x) interpretation
- What would change the calculus?

---

Write in institutional investment tone as a world-class market research strategist. Be specific to these brands. Use actual scores throughout. Include White Paper quotes where impactful. Every claim should be grounded in the data and framework."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Memo generation error: {e}")
        return None


def generate_rule_based_memo(
    brand1: str, brand2: str, s1: float, s2: float,
    scores1: dict, scores2: dict,
) -> str:
    """Generate a comprehensive rule-based analysis memo without AI."""
    winner = brand1 if s1 > s2 else brand2
    loser = brand2 if s1 > s2 else brand1
    winner_score = max(s1, s2)
    loser_score = min(s1, s2)
    winner_scores = scores1 if s1 > s2 else scores2
    loser_scores = scores2 if s1 > s2 else scores1
    ratio = winner_score / loser_score if loser_score > 0 else float('inf')
    num1 = scores1['M'] * scores1['E'] * scores1['F']
    den1 = scores1['B'] * scores1['K'] * scores1['C']
    num2 = scores2['M'] * scores2['E'] * scores2['F']
    den2 = scores2['B'] * scores2['K'] * scores2['C']

    def get_warnings(scores, name):
        w = []
        if scores['B'] >= 4:
            w.append(f"B={scores['B']} ⚠️ HIGH (many decisions)")
        if scores['K'] >= 4:
            w.append(f"K={scores['K']} ⚠️ HIGH (effort required)")
        if scores['C'] >= 4:
            w.append(f"C={scores['C']} ⚠️ CRITICAL (head arrives early)")
        return w

    b1_warnings = get_warnings(scores1, brand1)
    b2_warnings = get_warnings(scores2, brand2)

    memo = f"""# ELBOW INTERFERENCE ANALYSIS: {brand1} vs {brand2}

---

## Executive Summary

**{winner}** holds a **{ratio:.1f}x structural advantage** over {loser} in behavioral persistence.

Using the Satisfaction Equation: **S = (M × E × F) ÷ (B × K × C)**

| Brand | S-Score™ | Numerator | Denominator |
|-------|----------|-----------|-------------|
| {brand1} | **{s1:.2f}** | {num1} | {den1} |
| {brand2} | **{s2:.2f}** | {num2} | {den2} |

---

## {brand1}: Detailed Analysis

### Value Delivered (Numerator = {num1})

**M (Mouthfeel): {scores1['M']}/5**
- Sensory experience during consumption
- {"Strong sensory delivery" if scores1['M'] >= 4 else "Moderate sensory experience" if scores1['M'] >= 3 else "Limited mouthfeel impact"}

**E (Emotion): {scores1['E']}/5**
- Emotional satisfaction during occasion
- {"High emotional payoff - immediate pleasure" if scores1['E'] >= 4 else "Moderate emotional connection" if scores1['E'] >= 3 else "Low emotional engagement"}

**F (Familiarity): {scores1['F']}/5** {"⭐ STRENGTH" if scores1['F'] >= 4 else "⚠️ RISK" if scores1['F'] <= 2 else ""}
- {"Anchored to established ritual - autopilot purchasing" if scores1['F'] >= 4 else "Some brand recognition" if scores1['F'] >= 3 else "Requires building new behavior - unfamiliar to consumers"}

### Cost Extracted (Denominator = {den1})

**B (Bites/Decisions): {scores1['B']}/5** {"⚠️ HIGH FRICTION" if scores1['B'] >= 4 else ""}
- {"Many decisions before occasion ends - requires self-management" if scores1['B'] >= 4 else "Moderate decision count" if scores1['B'] >= 2 else "Occasion ends automatically - minimal decisions"}

**K (Kinetic Effort): {scores1['K']}/5** {"⚠️ HIGH FRICTION" if scores1['K'] >= 4 else ""}
- {"Significant physical effort required" if scores1['K'] >= 4 else "Moderate effort" if scores1['K'] >= 2 else "Minimal effort - grab and consume"}

**C (Cognitive Interference): {scores1['C']}/5** {"⚠️ CRITICAL WEAKNESS" if scores1['C'] >= 4 else ""}
- {"Head arrives before elbow finishes - consumer must think/evaluate" if scores1['C'] >= 4 else "Some cognitive processing required" if scores1['C'] >= 3 else "Autopilot consumption - elbow runs uninterrupted"}

{f"**Denominator Warnings:** {', '.join(b1_warnings)}" if b1_warnings else "✅ **No critical denominator weaknesses**"}

---

## {brand2}: Detailed Analysis

### Value Delivered (Numerator = {num2})

**M (Mouthfeel): {scores2['M']}/5**
- Sensory experience during consumption
- {"Strong sensory delivery" if scores2['M'] >= 4 else "Moderate sensory experience" if scores2['M'] >= 3 else "Limited mouthfeel impact"}

**E (Emotion): {scores2['E']}/5**
- Emotional satisfaction during occasion
- {"High emotional payoff - immediate pleasure" if scores2['E'] >= 4 else "Moderate emotional connection" if scores2['E'] >= 3 else "Low emotional engagement"}

**F (Familiarity): {scores2['F']}/5** {"⭐ STRENGTH" if scores2['F'] >= 4 else "⚠️ RISK" if scores2['F'] <= 2 else ""}
- {"Anchored to established ritual - autopilot purchasing" if scores2['F'] >= 4 else "Some brand recognition" if scores2['F'] >= 3 else "Requires building new behavior - unfamiliar to consumers"}

### Cost Extracted (Denominator = {den2})

**B (Bites/Decisions): {scores2['B']}/5** {"⚠️ HIGH FRICTION" if scores2['B'] >= 4 else ""}
- {"Many decisions before occasion ends - requires self-management" if scores2['B'] >= 4 else "Moderate decision count" if scores2['B'] >= 2 else "Occasion ends automatically - minimal decisions"}

**K (Kinetic Effort): {scores2['K']}/5** {"⚠️ HIGH FRICTION" if scores2['K'] >= 4 else ""}
- {"Significant physical effort required" if scores2['K'] >= 4 else "Moderate effort" if scores2['K'] >= 2 else "Minimal effort - grab and consume"}

**C (Cognitive Interference): {scores2['C']}/5** {"⚠️ CRITICAL WEAKNESS" if scores2['C'] >= 4 else ""}
- {"Head arrives before elbow finishes - consumer must think/evaluate" if scores2['C'] >= 4 else "Some cognitive processing required" if scores2['C'] >= 3 else "Autopilot consumption - elbow runs uninterrupted"}

{f"**Denominator Warnings:** {', '.join(b2_warnings)}" if b2_warnings else "✅ **No critical denominator weaknesses**"}

---

## The Core Problem: Head vs Elbow

> *"Consumption begins in the elbow. The elbow is the body acting without deliberation. Reaching, opening, tasting. The head is not involved."*

"""
    if loser_scores['C'] >= 4:
        memo += f"""**{loser} invites the Head immediately.**

With C={loser_scores['C']}, the consumer must THINK before/during consumption. This creates:
- Continuous self-interrogation ("Is this worth it?")
- Decision fatigue on repeat purchase
- Vulnerability to competitive switching

The White Paper is clear: *"The moment the head arrives, the elbow slows."*
"""
    elif max(loser_scores['B'], loser_scores['K']) >= 4:
        memo += f"""**{loser} creates friction through effort.**

With B={loser_scores['B']} and K={loser_scores['K']}, the physical structure of consumption creates repeated decision points. Each decision is an opportunity for the head to arrive.
"""
    else:
        memo += """Both brands have manageable interference profiles. The difference lies primarily in the numerator (value delivered) rather than denominator (cost extracted).
"""
    memo += f"""

---

## Comparative Scorecard

| Dimension | {brand1} | {brand2} |
|-----------|----------|----------|
| Elbow Entry | {"Easy - minimal prep" if scores1['K'] <= 2 else "Moderate" if scores1['K'] <= 3 else "Requires effort"} | {"Easy - minimal prep" if scores2['K'] <= 2 else "Moderate" if scores2['K'] <= 3 else "Requires effort"} |
| Cognitive Load | {"Low" if scores1['C'] <= 2 else "Medium" if scores1['C'] <= 3 else "High"} | {"Low" if scores2['C'] <= 2 else "Medium" if scores2['C'] <= 3 else "High"} |
| Head Arrival | {"Delayed" if scores1['C'] <= 2 else "Mid-occasion" if scores1['C'] <= 3 else "Early/Immediate"} | {"Delayed" if scores2['C'] <= 2 else "Mid-occasion" if scores2['C'] <= 3 else "Early/Immediate"} |
| Repeat Mechanism | {"Habitual" if den1 <= 6 else "Requires effort"} | {"Habitual" if den2 <= 6 else "Requires effort"} |

---

## Why This Matters for Enterprise Value

> *"TAM is the size of the door. Elbow Interference tells you whether consumers walk through it once or every week."*

"""
    if loser_score < 2:
        memo += f"""**{loser}** (S-Score: {loser_score:.2f}):
- High interference = velocity must be **purchased**, not compounded
- Repeat depends on consumer **discipline**, not automatic behavior
- Marketing must continuously **reactivate** ("Have you bought yours lately?")
- **Churn risk** when consumers forget, get busy, or encounter friction

**{winner}** (S-Score: {winner_score:.2f}):
- Lower interference = repeat **compounds naturally**
- Behavioral advantage creates **structural moat**
- Marketing drives **trial**; structure handles **repeat**
"""
    else:
        memo += f"""Both brands show viable persistence profiles, but **{winner}** has the structural edge.

- {winner}: Velocity earned through repeat structure
- {loser}: Requires more marketing support for same repeat rate
"""
    memo += f"""

---

## Where {loser} Could Improve (Through EIT Lens)

"""
    if loser_scores['C'] >= 4:
        memo += f"""1. **Lower Cognitive Friction**: Simplify the value proposition. Stop requiring consumers to think.
2. **Reduce Conceptual Hooks**: If brand relies on celebrity, trend, or complex benefits, find ways to make value embodied (felt immediately) rather than conceptual (requires explanation).
"""
    if loser_scores['B'] >= 4:
        memo += f"""3. **Reduce Decisions**: Consider portion-controlled or single-serve formats that end the occasion automatically.
"""
    if loser_scores['K'] >= 3:
        memo += f"""4. **Lower Kinetic Effort**: Ready-to-consume formats beat "some assembly required."
"""
    if loser_scores['F'] <= 2:
        memo += f"""5. **Build Familiarity**: Anchor to existing rituals rather than creating new behaviors.
"""
    memo += f"""

---

## Final Assessment

> *"Repeat behavior is not created by marketing. It is allowed or blocked by product structure."*

**{winner}**: {"Structural Compounder" if winner_score >= 5 else "Low-Friction Asset" if winner_score >= 2 else "Moderate Persistence"}
- {"Denominator collapse achieved - repeat is automatic" if winner_scores['B'] * winner_scores['K'] * winner_scores['C'] <= 6 else "Manageable friction profile"}
- Velocity {"compounds naturally" if winner_score >= 3 else "supported by structure"}

**{loser}**: {"High-Interference Asset" if loser_score < 1.5 else "Purchased Velocity Risk" if loser_score < 2.5 else "Moderate Persistence"}
- {"Heavy denominator blocks habitual repeat" if loser_scores['B'] * loser_scores['K'] * loser_scores['C'] >= 24 else "Some structural friction"}
- {"Velocity must be purchased through continuous marketing" if loser_score < 2 else "Requires some marketing support"}

**Investment Verdict:**

{winner} wins this duel with a **{ratio:.1f}x structural advantage**. 

{"This is a decisive gap - the structural difference is significant enough to impact long-term enterprise value." if ratio >= 2 else "This is a meaningful gap that compounds over time through repeat purchase behavior." if ratio >= 1.5 else "The gap is modest - competitive positioning and execution will matter as much as structure."}

---

*Analysis generated using the Elbow Interference Theory™ by Russell Barnett. Prepared with the rigor of a world-class market research strategist.*
"""
    return memo
