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
