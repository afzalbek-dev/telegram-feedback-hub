# Telegram Feedback Hub

Telegram botlar va kanallar orqali foydalanuvchilar fikrlari, takliflari, shikoyatlari va xatoliklar (bug reports) hisobini yurituvchi hamda admin javoblarini boshqaruvchi SQLite asosidagi tizim.

## Xususiyatlari
- **Kategoriyalar**: Taklif (suggestion), Shikoyat (complaint), Savol (question), Xatolik (bug).
- **Holatlar (Status Lifecycle)**: `new` -> `in_review` -> `resolved` / `rejected`.
- **Reyting & Statistika**: 1 dan 5 yulduzgacha bo'lgan baholar tahlili va o'rtacha qoniqish darajasi.
- **Admin Boshqaruvi**: Terminal yoki bot orqali har bir chiptaga to'g'ridan-to'g'ri javob yuborish.

## Foydalanish (Python)
```python
from feedback_hub import FeedbackHub, FeedbackStorage

storage = FeedbackStorage("feedback.db")
hub = FeedbackHub(storage)

# Foydalanuvchi fikrini saqlash
t_id = hub.submit_feedback(user_id=987654, username="shaxzod", category="suggestion", rating=5, message="Yangi mavzular qo'shing")

# Admin javob berishi
hub.resolve_ticket(t_id, "Taklifingiz uchun rahmat, tez orada qo'shamiz!")
```

## CLI
```bash
feedback-hub list --status new
feedback-hub reply 1 --msg "Muammo hal qilindi"
feedback-hub stats
```

## Testlar
```bash
pytest tests/ -v
```

## Litsenziya
MIT
