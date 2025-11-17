# ✈️ Priyadarshini - Complete Flight Booking IVR System

**Production-Ready Flight Booking IVR with Chat & Phone Interfaces**

## Features
- ✈️ Book Flight (Location, Date, Passengers, Class)
- 🔄 Change Booking (by PNR)
- 💼 Upgrade to Business Class (with charge)
- 📊 Check Status (by PNR)
- ❌ Cancel Booking (80% refund)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Access Interfaces

### Chat Interface
```
http://localhost:8000
```

### Phone Interface  
```
http://localhost:8000/phone
```

## Test

```bash
pytest
```

## API Endpoint

```
POST /process
{
  "text": "1",
  "session_id": "unique_id"
}
```

## Project Structure

```
├── main.py                    # FastAPI app
├── requirements.txt           # Dependencies
├── README.md
├── LICENSE
├── .gitignore
│
├── backend/
│   ├── nlp.py                # NLP logic
│   ├── logger.py             # Logging
│   └── __init__.py
│
├── frontend/
│   ├── index.html            # Chat UI
│   ├── phone.html            # Phone UI
│   ├── style.css             # Styling
│   ├── phone-style.css       # Phone styling
│   ├── script.js             # Chat logic
│   └── phone-script.js       # Phone logic
│
└── tests/
    ├── test_api.py
    ├── test_nlp.py
    └── __init__.py
