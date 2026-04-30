import sqlite3
from datetime import datetime

DB_PATH = "friday_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        type TEXT,
        content TEXT
    )""")
    conn.commit()
    conn.close()

def save_memory(type: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memory (date, type, content) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), type, content)
    )
    conn.commit()
    conn.close()

def get_memories(type: str, limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT date, content FROM memory WHERE type=? ORDER BY id DESC LIMIT ?",
        (type, limit)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_recent(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT date, type, content FROM memory ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows