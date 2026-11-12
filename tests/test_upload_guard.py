"""Secret guard tests for github_upload.py."""
import subprocess

import pytest

import github_upload as gu


def test_secret_basenames():
    assert gu.is_secret_path("identity.pem") is True
    assert gu.is_secret_path("passphrase.txt") is True
    assert gu.is_secret_path("passphrase_backup.txt") is True
    assert gu.is_secret_path("wallet.json") is True
    assert gu.is_secret_path(".env") is True
    assert gu.is_secret_path("src/main.py") is False
    assert gu.is_secret_path("README.md") is False


def test_secret_suffixes_and_paths():
    assert gu.is_secret_path("key.pem") is True
    assert gu.is_secret_path("id_rsa") is True
    assert gu.is_secret_path("deploy_key") is True
    assert gu.is_secret_path(".aws/credentials") is True
    assert gu.is_secret_path(".ssh/id_ed25519") is True
    assert gu.is_secret_path("notes.txt") is False


def test_guard_refuses_secret_in_folder(tmp_path):
    (tmp_path / "identity.pem").write_text("secret", encoding="utf-8")
    (tmp_path / "agent.py").write_text("print(1)\n", encoding="utf-8")
    with pytest.raises(RuntimeError):
        gu.guard(str(tmp_path))


def test_guard_allows_clean_folder(tmp_path):
    (tmp_path / "agent.py").write_text("print(1)\n", encoding="utf-8")
    gu.guard(str(tmp_path))


def test_guard_refuses_tracked_secret(git_repo):
    secret = git_repo / "identity.pem"
    secret.write_text("secret", encoding="utf-8")
    (git_repo / "agent.py").write_text("print(1)\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add files"], cwd=git_repo, check=True, capture_output=True)
    with pytest.raises(RuntimeError):
        gu.guard(str(git_repo))


def test_git_commit_works_with_local_config(git_repo):
    (git_repo / "agent.py").write_text("print(1)\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=git_repo, check=True, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "add files"], cwd=git_repo, capture_output=True, text=True
    )
    assert result.returncode == 0
    log = subprocess.run(["git", "log", "--oneline"], cwd=git_repo, capture_output=True, text=True, check=True)
    assert "add files" in log.stdout


def test_redact_token():
    token = "testtokenvalue123"
    text = f"failed with {token} and https://x-access-token:{token}@github.com/x/y.git"
    redacted = gu._redact(text, token)
    assert token not in redacted
    assert "***REDACTED***" in redacted
