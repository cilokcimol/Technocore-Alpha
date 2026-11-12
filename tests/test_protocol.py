"""Protocol validation tests."""
import pytest

import agent


def test_normalize_message():
    assert agent.normalize_message("  hello world  ") == "hello world"
    with pytest.raises(agent.ProtocolError):
        agent.normalize_message("   ")
    with pytest.raises(agent.ProtocolError):
        agent.normalize_message("x" * 5000)


def test_validate_name():
    assert agent.validate_name("lobby") == "lobby"
    assert agent.validate_name("hx-did-gameplay") == "hx-did-gameplay"
    with pytest.raises(agent.ProtocolError):
        agent.validate_name("Lobby")
    with pytest.raises(agent.ProtocolError):
        agent.validate_name("bad room")


def test_validate_nonce():
    assert agent.validate_nonce(123) == "123"
    with pytest.raises(agent.ProtocolError):
        agent.validate_nonce("abc")


def test_message_payload():
    text, payload = agent.message_payload("lobby", "123", "hello")
    assert text == "hello"
    assert payload == b"lobby|123|hello"


def test_sign_and_verify(loaded_key):
    did = agent.did_from_private_key(loaded_key)
    payload = b"lobby|123|hello"
    sig = agent.sign_bytes(loaded_key, payload)
    assert len(sig) == 86
    raw = agent.decode_signature(sig)
    agent.public_key_from_did(did).verify(raw, payload)
    with pytest.raises(agent.ProtocolError):
        agent.decode_signature("short")


def test_read_room_validation():
    with pytest.raises(agent.ProtocolError):
        agent.read_room("lobby", limit=0)
    with pytest.raises(agent.ProtocolError):
        agent.read_room("lobby", limit=201)
    with pytest.raises(agent.ProtocolError):
        agent.read_room("Bad Room")
