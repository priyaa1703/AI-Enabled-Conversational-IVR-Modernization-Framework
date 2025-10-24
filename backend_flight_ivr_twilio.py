from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
import uuid

app = FastAPI(title="Flight Booking IVR")

TWILIO_NUMBER = "+16205368678"

@app.get("/")
def home():
    return {
        "status": "ok",
        "ivr_service": "Skyline Airlines Voice Assistant",
        "twilio_number": TWILIO_NUMBER,
        "session_id": str(uuid.uuid4())
    }

@app.post("/twilio/voice")
async def twilio_voice(request: Request):
    vr = VoiceResponse()
    vr.say("Welcome to Skyline Airlines. Please say book flight, check booking, or cancel flight after the beep.", voice="alice")
    vr.record(action="/twilio/process", max_length=5, play_beep=True)
    return Response(content=str(vr), media_type="application/xml")

@app.post("/twilio/process")
async def twilio_process(request: Request):
    data = await request.form()
    speech = (data.get("SpeechResult") or "").strip().lower()
    vr = VoiceResponse()

    if not speech:
        vr.say("I didn't catch that. Please try again.", voice="alice")
        vr.redirect("/twilio/voice")
        return Response(content=str(vr), media_type="application/xml")

    if "book" in speech:
        vr.say("Sure. Where would you like to fly to?", voice="alice")
        vr.record(action="/twilio/destination", max_length=5, play_beep=True)
    elif "check" in speech:
        vr.say("Please say your booking ID.", voice="alice")
        vr.record(action="/twilio/check", max_length=5, play_beep=True)
    elif "cancel" in speech:
        vr.say("Please say your booking ID to cancel your flight.", voice="alice")
        vr.record(action="/twilio/cancel", max_length=5, play_beep=True)
    else:
        vr.say("Sorry, I didn’t understand. Let’s try again.", voice="alice")
        vr.redirect("/twilio/voice")

    return Response(content=str(vr), media_type="application/xml")

@app.post("/twilio/destination")
async def twilio_destination(request: Request):
    data = await request.form()
    dest = (data.get("SpeechResult") or "").strip()
    vr = VoiceResponse()

    if not dest:
        vr.say("I didn’t hear a destination. Please try again.", voice="alice")
        vr.redirect("/twilio/voice")
        return Response(content=str(vr), media_type="application/xml")

    vr.say(f"Booking flight to {dest}. Please say your preferred date of travel.", voice="alice")
    vr.record(action="/twilio/date", max_length=5, play_beep=True)
    return Response(content=str(vr), media_type="application/xml")

@app.post("/twilio/date")
async def twilio_date(request: Request):
    data = await request.form()
    date = (data.get("SpeechResult") or "").strip()
    vr = VoiceResponse()

    if not date:
        vr.say("I didn’t hear the date. Please try again.", voice="alice")
        vr.redirect("/twilio/voice")
        return Response(content=str(vr), media_type="application/xml")

    vr.say(f"Your flight on {date} has been scheduled. You will receive a confirmation message shortly. Thank you for choosing Skyline Airlines.", voice="alice")
    vr.hangup()
    return Response(content=str(vr), media_type="application/xml")

@app.post("/twilio/check")
async def twilio_check(request: Request):
    data = await request.form()
    booking_id = (data.get("SpeechResult") or "").strip()
    vr = VoiceResponse()

    if not booking_id:
        vr.say("I didn’t get your booking ID. Please try again.", voice="alice")
        vr.redirect("/twilio/voice")
        return Response(content=str(vr), media_type="application/xml")

    vr.say(f"Booking ID {booking_id} is confirmed and on schedule. Thank you for flying with Skyline Airlines.", voice="alice")
    vr.hangup()
    return Response(content=str(vr), media_type="application/xml")

@app.post("/twilio/cancel")
async def twilio_cancel(request: Request):
    data = await request.form()
    booking_id = (data.get("SpeechResult") or "").strip()
    vr = VoiceResponse()

    if not booking_id:
        vr.say("I didn’t hear your booking ID. Please try again.", voice="alice")
        vr.redirect("/twilio/voice")
        return Response(content=str(vr), media_type="application/xml")

    vr.say(f"Your booking with ID {booking_id} has been canceled. We hope to serve you again soon.", voice="alice")
    vr.hangup()
    return Response(content=str(vr), media_type="application/xml")
