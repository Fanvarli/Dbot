import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            sender_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS warnings (
            user_id INTEGER PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS muted (
            user_id INTEGER PRIMARY KEY,
            mute_until DATETIME
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS immunities (
            user_id INTEGER PRIMARY KEY
        )
    ''')

    conn.commit()
    conn.close()

def log_event(event, sender_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logs (event, sender_id) VALUES (?, ?)", (event, sender_id))
    conn.commit()
    conn.close()

def add_warning(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT count FROM warnings WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if row:
        count = row[0] + 1
        c.execute("UPDATE warnings SET count = ? WHERE user_id = ?", (count, user_id))
    else:
        count = 1
        c.execute("INSERT INTO warnings (user_id, count) VALUES (?, ?)", (user_id, count))
    conn.commit()
    conn.close()
    return count

def reset_warnings(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM warnings WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def mute_user(user_id, until_timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO muted (user_id, mute_until) VALUES (?, ?)", (user_id, until_timestamp))
    conn.commit()
    conn.close()

def unmute_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM muted WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def is_muted(user_id, now_timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT mute_until FROM muted WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        from datetime import datetime
        mute_until = datetime.fromisoformat(row[0])
        return mute_until > now_timestamp
    return False

def add_immunity(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO immunities (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def remove_immunity(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM immunities WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def has_immunity(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM immunities WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row is not None
