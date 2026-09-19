# Deployment evidence and verification status

Target: stable Studionet, chain ID **61999**, RPC `https://studio.genlayer.com/api`.

The IntentClearing contract and the start of a market lifecycle have been verified on stable Studionet. The complete requested lifecycle has not yet been run.

## Local verification performed

- `python scripts/preflight.py` — PASS.
- `python -m compileall -q contracts tests` — PASS.
- `python -m pytest tests/unit -q` — PASS, 8 tests.
- `python -m pytest tests/direct -q` — PASS, 26 tests using `genlayer-test 0.29.2`.
- `requirements-test.txt` pins `genlayer-testing-suite` v0.29.2. The installed package is v0.29.2; it was not upgraded to preview tooling.

## Stable Studionet verification

The CLI reported alias `studionet`, chain ID `61999`, RPC `https://studio.genlayer.com/api` immediately before deployment and the market writes. The CLI currently names `https://genlayer-explorer.vercel.app` as its explorer; the project’s required explorer is `https://explorer-studio.genlayer.com`.

The read-only account query succeeded for the selected, unlocked account and reported 100 GEN. The following transactions were accepted by consensus and later reported `FINALIZED` by `genlayer receipt`:

- IntentClearing deployment: `0xb9f29a54ba42e6ee4b14a468cdc1c6327c3c132d017912c8e1c8d43c430f6931`; address `0x949ddCdf53DDbF0931eCcd37dde0De50EF787376`.
- Market 1 creation: `0x652fdf6d0b9bd995719fe4243a893eda1e88bd98f965264d61f9848a40df4a0c`.
- First attribute (`UPGRADEABLE`): `0xc65dff5e4a593690605a53a9f304308380a9d1c4dd57e550f6afe758488c0a8e`.

The market read after creation confirmed ID 1 and the intended name/semantics. Attribute 1 was finalized. No definition hash, epoch, orders, semantic assessments, clearing result, fills, settlement root, or ClearingGate deployment have been produced yet.

The command `genlayer estimate-fees --json` failed with `TypeError: client.estimateTransactionFees is not a function`. The CLI’s normal `deploy` and first `write` commands nevertheless returned accepted transactions that finalized; no explicit `--fees` or `--fee-value` override was supplied. The next `add_attribute` command prompted for a keystore decryption password and returned no transaction hash. Do not report it as submitted.

## Repository delivery status

The dedicated public repository [BeatyXO/IntentClearing](https://github.com/BeatyXO/IntentClearing) was created after verifying that `BeatyXO/Corroborate` is a separate repository on `master`. GitHub reports the IntentClearing configured initial branch as `main`. Local commit `5dec3b354fed3d6c44fa2503d1d5f0a931929f64` contains the implementation. Push was rejected because the authenticated BeatyXO OAuth token lacks the `workflow` scope needed to publish `.github/workflows/ci.yml`. A GitHub device authorization request for that scope is waiting for account approval. No changes have been made to Corroborate.

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
