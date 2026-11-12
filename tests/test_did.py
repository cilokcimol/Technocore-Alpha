"""DID derivation, SS58 derivation, and DID note fingerprint tests."""
import hashlib

import agent
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REAL_DID = "did:key:z6MkuNFLm3gbGZibY9zGoEg4LajetxbZcZxiJ4stoywuP4Gj"
REAL_PUBKEY_HEX = "dd969a96261f20ede8c6bf65d8d5abff5f53f4b233458ca59bd5bd5a72f60d6c"
REAL_SS58 = "5H5FBJHh861Pj9kNZiXcbAgyH469ugsfqUqzBrkaxQgmfgZo"
REAL_FINGERPRINT = "10cbf746385504cf"


def test_did_derivation_roundtrip():
    seed = bytes([7]) * 32
    pk = Ed25519PrivateKey.from_private_bytes(seed)
    did = agent.did_from_private_key(pk)
    assert did.startswith("did:key:z")
    assert len(REAL_DID) == 56
    assert 54 <= len(did) <= 58
    recovered = agent.public_key_from_did(did)
    assert recovered.public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    ) == pk.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )


def test_real_did_pubkey_vector():
    pubkey = agent.public_key_bytes_from_did(REAL_DID)
    assert pubkey.hex() == REAL_PUBKEY_HEX
    assert len(pubkey) == 32


def test_ss58_derivation_real_vector():
    assert agent.ss58_address_from_did(REAL_DID) == REAL_SS58
    pubkey = bytes.fromhex(REAL_PUBKEY_HEX)
    assert agent.ss58_address_from_public_key(pubkey) == REAL_SS58


def test_ss58_address_format():
    address = agent.ss58_address_from_did(REAL_DID)
    assert address.startswith("5")
    assert len(address) == 48
    assert address == REAL_SS58


def test_did_note_fingerprint_real_vector():
    info = agent.did_note_fingerprint(REAL_DID)
    assert info["fingerprint"] == REAL_FINGERPRINT
    assert info["shard"] == "10"
    assert info["key"] == "cbf746385504cf"
    assert info["did"] == REAL_DID
    assert info["url"] == "https://technocore.chat/kv/did-10/cbf746385504cf"
    expected = hashlib.sha256(REAL_DID.encode()).hexdigest()[:16]
    assert info["fingerprint"] == expected


def test_invalid_did_rejected():
    import pytest

    with pytest.raises(agent.ProtocolError):
        agent.public_key_from_did("did:key:zInvalid")
    with pytest.raises(agent.ProtocolError):
        agent.public_key_from_did("not a did")
    with pytest.raises(agent.ProtocolError):
        agent.ss58_address_from_public_key(b"short")


def test_b58_roundtrip():
    data = b"\x00\x00hello world"
    encoded = agent._b58_encode(data)
    assert agent._b58_decode(encoded) == data
    assert agent._b58_encode(b"") == "1"
