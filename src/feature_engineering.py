# test_features.py
import pytest

from features import build_features


def test_build_features_should_not_crash_on_bad_age():
    # Bu test, "kötü age" geldiğinde crash olmamasını bekliyor.
    # Mevcut implementasyonda int("unknown") -> ValueError fırlatır, test FAIL olur.
    user_profile = {"country": "TR", "age": "unknown"}

    feats = build_features(user_profile, num_buckets=100)

    assert feats["age"] == 0
    assert 0 <= feats["country_bucket"] < 100
