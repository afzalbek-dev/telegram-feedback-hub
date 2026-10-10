from dataclasses import dataclass
from typing import Optional


class TicketStatus:
    NEW = "new"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class TicketCategory:
    SUGGESTION = "suggestion"  # Taklif
    COMPLAINT = "complaint"    # Shikoyat
    QUESTION = "question"      # Savol
    BUG = "bug"                # Xatolik


@dataclass
class FeedbackTicket:
    id: int
    user_id: int
    username: str
    category: str
    rating: int  # 1 dan 5 gacha
    message: str
    status: str
    admin_response: Optional[str]
    created_at: float
