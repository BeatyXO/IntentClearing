# Deployment evidence and verification status

Target network: stable Studionet (`studionet`), chain ID **61999**, RPC `https://studio.genlayer.com/api`, explorer `https://explorer-studio.genlayer.com`.

## Local verification

- `python scripts/preflight.py` — PASS.
- `python -m compileall -q contracts tests` — PASS.
- `python -m pytest tests/unit -q` — PASS, 8 tests.
- `python -m pytest tests/direct -q` — PASS, 26 tests using the pinned `genlayer-testing-suite` v0.29.2.
- No preview network or preview tooling was used.

## Final IntentClearing lifecycle

The CLI verified alias `studionet`, chain ID `61999`, and RPC `https://studio.genlayer.com/api`. Transactions below were observed finalized with `genlayer receipt`.

| Operation | Result |
|---|---|
| IntentClearing deployment | `0xd8A1F3888C5a15F685a690438436CC6FaA1A3443`; tx `0x6b0add62049529b25249e025eef7f2c14267ee200303aad773f7403c1c91f0b6` |
| Create market 1 | tx `0x5626324d84fee94ce6f28894a120ae88c3a0828861f272d4ec7c09dcb8037d4c` |
| Add `UPGRADEABLE` | tx `0x5b57a7e575b0165d739919adbabd3e8d042957702f65ea365393effd10834cfd` |
| Add `SOLIDITY` | tx `0x6ebe40e7aac5acf8890a5d7677dec7ca7bcf232413083e8cb6c0a4613fd34d18` |
| Add `RUSH` | tx `0x42b0887dc974cb34ac6e435cfe96ff4bec2f2a2a51ae28c1426ef7bba4a12f69` |
| Seal market | tx `0x4819134e4944d7f47d76af53b5433d92d39cf578a215347a6041ebfa42e85881`; `definition_hash` `eb7e859a3899de73f36cf55475021e8c5c69f1fa72975f75ca86c911fb2ed288` |
| Open epoch 1 | tx `0xc9c3919f5746caa68e1fd01387f597c862790a3a52bd57eb2c1576846f5eb591` |
| Submit request 1 (bid 5000) | tx `0xe0e870f93731a4c9b811723279db68c5c13fc5fa84aa9677c9b3a39faacafa87` |
| Submit rush offer 2 (ask 4000) | tx `0x3171b1de57aabc4149955ccbefdd83ed0bfd1a028314c3b8e462868ba5200a9e` |
| Submit non-rush offer 3 (ask 3500) | tx `0x819dc6997d241e3e4be1074af29bebf69e5423376027a750aaf2c1876c9cd391` |
| Consensus assessment, request 1 | tx `0x027d79b3599d3864f558cf0c1445e516314cae8d3e30012a0044d64be6e635`; required mask 3, preferred mask 4, ambiguous mask 0 |
| Consensus assessment, offer 2 | tx `0xba8677b4e43f95cb0ae7fdac4b9356ec1adb05d3b0dd5e4bdcc6965702f2e0c1`; present mask 7, ambiguous mask 0 |
| Consensus assessment, offer 3 | tx `0x1e39fba6a4171c13e0e31a0ea815eabb3b641639e4dd634b2921aaad6ec0786b`; present mask 3, absent mask 4, ambiguous mask 0 |
| Freeze epoch | tx `0xf6b51573c5efafc933baa45dae2204d8a0dc55485b0d708a12da1a7de4851ba8`; `epoch_hash` `2ea89e74623866548d24d2e614688efba7f349e89a65348311cbf33d24433ae5` |
| Deterministic clear | tx `0x5046d4b3c0ef367c12e35c28451a8bd8d62679d673e43582060a0285ce131239`; created one fill; `settlement_root` `c46e4103b2ce75a5b40af5880a4345d9ca17babb386e97e15632d2b1c5aa1e1b` |

Fill 1 maps request 1 to offer 2, quantity 1, ask/trade price 4000, preference score 1. This verifies that the semantically preferred rush offer ranked ahead of the cheaper non-rush offer. Fill hash: `e47e6aeef2af86ae28aca4cce9eff1f1baded7079077ab5651e4eb90a5ff2aa0`.

## ClearingGate evidence

- Deployment: `0x20E26FA22a6163e8c835320028C7ba00231774c6`; tx `0xa652d6be87c3e7fa4fd154671c92e4d2222e727c2221cb74e77d08654ad4f2b2`.
- A fill party consumed the fill with the exact market, epoch, and fill pins: tx `0xc34dd153fb113c58fc47d086f6df9e991b18d377efaec152a5388c6a9984f4f8` finalized. A read-only `is_fill_valid` check with those pins returned true.
- Stable Studionet rejection attempts using valid 64-character digest strings finalized with `leader_receipt.execution_result = ERROR`; follow-up `was_consumed` reads confirmed they did not consume their fresh action hashes:
  - Wrong market: tx `0x370e6595f69aa89b4c4e4f0ddd4d74a1703adb8775d312e2b5bce1836cbb2949`; action `5555…5555` remains unconsumed.
  - Wrong epoch: tx `0x2c5edddc6734f86431e43727f46c7fa9f81148135843bc85ef7a89effec8069b`; action `6666…6666` remains unconsumed.
  - Wrong fill: tx `0xfc499722af92f0f73e733d908caa2fc6eaca723f898b833487f31428ea012198`; action `a888…8888` remains unconsumed.
  - Non-party with exact pins: tx `0x1ea7c377f54de867146b62b1c95e71dc5dd5c32cc7c62f575947c01f35ebc7dd`; action `b999…9999` remains unconsumed.
  - Repeated action: tx `0x3e7805ae0caa419cd9d7e31d942e0826477ef97aecff4b0164370220bfa85f09`; pre- and post-reads show the original action `007ff0…acd00` remains consumed.
  - Same fill + same party with a fresh action: tx `0xb91a7831935bcf79199610f68c3a538e6913d0615ed5bc1910c9b179b6e0f6b8` finalized; action `82b1…1871` remains unconsumed.
- The CLI did not expose the GenVM user-error text in these receipts; the evidence above is the finalized transaction status and post-call consumed-state reads. An earlier all-numeric wrong-market argument was parsed by the CLI as integer `0` and is excluded from the wrong-hash evidence.

An earlier separate deployment and partial market setup preceded the final deployment above. They are superseded and are not the final lifecycle evidence.

## Tooling note

`genlayer estimate-fees --json` returned `TypeError: client.estimateTransactionFees is not a function`. Normal deployment and write commands were accepted and finalized without explicit fee overrides. No fee-estimation success is claimed.

## Repository and CI delivery

The dedicated repository is [BeatyXO/IntentClearing](https://github.com/BeatyXO/IntentClearing), configured on `main`; the separate `BeatyXO/Corroborate` repository was not changed. GitHub Actions run `35505058611` passed for implementation commit `f5e2c740a4542c5b3c8e54385f2129c76fa87f9a`. The initial CI run identified two actual problems: the v0.29.2 loader expected a universal runner artifact no longer published in the latest release, and the Linux test adapter did not update the mocked timestamp after `warp`. CI now seeds the verified official runner bundle `genvm-runners-all.tar.xz` from GenVM `v0.3.0-rc7` into the v0.29.2 loader cache under its expected filename and checks the published SHA-256; the test adapter synchronizes timestamps across platforms. The pinned testing-suite version and stable Studionet network remain unchanged.
