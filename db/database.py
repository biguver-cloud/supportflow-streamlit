import sqlite3
from pathlib import Path
from datetime import datetime

# ------------------------------------------------------------
# 1) このファイル(db/database.py)の場所からプロジェクトルートを特定
#    db/database.py → parent = db/ → parent.parent = プロジェクト直下
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------
# 2) DBファイルは「プロジェクト直下の supportflow.db」を指す
# ------------------------------------------------------------
DB_PATH = BASE_DIR / "supportflow.db"


def get_connection():
    # ------------------------------------------------------------
    # 3) SQLite接続（パスは絶対パス化済みなので環境差で壊れない）
    # ------------------------------------------------------------
    return sqlite3.connect(DB_PATH)


def init_db():
    # ------------------------------------------------------------
    # 4) テーブル作成（存在していれば何もしない）
    # ------------------------------------------------------------
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
