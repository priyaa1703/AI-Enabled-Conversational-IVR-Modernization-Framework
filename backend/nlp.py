def get_intent(text: str) -> str:
    """Determine user intent from input text"""
    text = (text or "").lower()

    if any(w in text for w in ["book", "booking", "1", "reserve", "flight"]):
        return "booking"
    elif any(w in text for w in ["change", "2", "modify", "reschedule", "update"]):
        return "change"
    elif any(w in text for w in ["upgrade", "3", "business", "class", "premium"]):
        return "upgrade"
    elif any(w in text for w in ["status", "4", "check", "track", "info"]):
        return "status"
    elif any(w in text for w in ["cancel", "5", "stop", "delete", "refund"]):
        return "cancel"
    return "unknown"

def extract_location(text: str) -> str:
    """Extract city/location from text"""
    text = (text or "").lower()
    cities = {
        "1": "Chennai", "2": "Delhi", "3": "Mumbai",
        "4": "Bangalore", "5": "Hyderabad", "6": "Goa"
    }
    if text in cities:
        return cities[text]
    for city in ["chennai", "delhi", "mumbai", "bangalore", "hyderabad", "goa"]:
        if city in text:
            return city.capitalize()
    return "Chennai"

def extract_pnr(text: str) -> str:
    """Extract 6-digit PNR from text"""
    text = (text or "").strip().upper()
    text = text.replace("#", "").replace(" ", "")

    pnr = ""
    for char in text:
        if char.isalnum():
            pnr += char
        if len(pnr) == 6:
            break

    return pnr if len(pnr) == 6 else None
