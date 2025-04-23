import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join("db", "taxi.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_seen TEXT
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                pickup TEXT,
                destination TEXT,
                distance REAL,
                amount REAL,
                timestamp TEXT
            )
        ''')
    conn.commit()
    conn.close()

def log_user(name):
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET last_seen = ? WHERE name = ?", (timestamp, name))
    else:
        cursor.execute("INSERT INTO users (name, last_seen) VALUES (?, ?)", (name, timestamp))

    conn.commit()
    conn.close()

def log_bill(name, pickup, destination, distance, amount):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO bills (username, pickup, destination, distance, amount, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, pickup, destination, distance, amount, timestamp))
        bill_id = cursor.lastrowid  # Get the ID of the inserted row
        conn.commit()
        return bill_id


def update_bill(utr, id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            UPDATE bills
            SET utr = ?, timestamp = ?
            WHERE id = ?
        ''', (utr, timestamp, id))
        conn.commit()
        return cursor.rowcount  # Returns number of rows updated
