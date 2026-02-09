"""
Copy consistency tests — LOCKED IN.
Ensures equation vs persistence is never conflated in UI or copy.
See COPY_RULES.md. Run: python3 -m pytest test_copy_consistency.py -v
"""

import pytest
import os

# Forbidden: equation label must NOT say S = Satisfaction (enables persistence)
FORBIDDEN_EQUATION_LABEL = "S = Satisfaction (enables persistence)"

# Forbidden: any single phrase that defines the equation as "enables persistence"
FORBIDDEN_PATTERNS = [
    "S = Satisfaction (enables persistence)",
    "S=Satisfaction (enables persistence)",
]

# Required: correct framing must appear in config (source of truth for tooltips)
REQUIRED_IN_CONFIG = "persistence is not the equation itself"


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _relevant_source_files():
    """All .py and .md in project root that could contain equation copy. Exclude this test and COPY_RULES."""
    root = os.path.dirname(os.path.abspath(__file__))
    for name in sorted(os.listdir(root)):
        if not name.endswith((".py", ".md")):
            continue
        if name in ("test_copy_consistency.py", "COPY_RULES.md"):
            continue
        path = os.path.join(root, name)
        if os.path.isfile(path):
            yield path, name


class TestEquationVsPersistenceLocked:
    """Equation = Satisfaction. Persistence = outcome, not the equation. Do not conflate."""

    def test_forbidden_equation_label_not_in_app(self):
        """app.py must NOT contain 'S = Satisfaction (enables persistence)'."""
        root = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(root, "app.py")
        content = _read_file(app_path)
        for forbidden in FORBIDDEN_PATTERNS:
            assert forbidden not in content, (
                f"FORBIDDEN copy in app.py: '{forbidden}'. "
                "See COPY_RULES.md: equation label must not say (enables persistence)."
            )

    def test_forbidden_equation_label_not_in_config(self):
        """config.py must NOT contain the forbidden equation label."""
        root = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(root, "config.py")
        content = _read_file(config_path)
        for forbidden in FORBIDDEN_PATTERNS:
            assert forbidden not in content, (
                f"FORBIDDEN copy in config.py: '{forbidden}'. See COPY_RULES.md."
            )

    def test_forbidden_equation_label_not_in_any_relevant_file(self):
        """No .py or .md in project root may use the forbidden equation label."""
        for path, name in _relevant_source_files():
            content = _read_file(path)
            for forbidden in FORBIDDEN_PATTERNS:
                assert forbidden not in content, (
                    f"FORBIDDEN copy in {name}: '{forbidden}'. See COPY_RULES.md."
                )

    def test_config_contains_correct_framing(self):
        """config.py must contain the correct framing (persistence is not the equation)."""
        from config import TOOLTIPS
        equation_tip = TOOLTIPS.get("equation", "")
        assert REQUIRED_IN_CONFIG in equation_tip, (
            f"config TOOLTIPS['equation'] must contain '{REQUIRED_IN_CONFIG}'. See COPY_RULES.md."
        )
