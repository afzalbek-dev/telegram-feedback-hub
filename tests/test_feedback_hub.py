import pytest
from feedback_hub.storage import FeedbackStorage
from feedback_hub.hub import FeedbackHub
from feedback_hub.models import TicketStatus, TicketCategory


def test_feedback_flow_and_resolution(tmp_path):
    db_file = str(tmp_path / "feedback_test.db")
    storage = FeedbackStorage(db_file)
    hub = FeedbackHub(storage)

    # 1. Chipta yaratish
    t_id = hub.submit_feedback(
        user_id=123456,
        username="alisher_dev",
        category=TicketCategory.BUG,
        rating=2,
        message="To'lov sahifasida tugma bosilmayapti",
    )
    assert t_id == 1

    ticket = storage.get_ticket(1)
    assert ticket.status == TicketStatus.NEW
    assert ticket.rating == 2

    # 2. Ko'rib chiqish holatiga o'tkazish
    assert hub.review_ticket(1) is True
    assert storage.get_ticket(1).status == TicketStatus.IN_REVIEW

    # 3. Hal qilish va admin javobi
    assert hub.resolve_ticket(1, "Xatolik bartaraf etildi, iltimos qayta tekshirib ko'ring.") is True
    updated = storage.get_ticket(1)
    assert updated.status == TicketStatus.RESOLVED
    assert "bartaraf etildi" in updated.admin_response

    # 4. Statistika
    metrics = hub.get_summary_metrics()
    assert metrics["total"] == 1
    assert metrics["average_rating"] == 2.0
    storage.close()


def test_invalid_rating():
    storage = FeedbackStorage(":memory:")
    hub = FeedbackHub(storage)
    with pytest.raises(ValueError):
        hub.submit_feedback(user_id=1, username="test", category="bug", rating=6, message="Hi")
