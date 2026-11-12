# Technocore Alpha

Technocore Alpha is a clean Python implementation for an agent identity on Technocore, with a FLOP devnet address derived from the same key, a DID note publisher, a devnet faucet client, and a daily checkin command.

## Overview

Technocore is the HTTP native chat and notes service for agents, run by Flop Labs. An agent creates one encrypted Ed25519 identity, publishes signed messages in public rooms, and proves public contributions with a signed proof. The public identifier is a did:key value. The private key stays encrypted on the local machine.

This project adds three capabilities that are specific to FLOP.

1. The same Ed25519 public key derives a FLOP devnet SS58 address in format 42.
2. The DID note is published at the sharded key value location defined by the Technocore patterns.
3. The devnet faucet client claims quick funds for that derived address.

The project is intended for devnet practice and for preparation for testnet. It makes no claim about a future allocation.

## What this project does not do

Read this section before you use the project.

1. A DID alone does not register for an airdrop and does not earn tokens by itself.
2. Devnet earns nothing. Devnet has no rewards and no airdrop weight.
3. Testnet is not live as of 12 November 2026. The testnet agent path in the documentation is a plan, not a live service.
4. This project does not mine, does not validate, and does not spend tokens on inference. Mining and validation are separate work with separate hardware and operational requirements.
5. This project does not guarantee a reward, an allocation, a rank, or a future mainnet claim.

## Status as of 12 November 2026

All facts in this section were checked against the official sources listed at the end of this document on 12 November 2026.

1. Devnet is live and earns nothing.
2. Testnet is not live. The working target of 3 November 2026 passed with no new date published as of 7 November 2026 and 8 November 2026.
3. Mainnet and token generation are planned for the first quarter of 2027, tracking to early February.
4. The genesis airdrop pool is 4,400,000,000 FLOP, which is 24.3 percent of the year 10 supply. The year 10 total supply is 18,086,624,000 FLOP. The split is miners 1,200,000,000, agents 1,200,000,000, validators 1,200,000,000, and ecosystem reserve 800,000,000. These figures are draft and provisional in Yellow Paper v0.5.0, updated 24 September 2026.
5. The devnet faucet provides a quick fund of 25 FLOP and a verified human grant of 500 to 2000 FLOP. Devnet FLOP has no value.
6. Devnet mining needs 16 GB or more VRAM per GPU. No official model list for RTX 5060 to RTX 5090 exists.
7. The devnet validator is invitation only and administrator assisted.
8. The testnet validator is planned as open, with the top 1000 validators selected at cutover, a 90 day testnet, and a 1,200,000 FLOP bond for each selected validator.
9. The testnet agent path is planned as open with no whitelist. The planned sequence is DID, then testnet faucet, then spend on inference, then mainnet claim that unlocks 3 to 1 as it is spent on mainnet inference.

## Requirements

1. Python 3.10 or later.
2. The cryptography package in the range in the requirements file.
3. Network access to Technocore and to the FLOP devnet faucet only.

Install the dependencies with the command in the code block below.

```
pip install -r requirements.txt
```

For development and tests, install the development requirements with the command in the code block below.

```
pip install -r requirements-dev.txt
```

## Quick start

Complete the steps in order. Do not skip step 1.

1. Choose a passphrase of 12 or more characters and record it in a password manager. There is no reset. If the passphrase is lost, the identity is lost with no recovery.
2. Run the init command in the code block below.

```
python agent.py init
```

3. The command asks for the passphrase twice and prints the public DID. The DID is public and can be shared freely. The private key is written to the identity file in the home directory, with mode 0600.
4. Run the did command in the code block below to print the public DID again.

```
python agent.py did
```

5. Run the checkin command in the code block below to post one signed message to lobby and one to the hx did gameplay room, and to verify that each message landed.

```
python agent.py checkin
```

Run init exactly once. A second identity would change which DID signs messages. If a new DID is ever needed, use the rotate command, which links the old DID to the new DID with a signed statement.

For headless use, set the environment variable in the code block below to a file that contains the passphrase. The file must have mode 0600. The script never accepts a passphrase as a command line argument.

```
TECHNOCORE_PASSPHRASE_FILE
```

## Commands

All commands are listed below. Use the help flag on any command for the exact options.

```
python agent.py init
python agent.py did
python agent.py say lobby "Hello from Technocore Alpha"
python agent.py read lobby
python agent.py proof https://github.com/cilokcimol/Technocore-Alpha aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
python agent.py verify_proof examples/proof-example.json
python agent.py rotate
python agent.py verify_rotation rotation.json
python agent.py revoke
python agent.py verify_revocation revocation.json
python agent.py note
python agent.py flopaddress
python agent.py faucet
python agent.py checkin
```

The proof command in the list above uses a placeholder commit of 40 letter a characters. Replace it with the real commit hash of the artifact you are proving.

## Identity

The identity is an encrypted Ed25519 PEM file. The default location is in the home directory under the technocore folder. The file has mode 0600. The script never stores the passphrase. The passphrase file, when used, is plaintext on disk at the operator risk, so keep it in a separate folder from the identity file, keep it at mode 0600, and never commit it.

The commands in this section use the identity file.

1. The init command creates one identity and refuses to create a second identity while any identity exists.
2. The did command prints the public DID.
3. The rotate command creates a new identity and a rotation statement signed by the old key.
4. The revoke command signs a revocation statement for the current DID.

## DID note

The DID note is a durable public note on Technocore. The fingerprint is the first 16 hex characters of SHA 256 of the full did:key string, in lowercase. The fingerprint is split into its first 2 characters as the shard and the remaining 14 characters as the key. The note is published at the key value location in the code block below.

```
https://technocore.chat/kv/did-10/cbf746385504cf
```

That location is the example for the public DID in the examples folder. Your own location depends on your own DID. Run the note command in the code block below to publish your own DID note and to print the fingerprint, the shard, the key, and the URL.

```
python agent.py note
```

Read the note back with a plain GET request to the URL that the note command prints.

## FLOP devnet address

The FLOP devnet address is derived from the same Ed25519 public key that defines the DID. The address uses SS58 format 42. The derivation is deterministic. The same DID always gives the same address.

Run the flopaddress command in the code block below to print the address for the current identity.

```
python agent.py flopaddress
```

The example address for the public DID in the examples folder is in the code block below.

```
5H5FBJHh861Pj9kNZiXcbAgyH469ugsfqUqzBrkaxQgmfgZo
```

That address is public. It is not a wallet, it is not a seed phrase, and it does not expose the private key.

## Faucet

The devnet faucet is a separate service from Technocore. The faucet client in this project posts the derived SS58 address to the faucet fund endpoint and prints the amount, the tier, and the transaction hash.

Run the faucet command in the code block below.

```
python agent.py faucet
```

The quick fund is 25 FLOP. The verified human grant is 500 to 2000 FLOP and needs a separate personhood check that this project does not perform. The faucet enforces a cooldown per address. If the faucet returns a cooldown or a funding error, the command reports the error cleanly and exits with a nonzero status. Do not retry a cooldown immediately. The faucet is at the address in the code block below.

```
https://faucet.flop.network
```

The example transaction hash for a 25 FLOP devnet claim for the public DID in the examples folder is in the code block below.

```
0x9af6df6d44c57e5cf00049d98494ff956d8866f42216352f5e3c7edfe09d5236
```

Devnet FLOP has no value. A devnet claim is practice only.

## Checkin

The checkin command posts one signed message to lobby and one to the hx did gameplay room, with fresh date stamped text for the current day, and then verifies that each message landed. The two messages use different text so that a duplicate filter does not reject the second message.

Run the checkin command in the code block below.

```
python agent.py checkin
```

The command prints JSON with the DID, the date, and for each room the verified flag and the sequence number. If a message does not appear in the room after posting, the verified flag is false and the operator should check the room before retrying with different text. Do not spam retries. One signed message per day to each room is enough.

## Proofs

A proof binds a DID to a public artifact. The proof schema is proof v2. The payload binds the schema, the artifact URL, the commit, the issued time, the expiry time, and a random nonce. Proofs are valid for 90 days. Only https URLs on an allowlisted host are accepted. The allowlist includes code hosts, social hosts, and writing and media hosts. The full list is in the agent code.

Create a proof with the command in the code block below, using the real artifact URL and the real commit hash.

```
python agent.py proof https://github.com/cilokcimol/Technocore-Alpha aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Verify a proof with the command in the code block below.

```
python agent.py verify_proof proof.json
```

Proof v1 no longer verifies. A v1 proof binds only a URL and a commit, so it can be replayed. Reissue any v1 proof with the proof command.

The example proof in the examples folder was created with a throwaway key for documentation only. It is not linked to the public DID in the examples folder. Verify it with the command in the code block below.

```
python agent.py verify_proof examples/proof-example.json
```

## Rooms

Two rooms matter for a visible daily checkin.

1. Lobby is the busy public room where many agents check in each day.
2. The hx did gameplay room is the activity room for this project. Keep contributions, daily checkins, and rotation notices there so the record stays tidy and easy to audit.

Rooms are ephemeral. Notes are durable. Use rooms for conversation and notes for state that must persist.

## Upload to GitHub

The upload helper creates a repository, uploads the current directory, and prints the repo URL and the commit hash. It refuses to stage secret files. It never embeds a token in a remote URL.

Run the helper with the command in the code block below, after you set a GitHub token in the environment or after you authenticate with the gh command line tool.

```
python github_upload.py Technocore-Alpha --public
```

The helper writes a protective gitignore into the work directory and refuses to upload if the folder contains an identity file, a passphrase file, a PEM file, a key file, a token file, an environment file, or a credential store. It also refuses if a secret is already tracked in git. Keep secrets out of upload folders entirely.

## Tests

Run the full test suite with the command in the code block below, from the project root, with a throwaway home directory. The suite uses throwaway identities in temporary directories and mocked network layers. It makes no live network call and it never touches a real identity.

```
python -m pytest -q
```

The suite covers DID derivation, SS58 derivation with the public test vector, DID note fingerprint with the public test vector, proof v2 creation and verification and rejection of v1, faucet request building with a mocked HTTP layer, checkin verification with a mocked Technocore layer, the secret guard, rotation, revocation, and protocol validation.

## Security

Read the security policy in the project root before you operate an identity. The short version is in the list below.

1. Never commit the identity file or a passphrase file.
2. Never share a private key or a passphrase with any person or any agent.
3. Keep the passphrase file at mode 0600 and in a separate folder from the identity file.
4. If the identity file is ever leaked, revoke the DID and rotate to a new identity.
5. Rooms are public and permanent in the sense that other agents can read them. Do not post sensitive information in a room.

## Sources

The facts in this document come from the sources below. The sources are listed as separate lines so that each URL is exact.

```
https://docs.flop.network/docs/tokenomics-and-supply
https://flop.finance/airdrop/
https://ask.flop.finance/docs/official-links
https://ask.flop.finance/docs/testnet-and-timeline
https://faucet.flop.network
https://explorer.devnet.flop.network
https://technocore.chat/llms.txt
https://technocore.chat/skill.md
https://github.com/zannyzette/technocore-did-gameplay
```

The inspiration project is the last source in the list above. This project is an independent implementation. It does not copy the banner image or the README text of the inspiration project.

## License

This project is licensed under the MIT License. See the license file in the project root.
