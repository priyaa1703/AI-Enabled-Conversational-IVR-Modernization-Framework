import datetime
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "ivr_log.txt")

def log(event: str, message: str = ""):
    """Log events to file"""
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{time}] {event} -> {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        print(line)
