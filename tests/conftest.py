"""Shared fixtures for Technocore Alpha tests.

All identities in this suite are throwaway keys in temporary directories.
No test touches a real identity, a real passphrase file, or a live network.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import agent


@pytest.fixture
def passphrase():
    import secrets

    return secrets.token_hex(16)


@pytest.fixture
def key_path(tmp_path, passphrase):
    path = tmp_path / "identity.pem"
    agent.create_identity(path=path, passphrase=passphrase)
    return path


@pytest.fixture
def loaded_key(key_path, passphrase):
    return agent.load_identity(path=key_path, passphrase=passphrase)


@pytest.fixture
def passphrase_file(tmp_path, passphrase):
    path = tmp_path / "passphrase.txt"
    path.write_text(passphrase + "\n", encoding="utf-8")
    path.chmod(0o600)
    return path


@pytest.fixture
def git_repo(tmp_path):
    import subprocess

    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True, capture_output=True)
    return repo
