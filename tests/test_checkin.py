"""Checkin and DID note tests with a mocked Technocore layer. No live call."""
import agent

REAL_DID = "did:key:z6MkuNFLm3gbGZibY9zGoEg4LajetxbZcZxiJ4stoywuP4Gj"


def test_publish_did_note(monkeypatch, loaded_key):
    seen = {}

    def fake_text(url):
        seen["url"] = url
        return "ok did-10/cbf746385504cf 56B"

    monkeypatch.setattr(agent, "_http_text", fake_text)
    result = agent.publish_did_note(loaded_key)
    did = agent.did_from_private_key(loaded_key)
    assert result["did"] == did
    assert result["fingerprint"] == agent.did_note_fingerprint(did)["fingerprint"]
    assert seen["url"].startswith("https://technocore.chat/kv/did-")
    assert "/set/" in seen["url"]


def test_checkin_verified(monkeypatch, loaded_key):
    did = agent.did_from_private_key(loaded_key)
    posted = {}

    def fake_post(pk, room, text):
        posted[room] = text
        return {
            "room": room,
            "messages": [{"seq": 100, "from": did, "text": text}],
        }

    monkeypatch.setattr(agent, "post_signed_message", fake_post)
    result = agent.do_checkin(loaded_key, date_text="12 November 2026 08:07 UTC")
    assert result["did"] == did
    assert result["rooms"]["lobby"]["verified"] is True
    assert result["rooms"]["lobby"]["seq"] == 100
    assert result["rooms"]["hx-did-gameplay"]["verified"] is True
    assert posted["lobby"] != posted["hx-did-gameplay"]


def test_checkin_unverified_when_missing(monkeypatch, loaded_key):
    def fake_post(pk, room, text):
        return {"room": room, "messages": []}

    def fake_read(room, limit=50, since=None):
        return {"room": room, "messages": []}

    monkeypatch.setattr(agent, "post_signed_message", fake_post)
    monkeypatch.setattr(agent, "read_room", fake_read)
    result = agent.do_checkin(loaded_key, date_text="12 November 2026 08:07 UTC")
    assert result["rooms"]["lobby"]["verified"] is False
    assert result["rooms"]["lobby"]["seq"] is None


def test_message_in_room():
    did = REAL_DID
    result = {"messages": [{"seq": 5, "from": did, "text": "hello"}]}
    found = agent.message_in_room(result, did, "hello")
    assert found is not None
    assert found["seq"] == 5
    assert agent.message_in_room(result, did, "other") is None
