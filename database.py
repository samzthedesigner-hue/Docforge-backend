import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "docforge_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  original_name TEXT,
                  new_name TEXT,
                  format TEXT,
                  timestamp TEXT,
                  download_link TEXT,
                  metadata TEXT,
                  backed_up INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def save_history(original_name, new_name, format_type, download_link, metadata=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO history 
                 (original_name, new_name, format, timestamp, download_link, metadata) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (original_name, new_name, format_type, datetime.now().isoformat(), download_link, json.dumps(metadata or {})))
    conn.commit()
    conn.close()
    return True

def get_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, original_name, new_name, format, timestamp, download_link, metadata, backed_up FROM history ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def mark_backed_up(record_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE history SET backed_up = 1 WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
