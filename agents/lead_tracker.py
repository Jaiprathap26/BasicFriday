import sqlite3
from datetime import datetime

DB_PATH = "friday_memory.db"

def init_leads():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        name TEXT,
        platform TEXT,
        status TEXT,
        notes TEXT
    )""")
    conn.commit()
    conn.close()

def add_lead(name: str, platform: str, notes: str = ""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO leads (date, name, platform, status, notes) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d"), name, platform, "contacted", notes)
    )
    conn.commit()
    conn.close()
    return f"lead saved: {name} on {platform}"

def get_leads(status: str = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute("SELECT date, name, platform, status, notes FROM leads WHERE status=? ORDER BY id DESC", (status,))
    else:
        c.execute("SELECT date, name, platform, status, notes FROM leads ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return rows

def update_lead_status(name: str, new_status: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE leads SET status=? WHERE name LIKE ?", (new_status, f"%{name}%"))
    conn.commit()
    conn.close()
    return f"updated {name} → {new_status}"