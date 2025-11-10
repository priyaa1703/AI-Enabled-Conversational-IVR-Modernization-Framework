import time, requests
def test_performance():
    start = time.time()
    requests.post("http://127.0.0.1:8000/predict", json={"text":"hello"})
    elapsed = time.time() - start
    assert elapsed < 1.5
