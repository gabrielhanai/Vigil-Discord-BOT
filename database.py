import sqlite3

def conectar():
    return sqlite3.connect("vigil.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            keyword TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            channel_id TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configs (
            user_id TEXT PRIMARY KEY,
            paused INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

# KEYWORDS
def add_keyword(user_id, keyword):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO keywords (user_id, keyword) VALUES (?, ?)", (user_id, keyword))
    conn.commit()
    conn.close()

def remove_keyword(user_id, keyword):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keywords WHERE user_id = ? AND keyword = ?", (user_id, keyword))
    conn.commit()
    conn.close()

def list_keywords(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT keyword FROM keywords WHERE user_id = ?", (user_id,))
    keywords = cursor.fetchall()
    conn.close()
    return [k[0] for k in keywords]

# CHANNELS
def add_channel(user_id, channel_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO channels (user_id, channel_id) VALUES (?, ?)", (user_id, channel_id))
    conn.commit()
    conn.close()

def remove_channel(user_id, channel_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels WHERE user_id = ? AND channel_id = ?", (user_id, channel_id))
    conn.commit()
    conn.close()

def list_channels(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id FROM channels WHERE user_id = ?", (user_id,))
    channels = cursor.fetchall()
    conn.close()
    return [c[0] for c in channels]

# CONFIGS
def set_paused(user_id, paused):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO configs (user_id, paused) VALUES (?, ?)", (user_id, paused))
    conn.commit()
    conn.close()

def is_paused(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT paused FROM configs WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 1 if result else False