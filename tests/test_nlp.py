from backend.nlp import get_intent, extract_pnr

def test_intents():
    assert get_intent("book") == "booking"
    assert get_intent("1") == "booking"
    assert get_intent("change") == "change"
    assert get_intent("2") == "change"
    assert get_intent("upgrade") == "upgrade"
    assert get_intent("3") == "upgrade"
    assert get_intent("status") == "status"
    assert get_intent("4") == "status"
    assert get_intent("cancel") == "cancel"
    assert get_intent("5") == "cancel"

def test_pnr():
    assert extract_pnr("ABC123") == "ABC123"
    assert extract_pnr("ABC123#") == "ABC123"
    assert len(extract_pnr("123456")) == 6
