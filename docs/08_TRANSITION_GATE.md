# 08 — Transition Gate

> **Status:** Header-only skeleton in PR-0. Fully written in PR-3.

A `TransitionGate` is the only legal cross-layer or cross-slot move.

## Signature

```text
gate.decide(input_graph, target_layer, evidence) -> TransitionVerdict
```

## Verdicts

- `APPROVED` — the move is licensed; the new graph carries a rank no
  higher than the lattice meet of all inputs.
- `DEFERRED` — preconditions are not yet met; retry is permitted once
  more evidence arrives.
- `BLOCKED` — a blocking residual prevents the move.
- `REJECTED` — the move is well-formed but unlicensed for this gate.
- `FORBIDDEN_LEAP` — the source/target pair is in the forbidden
  straight-line registry and no bridge gate is being used. Fatal.

## Required preconditions

Every gate, before returning anything other than a refusal, must:

1. Confirm `evidence` is non-empty and carries an `evidence_rank`.
2. Call `RankLattice.meet` over all inputs.
3. Call `ResidualPolicy.evaluate` and respect the ceiling it returns.
4. Emit a `TraceEntryCandidate` for the caller to append.
5. Return a typed `FailureCode` on any refusal; never raise.
