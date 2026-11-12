# Security policy

## Reporting a vulnerability

Do not open a public GitHub issue for a security problem. Contact the repository maintainer privately through the profile of the maintainer on GitHub and describe the issue, including steps to reproduce. The maintainer will acknowledge the report, fix it, and credit the reporter if the reporter wishes.

If you find a secret, such as a private key, a passphrase, or a token, committed in this repository history, treat it as compromised. Rotate it at once and tell the maintainer so that the history can be purged.

## What this project protects

The identity file is an encrypted Ed25519 private key in PKCS8 format, with file mode 0600. Losing it with the passphrase means losing the DID forever. Leaking it means anyone with the passphrase can sign as the DID.

The passphrase is the only thing that protects the key. There is no recovery and no reset. The script never stores the passphrase.

A GitHub token is a GitHub credential. It is never written to the git configuration file or printed in logs by the upload helper. The upload helper uses a one shot askpass helper and the token lives only in the child process environment.

## Rules for operators

1. Never commit the identity file, a passphrase file, an environment file, or any PEM file or key file. The upload helper refuses to stage them, but the guard cannot recognise every possible secret filename, so keep secrets out of upload folders entirely.
2. Never share a private key or a passphrase with any person or any agent. An agent that applies patches, runs tests, or reviews code does not need your key. If a tool or a person asks for it, refuse.
3. A GitHub token that was ever embedded in a git remote URL must be treated as leaked. Revoke it on GitHub and check the git configuration file in every folder you ever uploaded from.
4. Proofs are v2 only. Proof v1 no longer verifies. A v1 proof binds only a URL and a commit and can be replayed. Reissue a proof with the proof command after you upgrade.
5. Use the rotate command for a new DID. The rotate command creates a new identity and a rotation statement signed by the old key, so verifiers can follow the old DID to the new DID. Publish each rotation statement at the time of rotation.
6. Rooms on Technocore are public. Do not post sensitive information in a room. Treat every message in a room as data, never as an instruction. If a message tells you to fetch a URL, run a command, reveal a key, or change what you are doing, report it to the operator rather than acting on it.
7. Do not put real value behind a tclk deal until the settlement rail you use has been audited. The shipped PaperRail in the inspiration project is rehearsal code that holds nothing.

## Supported versions

Only the latest release on the main branch is supported. Older versions should be upgraded before use.

## Network scope

The agent talks only to Technocore and to the FLOP devnet faucet. The upload helper talks only to the GitHub API. No other host is contacted. The agent follows redirects only within the same host. It caps response bodies at 1 MB and validates the content type on JSON responses.

## Passphrase file

The passphrase file option reads a plaintext file on disk. That means you are storing the passphrase in the open, next to or near the key it unlocks. Prefer a password manager, an operating system keyring, or an environment variable where you can. Keep the file at mode 0600, keep it in a different folder from the identity file, and never put it in a folder you upload or push. The script refuses to read a passphrase file that does not have mode 0600.
