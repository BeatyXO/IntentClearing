# Threat model

## Prompt injection in order descriptions
Descriptions and market text are explicitly treated as untrusted data. Profiling prompts forbid following embedded instructions. Validators independently reproduce the semantic masks.

## Forged leader profile
The custom validator requires a valid bounded shape and independently reruns profiling. A leader cannot gain acceptance merely by returning syntactically valid JSON.

## Capability hallucination
Offer silence is ambiguous, not present. Ambiguity on required/forbidden dimensions fails closed.

## Selective omission
The batch cannot clear while any active order remains unassessed. A caller cannot clear only favorable assessed orders while ignoring pending competitors.

## Definition substitution
Orders and epochs pin a sealed market hash. Fills additionally pin the frozen epoch hash.

## Duplicate economic actions
`client_order_hash` prevents resubmitting the same client identity. The example consumer separately rejects repeated `action_hash` values.

## Allocation manipulation
The LLM cannot set price, quantity, counterparties, priority, or fill amount. Clearing is deterministic from stored profiles and explicit numeric terms.

## Bounded execution
Each epoch side is capped, semantic attributes are capped, and clearing work is therefore bounded.
