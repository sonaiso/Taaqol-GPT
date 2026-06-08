# 03 — Gamma Closure Contract

> **Status:** Header-only skeleton in PR-0. Fully written in PR-1.

`gamma(graph: SlotGraph) → GammaResult` is the pure verdict function.

## States (to be specified in PR-1)

- `OPEN` — required slots not yet filled.
- `MINIMALLY_CLOSED` — all required slots filled, no residuals.
- `PERFORATED_CLOSED` — all required slots filled, non-blocking
  residuals declared.
- `BLOCKED` — a blocking residual is present.
- `INVALID` — the graph's identity is broken or a hidden residual was
  detected (hidden residuals must be surfaced *before* gamma).
- `FORBIDDEN_LEAP` — the graph claims a layer it is not authorised for.

## Purity rule

`gamma` is a pure function. It returns a `TraceEntryCandidate` inside
its `GammaResult`; appending to the `TraceLedger` is the caller's
responsibility. See `07_TRACE_LEDGER.md`.

## PR-1 decision table

`gamma(graph)` evaluates the conditions below **in order** and returns
on the first match. Every refusal carries a named `FailureCode` (see
`core/failure_taxonomy.py`). Successful closures carry
`failure_code = None`.

| # | Condition                                                                                   | Verdict              | `FailureCode`                |
| - | ------------------------------------------------------------------------------------------- | -------------------- | ---------------------------- |
| 1 | Any `Slot.state == BROKEN`                                                                  | `INVALID`            | `IDENTITY_BROKEN`            |
| 2 | Any residual has `kind == HIDDEN_FORBIDDEN` **or** `visible is False`                       | `INVALID`            | `HIDDEN_RESIDUAL`            |
| 3 | `output_boundary is not None` and `output_boundary > declared_layer` (generic `Layer` enum) | `FORBIDDEN_LEAP`     | `OUTPUT_EXCEEDS_LAYER`       |
| 4 | Any residual has `kind == BLOCKING`                                                         | `BLOCKED`            | `BLOCKING_RESIDUAL_PRESENT`  |
| 5 | Any required slot has `state == EMPTY`                                                      | `OPEN`               | `REQUIRED_SLOT_EMPTY`        |
| 6 | All required slots filled and at least one (visible, non-blocking) residual is declared     | `PERFORATED_CLOSED`  | `None`                       |
| 7 | All required slots filled and no residuals at all                                           | `MINIMALLY_CLOSED`   | `None`                       |

Precedence is load-bearing: a graph that both leaps and has an empty
required slot returns `INVALID` if a slot is `BROKEN`, otherwise
`FORBIDDEN_LEAP` — never `OPEN`. A graph with a hidden residual is
never approved, even if all required slots are filled.

`gamma` never raises. Every return value is a `GammaResult` carrying:

- the `GammaState`,
- the `FailureCode` (or `None` for closure verdicts),
- a `TraceEntryCandidate` (the caller appends it to a `TraceLedger`),
- a tuple of human-readable `reasons` for diagnostics.

The `Layer` ordering used for rule 3 is the generic enum declared
alongside `SlotGraph`. PR-1 does not ship a forbidden-transition
registry; that is PR-4.
