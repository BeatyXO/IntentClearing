# IntentClearing

IntentClearing is a standalone reusable GenLayer Intelligent Contract primitive for **batch markets whose important requirements are partly qualitative**.

A normal order book can compare price and quantity, but it cannot safely reduce requirements such as “upgradeable-contract audit experience”, “French-language support”, or “GPU with confidential-compute capability” to raw numbers. A naive AI marketplace would ask an LLM to pick winners. IntentClearing does not.

Instead, a market owner creates and seals a bounded **market-local semantic attribute dictionary**. Each request and offer is independently profiled by GenLayer consensus against that dictionary. The LLM never compares two orders. Once profiles exist, compatibility, preference scoring, price checks, quantities, partial fills, ordering, settlement roots, and replay-safe consumption are deterministic.

## Protocol split

**Consensus-backed:** one-order-at-a-time semantic profiling into bounded bitmasks.

**Deterministic:** request/offer compatibility, max-bid vs ask checks, required/forbidden constraints, preference score, partial fills, clearing order, fill hashes, epoch hash, settlement root, and consumer replay protection.

This separation is the core product boundary. Do not collapse the project into “AI matches buyers and sellers.”

## Why this is distinct

IntentClearing intentionally avoids pairwise AI comparison. It does not ask whether request A matches offer B, and it does not perform semantic scheduling. That keeps it architecturally distinct from semantic concurrency/locking systems: each order receives a reusable market-local profile once, then the clearing algorithm works mechanically.

## State model

1. `create_market` creates a draft market.
2. `add_attribute` defines up to 16 bounded semantic dimensions.
3. `seal_market` freezes the market definition and creates `definition_hash`.
4. `open_epoch` starts an order batch pinned to that definition.
5. requesters/offers submit qualitative descriptions plus explicit quantitative price/quantity.
6. `assess_order` reaches consensus on that single order's semantic profile.
7. market owner freezes the order set, producing `epoch_hash`.
8. `clear_epoch` is permissionless and deterministic once every active order is assessed.
9. every fill pins market, epoch, and exact fill hashes; `ClearingGate` demonstrates typed IC-to-IC reuse and action replay protection.

## Deterministic clearing policy

Requests clear by maximum unit price descending, then submission time, then order ID. For each request, compatible offers rank by semantic preference score descending, ask price ascending, submission time, then order ID. Trade price is the offer ask. Quantities may partially fill. No LLM controls allocation.

## Target network

Stable Studionet only:

- alias: `studionet`
- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- explorer: `https://explorer-studio.genlayer.com`

## Repository shape

- `contracts/intentclearing.py` — primary primitive
- `contracts/clearing_gate.py` — minimal consumer IC
- `tests/direct/` — Direct Mode protocol/adversarial tests
- `tests/unit/` — static product-boundary checks
- `docs/ARCHITECTURE.md` — design and clearing rules
- `docs/INVARIANTS.md` — reviewer-facing invariants
- `docs/THREAT_MODEL.md` — failure model
- `DEPLOYMENT.md` — live proof template; no invented evidence
- `SUBMISSION.md` — submission-facing summary
- `scripts/preflight.py` — static final gate

## Current package status

The pinned `genlayer-testing-suite` v0.29.2 runs locally in Direct Mode. Current verification is recorded in `DEPLOYMENT.md`; it includes preflight, Python compilation, unit/static tests, and adversarial Direct Mode coverage. IntentClearing has been deployed on stable Studionet and market setup is in progress. The deployment address and verified transactions are documented there; no unproduced lifecycle evidence is claimed. The dedicated `BeatyXO/IntentClearing` repository exists; its first push awaits a GitHub token with permission to publish the existing CI workflow. It must never be pushed to `BeatyXO/Corroborate`.
