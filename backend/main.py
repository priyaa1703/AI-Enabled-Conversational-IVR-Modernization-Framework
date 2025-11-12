from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.logger import log


from nlp import get_intent

app = FastAPI(title="IVR System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class TextIn(BaseModel):
    text: str

reply_map = {
    "booking": "Booking selected. Redirecting…",
    "status": "Status checking initiated.",
    "cancel": "Cancellation process started.",
    "unknown": "Sorry, I didn’t understand your request."
}

@app.get("/")
def home():
    log("ACCESS_HOME", "Home endpoint accessed")
    return {"message": "IVR backend running!"}

@app.post("/predict")
def predict_text(data: TextIn):
    text = data.text or ""
    log("REQUEST_TEXT", text)
    intent = get_intent(text)
    log("INTENT_IDENTIFIED", intent)
    return {
        "user_text": text,
        "intent": intent,
        "reply": reply_map.get(intent, reply_map["unknown"])
    }
