# Deployment evidence and verification status

Target: stable Studionet, chain ID **61999**, RPC `https://studio.genlayer.com/api`.

No deployment or lifecycle evidence has been produced. No address, transaction, or hash is claimed.

## Local verification performed

- `python scripts/preflight.py` — PASS.
- `python -m compileall -q contracts tests` — PASS.
- `python -m pytest tests/unit -q` — PASS, 8 tests.
- `python -m pytest tests/direct -q` — PASS, 26 tests using `genlayer-test 0.29.2`.
- `requirements-test.txt` pins `genlayer-testing-suite` v0.29.2. The installed package is v0.29.2; it was not upgraded to preview tooling.

## Stable Studionet verification

Read-only CLI network configuration reported alias `studionet`, chain ID `61999`, RPC `https://studio.genlayer.com/api`. The configured explorer reported by the CLI is `https://genlayer-explorer.vercel.app`; the project reference explorer remains `https://explorer-studio.genlayer.com`.

No live deployment or writes were attempted. The read-only balance lookup for both the active CLI account and a previously generated fresh account failed with `GenLayer RPC error (eth_getBalance): fetch failed`. Signing and funding readiness could not be established. No live lifecycle evidence exists.

## Repository delivery status

The dedicated public repository [BeatyXO/IntentClearing](https://github.com/BeatyXO/IntentClearing) was created after verifying that `BeatyXO/Corroborate` is a separate repository on `master`. GitHub reports the new IntentClearing repository's configured initial branch as `main` and its repository as empty. The local initial implementation commit is `2a01a595ddeddf328822de38a790ddc5e78913c3`; push, post-push inspection, and CI are pending. No changes have been made to Corroborate.

## Required final evidence

- IntentClearing address + deployment tx
- ClearingGate address + deployment tx
- sealed market ID + definition hash
- epoch ID + epoch hash
- request and offer submission txs
- semantic assessment txs demonstrating real consensus
- deterministic clearing tx
- fill ID/hash + settlement root
- successful correctly pinned ClearingGate consumption tx
- wrong-market-hash rejection
- wrong-epoch-hash rejection
- non-party rejection
- replay rejection
- exact test commands and real pass counts
- final Git commit SHA
