from backend.nlp import get_intent as gi

def test_booking():
    assert gi("book a flight") == "booking"

def test_status():
    assert gi("check status") == "status"

def test_cancel():
    assert gi("please cancel my booking") == "cancel"
