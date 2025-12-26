import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("supportflow.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            customer_type TEXT,
            category TEXT,
            status TEXT,
            assignee TEXT,
            memo TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def now_iso():
    return datetime.now().isoformat()
