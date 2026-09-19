# Architecture

## 1. Market-local semantic vocabulary
A market contains a bounded list of attributes with human-readable definitions. Once sealed, the dictionary is immutable and identified by `definition_hash`. Orders and epochs pin this hash.

## 2. Independent profiling, never pairwise adjudication
Each order is classified alone. A REQUEST yields `required_mask`, `forbidden_mask`, `preferred_mask`, and `ambiguous_mask`. An OFFER yields `present_mask`, `absent_mask`, and `ambiguous_mask`.

Validators independently rerun the same profiling task. Only bounded decision masks determine equivalence; free-form rationale is not consensus-critical.

## 3. Fail-closed ambiguity
An offer cannot satisfy a required or forbidden request dimension when that offer dimension is ambiguous. Silence in an offer is ambiguous, not proof of capability.

## 4. Deterministic compatibility
A request/offer pair is compatible only if they share the same pinned epoch/market, both profiles are ready, ask <= max bid, all required bits are present, no forbidden bits are present, and required/forbidden bits are not ambiguous in the offer.

## 5. Deterministic batch clearing
Requests rank by max price descending then time/ID. Compatible offers rank per request by preferred-bit overlap descending, ask ascending, then time/ID. Fills use the offer ask and support partial quantities.

## 6. Immutable epoch proof
Freezing commits the active order hashes into `epoch_hash`. Every fill pins this hash and the market definition hash. `settlement_root` folds fill hashes in deterministic creation order.

## 7. Consumer proof
`ClearingGate` does not trust a free-form result. It makes typed IC-to-IC reads, pins exact market/epoch/fill hashes, requires the caller to be one of the fill parties, and rejects replayed action hashes.
