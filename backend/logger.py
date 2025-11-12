import datetime

LOG_FILE = "ivr_log.txt"

def log(event: str, message: str):
    """Simple file-based logger"""
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{time}] {event} -> {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
