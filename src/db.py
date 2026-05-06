import sqlite3
import datetime
import os

DB_PATH = 'itkit.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT,
        manager TEXT,
        status TEXT NOT NULL
    )''')
    
    # Assets Table
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        serial TEXT UNIQUE NOT NULL,
        assigned_to TEXT,
        status TEXT NOT NULL
    )''')
    
    # Audit Logs Table
    c.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT
    )''')
    
    conn.commit()
    conn.close()

def log_action(action, details=""):
    conn = get_connection()
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO audit_logs (timestamp, action, details) VALUES (?, ?, ?)", (now, action, details))
    conn.commit()
    conn.close()
