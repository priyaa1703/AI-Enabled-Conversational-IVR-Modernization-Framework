from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.logger import log
from backend.nlp import get_intent, extract_location, extract_pnr
import os
import uuid
from typing import Dict

app = FastAPI(title="Priyadarshini Flight IVR", version="2.0.0")

# Mount static files
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# In-memory storage
sessions: Dict[str, Dict] = {}
bookings: Dict[str, Dict] = {}

# ============ ROUTES ============

@app.get("/")
async def home():
    """Serve chat interface"""
    log("ACCESS_HOME", "Chat UI requested")
    return FileResponse(os.path.join("frontend", "index.html"))

@app.get("/phone")
async def phone():
    """Serve phone interface"""
    log("ACCESS_PHONE", "Phone UI requested")
    return FileResponse(os.path.join("frontend", "phone.html"))

@app.post("/process")
async def process(req: Request):
    """Process user input and return AI response"""
    payload = await req.json()
    text = (payload.get("text") or "").strip()
    session_id = payload.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())

    log("USER_MSG", f"{session_id} -> {text}")
    session = sessions.get(session_id, {"intent": None, "step": None, "data": {}})
    reply = ""
    intent = get_intent(text)

    # MAIN MENU
    if text.lower() in ("0", "menu"):
        reply = "Menu: Press 1=Book Flight, 2=Change Booking, 3=Upgrade to Business, 4=Check Status, 5=Cancel Booking, 0=Exit"
        session["intent"] = None
        session["step"] = None

    # ============ BOOK FLIGHT (1) ============
    elif intent == "booking" or text == "1":
        session["intent"] = "booking"
        if session.get("step") is None:
            session["step"] = "ask_destination"
            reply = "Which city? 1=Chennai, 2=Delhi, 3=Mumbai, 4=Bangalore, 5=Hyderabad"
        elif session["step"] == "ask_destination":
            cities = {"1": "Chennai", "2": "Delhi", "3": "Mumbai", "4": "Bangalore", "5": "Hyderabad"}
            city = cities.get(text, "Chennai")
            session["data"]["destination"] = city
            session["step"] = "ask_date"
            reply = f"Destination: {city}. Which date? 1=Dec25, 2=Dec26, 3=Dec27, 4=Dec28, 5=Dec29"
        elif session["step"] == "ask_date":
            dates = {"1": "2025-12-25", "2": "2025-12-26", "3": "2025-12-27", "4": "2025-12-28", "5": "2025-12-29"}
            date = dates.get(text, "2025-12-25")
            session["data"]["date"] = date
            session["step"] = "ask_passengers"
            reply = f"Date: {date}. How many passengers? 1=1 pax, 2=2 pax, 3=3 pax, 4=4 pax, 5=5 pax"
        elif session["step"] == "ask_passengers":
            session["data"]["passengers"] = text
            session["step"] = "ask_class"
            reply = f"Passengers: {text}. Which class? 1=Economy, 2=Business, 3=First"
        elif session["step"] == "ask_class":
            classes = {"1": "Economy", "2": "Business", "3": "First"}
            cls = classes.get(text, "Economy")
            session["data"]["class"] = cls
            session["step"] = "confirm_booking"
            dest = session["data"].get("destination")
            date = session["data"].get("date")
            pax = session["data"].get("passengers")
            reply = f"Confirm: {pax} pax to {dest} on {date} ({cls})? 1=Yes, 2=No"
        elif session["step"] == "confirm_booking":
            if text == "1":
                pnr = str(uuid.uuid4())[:6].upper()
                bookings[pnr] = {
                    "destination": session["data"].get("destination"),
                    "date": session["data"].get("date"),
                    "passengers": session["data"].get("passengers"),
                    "class": session["data"].get("class"),
                    "status": "Confirmed"
                }
                log("BOOKING_CREATED", f"PNR: {pnr}")
                reply = f"✅ Booked! PNR: {pnr}. Save this for future reference!"
                session["step"] = None
                session["intent"] = None
            else:
                reply = "Booking cancelled. Press 1=Book, 2=Change, 3=Upgrade, 4=Status, 5=Cancel, 0=Menu"
                session["step"] = None
                session["intent"] = None

    # ============ CHANGE BOOKING (2) ============
    elif intent == "change" or text == "2":
        session["intent"] = "change"
        if session.get("step") is None:
            session["step"] = "ask_pnr_change"
            reply = "Enter 6-digit PNR followed by #"
        elif session["step"] == "ask_pnr_change":
            pnr = extract_pnr(text)
            if pnr and pnr in bookings:
                session["data"]["pnr"] = pnr
                session["step"] = "ask_change_type"
                reply = f"PNR: {pnr}. Change what? 1=Date, 2=Destination, 3=Passengers"
            else:
                reply = "Invalid PNR. Enter 6-digit PNR followed by #"
        elif session["step"] == "ask_change_type":
            pnr = session["data"]["pnr"]
            if text == "1":
                session["step"] = "change_date"
                reply = "New date? 1=Dec25, 2=Dec26, 3=Dec27, 4=Dec28, 5=Dec29"
            elif text == "2":
                session["step"] = "change_destination"
                reply = "New city? 1=Chennai, 2=Delhi, 3=Mumbai, 4=Bangalore, 5=Hyderabad"
            elif text == "3":
                session["step"] = "change_passengers"
                reply = "New passengers? 1=1 pax, 2=2 pax, 3=3 pax, 4=4 pax, 5=5 pax"
            else:
                reply = "Invalid option. Press 1=Date, 2=Destination, 3=Passengers"
        elif session["step"] == "change_date":
            dates = {"1": "2025-12-25", "2": "2025-12-26", "3": "2025-12-27", "4": "2025-12-28", "5": "2025-12-29"}
            pnr = session["data"]["pnr"]
            bookings[pnr]["date"] = dates.get(text, "2025-12-25")
            log("BOOKING_CHANGED", f"PNR: {pnr}, Date changed")
            reply = f"✅ Date changed! PNR: {pnr}. Press 0=Menu"
            session["step"] = None
            session["intent"] = None
        elif session["step"] == "change_destination":
            cities = {"1": "Chennai", "2": "Delhi", "3": "Mumbai", "4": "Bangalore", "5": "Hyderabad"}
            pnr = session["data"]["pnr"]
            bookings[pnr]["destination"] = cities.get(text, "Chennai")
            log("BOOKING_CHANGED", f"PNR: {pnr}, Destination changed")
            reply = f"✅ Destination changed! PNR: {pnr}. Press 0=Menu"
            session["step"] = None
            session["intent"] = None
        elif session["step"] == "change_passengers":
            pnr = session["data"]["pnr"]
            bookings[pnr]["passengers"] = text
            log("BOOKING_CHANGED", f"PNR: {pnr}, Passengers changed")
            reply = f"✅ Passengers changed! PNR: {pnr}. Press 0=Menu"
            session["step"] = None
            session["intent"] = None

    # ============ UPGRADE TO BUSINESS (3) ============
    elif intent == "upgrade" or text == "3":
        session["intent"] = "upgrade"
        if session.get("step") is None:
            session["step"] = "ask_pnr_upgrade"
            reply = "Enter 6-digit PNR to upgrade to Business Class #"
        elif session["step"] == "ask_pnr_upgrade":
            pnr = extract_pnr(text)
            if pnr and pnr in bookings:
                session["data"]["pnr"] = pnr
                current_class = bookings[pnr]["class"]
                if current_class == "Business":
                    reply = f"Already Business! PNR: {pnr}. Press 0=Menu"
                    session["step"] = None
                    session["intent"] = None
                elif current_class == "First":
                    reply = f"Already First Class! PNR: {pnr}. Press 0=Menu"
                    session["step"] = None
                    session["intent"] = None
                else:
                    session["step"] = "confirm_upgrade"
                    reply = f"Upgrade {current_class} to Business? Extra cost: $50. 1=Yes, 2=No"
            else:
                reply = "Invalid PNR. Enter 6-digit PNR followed by #"
        elif session["step"] == "confirm_upgrade":
            if text == "1":
                pnr = session["data"]["pnr"]
                bookings[pnr]["class"] = "Business"
                log("UPGRADE_PROCESSED", f"PNR: {pnr}, Upgraded to Business")
                reply = f"✅ Upgraded to Business! PNR: {pnr}. Charge: $50. Press 0=Menu"
                session["step"] = None
                session["intent"] = None
            else:
                reply = "Upgrade cancelled. Press 0=Menu"
                session["step"] = None
                session["intent"] = None

    # ============ CHECK STATUS (4) ============
    elif intent == "status" or text == "4":
        session["intent"] = "status"
        if session.get("step") is None:
            session["step"] = "ask_pnr_status"
            reply = "Enter 6-digit PNR followed by #"
        elif session["step"] == "ask_pnr_status":
            pnr = extract_pnr(text)
            if pnr and pnr in bookings:
                booking = bookings[pnr]
                reply = f"Status: {booking['status']} | {booking['passengers']} pax | {booking['destination']} | {booking['date']} | {booking['class']} | Press 0=Menu"
                log("STATUS_CHECKED", f"PNR: {pnr}")
                session["step"] = None
                session["intent"] = None
            else:
                reply = "Invalid PNR. Enter 6-digit PNR followed by #"

    # ============ CANCEL BOOKING (5) ============
    elif intent == "cancel" or text == "5":
        session["intent"] = "cancel"
        if session.get("step") is None:
            session["step"] = "ask_pnr_cancel"
            reply = "Enter 6-digit PNR to cancel followed by #"
        elif session["step"] == "ask_pnr_cancel":
            pnr = extract_pnr(text)
            if pnr and pnr in bookings:
                session["data"]["pnr"] = pnr
                session["step"] = "confirm_cancel"
                reply = f"Cancel PNR: {pnr}? Refund: 80%. 1=Yes, 2=No"
            else:
                reply = "Invalid PNR. Enter 6-digit PNR followed by #"
        elif session["step"] == "confirm_cancel":
            if text == "1":
                pnr = session["data"]["pnr"]
                del bookings[pnr]
                log("BOOKING_CANCELLED", f"PNR: {pnr}")
                reply = f"✅ Cancelled! Refund: 80% will be credited in 5-7 days. Press 0=Menu"
                session["step"] = None
                session["intent"] = None
            else:
                reply = "Cancellation cancelled. Press 0=Menu"
                session["step"] = None
                session["intent"] = None

    else:
        reply = "Menu: 1=Book, 2=Change, 3=Upgrade, 4=Status, 5=Cancel, 0=Menu"

    sessions[session_id] = session
    log("BOT_REPLY", f"{session_id} -> {reply}")
    return JSONResponse({"reply": reply, "session_id": session_id})

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "app": "Priyadarshini Flight IVR", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
