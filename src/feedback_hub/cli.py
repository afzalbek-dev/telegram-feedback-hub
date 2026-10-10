import argparse
import sys
import json
from .storage import FeedbackStorage
from .hub import FeedbackHub
from .models import TicketStatus


def main():
    parser = argparse.ArgumentParser(description="Telegram Feedback Hub - Mijozlar fikrlari boshqaruvi")
    parser.add_argument("--db", default="/tmp/feedback.db", help="SQLite ma'lumotlar bazasi fayli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_p = subparsers.add_parser("submit", help="Yangi fikr/shikoyat qoldirish")
    submit_p.add_argument("--user-id", type=int, required=True, help="Telegram User ID")
    submit_p.add_argument("--username", default="", help="Telegram @username")
    submit_p.add_argument("--category", choices=["suggestion", "complaint", "question", "bug"], default="suggestion")
    submit_p.add_argument("--rating", type=int, default=5, help="Baho (1-5)")
    submit_p.add_argument("--msg", required=True, help="Xabar matni")

    list_p = subparsers.add_parser("list", help="Kelib tushgan chiptalarni ko'rish")
    list_p.add_argument("--status", choices=["new", "in_review", "resolved", "rejected"], help="Status bo'yicha filter")

    reply_p = subparsers.add_parser("reply", help="Chiptaga javob qaytarish va yopish")
    reply_p.add_argument("id", type=int, help="Chipta ID")
    reply_p.add_argument("--msg", required=True, help="Admin javobi")

    stats_p = subparsers.add_parser("stats", help="Umumiy statistika")

    args = parser.parse_args()
    storage = FeedbackStorage(args.db)
    hub = FeedbackHub(storage)

    if args.command == "submit":
        tid = hub.submit_feedback(args.user_id, args.username, args.category, args.rating, args.msg)
        print(f"✅ Chipta qabul qilindi! ID: {tid}")
    elif args.command == "list":
        tickets = storage.list_tickets(status=args.status)
        print(f"Chiptalar soni: {len(tickets)}")
        for t in tickets:
            print(f"#{t.id} [{t.status}] ({t.category}, {t.rating}⭐️) @{t.username}: {t.message[:50]}...")
    elif args.command == "reply":
        ok = hub.resolve_ticket(args.id, args.msg)
        if ok:
            print(f"✅ #{args.id} chiptasiga javob berildi va holat 'resolved'ga o'zgardi.")
        else:
            print(f"Chipta topilmadi: #{args.id}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "stats":
        m = hub.get_summary_metrics()
        print(json.dumps(m, indent=2))


if __name__ == "__main__":
    main()
