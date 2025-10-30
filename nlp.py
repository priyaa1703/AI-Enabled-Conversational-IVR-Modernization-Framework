from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
import os

app = FastAPI()

# ✅ Load your Twilio credentials from environment variables (GitHub-safe)
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# ---- Simple NLP ----
def get_intent(text):
    text = text.lower()

    booking_words = ["book", "booking", "reserve", "new flight", "ticket booking"]
    status_words = ["status", "check", "details", "info", "information"]
    cancel_words = ["cancel", "cancellation", "drop", "stop booking"]

    if any(w in text for w in booking_words):
        return "booking"
    if any(w in text for w in status_words):
        return "status"
    if any(w in text for w in cancel_words):
        return "cancel"

    return "unknown"


@app.post("/ivr", response_class=PlainTextResponse)
async def ivr():
    r = VoiceResponse()
    r.say("Hello. Welcome to the airline service. You may speak after the beep.")
    r.gather(
        input="speech",
        action="/process",
        timeout=4
    )
    return str(r)


@app.post("/process", response_class=PlainTextResponse)
async def process(speechResult: str = Form("")):
    text = speechResult.lower() if speechResult else ""
    intent = get_intent(text)
    r = VoiceResponse()

    if intent == "booking":
        r.say("You selected booking. Redirecting.")
    elif intent == "status":
        r.say("You selected status checking. Redirecting.")
    elif intent == "cancel":
        r.say("You selected cancellation. Redirecting.")
    else:
        r.say("I could not understand your request. Please say book, check or cancel.")
        r.redirect("/ivr")

    return str(r)
