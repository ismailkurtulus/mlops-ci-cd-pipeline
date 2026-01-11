import math
from typing import Dict


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


class ToyModel:
    """Minimal model object."""

    def __init__(self, num_buckets: int = 100):
        self.num_buckets = num_buckets

    def predict_proba(self, features: Dict) -> float:
        bucket = int(features["country_bucket"])
        age = float(features["age"])

        w_bucket = (bucket % 10) * 0.05  # 0..0.45
        w_age = (age - 30.0) * 0.02      # centered around 30
        bias = -0.2

        score = bias + w_bucket + w_age
        return sigmoid(score)
