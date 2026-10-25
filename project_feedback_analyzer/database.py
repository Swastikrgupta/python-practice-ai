import sqlite3

DB_PATH = "reviews.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                label TEXT NOT NULL,
                score INTEGER NOT NULL,
                service TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

def save_review(text: str, label: str, score: int, service: str):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO reviews (text, label, score, service) VALUES (?, ?, ?, ?)",
            (text, label, score, service),
        )

def get_reviews():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]
