"""
Unit tests for brands module (archetypes, database, normalize, hunt, similarity).
Run: python -m pytest test_brands.py -v
"""

import pytest
from brands import (
    Archetype,
    ARCHETYPES,
    BRAND_DATABASE,
    KNOWN_BRANDS,
    normalize_brand_name,
    levenshtein_distance,
    similarity_score,
    find_similar_brands,
    hunt_brand,
)


class TestArchetypes:
    def test_three_archetypes(self):
        assert set(ARCHETYPES.keys()) == {"unitized", "bulk", "ritual"}

    def test_unitized_denominator_one(self):
        u = ARCHETYPES["unitized"]
        assert u.B == 1 and u.K == 1 and u.C == 1

    def test_bulk_high_friction(self):
        b = ARCHETYPES["bulk"]
        assert b.B >= 4 and b.K >= 3


class TestBrandDatabase:
    def test_my_mochi_entries(self):
        assert "my/mochi" in BRAND_DATABASE
        assert "mymochi" in BRAND_DATABASE
        arch, desc = BRAND_DATABASE["my/mochi"]
        assert arch == "unitized"

    def test_known_brands_has_scores(self):
        for key, data in KNOWN_BRANDS.items():
            assert "M" in data and "E" in data and "F" in data
            assert "B" in data and "K" in data and "C" in data
            assert 1 <= data["M"] <= 5 and 1 <= data["C"] <= 5


class TestNormalizeBrandName:
    def test_dr_bombay_variants(self):
        assert normalize_brand_name("dr bombay") == "Dr. Bombay"
        assert normalize_brand_name("drbombay") == "Dr. Bombay"

    def test_my_mochi_variants(self):
        assert normalize_brand_name("mymochi") == "My/Mochi"
        assert normalize_brand_name("my mochi") == "My/Mochi"

    def test_coke_normalizes(self):
        assert normalize_brand_name("coke") == "Coca-Cola"

    def test_empty_passthrough(self):
        assert normalize_brand_name("") == ""
        assert normalize_brand_name(None) is None

    def test_unknown_returns_stripped(self):
        assert normalize_brand_name("  Unknown Brand  ") == "Unknown Brand"


class TestLevenshtein:
    def test_equal_zero(self):
        assert levenshtein_distance("abc", "abc") == 0

    def test_one_insert(self):
        assert levenshtein_distance("ab", "abc") == 1

    def test_symmetry(self):
        assert levenshtein_distance("kitten", "sitting") == levenshtein_distance("sitting", "kitten")


class TestSimilarityScore:
    def test_identical_one(self):
        assert similarity_score("coke", "coke") == 1.0

    def test_empty_query(self):
        # Empty string vs non-empty: max_len > 0, distance = len(non_empty) -> score 0.0
        assert similarity_score("", "coke") == 0.0

    def test_range_zero_to_one(self):
        s = similarity_score("xyz", "abc")
        assert 0 <= s <= 1


class TestFindSimilarBrands:
    def test_exact_match_returns_single(self):
        assert find_similar_brands("my/mochi") == [("my/mochi", 1.0)]

    def test_empty_returns_empty(self):
        assert find_similar_brands("") == []

    def test_typo_returns_suggestions(self):
        results = find_similar_brands("mymochi", threshold=0.5)
        assert len(results) >= 1
        assert results[0][0] in BRAND_DATABASE


class TestHuntBrand:
    def test_exact_match(self):
        arch, desc, ambiguous, similar = hunt_brand("My/Mochi")
        assert arch == "unitized"
        assert desc is not None
        assert ambiguous is False

    def test_empty_returns_none(self):
        assert hunt_brand("") == (None, None, False, [])

    def test_unknown_returns_none_and_maybe_similar(self):
        arch, desc, ambiguous, similar = hunt_brand("UnknownBrandXYZ")
        assert arch is None
        assert desc is None
