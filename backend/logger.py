import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Logger setup
logger = logging.getLogger("app-logger")
logger.setLevel(logging.INFO)

# Rotating file handler (5 MB per file, keep 3 backups)
handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# To avoid duplicates
if not logger.handlers:
    logger.addHandler(handler)

def log(message: str):
    """Simple log function used everywhere."""
    logger.info(message)
