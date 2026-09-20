# Build status

The local handoff includes strict profile-field validation, exact lowercase digest validation, fill hashes that explicitly include both market and epoch pins, and checks for mask shape, digest format, prompt injection handling, and the one-order AI boundary.

Verified locally:

- `python scripts/preflight.py` — PASS.
- `python -m compileall -q contracts tests` — PASS.
- `python -m pytest tests/unit -q` — PASS, 8 tests.
- `python -m pytest tests/direct -q` — PASS, 26 tests on pinned genlayer-test v0.29.2.

Live lifecycle and remaining delivery blockers:

- Final IntentClearing deployment and a complete semantic-profile/clear lifecycle are finalized on stable Studionet; the preferred rush offer wins over the cheaper offer. Final addresses, hashes, and transactions are in `DEPLOYMENT.md`.
- ClearingGate is deployed and the correctly pinned fill consumption by a party finalized. Live rejection receipts for wrong pins, non-party, and replay remain unverified; the previous wrong-market attempt actually used the correct market hash.
- Public `BeatyXO/IntentClearing` exists on `main`, but current local `gh auth status` reports its token invalid. The push and remote CI remain blocked until GitHub CLI authentication is restored with the `workflow` scope. The Corroborate repository was not touched.

See `DEPLOYMENT.md` for exact finalized lifecycle evidence and the remaining live rejection and GitHub delivery blockers.
