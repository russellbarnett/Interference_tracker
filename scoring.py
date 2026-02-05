"""
Elbow Interference Evaluator™ — S-Score and validation.
Pure scoring logic: no UI, no AI.
CONFIDENTIAL: Russell Barnett © 2026.
"""


def calculate_s_score(m: float, e: float, f: float, b: float, k: float, c: float) -> float:
    """S = (M×E×F) / (B×K×C). Accepts int or float; denominator clamped to avoid div-by-zero."""
    num = float(m) * float(e) * float(f)
    den = max(1.0, float(b) * float(k) * float(c))
    if den <= 0 or num < 0:
        return 0.0
    result = num / den
    return result if (result == result and result != float("inf")) else 0.0  # guard nan/inf


def validate_rationale(text: str) -> bool:
    """Require at least 25 alphanumeric characters for override rationale."""
    if not text:
        return False
    return sum(1 for c in text.strip() if c.isalnum()) >= 25
