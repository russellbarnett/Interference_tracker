"""
Unit tests for config module (TOOLTIPS, tip, DEFAULT_CATEGORY, WHITE_PAPER).
Run: python -m pytest test_config.py -v
"""

import pytest
from config import TOOLTIPS, tip, DEFAULT_CATEGORY, WHITE_PAPER_CONTEXT


class TestTooltips:
    def test_equation_key_exists(self):
        assert "equation" in TOOLTIPS
        assert "S" in TOOLTIPS["equation"]

    def test_six_variables_present(self):
        for key in "M", "E", "F", "B", "K", "C":
            assert key in TOOLTIPS
            assert len(TOOLTIPS[key]) > 10

    def test_tip_returns_string(self):
        assert isinstance(tip("equation"), str)
        assert isinstance(tip("nonexistent"), str)
        assert tip("nonexistent") == ""


class TestDefaultCategory:
    def test_is_string(self):
        assert isinstance(DEFAULT_CATEGORY, str)
        assert len(DEFAULT_CATEGORY) > 0


class TestWhitePaperContext:
    def test_non_empty(self):
        assert len(WHITE_PAPER_CONTEXT.strip()) > 100

    def test_contains_equation(self):
        assert "S = (M × E × F)" in WHITE_PAPER_CONTEXT or "S =" in WHITE_PAPER_CONTEXT

    def test_contains_elbow_language(self):
        assert "elbow" in WHITE_PAPER_CONTEXT.lower() or "Elbow" in WHITE_PAPER_CONTEXT
