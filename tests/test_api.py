import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_phone():
    response = client.get("/phone")
    assert response.status_code == 200

def test_book():
    response = client.post("/process", json={"text": "1", "session_id": "test_1"})
    assert response.status_code == 200
    assert "reply" in response.json()

def test_change():
    response = client.post("/process", json={"text": "2", "session_id": "test_2"})
    assert response.status_code == 200

def test_upgrade():
    response = client.post("/process", json={"text": "3", "session_id": "test_3"})
    assert response.status_code == 200

def test_status():
    response = client.post("/process", json={"text": "4", "session_id": "test_4"})
    assert response.status_code == 200

def test_cancel():
    response = client.post("/process", json={"text": "5", "session_id": "test_5"})
    assert response.status_code == 200
