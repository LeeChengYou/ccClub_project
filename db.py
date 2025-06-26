import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'stock_analysis.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def register_user(username, password):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            hashed = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # 使用者名稱重複

def validate_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result and check_password_hash(result[0], password):
            return True
    return False
