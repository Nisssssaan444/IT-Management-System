"""
database.py — SQLite setup for ITKit
Handles assets table and audit log table.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "itkit.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Assets table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL UNIQUE,
            asset_type  TEXT    NOT NULL,
            serial      TEXT,
            assigned_to TEXT,
            added_on    TEXT    NOT NULL
        )
    """)

    # Users table (simulated AD/M365 accounts)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL UNIQUE,
            full_name   TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            department  TEXT,
            manager     TEXT,
            status      TEXT    NOT NULL DEFAULT 'active',
            created_on  TEXT    NOT NULL,
            disabled_on TEXT
        )
    """)

    # Audit log table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT    NOT NULL,
            action    TEXT    NOT NULL,
            target    TEXT,
            details   TEXT,
            performed_by TEXT  DEFAULT 'itkit-cli'
        )
    """)

    conn.commit()
    conn.close()
