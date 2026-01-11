import pytest
from app.feature_engineering import hashed_bucket

def test_hashed_bucket_deterministic():
    assert hashed_bucket("hello", 100) == hashed_bucket("hello", 100)

def test_hashed_bucket_range():
    b = hashed_bucket("x", 10)
    assert 0 <= b < 10

def test_hashed_bucket_invalid():
    with pytest.raises(ValueError):
        hashed_bucket("x", 0)
