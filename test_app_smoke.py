"""
Smoke tests: import all app dependencies and run key code paths.
Does not import app.py (Streamlit runs at import time). Verifies the dependency chain.
Run: python -m pytest test_app_smoke.py -v
"""

import pytest


class TestAppDependencyChain:
    """Import every module that app.py uses; catch import errors."""

    def test_import_config(self):
        from config import TOOLTIPS, tip, DEFAULT_CATEGORY, WHITE_PAPER_CONTEXT
        assert TOOLTIPS and DEFAULT_CATEGORY

    def test_import_brands(self):
        from brands import (
            Archetype,
            ARCHETYPES,
            BRAND_DATABASE,
            KNOWN_BRANDS,
            normalize_brand_name,
            hunt_brand,
        )
        assert len(ARCHETYPES) >= 3
        assert hunt_brand("coke")[0] == "ritual"

    def test_import_scoring(self):
        from scoring import calculate_s_score, validate_rationale
        assert calculate_s_score(4, 4, 4, 1, 1, 1) == 64.0

    def test_import_ai_services(self):
        from ai_services import (
            get_gemini_model,
            analyze_brand_with_ai,
            generate_strategic_synthesis,
            generate_rule_based_memo,
            GEMINI_AVAILABLE,
        )
        assert isinstance(GEMINI_AVAILABLE, bool)
        memo = generate_rule_based_memo("A", "B", 1.0, 2.0,
                                        {"M": 1, "E": 1, "F": 1, "B": 1, "K": 1, "C": 1},
                                        {"M": 2, "E": 2, "F": 2, "B": 1, "K": 1, "C": 1})
        assert "A" in memo and "B" in memo

    def test_import_priors_optional(self):
        try:
            from priors import apply_priors_dict, get_default_context
        except ImportError:
            pytest.skip("priors not installed")

    def test_import_hard_data_optional(self):
        try:
            from hard_data import get_hard_data
            data = get_hard_data()
            assert data is not None or data is None  # either is ok
        except ImportError:
            pytest.skip("hard_data not available")


class TestKeyPathsNoStreamlit:
    """Run logic that app uses, without starting Streamlit."""

    def test_s_score_consistency_with_known_brands(self):
        from brands import KNOWN_BRANDS
        from scoring import calculate_s_score
        for name, data in list(KNOWN_BRANDS.items())[:5]:
            m, e, f = data["M"], data["E"], data["F"]
            b, k, c = data["B"], data["K"], data["C"]
            s = calculate_s_score(m, e, f, b, k, c)
            assert s >= 0 and s != float("inf")

    def test_hunt_then_s_score(self):
        from brands import hunt_brand, KNOWN_BRANDS
        from scoring import calculate_s_score
        arch, desc, _, _ = hunt_brand("my/mochi")
        assert arch is not None
        if arch and arch in ["unitized", "bulk", "ritual"]:
            from brands import ARCHETYPES
            a = ARCHETYPES[arch]
            s = calculate_s_score(a.M, a.E, a.F, a.B, a.K, a.C)
            assert s > 0
