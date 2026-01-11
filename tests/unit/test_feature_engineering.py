import pytest
from src.feature_engineering import hashed_feature


def test_hashed_feature_known_value():
    assert hashed_feature("user_123", 1000, seed="v1") == 515


def test_hashed_feature_in_range():
    idx = hashed_feature("cat", 50, seed="v1")
    assert 0 <= idx < 50


def test_hashed_feature_none_treated_as_empty():
    assert hashed_feature(None, 10, seed="v1") == hashed_feature("", 10, seed="v1")


def test_hashed_feature_invalid_buckets():
    with pytest.raises(ValueError):
        hashed_feature("x", 0)
