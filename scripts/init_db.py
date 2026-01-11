import json
import sqlite3
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parents[1]
    schema_path = repo_root / "db" / "schema.sql"
    data_path = repo_root / "data" / "test_users.json"

    out_db = repo_root / "db" / "app.db"
    out_db.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(out_db))
    try:
        cur = conn.cursor()
        cur.executescript(schema_path.read_text(encoding="utf-8"))

        users = json.loads(data_path.read_text(encoding="utf-8"))
        cur.execute("DELETE FROM users;")
        cur.executemany(
            "INSERT INTO users(user_id, country, age) VALUES (?, ?, ?)",
            [(u["user_id"], u["country"], u["age"]) for u in users],
        )
        conn.commit()
        print(f"Initialized DB at: {out_db}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
