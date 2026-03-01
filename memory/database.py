import sqlite3
import os

DB_PATH = "memory/ai_os.db"

def init_db():
    if not os.path.exists("memory"):
        os.makedirs("memory")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        ai TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_log(user, ai):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 🔥 FIX → force string
    user_str = str(user)
    ai_str = str(ai)

    c.execute(
        "INSERT INTO logs (user, ai) VALUES (?, ?)",
        (user_str, ai_str)
    )

    conn.commit()
    conn.close()