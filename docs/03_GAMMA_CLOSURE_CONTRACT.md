# 03 — Gamma Closure Contract

> **Status:** Constitutional contract. PR-1 ratifies the ordered law
> below; PR-2 binds it in code via a pure ``gamma(graph)`` function.

`Γ : SlotGraph → ClosureState` is the pure verdict function over a
constitutional `SlotGraph`. It returns one of six verdicts and never
raises for expected refusals. Every refusal carries a member of
[`FailureCode`](../src/taaqqul_slot_geometry/core/failure_taxonomy.py).

## The six verdicts

```text
ClosureState ∈ {
  OPEN,
  MINIMALLY_CLOSED,
  PERFORATED_CLOSED,
  BLOCKED,
  INVALID,
  FORBIDDEN_LEAP,
}
```

- `OPEN` — required slots not yet filled.
- `MINIMALLY_CLOSED` — all required slots filled, no residuals,
  identity intact, output within layer.
- `PERFORATED_CLOSED` — all required slots filled, non-blocking
  residuals declared visibly; licenses a `Candidate`, never a
  `Certificate`.
- `BLOCKED` — a blocking residual is present.
- `INVALID` — the graph's identity is broken, a required
  constitutional field is missing (center, boundary, domain, scope,
  trace), or a residual is hidden.
- `FORBIDDEN_LEAP` — the graph claims an output above its declared
  layer, or attempts a transition that requires a bridge gate (the
  bridge registry lands in PR-5).

## Purity law

`Γ` is a pure function. It returns a `ClosureState` (and, in the
PR-2 binding, a `TraceEntryCandidate` packaged inside a `GammaResult`).
Appending to the `TraceLedger` is the caller's responsibility. See
[`07_TRACE_LEDGER.md`](07_TRACE_LEDGER.md).

## The ordered closure law

`Γ` is **not** a free `if/else` over a graph. It is a fixed-order
application of constitutional checks. The order is load-bearing: a
refusal at step *k* short-circuits steps *k+1 … 10* and is reported
with the corresponding `FailureCode`.

| Step | Check                                                                                                              | On refusal                                                       |
| ---- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| 1    | `Center` is present and carries an `IdentityClaim`                                                                 | `INVALID` / `CENTER_MISSING`                                     |
| 2    | `Trace` reference is present                                                                                       | `INVALID` / `TRACE_MISSING`                                      |
| 3    | `Domain`, `Scope`, and `Boundary` declarations are present                                                         | `INVALID` / `DOMAIN_MISSING` ∨ `SCOPE_MISSING` ∨ `BOUNDARY_MISSING` |
| 4    | No slot has `value_state == BROKEN`                                                                                | `INVALID` / `IDENTITY_BROKEN`                                    |
| 5    | `output_boundary` does not exceed `declared_layer` in the layer order                                              | `FORBIDDEN_LEAP` / `OUTPUT_EXCEEDS_LAYER`                        |
| 6    | No residual has `kind == HIDDEN_FORBIDDEN` or `visible == false`                                                   | `INVALID` / `HIDDEN_RESIDUAL`                                    |
| 7    | No residual has `kind == BLOCKING`                                                                                 | `BLOCKED` / `BLOCKING_RESIDUAL_PRESENT`                          |
| 8    | Every required slot has `value_state == FILLED`                                                                    | `OPEN` / `REQUIRED_SLOT_EMPTY`                                   |
| 9    | Rank ceiling = `meet(EvidenceRank, IdentityRank, ResidualCeiling, GateRank)` is computed (no path exceeds the meet) | `INVALID` / `RANK_EXCEEDS_CEILING`                               |
| 10   | If any visible non-blocking residual remains → `PERFORATED_CLOSED`; else → `MINIMALLY_CLOSED`                       | (closure verdict)                                                |

Note: Step 9's rank computation is fully implemented in PR-3
alongside `RankLattice` + `ResidualPolicy`. The PR-2 implementation
of `Γ` reserves the step (and the `RANK_EXCEEDS_CEILING` failure
code) and treats the carrier `rank` as a passthrough; it must not
*promote* a rank.

## ClosureState ≠ TruthState

A constitutional axiom:

```text
A MINIMALLY_CLOSED graph is not a true statement.
A PERFORATED_CLOSED graph is not a certified statement.
Closure is boundary satisfaction, not truth.
```

The implementation must never collapse the two. A `MINIMALLY_CLOSED`
verdict licenses *continuation*: the caller may submit the graph to
a `TransitionGate` for promotion. It does not license certainty.

## What `Γ` may never do

- `Γ` may not append to a `TraceLedger`.
- `Γ` may not promote a `Rank` (only a `TransitionGate` may, and only
  bounded by the lattice `meet`).
- `Γ` may not hide a residual.
- `Γ` may not synthesise a center, a boundary, a domain, a scope, or
  a trace if they are missing — it refuses.
- `Γ` may not return `MINIMALLY_CLOSED` or `PERFORATED_CLOSED` when
  any of: a hidden residual, a missing center, a missing trace, a
  broken identity, a forbidden leap, an unlicensed opening, or a
  blocking residual obtains.

## PR-1 scope vs. PR-2 binding

PR-1 ratifies the law above and ships the `ClosureState` enum so
tests and downstream docs can reference the verdict names exactly.
PR-2 binds the law in code: the pure `gamma(graph)` function lives
in
[`src/taaqqul_slot_geometry/core/gamma.py`](../src/taaqqul_slot_geometry/core/gamma.py)
and returns a `GammaResult` carrying the verdict and a
`TraceEntryCandidate` (see
[`src/taaqqul_slot_geometry/core/trace_ledger.py`](../src/taaqqul_slot_geometry/core/trace_ledger.py)).
The constructor surface lives in
[`src/taaqqul_slot_geometry/core/slot_graph.py`](../src/taaqqul_slot_geometry/core/slot_graph.py).
The order of checks in `gamma.py` matches §7 verbatim; step 9 is
reserved (carrier-only rank passthrough) until the `RankLattice`
lands in PR-3.
