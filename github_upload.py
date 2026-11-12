#!/usr/bin/env python3
"""GitHub upload helper for Technocore Alpha contributions.

Create a public or private repository, upload the current directory, and
print the repo URL and the latest commit hash. The result is ready for a
signed contribution proof.

The helper refuses to stage secret files, and it never embeds a token in
a remote URL. A token lives only in a child process environment for one
push, and the remote is always restored to the clean URL.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"

SECRET_BASENAMES = frozenset({
    "identity.pem",
    ".env",
    ".git-credentials",
    "hosts.yml",
    "credentials",
    "token.txt",
    "github_token.txt",
    "seed.txt",
    "seedphrase.txt",
    "deploy_key",
    "deploy_key.pem",
    ".npmrc",
    ".pypirc",
    ".netrc",
    "wallet.json",
    "keystore.json",
})
SECRET_BASENAME_PREFIXES = (
    "passphrase",
    "id_rsa",
    "id_ed25519",
    "id_ecdsa",
    "id_ed448",
    ".env.",
)
SECRET_SUFFIXES = (".pem", ".key", ".token", ".p12", ".pfx")
SECRET_PATH_PARTS = frozenset({".aws", ".ssh", ".gnupg"})
SECRET_WORD_SUFFIXES = (".txt", ".json", ".yaml", ".yml", ".ini", ".cfg")
TEMPLATE_SUFFIXES = (
    ".example", ".sample", ".template", ".tmpl", ".dist", ".defaults",
)
PUBLIC_SUFFIXES = (".pub", ".example", ".sample", ".template", ".dist")

PROTECTIVE_GITIGNORE = """# added by github_upload.py: never commit secrets
identity.pem
*.pem
*.key
passphrase*
*.secret
*secret*.txt
*secret*.json
id_rsa*
id_ed25519*
id_ecdsa*
id_ed448*
*.token
*token*.txt
.p12
.pfx
.npmrc
.pypirc
.netrc
wallet.json
keystore.json
seed.txt
seedphrase.txt
deploy_key
.env
.env.*
credentials
credentials*
.aws/
.ssh/
"""


def is_secret_path(path: str) -> bool:
    name = os.path.basename(path)
    lower = name.lower()
    if name in SECRET_BASENAMES:
        return True
    if any(lower.startswith(prefix) for prefix in SECRET_BASENAME_PREFIXES):
        return True
    if any(lower.endswith(suffix) for suffix in SECRET_SUFFIXES):
        return True
    parts = set(path.split(os.sep))
    if parts & SECRET_PATH_PARTS:
        return True
    if ("secret" in lower or "token" in lower) and lower.endswith(SECRET_WORD_SUFFIXES):
        if not any(lower.endswith(suffix) for suffix in TEMPLATE_SUFFIXES):
            return True
    if any(lower.endswith(suffix) for suffix in PUBLIC_SUFFIXES):
        return False
    return False


def ensure_protective_gitignore(workdir: str) -> None:
    path = os.path.join(workdir, ".gitignore")
    existing = ""
    if os.path.exists(path):
        existing = open(path, encoding="utf-8").read()
    if "added by github_upload.py" not in existing:
        with open(path, "a", encoding="utf-8") as f:
            f.write(PROTECTIVE_GITIGNORE)


def tracked_secrets(workdir: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=workdir, capture_output=True, text=True, check=False
    )
    found = []
    for line in result.stdout.splitlines():
        if is_secret_path(line.strip()):
            found.append(line.strip())
    return found


def scan_workdir(workdir: str) -> list[str]:
    found = []
    for root, dirs, files in os.walk(workdir):
        if ".git" in root.split(os.sep):
            continue
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            rel = os.path.relpath(os.path.join(root, name), workdir)
            if is_secret_path(rel):
                found.append(rel)
    return found


def guard(workdir: str) -> None:
    tracked = tracked_secrets(workdir)
    if tracked:
        raise RuntimeError(
            "refusing to upload: secret file or files already tracked in git: "
            + ", ".join(tracked)
        )
    present = scan_workdir(workdir)
    if present:
        raise RuntimeError(
            "refusing to upload: secret file or files in upload folder: "
            + ", ".join(present)
            + ". Move them out of this folder and try again"
        )


def run(cmd: list[str], check: bool = True, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check, cwd=cwd)


def _redact(text: str, token: str | None = None) -> str:
    text = re.sub(r"https://x-access-token:[^@\s]+@", "https://x-access-token:***@", text)
    text = re.sub(r"https://[^:\s]+:[^@\s]+@github\.com", "https://***@github.com", text)
    if token:
        text = text.replace(token, "***REDACTED***")
    return text


def token_username(token: str) -> str:
    req = urllib.request.Request(API + "/user", headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": "technocorealpha",
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        import json

        return json.loads(resp.read().decode("utf-8"))["login"]


def create_repo_api(token: str, name: str, private: bool, description: str) -> str:
    import json

    body = json.dumps({
        "name": name, "private": private, "description": description,
    }).encode()
    req = urllib.request.Request(API + "/user/repos", data=body, method="POST", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "technocorealpha",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))["full_name"]
    except urllib.error.HTTPError as e:
        detail = e.read(300).decode("utf-8", errors="replace")
        raise RuntimeError(f"repo create failed: HTTP {e.code}: {detail}")


def _push_with_askpass(workdir: str, branch: str, token: str) -> None:
    script = os.path.join(workdir, ".git", "askpass.py")
    with open(script, "w", encoding="utf-8") as f:
        f.write("import os\nprint(os.environ.get('GH_ASKPASS_TOKEN', ''))\n")
    env = dict(os.environ)
    env["GH_ASKPASS_TOKEN"] = token
    env["GIT_ASKPASS"] = script
    try:
        subprocess.run(
            ["git", "push", "-u", "origin", branch],
            cwd=workdir, check=True, capture_output=True, text=True, env=env,
        )
    finally:
        if "GH_ASKPASS_TOKEN" in env:
            del env["GH_ASKPASS_TOKEN"]
        try:
            os.remove(script)
        except OSError:
            pass


def push_with_token(token: str, repo_full: str, name: str, branch: str, workdir: str) -> str:
    clean_url = f"https://github.com/{repo_full}.git"
    subprocess.run(["git", "remote", "remove", "origin"], cwd=workdir, check=False, capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", clean_url], cwd=workdir, check=True, capture_output=True)
    try:
        _push_with_askpass(workdir, branch, token)
    finally:
        subprocess.run(["git", "remote", "set-url", "origin", clean_url], cwd=workdir, check=False, capture_output=True)
    result = run(["git", "remote", "-v"], cwd=workdir, check=False)
    if token in result.stdout or "x-access-token" in result.stdout:
        raise RuntimeError("refusing to leave a token in the git remote URL")
    result = run(["git", "rev-parse", "HEAD"], cwd=workdir)
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload a Technocore Alpha contribution to GitHub.")
    parser.add_argument("name", help="repository name")
    parser.add_argument("--public", action="store_true", help="create a public repository")
    parser.add_argument("--private", action="store_true", help="create a private repository")
    parser.add_argument("--dir", default=".", help="directory to upload")
    parser.add_argument("--branch", default="main", help="branch name")
    parser.add_argument("--description", default="Technocore Alpha contribution", help="repository description")
    args = parser.parse_args()
    workdir = os.path.abspath(args.dir)
    token = os.environ.get("GITHUB_TOKEN", "")
    try:
        ensure_protective_gitignore(workdir)
        guard(workdir)
        if not os.path.exists(os.path.join(workdir, ".git")):
            subprocess.run(["git", "init", "-b", args.branch], cwd=workdir, check=True, capture_output=True)
        subprocess.run(["git", "add", "-A"], cwd=workdir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"Technocore Alpha contribution: {args.name}"],
            cwd=workdir, check=True, capture_output=True,
        )
        if token:
            username = token_username(token)
            full = create_repo_api(token, args.name, bool(args.private), args.description)
            commit = push_with_token(token, full, args.name, args.branch, workdir)
            print(f"repo: https://github.com/{full}")
            print(f"commit: {commit}")
        else:
            result = run(["git", "rev-parse", "HEAD"], cwd=workdir)
            print("local commit ready. Set GITHUB_TOKEN or use gh auth login to push.")
            print(f"commit: {result.stdout.strip()}")
        return 0
    except Exception as e:
        print(f"error: {_redact(str(e), token)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
