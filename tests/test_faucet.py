"""Faucet request building tests with a mocked HTTP layer. No live call."""
import pytest

import agent

ADDRESS = "5H5FBJHh861Pj9kNZiXcbAgyH469ugsfqUqzBrkaxQgmfgZo"
TXHASH = "0x9af6df6d44c57e5cf00049d98494ff956d8866f42216352f5e3c7edfe09d5236"


def test_faucet_claim_success(monkeypatch):
    seen = {}

    def fake_http(method, url, body=None):
        seen["method"] = method
        seen["url"] = url
        seen["body"] = body
        return {"success": True, "amount": 25, "tier": "anonymous", "txHash": TXHASH}

    monkeypatch.setattr(agent, "_http_json", fake_http)
    result = agent.faucet_claim(ADDRESS)
    assert seen["method"] == "POST"
    assert seen["url"] == "https://faucet.flop.network/fund"
    assert seen["body"] == {"address": ADDRESS}
    assert result["amount"] == 25
    assert result["tier"] == "anonymous"
    assert result["txHash"] == TXHASH
    assert result["address"] == ADDRESS


def test_faucet_claim_cooldown(monkeypatch):
    def fake_http(method, url, body=None):
        raise agent.NetworkError("HTTP 429: address cooldown active")

    monkeypatch.setattr(agent, "_http_json", fake_http)
    with pytest.raises(agent.NetworkError):
        agent.faucet_claim(ADDRESS)


def test_faucet_claim_missing_field(monkeypatch):
    def fake_http(method, url, body=None):
        return {"success": True, "amount": 25}

    monkeypatch.setattr(agent, "_http_json", fake_http)
    with pytest.raises(agent.NetworkError):
        agent.faucet_claim(ADDRESS)


def test_faucet_claim_failed_flag(monkeypatch):
    def fake_http(method, url, body=None):
        return {"success": False, "error": "funding unavailable"}

    monkeypatch.setattr(agent, "_http_json", fake_http)
    with pytest.raises(agent.NetworkError):
        agent.faucet_claim(ADDRESS)


def test_faucet_rejects_bad_address():
    with pytest.raises(agent.ProtocolError):
        agent.faucet_claim("not an address")


def test_faucet_http_host_guard():
    with pytest.raises(agent.NetworkError):
        agent._http_json("POST", "https://evil.example/fund", {"address": ADDRESS})
