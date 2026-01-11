import hashlib

def hashed_bucket(text: str, num_buckets: int) -> int:
    if num_buckets <= 0:
        raise ValueError("num_buckets must be > 0")
    h = hashlib.md5(text.encode("utf-8")).hexdigest()
    return int(h, 16) % num_buckets
