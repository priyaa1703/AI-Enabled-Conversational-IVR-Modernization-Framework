import requests
def test_e2e():
    res = requests.post("http://127.0.0.1:8000/predict", json={"text":"cancel ticket"})
    assert res.status_code == 200
    assert "cancel" in res.json().get("intent","")
