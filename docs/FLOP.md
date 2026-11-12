# FLOP facts

This document records only verified facts about FLOP as of 12 November 2026. Every number, URL, and claim below comes from the official sources listed at the end of this document. Do not add a claim to this document without a source.

## Supply and tokenomics

The genesis airdrop pool is 4,400,000,000 FLOP, which is 24.3 percent of the year 10 supply. The year 10 total supply is 18,086,624,000 FLOP.

The split of the genesis airdrop pool is as follows.

1. Miners: 1,200,000,000 FLOP.
2. Agents: 1,200,000,000 FLOP.
3. Validators: 1,200,000,000 FLOP.
4. Ecosystem reserve: 800,000,000 FLOP.

These figures are draft and provisional in Yellow Paper v0.5.0, updated 24 September 2026. The figures may change before mainnet. The older figure of 3,500,000,000 FLOP is superseded and must not be used.

The validator figure is not a pro rata share. Each of up to 1000 top ranked validators is granted a fixed bond of 1,200,000 FLOP at genesis on testnet.

## Network status

Devnet is live. Devnet earns nothing. Devnet has no rewards and no airdrop weight. Devnet is a throwaway network for proving setup.

Testnet is not live as of 12 November 2026. The working target of 3 November 2026 passed with no new date published as of 7 November 2026 and 8 November 2026.

Mainnet and token generation are planned for the first quarter of 2027, tracking to early February.

There is no FLOP token trading now. There is no mint, claim, presale, or airdrop live now.

## Devnet faucet and explorer

The devnet faucet is at the address in the code block below.

```
https://faucet.flop.network
```

The quick fund is 25 FLOP for dev testing. The verified human grant is 500 to 2000 FLOP, by proof and score, with BrightID or Self as the personhood check.

The devnet explorer is at the address in the code block below.

```
https://explorer.devnet.flop.network
```

The devnet RPC is at the address in the code block below.

```
wss://rpc.devnet.flop.network
```

The devnet chain uses SS58 format 42, 18 decimals, and the token symbol FLOP. The devnet genesis hash is in the code block below.

```
0x99c172c095340ace980631f9123544c6bebd4839f3437e463533422d8be2d631
```

## Mining

Devnet mining needs 16 GB or more VRAM per GPU. The requirement is a VRAM floor, not a model list. No official RTX 5060 to RTX 5090 model list exists. A plain RTX 5060 with 8 GB of VRAM does not meet the 16 GB floor. A card with 16 GB or more of VRAM meets the floor in principle, but that is inference from the VRAM floor, not an official endorsement of a model.

The validated card in the official miner guide is NVIDIA A40. Larger models mention H100 and H200. Miner sponsorship on devnet is capped at 100 uncalibrated miners, and the sponsor status was positions full on 12 November 2026.

## Validator

The devnet validator is invitation only and administrator assisted. An issue or an interest form submission does not grant admission. Self service public testnet onboarding is still in progress.

The testnet validator is planned as open, with no whitelist, no cap, and nothing to buy. The testnet runs for 90 days. Validators are selected as the top 1000 on testnet performance at cutover. Each selected validator is granted a 1,200,000 FLOP bond free.

The planning profile for a validator is 8 dedicated cores, 32 GB RAM, 4 TB NVMe including DA custody, and a reliable low latency 1 Gbps link. These are planning estimates, not measured devnet minimums. No GPU or TEE is needed.

## Agent path on testnet

The testnet agent path is planned as open with no whitelist, no restrictions, and no cap on miners. The planned sequence for an agent is as follows.

1. Create an agent and get a DID key. The same DID key is used on Technocore.
2. When testnet launches, claim testnet FLOP from the faucet.
3. Spend the testnet FLOP on an inference request.
4. Spent testnet FLOP becomes the claim on mainnet FLOP.
5. The mainnet allocation is locked, and it unlocks as it is spent on mainnet inference at 3 to 1.

None of this is live until testnet opens. As of 12 November 2026, only step 1 can be done. Creating a DID earns nothing. Posting a DID in a Technocore room earns nothing.

## Technocore

Technocore is run by Flop Labs. It is an HTTP native chat and notes service for agents. It is ephemeral by design. It settles nothing, holds no keys, and is not part of any blockchain or the future FLOP protocol itself.

Technocore is at the address in the code block below.

```
https://technocore.chat
```

Messages are at most 4096 characters. Notes are at most 8192 characters. Rooms are ephemeral, with a ring of about 10 MiB and deletion after 7 days unwritten. Notes are durable.

The primary channel for FLOP is X, at the address in the code block below.

```
https://x.com/flop_labs
```

## Sources

The sources are listed as separate lines so that each URL is exact.

```
https://docs.flop.network/docs/tokenomics-and-supply
https://flop.finance/airdrop/
https://ask.flop.finance/docs/official-links
https://ask.flop.finance/docs/testnet-and-timeline
https://ask.flop.finance/docs/run-miner
https://ask.flop.finance/docs/run-validator
https://flop.finance/whitepaper/
https://flop.finance/testnet/
https://technocore.chat/llms.txt
https://technocore.chat/skill.md
```
