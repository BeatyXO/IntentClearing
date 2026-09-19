# Build status

The local handoff now includes strict profile-field validation, exact lowercase digest validation, fill hashes that explicitly include both market and epoch pins, and additional offline checks for mask shape, digest format, prompt injection handling, and the one-order AI boundary.

Verified locally:

- `python scripts/preflight.py` — PASS.
- `python -m compileall -q contracts tests` — PASS.
- `python -m pytest tests/unit -q` — PASS, 8 tests.
- `python -m pytest tests/direct -q` — PASS, 26 tests on pinned genlayer-test v0.29.2.

Still unverified or blocked:

- Live Studionet writes were not attempted. Read-only balance calls for both configured accounts failed with RPC `fetch failed`.
- The dedicated public `BeatyXO/IntentClearing` repository is created on its configured initial `main` branch. Local commit `2a01a595ddeddf328822de38a790ddc5e78913c3` is ready to push; remote inspection and CI remain pending.

See `DEPLOYMENT.md` for exact command outcomes. No deployment evidence is claimed.
