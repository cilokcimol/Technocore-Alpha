"""Identity creation, loading, rotation, and revocation tests."""
import os
import stat

import pytest

import agent


def test_create_identity_is_encrypted_and_mode_0600(key_path, passphrase):
    mode = stat.S_IMODE(key_path.stat().st_mode)
    assert mode == 0o600
    data = key_path.read_bytes()
    assert b"ENCRYPTED" in data
    loaded = agent.load_identity(path=key_path, passphrase=passphrase)
    assert agent.did_from_private_key(loaded).startswith("did:key:z")


def test_create_identity_refuses_second(tmp_path, passphrase):
    path = tmp_path / "identity.pem"
    agent.create_identity(path=path, passphrase=passphrase)
    with pytest.raises(agent.IdentityError):
        agent.create_identity(path=path, passphrase=passphrase)
    assert agent.find_existing_identities(path) == [path]


def test_short_passphrase_rejected(tmp_path):
    path = tmp_path / "identity.pem"
    with pytest.raises(agent.IdentityError):
        agent.create_identity(path=path, passphrase="short")


def test_wrong_passphrase_rejected(key_path, passphrase):
    with pytest.raises(agent.IdentityError):
        agent.load_identity(path=key_path, passphrase=passphrase + "wrong")


def test_missing_identity_rejected(tmp_path, passphrase):
    with pytest.raises(agent.IdentityError):
        agent.load_identity(path=tmp_path / "missing.pem", passphrase=passphrase)


def test_passphrase_file_mode_enforced(tmp_path, passphrase):
    path = tmp_path / "passphrase.txt"
    path.write_text(passphrase + "\n", encoding="utf-8")
    path.chmod(0o644)
    with pytest.raises(agent.IdentityError):
        agent.read_passphrase_file(path)
    path.chmod(0o600)
    assert agent.read_passphrase_file(path) == passphrase


def test_passphrase_from_env(monkeypatch, passphrase_file, passphrase):
    monkeypatch.setenv("TECHNOCORE_PASSPHRASE_FILE", str(passphrase_file))
    assert agent.passphrase_from_env() == passphrase
    monkeypatch.delenv("TECHNOCORE_PASSPHRASE_FILE")
    assert agent.passphrase_from_env() is None


def test_rotation_roundtrip(tmp_path, passphrase):
    old_path = tmp_path / "old.pem"
    new_path = tmp_path / "new.pem"
    old_did = agent.create_identity(path=old_path, passphrase=passphrase)
    new_did = agent.create_identity(path=new_path, passphrase=passphrase)
    old_pk = agent.load_identity(path=old_path, passphrase=passphrase)
    statement = agent.rotation_statement(old_pk, new_did)
    assert statement["previous_did"] == old_did
    assert statement["did"] == new_did
    agent.verify_rotation_statement(statement)
    statement["did"] = old_did
    with pytest.raises(agent.ProtocolError):
        agent.verify_rotation_statement(statement)


def test_revocation_roundtrip(loaded_key):
    statement = agent.revocation_statement(loaded_key, reason="test retirement")
    agent.verify_revocation_statement(statement)
    statement["signature"] = "A" * 86
    with pytest.raises(agent.IdentityError):
        agent.verify_revocation_statement(statement)


def test_unencrypted_key_rejected(tmp_path, passphrase):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    pk = Ed25519PrivateKey.generate()
    raw = pk.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    path = tmp_path / "identity.pem"
    path.write_bytes(raw)
    path.chmod(0o600)
    with pytest.raises(agent.IdentityError):
        agent.load_identity(path=path, passphrase=passphrase)
