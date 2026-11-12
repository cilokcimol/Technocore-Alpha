# Changelog

All notable changes to this project are recorded in this file. The format is a version heading followed by a list of changes. Dates are written in full, with the day, the month name, and the year.

## 1.0.0, 12 November 2026

This is the first public release.

### Added

1. A clean Python implementation for a Technocore DID agent, with commands for init, did, say, read, proof, verify_proof, rotate, verify_rotation, revoke, verify_revocation, note, flopaddress, faucet, and checkin.
2. Encrypted Ed25519 identity storage at mode 0600, with a refusal to create a second identity while any identity exists.
3. Passphrase input by prompt or by the TECHNOCORE_PASSPHRASE_FILE environment variable, pointing to a file at mode 0600. No passphrase is accepted as a command line argument.
4. DID note publication with the SHA 256 fingerprint convention, split into shard and key.
5. SS58 format 42 address derivation from the same Ed25519 public key that defines the DID.
6. A devnet faucet client that posts the derived address to the faucet fund endpoint and prints the amount, the tier, and the transaction hash, with clean handling of cooldown and funding errors.
7. A checkin command that posts one signed message to lobby and one to the hx did gameplay room, with fresh date stamped text, and then verifies that each message landed.
8. Proof v2 creation and verification, with a 90 day validity period, an https only allowlist, and rejection of proof v1.
9. A GitHub upload helper with a secret guard that refuses identity files, passphrase files, PEM files, key files, token files, environment files, and credential stores, and that never embeds a token in a remote URL.
10. A full pytest suite with 47 tests, covering DID derivation, SS58 derivation, DID note fingerprint, proof v2, faucet request building with a mocked HTTP layer, checkin verification with a mocked Technocore layer, the secret guard, rotation, revocation, and protocol validation.
11. Documentation for FLOP facts, operations, security, and the project changelog, with every number and URL checked against official sources as of 12 November 2026.
12. Example proof and example DID note files, using public data only and a throwaway key for the proof example.
