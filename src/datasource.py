import sqlite3
from typing import Optional, Dict


def get_user_profile(db_path: str, user_id: str) -> Optional[Dict]:
    """
    Read from SQLite. Allowed for component/integration tests.
    Unit tests must NOT touch DB/network.
    """
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT user_id, country, age FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return {"user_id": row[0], "country": row[1], "age": row[2]}
    finally:
        conn.close()
