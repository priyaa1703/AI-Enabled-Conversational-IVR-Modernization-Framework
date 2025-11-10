from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)

def test_predict():
    res = client.post("/predict", json={"text":"book flight"})
    assert res.status_code == 200
    data = res.json()
    assert "intent" in data
