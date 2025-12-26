import sqlite3
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from db.database import DB_PATH


def _dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dict[str, Any]:
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    return conn


def now_iso() -> str:
    return datetime.now().isoformat()


def fetch_tickets(
    status: Optional[str] = None,
    category: Optional[str] = None,
    customer_type: Optional[str] = None,
    assignee: Optional[str] = None,
    keyword: Optional[str] = None,
) -> List[Dict[str, Any]]:
    sql = "SELECT * FROM tickets WHERE 1=1"
    params: List[Any] = []

    if status and status != "全て":
        sql += " AND status = ?"
        params.append(status)

    if category and category != "全て":
        sql += " AND category = ?"
        params.append(category)

    if customer_type and customer_type != "全て":
        sql += " AND customer_type = ?"
        params.append(customer_type)

    if assignee and assignee != "全て":
        sql += " AND assignee = ?"
        params.append(assignee)

    if keyword:
        sql += " AND (title LIKE ? OR body LIKE ? OR memo LIKE ?)"
        k = f"%{keyword}%"
        params.extend([k, k, k])

    sql += " ORDER BY updated_at DESC"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def create_ticket(
    title: str,
    body: str,
    customer_type: str,
    category: str,
    assignee: str = "",
    memo: str = "",
) -> str:
    ticket_id = str(uuid.uuid4())
    created_at = now_iso()
    updated_at = created_at
    status = "未対応"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO tickets (
            id, created_at, updated_at, title, body,
            customer_type, category, status, assignee, memo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ticket_id,
            created_at,
            updated_at,
            title,
            body,
            customer_type,
            category,
            status,
            assignee,
            memo,
        ),
    )
    conn.commit()
    conn.close()
    return ticket_id


def update_ticket(
    ticket_id: str,
    status: str,
    assignee: str,
    memo: str,
) -> None:
    updated_at = now_iso()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE tickets
        SET updated_at = ?, status = ?, assignee = ?, memo = ?
        WHERE id = ?
        """,
        (updated_at, status, assignee, memo, ticket_id),
    )
    conn.commit()
    conn.close()
