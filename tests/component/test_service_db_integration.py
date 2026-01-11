import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient
from src.service import app


def _create_temp_db(tmp_path: Path) -> str:
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        cur.executescript(
            """
            CREATE TABLE users (
              user_id TEXT PRIMARY KEY,
              country TEXT NOT NULL,
              age INTEGER NOT NULL
            );
            """
        )
        cur.execute(
            "INSERT INTO users(user_id, country, age) VALUES (?, ?, ?)",
            ("user_123", "TR", 25),
        )
        conn.commit()
    finally:
        conn.close()
    return str(db_path)


def test_predict_reads_from_sqlite(tmp_path: Path, monkeypatch):
    db_path = _create_temp_db(tmp_path)
    monkeypatch.setenv("DB_PATH", db_path)

    client = TestClient(app)
    r = client.post("/predict", json={"user_id": "user_123"})

    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "user_123"
    assert body["features"]["age"] == 25
