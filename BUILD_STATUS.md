# Build status

The local handoff now includes strict profile-field validation, exact lowercase digest validation, fill hashes that explicitly include both market and epoch pins, and additional offline checks for mask shape, digest format, prompt injection handling, and the one-order AI boundary.

Verified locally:

- `python scripts/preflight.py` — PASS.
- `python -m compileall -q contracts tests` — PASS.
- `python -m pytest tests/unit -q` — PASS, 8 tests.
- `python -m pytest tests/direct -q` — PASS, 26 tests on pinned genlayer-test v0.29.2.

Live progress and remaining blockers:

- IntentClearing is finalized at `0x949ddCdf53DDbF0931eCcd37dde0De50EF787376`. Market 1 creation and its first `UPGRADEABLE` attribute are also finalized; see `DEPLOYMENT.md` for transactions.
- The next write prompted for the wallet keystore password and produced no transaction hash. Sealing, epoch/orders, assessments, clearing, fills, and ClearingGate are not yet verified.
- Public `BeatyXO/IntentClearing` exists on configured branch `main`. Local commit `5dec3b354fed3d6c44fa2503d1d5f0a931929f64` is not pushed: GitHub rejected the workflow file because the active token lacks `workflow` scope. Device authorization is pending. Remote CI is therefore not available yet.

See `DEPLOYMENT.md` for the exact finalized deployment and market transaction evidence, plus the remaining live-chain blockers.
