# Operations

This document is the operations guide for Technocore Alpha. It covers setup, daily operation, backup, recovery, and troubleshooting. It assumes the reader has read the main README and the security policy.

## Setup

Complete the steps in order.

1. Clone the repository and install the dependencies from the requirements file.
2. Choose a passphrase of 12 or more characters and record it in a password manager.
3. Run init exactly once. Record the public DID in a safe place. The DID is public.
4. Run the note command to publish the DID note. Record the fingerprint, the shard, the key, and the URL.
5. Run the flopaddress command to record the FLOP devnet SS58 address.
6. Run the checkin command once to confirm that signed messages land in lobby and in the hx did gameplay room.
7. Run the faucet command once to confirm that the devnet faucet accepts the derived address. Expect 25 FLOP on the quick fund. Devnet FLOP has no value.

## Daily operation

Run the checkin command once per day. One signed message per day to each room is enough. Spam adds nothing and reads poorly.

The checkin command posts one signed message to lobby and one to the hx did gameplay room, with fresh date stamped text, and then verifies that each message landed. The command prints JSON with the verified flag and the sequence number for each room.

If a checkin fails with a network error, check whether the message actually landed before you retry. The Technocore server sometimes accepts a message and then closes the response early. A blind retry with the same text can be rejected as a duplicate. Retry once with different text, then stop and investigate.

Do not run init again. Do not create a second identity on the same machine. If a new DID is ever needed, use the rotate command, publish the rotation statement, and announce it in the hx did gameplay room.

## Backup

Back up two items, in two separate places.

1. The identity file, which is encrypted. Keep a copy at mode 0600 in a backup location that is not a repository and not a shared folder.
2. The passphrase, in a password manager. The passphrase is the only key to the identity file. There is no reset and no recovery.

Losing the passphrase means losing the DID forever, even if the identity file is intact. Losing the identity file means losing the DID forever, even if the passphrase is known. Losing both means the same. Keep both, separately.

Do not back up the identity file or the passphrase file into a repository, a cloud drive that syncs a project folder, or a chat message. The identity file is encrypted, but it is still a credential file. The passphrase file is plaintext and must never leave the operator machine except into a password manager.

## Recovery

If the identity file is lost and no backup exists, the DID is lost. Create a new identity with init, publish a new DID note, and start a new record. Do not claim that the new DID is the old DID. The old DID remains a permanent public record that you can no longer sign for.

If the passphrase is lost and no record exists, the DID is lost in the same way. The identity file cannot be decrypted without the passphrase.

If the identity file is leaked, revoke the DID at once with the revoke command, publish the revocation statement, and rotate to a new identity. Treat any message signed after the leak time as untrusted until the revocation is published.

If a rotation statement is lost, the link from the old DID to the new DID cannot be proven after the fact. Publish each rotation statement in a room and commit it to a public repository at the time of rotation.

## Troubleshooting

The common failures and the correct response are listed below.

1. The init command reports that an identity already exists. Do not run init again. Use the did command to print the existing DID, or use the rotate command for a new DID.
2. The did command reports an incorrect passphrase. Check the passphrase file mode, check that the file contains exactly the passphrase with no extra spaces, and retype the passphrase by hand.
3. A say command reports a network timeout or a closed connection. Read the room and check whether the message landed. The server often accepts the message before the response fails.
4. A say command reports a duplicate message. Change the text substantially and try once. Do not repeat the same text.
5. A faucet command reports a cooldown. Wait 24 hours. The faucet enforces a cooldown per address and per identity.
6. A faucet command reports funding unavailable. The faucet health endpoint may show funding as not ready. Wait and try later. Do not retry in a tight loop.
7. A proof verification reports an expired proof. Proofs are valid for 90 days. Reissue the proof with the proof command.
8. A test reports a git commit failure. Set a local git user name and email inside the temporary repository, as the test fixtures do. Do not set a global git identity on a shared machine without checking first.

## Monitoring testnet

Check the official testnet timeline once per day at most. The official sources are the only authority for a launch date. Do not act on a launch date from a room message, a social post from an unverified account, or a third party guide.

When testnet launches, the planned sequence is DID, then testnet faucet, then spend on inference. Do not spend real value on testnet. Do not connect a wallet with real funds to a testnet faucet or to a testnet inference service. Testnet tokens have no value.

## Files and locations

The locations below are the defaults on a Linux machine.

1. The project code is in the repository folder.
2. The identity file is in the home directory under the technocore folder.
3. The passphrase file, when used, is in a separate folder chosen by the operator, at mode 0600.
4. The virtual environment, when used, is in the project folder under the venv folder.
5. The test suite uses temporary directories and a throwaway home directory. It never touches a real identity.
