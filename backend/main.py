from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.logger import log
from backend.nlp import get_intent

app = FastAPI()

# ✅ Serve static UI files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ HOME → serve index.html UI
@app.get("/")
async def home():
    log("ACCESS_HOME", "User opened the IVR UI")
    return FileResponse("static/index.html")


# ✅ PROCESS TEXT (Main IVR Logic)
@app.post("/process")
async def process_text(request: Request):
    data = await request.json()
    text = data.get("text", "")

    log("USER_MESSAGE", text)

    intent = get_intent(text)
    log("DETECTED_INTENT", intent)

    # ✅ Simple IVR Logic
    if intent == "booking":
        reply = "Sure! I can help you with flight booking. What is your destination?"
    elif intent == "status":
        reply = "Alright! Please provide your booking ID to check the status."
    elif intent == "cancel":
        reply = "I can help you cancel your booking. Please share your ticket number."
    else:
        reply = "I'm not sure I understood that. Could you please repeat?"

    log("BOT_REPLY", reply)

    return JSONResponse({"reply": reply})

