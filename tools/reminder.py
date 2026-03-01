import sqlite3
from datetime import datetime

DB_PATH = "memory/ai_os.db"


# ---------- CREATE TABLE IF NOT EXISTS ----------
def _ensure_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            time TEXT,
            created TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------- SET REMINDER ----------
def set_reminder(task=None, time=None):

    if not task:
        return "No reminder task provided."

    _ensure_table()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO reminders (task, time, created) VALUES (?, ?, ?)",
        (task, time if time else "unspecified", created_time)
    )

    conn.commit()
    conn.close()

    return f"Reminder set: {task} at {time}"


# ---------- SHOW REMINDERS ----------
def show_reminders():

    _ensure_table()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT task, time FROM reminders")
    rows = c.fetchall()

    conn.close()

    if not rows:
        return "No reminders found."

    out = "Your reminders:\n"
    for r in rows:
        out += f"- {r[0]} at {r[1]}\n"

    return out


# ---------- DELETE REMINDERS ----------
def delete_reminders():

    _ensure_table()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DELETE FROM reminders")
    conn.commit()
    conn.close()

    return "All reminders cleared."
