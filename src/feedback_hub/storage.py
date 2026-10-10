import sqlite3
import time
from typing import List, Optional
from .models import FeedbackTicket, TicketStatus


class FeedbackStorage:
    """Mijozlar fikrlari va chiptalarni SQLite bazasida saqlash."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback_tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    category TEXT NOT NULL,
                    rating INTEGER DEFAULT 5,
                    message TEXT NOT NULL,
                    status TEXT NOT NULL,
                    admin_response TEXT,
                    created_at REAL NOT NULL
                )
                """
            )

    def create_ticket(
        self,
        user_id: int,
        username: str,
        category: str,
        rating: int,
        message: str,
    ) -> int:
        with self._conn:
            cur = self._conn.execute(
                """
                INSERT INTO feedback_tickets (user_id, username, category, rating, message, status, admin_response, created_at)
                VALUES (?, ?, ?, ?, ?, ?, NULL, ?)
                """,
                (user_id, username, category, rating, message, TicketStatus.NEW, time.time()),
            )
            return cur.lastrowid

    def get_ticket(self, ticket_id: int) -> Optional[FeedbackTicket]:
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT id, user_id, username, category, rating, message, status, admin_response, created_at
            FROM feedback_tickets WHERE id = ?
            """,
            (ticket_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return FeedbackTicket(*row)

    def list_tickets(self, status: Optional[str] = None, category: Optional[str] = None) -> List[FeedbackTicket]:
        cur = self._conn.cursor()
        sql = "SELECT id, user_id, username, category, rating, message, status, admin_response, created_at FROM feedback_tickets WHERE 1=1"
        params = []
        if status:
            sql += " AND status = ?"
            params.append(status)
        if category:
            sql += " AND category = ?"
            params.append(category)

        sql += " ORDER BY id DESC"
        cur.execute(sql, params)
        return [FeedbackTicket(*r) for r in cur.fetchall()]

    def update_status(self, ticket_id: int, status: str, admin_response: Optional[str] = None) -> bool:
        with self._conn:
            cur = self._conn.execute(
                """
                UPDATE feedback_tickets
                SET status = ?, admin_response = COALESCE(?, admin_response)
                WHERE id = ?
                """,
                (status, admin_response, ticket_id),
            )
            return cur.rowcount > 0

    def close(self):
        self._conn.close()
