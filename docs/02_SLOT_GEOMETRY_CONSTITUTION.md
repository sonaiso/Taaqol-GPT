# 02 — Slot Geometry Constitution

> **Status:** Skeleton in PR-0. Fully written alongside PR-1.

This document will specify the formal constitution of the six cores and
how they compose. It is intentionally a header-only skeleton in PR-0 so
that the constitution is *named* before any code references it.

## The six cores

1. **`SlotGraph`** — the geometric carrier of every entity that enters
   the engine. Comprises a `center` (identity), `openings` (unresolved
   possibilities), `closures` (licensed resolutions), `slots`, `edges`,
   `constraints`, `residuals`, `rank`, and a `trace_ref`.
2. **`GammaClosure`** — the pure verdict function
   `gamma(SlotGraph) → GammaResult`. Returns one of `OPEN`,
   `MINIMALLY_CLOSED`, `PERFORATED_CLOSED`, `BLOCKED`, `INVALID`,
   `FORBIDDEN_LEAP`.
3. **`TransitionGate`** — the only legal cross-layer or cross-slot move.
   Requires `Evidence`, `Rank`, and a `ResidualPolicy` result. Returns
   one of `APPROVED`, `DEFERRED`, `BLOCKED`, `REJECTED`,
   `FORBIDDEN_LEAP`.
4. **`RankLattice`** — the bounded partial order
   `ZERO < TRACE < CANDIDATE < HYPOTHESIS < LICENSED < STRONG < CERTIFICATE`
   with a monotone `meet` operation. No rank promotion without a gate.
5. **`ResidualPolicy`** — the law that classifies residuals as
   `BLOCKING`, `DEFERRABLE`, `NON_BLOCKING`, `EXPLANATORY`, or
   `HIDDEN_FORBIDDEN`, and computes a ceiling rank for the output.
6. **`TraceLedger`** — the append-only record of every verdict the
   engine has produced. Required for audit; *not* called from inside
   pure core functions.

## Composition rules

- `SlotGraph` is immutable. Transitions return new graphs.
- `gamma` is pure. It does not write to the ledger; it returns a
  `TraceEntryCandidate` that an outer caller appends.
- Every gate consults the `RankLattice` and the `ResidualPolicy` before
  returning anything other than a refusal.
- An output may exist only if a `TransitionGate` has returned
  `APPROVED` *and* the resulting `SlotGraph` is at least
  `MINIMALLY_CLOSED` or `PERFORATED_CLOSED` with all residuals visible.

The detailed contracts for each core live in the matching numbered
documents (`03`–`08`).
