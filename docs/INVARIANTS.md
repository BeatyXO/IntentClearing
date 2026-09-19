# Protocol invariants

1. **Sealed vocabulary:** attributes cannot change after `seal_market`.
2. **Version pinning:** every epoch/order/fill carries the exact market definition hash.
3. **Single-order AI boundary:** consensus may profile one order only; it never chooses counterparties or allocations.
4. **Validator independence:** validators independently regenerate the bounded masks rather than checking JSON shape only.
5. **Quantitative determinism:** quantity and price are explicit inputs and are never inferred by an LLM.
6. **No selective clearing:** every non-cancelled order in a frozen epoch must have a profile before clearing can begin.
7. **Fail-closed ambiguity:** ambiguity on a request's required/forbidden offer dimensions blocks compatibility.
8. **Deterministic allocation:** sorting and fill quantity/price rules contain no nondeterminism.
9. **Replay resistance:** client order hashes are globally unique; consumer action hashes are one-time.
10. **Historical commitment:** `epoch_hash`, fill hashes, and settlement root are append-only evidence of the frozen batch outcome.
