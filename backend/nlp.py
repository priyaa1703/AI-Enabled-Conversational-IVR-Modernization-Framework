def get_intent(text: str) -> str:
    text = (text or "").lower()

    booking_words = ["book", "booking", "reserve", "flight", "ticket"]
    status_words = ["status", "check", "information", "track"]
    cancel_words = ["cancel", "stop", "drop", "terminate"]

    if any(w in text for w in booking_words):
        return "booking"
    if any(w in text for w in status_words):
        return "status"
    if any(w in text for w in cancel_words):
        return "cancel"
    return "unknown"
