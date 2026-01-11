import hashlib


def hashed_feature(value: str, num_buckets: int, seed: str = "v1") -> int:
    """
    Deterministic hashing for high-cardinality categorical features.
    Fast, isolated, no external dependencies.
    """
    if num_buckets <= 0:
        raise ValueError("num_buckets must be positive")

    if value is None:
        value = ""

    digest = hashlib.md5((seed + value).encode("utf-8")).hexdigest()
    return int(digest, 16) % num_buckets


def build_features(user_profile: dict, num_buckets: int = 100) -> dict:
    """
    Convert user_profile -> model input features.
    Example: country hashed into buckets + numeric age.
    """
    country = user_profile.get("country", "")
    age = int(user_profile.get("age", 0))

    return {
        "country_bucket": hashed_feature(country, num_buckets=num_buckets, seed="country"),
        "age": age,
    }
