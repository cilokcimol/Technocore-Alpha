"""Proof v2 creation, verification, and rejection tests."""
import time

import pytest

import agent

URL = "https://github.com/cilokcimol/Technocore-Alpha"
COMMIT = "a" * 40


def test_proof_v2_roundtrip(loaded_key):
    proof = agent.contribution_proof(loaded_key, URL, COMMIT)
    assert proof["schema"] == "technocore-contribution-proof-v2"
    assert proof["artifact_url"] == URL
    assert proof["commit"] == COMMIT
    assert proof["expires_at"] == proof["issued_at"] + 90 * 24 * 3600
    assert len(proof["nonce"]) == 32
    agent.verify_contribution_proof(proof)


def test_proof_tamper_rejected(loaded_key):
    proof = agent.contribution_proof(loaded_key, URL, COMMIT)
    proof["commit"] = "b" * 40
    with pytest.raises(agent.IdentityError):
        agent.verify_contribution_proof(proof)


def test_proof_v1_rejected(loaded_key):
    proof = agent.contribution_proof(loaded_key, URL, COMMIT)
    proof["schema"] = "technocore-contribution-proof-v1"
    with pytest.raises(agent.ProtocolError):
        agent.verify_contribution_proof(proof)


def test_proof_bad_host_rejected(loaded_key):
    with pytest.raises(agent.ProtocolError):
        agent.contribution_proof(loaded_key, "https://evil.example/x", COMMIT)
    with pytest.raises(agent.ProtocolError):
        agent.contribution_proof(loaded_key, "http://github.com/cilokcimol/Technocore-Alpha", COMMIT)


def test_proof_expired_rejected(loaded_key):
    now = int(time.time())
    proof = agent.contribution_proof(
        loaded_key, URL, COMMIT, issued_at=now - 200 * 24 * 3600, expires_at=now - 100 * 24 * 3600
    )
    with pytest.raises(agent.ProtocolError):
        agent.verify_contribution_proof(proof)


def test_proof_bad_commit_rejected(loaded_key):
    with pytest.raises(agent.ProtocolError):
        agent.contribution_proof(loaded_key, URL, "not a commit")


def test_proof_missing_field_rejected(loaded_key):
    proof = agent.contribution_proof(loaded_key, URL, COMMIT)
    del proof["nonce"]
    with pytest.raises(agent.ProtocolError):
        agent.verify_contribution_proof(proof)
