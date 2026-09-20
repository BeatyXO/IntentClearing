# Build status

The local handoff includes strict profile-field validation, exact lowercase digest validation, fill hashes that explicitly include both market and epoch pins, and checks for mask shape, digest format, prompt injection handling, and the one-order AI boundary.

Verified locally:

- `python scripts/preflight.py` — PASS.
- `python -m compileall -q contracts tests` — PASS.
- `python -m pytest tests/unit -q` — PASS, 8 tests.
- `python -m pytest tests/direct -q` — PASS, 26 tests on pinned genlayer-test v0.29.2.

Verified live lifecycle and delivery:

- Final IntentClearing deployment and a complete semantic-profile/clear lifecycle are finalized on stable Studionet; the preferred rush offer wins over the cheaper offer. Final addresses, hashes, and transactions are in `DEPLOYMENT.md`.
- ClearingGate is deployed; correct party consumption finalized. Wrong-market, wrong-epoch, wrong-fill, non-party, repeated-action, and same-fill/same-party replay calls also finalized with execution errors, and post-call reads confirmed no new action consumption. The earlier all-numeric digest attempt was malformed by CLI parsing and was excluded.
- Public `BeatyXO/IntentClearing` is on `main`; the Corroborate repository was not touched. GitHub Actions run `35505058611` passed on implementation commit `f5e2c740a4542c5b3c8e54385f2129c76fa87f9a`, including preflight, unit, and Direct Mode jobs.

See `DEPLOYMENT.md` for exact finalized lifecycle and CI evidence.
