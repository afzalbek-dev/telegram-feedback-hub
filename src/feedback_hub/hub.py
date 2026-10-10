from typing import List, Optional, Dict, Any
from .models import FeedbackTicket, TicketStatus, TicketCategory
from .storage import FeedbackStorage


class FeedbackHub:
    """Feedback jarayonini boshqarish, tahlil qilish va admin javoblarini qayta ishlash."""

    def __init__(self, storage: FeedbackStorage):
        self.storage = storage

    def submit_feedback(
        self,
        user_id: int,
        username: str,
        category: str,
        rating: int,
        message: str,
    ) -> int:
        if not (1 <= rating <= 5):
            raise ValueError("Baho (rating) 1 dan 5 gacha bo'lishi kerak")
        if not message.strip():
            raise ValueError("Xabar matni bo'sh bo'lishi mumkin emas")
        return self.storage.create_ticket(user_id, username, category, rating, message)

    def review_ticket(self, ticket_id: int) -> bool:
        return self.storage.update_status(ticket_id, TicketStatus.IN_REVIEW)

    def resolve_ticket(self, ticket_id: int, admin_reply: str) -> bool:
        if not admin_reply.strip():
            raise ValueError("Javob matni bo'sh bo'lishi mumkin emas")
        return self.storage.update_status(ticket_id, TicketStatus.RESOLVED, admin_response=admin_reply)

    def get_summary_metrics(self) -> Dict[str, Any]:
        all_tickets = self.storage.list_tickets()
        if not all_tickets:
            return {"total": 0, "average_rating": 0.0, "status_breakdown": {}}

        total = len(all_tickets)
        avg_rating = sum(t.rating for t in all_tickets) / total
        status_counts = {}
        for t in all_tickets:
            status_counts[t.status] = status_counts.get(t.status, 0) + 1

        return {
            "total": total,
            "average_rating": round(avg_rating, 2),
            "status_breakdown": status_counts,
        }
