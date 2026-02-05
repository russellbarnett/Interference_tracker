"""
Elbow Interference Evaluator™ — Brand data and lookup.
Archetypes, BRAND_DATABASE, KNOWN_BRANDS, and fuzzy brand resolution.
CONFIDENTIAL: Russell Barnett © 2026.
"""

from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List


# ═══════════════════════════════════════════════════════════════════════════════
# PRODUCT FORMATS (Archetypes)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Archetype:
    name: str
    short_name: str
    examples: str
    description: str
    M: int
    E: int
    F: int
    B: int
    K: int
    C: int
    why_denominator: str


ARCHETYPES: Dict[str, Archetype] = {
    "unitized": Archetype(
        name="Single-Serve / Portion-Controlled",
        short_name="Single-Serve",
        examples="Mochi bites, protein bars, ice cream bars, snack packs",
        description="The package decides when you're done. One portion = one occasion. No decisions needed.",
        M=4, E=4, F=3, B=1, K=1, C=1,
        why_denominator="B=1, K=1, C=1 because you eat the whole thing without deciding to stop. The format does the work."
    ),
    "bulk": Archetype(
        name="Multi-Serve / Open Container",
        short_name="Multi-Serve",
        examples="Pints, tubs, chip bags, family-size containers",
        description="YOU decide when to stop. Each bite is a new decision. More chances to quit early.",
        M=5, E=4, F=4, B=4, K=3, C=3,
        why_denominator="B=4, K=3, C=3 because you must self-regulate. Many bites = many chances for your brain to say 'stop'."
    ),
    "ritual": Archetype(
        name="Ritual / Single-Occasion Beverage",
        short_name="Ritual Drink",
        examples="Soda cans, energy drinks, bottled beverages, sparkling water",
        description="One can = one ritual. Highly familiar. You drink it without thinking.",
        M=3, E=3, F=5, B=1, K=1, C=1,
        why_denominator="B=1, K=1, C=1 because it's automatic. High familiarity (F=5) means zero cognitive friction."
    ),
}

BRAND_DATABASE: Dict[str, Tuple[str, str]] = {
    "my/mochi": ("unitized", "Premium frozen mochi"),
    "mymochi": ("unitized", "Premium frozen mochi"),
    "my mochi": ("unitized", "Premium frozen mochi"),
    "mochi": ("unitized", "Premium frozen mochi"),
    "kind": ("unitized", "Nutrition bars"),
    "kind bar": ("unitized", "Nutrition bars"),
    "rxbar": ("unitized", "Protein bars"),
    "rx bar": ("unitized", "Protein bars"),
    "quest": ("unitized", "Protein snacks"),
    "yasso": ("unitized", "Frozen yogurt bars"),
    "magnum": ("unitized", "Ice cream bars"),
    "doughlicious": ("unitized", "Cookie dough bites"),
    "doughliscious": ("unitized", "Cookie dough bites"),
    "ben & jerry's": ("bulk", "Premium pints"),
    "ben and jerry's": ("bulk", "Premium pints"),
    "ben and jerrys": ("bulk", "Premium pints"),
    "ben jerry": ("bulk", "Premium pints"),
    "häagen-dazs": ("bulk", "Premium pints"),
    "haagen-dazs": ("bulk", "Premium pints"),
    "haagen dazs": ("bulk", "Premium pints"),
    "hagendaz": ("bulk", "Premium pints"),
    "haagendazs": ("bulk", "Premium pints"),
    "talenti": ("bulk", "Gelato pints"),
    "dr. bombay": ("bulk", "Celebrity pints"),
    "dr bombay": ("bulk", "Celebrity pints"),
    "doctor bombay": ("bulk", "Celebrity pints"),
    "drbombay": ("bulk", "Celebrity pints"),
    "serendipity": ("bulk", "Premium pints"),
    "jeni's": ("bulk", "Artisan pints"),
    "jenis": ("bulk", "Artisan pints"),
    "lay's": ("bulk", "Multi-serve chips"),
    "lays": ("bulk", "Multi-serve chips"),
    "doritos": ("bulk", "Multi-serve chips"),
    "cheetos": ("bulk", "Multi-serve snacks"),
    "poppi": ("ritual", "Prebiotic soda"),
    "poppie": ("ritual", "Prebiotic soda"),
    "olipop": ("ritual", "Functional soda"),
    "oli pop": ("ritual", "Functional soda"),
    "liquid death": ("ritual", "Canned water"),
    "liquiddeath": ("ritual", "Canned water"),
    "celsius": ("ritual", "Energy drinks"),
    "red bull": ("ritual", "Energy drinks"),
    "redbull": ("ritual", "Energy drinks"),
    "coca-cola": ("ritual", "Carbonated beverages"),
    "coca cola": ("ritual", "Carbonated beverages"),
    "coke": ("ritual", "Carbonated beverages"),
    "pepsi": ("ritual", "Carbonated beverages"),
    "monster": ("ritual", "Energy drinks"),
}

# Known brand scores (M,E,F,B,K,C) and reasoning for overrides / display.
KNOWN_BRANDS = {
    'serendipity': {'M': 4, 'E': 4, 'F': 5, 'B': 4, 'K': 3, 'C': 3,
                    'reasoning': 'Serendipity: NYC legacy brand since 1954. High Familiarity (F=5) from decades of brand building. Standard pint format drives B/K. Low cognitive friction (C=3) - no justification needed for a known indulgence.'},
    'dr. bombay': {'M': 4, 'E': 4, 'F': 3, 'B': 4, 'K': 3, 'C': 5,
                   'reasoning': 'Dr. Bombay: Celebrity brand (Snoop Dogg). Low Familiarity (F=3) - new entrant without legacy. HIGH Cognitive (C=5) - celebrity branding invites consumer to evaluate/justify purchase. The "head" arrives before consumption.'},
    'dr bombay': {'M': 4, 'E': 4, 'F': 3, 'B': 4, 'K': 3, 'C': 5,
                  'reasoning': 'Dr. Bombay: Celebrity brand (Snoop Dogg). Low Familiarity (F=3) - new entrant without legacy. HIGH Cognitive (C=5) - celebrity branding invites consumer to evaluate/justify purchase.'},
    'häagen-dazs': {'M': 5, 'E': 5, 'F': 5, 'B': 4, 'K': 3, 'C': 2,
                    'reasoning': 'Häagen-Dazs: Ultra-legacy premium brand. Maximum Familiarity (F=5). Premium positioning but so established that C is low - consumers know what they are getting.'},
    'haagen-dazs': {'M': 5, 'E': 5, 'F': 5, 'B': 4, 'K': 3, 'C': 2,
                    'reasoning': 'Häagen-Dazs: Ultra-legacy premium brand.'},
    'ben & jerry\'s': {'M': 5, 'E': 5, 'F': 5, 'B': 4, 'K': 3, 'C': 2,
                       'reasoning': 'Ben & Jerry\'s: Iconic legacy brand with decades of equity.'},
    'my/mochi': {'M': 4, 'E': 4, 'F': 4, 'B': 1, 'K': 1, 'C': 1,
                 'reasoning': 'My/Mochi: Unitized format = Denominator Collapse. B=1, K=1, C=1 because occasion ends automatically.'},
    'mymochi': {'M': 4, 'E': 4, 'F': 4, 'B': 1, 'K': 1, 'C': 1,
                'reasoning': 'My/Mochi: Unitized format = Denominator Collapse.'},
    'coca-cola': {'M': 4, 'E': 4, 'F': 5, 'B': 1, 'K': 1, 'C': 1,
                  'reasoning': 'Coca-Cola: Maximum legacy (F=5). Ritual format (can) = Denominator Collapse.'},
    'coke': {'M': 4, 'E': 4, 'F': 5, 'B': 1, 'K': 1, 'C': 1,
             'reasoning': 'Coca-Cola: Maximum legacy.'},
    'pepsi': {'M': 4, 'E': 4, 'F': 5, 'B': 1, 'K': 1, 'C': 1,
              'reasoning': 'Pepsi: Maximum legacy (F=5). Ritual format.'},
    'oreo': {'M': 4, 'E': 4, 'F': 5, 'B': 2, 'K': 1, 'C': 1,
             'reasoning': 'Oreo: Iconic snack brand. Maximum Familiarity.'},
    'poppi': {'M': 3, 'E': 3, 'F': 4, 'B': 1, 'K': 1, 'C': 2,
              'reasoning': 'Poppi: Growing familiarity. Ritual preservation (soda format). Some cognitive for "better-for-you" positioning.'},
    'lays': {'M': 4, 'E': 4, 'F': 5, 'B': 5, 'K': 2, 'C': 1,
             'reasoning': 'Lay\'s: Maximum legacy. Bulk format = high B (decisions). Low C (autopilot snacking).'},
    'popchips': {'M': 3, 'E': 3, 'F': 3, 'B': 5, 'K': 2, 'C': 3,
                 'reasoning': 'Popchips: Moderate familiarity. "Better" positioning adds cognitive friction.'},
    'clif bar': {'M': 3, 'E': 3, 'F': 4, 'B': 1, 'K': 1, 'C': 2,
                 'reasoning': 'Clif Bar: Established energy bar brand (F=4). Unitized format = B=1, K=1. Some health consideration (C=2).'},
    'clif': {'M': 3, 'E': 3, 'F': 4, 'B': 1, 'K': 1, 'C': 2,
             'reasoning': 'Clif Bar: Established energy bar brand.'},
    'kind bar': {'M': 4, 'E': 3, 'F': 4, 'B': 1, 'K': 1, 'C': 2,
                 'reasoning': 'KIND: Well-established healthy snack (F=4). Unitized bar format.'},
    'kind': {'M': 4, 'E': 3, 'F': 4, 'B': 1, 'K': 1, 'C': 2,
             'reasoning': 'KIND: Well-established healthy snack.'},
    'rxbar': {'M': 3, 'E': 3, 'F': 3, 'B': 1, 'K': 1, 'C': 3,
              'reasoning': 'RXBAR: Growing brand, transparency messaging adds cognitive load.'},
    'joy days': {'M': 4, 'E': 4, 'F': 2, 'B': 1, 'K': 1, 'C': 3,
                 'reasoning': 'Joy Days: Newer frozen novelty brand (F=2). Unitized format. Some premium/health consideration.'},
    'joydays': {'M': 4, 'E': 4, 'F': 2, 'B': 1, 'K': 1, 'C': 3,
                'reasoning': 'Joy Days: Newer frozen novelty brand.'},
    'magnum': {'M': 5, 'E': 5, 'F': 4, 'B': 1, 'K': 1, 'C': 2,
               'reasoning': 'Magnum: Premium ice cream bar, established global brand (F=4). Unitized format.'},
    'mars': {'M': 4, 'E': 4, 'F': 5, 'B': 1, 'K': 1, 'C': 1,
             'reasoning': 'Mars: Iconic legacy brand (F=5). Autopilot purchase (C=1).'},
    'snickers': {'M': 5, 'E': 4, 'F': 5, 'B': 1, 'K': 1, 'C': 1,
                 'reasoning': 'Snickers: Maximum legacy (F=5). Autopilot purchase.'},
    'twix': {'M': 4, 'E': 4, 'F': 5, 'B': 1, 'K': 1, 'C': 1,
             'reasoning': 'Twix: Iconic candy bar. Maximum legacy.'},
    'talenti': {'M': 5, 'E': 5, 'F': 4, 'B': 4, 'K': 3, 'C': 2,
                'reasoning': 'Talenti: Premium gelato, well-known (F=4). Pint format = bulk denominator.'},
    'halo top': {'M': 3, 'E': 3, 'F': 3, 'B': 4, 'K': 3, 'C': 3,
                 'reasoning': 'Halo Top: Growing "better-for-you" ice cream. Cognitive for health positioning.'},
    'red bull': {'M': 3, 'E': 4, 'F': 5, 'B': 1, 'K': 1, 'C': 1,
                 'reasoning': 'Red Bull: Maximum legacy energy drink. Ritual can format.'},
    'monster': {'M': 3, 'E': 4, 'F': 4, 'B': 1, 'K': 1, 'C': 1,
                'reasoning': 'Monster: Established energy drink brand.'},
    'prime': {'M': 3, 'E': 3, 'F': 3, 'B': 1, 'K': 1, 'C': 4,
              'reasoning': 'Prime: Celebrity brand (Logan Paul/KSI). F=3 (new), C=4 (celebrity cognitive load).'},
    'feastables': {'M': 4, 'E': 4, 'F': 2, 'B': 2, 'K': 1, 'C': 5,
                   'reasoning': 'Feastables: MrBeast celebrity chocolate. Low F (new), High C (celebrity evaluation).'},
    'liquid death': {'M': 2, 'E': 3, 'F': 3, 'B': 1, 'K': 1, 'C': 3,
                     'reasoning': 'Liquid Death: Growing brand with edgy marketing. Some cognitive for branding novelty.'},
    'celsius': {'M': 3, 'E': 4, 'F': 3, 'B': 1, 'K': 1, 'C': 2,
                'reasoning': 'Celsius: Growing fitness energy drink brand.'},
}


def normalize_brand_name(name: str) -> str:
    """Normalize brand name for better AI recognition."""
    if not name:
        return name
    variations = {
        "dr bombay": "Dr. Bombay",
        "drbombay": "Dr. Bombay",
        "dr.bombay": "Dr. Bombay",
        "doctor bombay": "Dr. Bombay",
        "mymochi": "My/Mochi",
        "my mochi": "My/Mochi",
        "cocacola": "Coca-Cola",
        "coca cola": "Coca-Cola",
        "coke": "Coca-Cola",
        "pepsicola": "Pepsi",
        "pepsi cola": "Pepsi",
        "lays": "Lay's",
        "lay's": "Lay's",
        "haagen dazs": "Häagen-Dazs",
        "haagendazs": "Häagen-Dazs",
        "haagen-dazs": "Häagen-Dazs",
        "ben and jerrys": "Ben & Jerry's",
        "ben & jerry's": "Ben & Jerry's",
        "ben jerrys": "Ben & Jerry's",
    }
    normalized = name.strip().lower()
    if normalized in variations:
        return variations[normalized]
    return name.strip()


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity between two strings (0-1, higher is better)."""
    distance = levenshtein_distance(s1.lower(), s2.lower())
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    return 1 - (distance / max_len)


def find_similar_brands(query: str, threshold: float = 0.6) -> list:
    """Find brands similar to the query."""
    if not query:
        return []
    normalized = query.lower().strip()
    matches = []
    for brand_key in BRAND_DATABASE.keys():
        if brand_key in normalized or normalized in brand_key:
            return [(brand_key, 1.0)]
        score = similarity_score(normalized, brand_key)
        clean_query = ''.join(c for c in normalized if c.isalnum())
        clean_brand = ''.join(c for c in brand_key if c.isalnum())
        score2 = similarity_score(clean_query, clean_brand)
        best_score = max(score, score2)
        if best_score >= threshold:
            matches.append((brand_key, best_score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:3]


def hunt_brand(brand_name: str) -> Tuple[Optional[str], Optional[str], bool, list]:
    """
    Hunt for brand in database with fuzzy matching.
    Returns: (archetype, description, is_ambiguous, similar_brands)
    """
    if not brand_name:
        return None, None, False, []
    normalized = brand_name.lower().strip()
    for brand_key, (archetype, desc) in BRAND_DATABASE.items():
        if brand_key in normalized or normalized in brand_key:
            return archetype, desc, False, []
    similar = find_similar_brands(normalized)
    if similar:
        if similar[0][1] >= 0.8:
            best_match = similar[0][0]
            archetype, desc = BRAND_DATABASE[best_match]
            return archetype, desc, False, similar
        return None, None, False, similar
    return None, None, False, []
