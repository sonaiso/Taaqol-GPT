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

## PR-1 binding subset (kernel surface)

PR-1 freezes the *minimum* surface that the rest of the constitution
will rest on. Everything below is binding: code outside `core/` is not
permitted in PR-1, and the shapes here must not be widened until a
later PR opens its corresponding section.

### Immutability law

All PR-1 core dataclasses are declared `frozen=True, slots=True`. A
transition does not mutate a `SlotGraph`; it constructs a new one. Any
in-place mutation attempt must raise (this is the default behaviour of
frozen dataclasses).

### `SlotState` (enum)

```text
SlotState = { EMPTY, FILLED, BROKEN }
```

- `EMPTY` — required content not yet supplied.
- `FILLED` — content present and accepted by the slot's local checks.
- `BROKEN` — identity violation at the slot level (e.g., content
  declared but with a contradicting boundary). A single `BROKEN` slot
  drives the graph to `INVALID` at gamma time.

### `SlotBoundary` (frozen dataclass, label-only in PR-1)

```text
SlotBoundary(name: str)
```

PR-1 ships `SlotBoundary` as a label-only carrier. No layer semantics,
no constraint inference. The field exists so that later PRs can attach
boundary policies without changing the `Slot` shape.

### `Slot` (frozen dataclass)

```text
Slot(
  name: str,
  required: bool,
  state: SlotState,
  boundary: SlotBoundary | None = None,
  value_ref: str | None = None,
)
```

`value_ref` is an opaque identifier (e.g., a hash or an id into an
external store). PR-1 does not interpret it.

### `Layer` (enum, generic ordering only)

```text
Layer = ( L0_RAW, L1_FORM, L2_MEANING, L3_JUDGMENT, L4_APPLICATION )
```

PR-1 ships a small, *generic* ordered `Layer` enum so the
`FORBIDDEN_LEAP` test has something to compare. This is **not** the
Forbidden Straight-Line Registry — there is no source/target table, no
required-bridge mapping, and no Arabic layering. Those land in PR-4.
The ordering is the only thing `gamma` consults.

### `SlotGraph` (frozen dataclass)

```text
SlotGraph(
  center: str,                              # identity label
  slots: tuple[Slot, ...],
  edges: tuple[tuple[str, str], ...],       # (slot_name, slot_name)
  constraints: tuple[str, ...],             # opaque labels in PR-1
  residuals: tuple[Residual, ...],
  rank: Rank,                               # carrier only (PR-2 promotes)
  declared_layer: Layer,
  output_boundary: Layer | None = None,     # layer the graph claims to output
  trace_ref: str | None = None,
)
```

PR-1 validators (raise `ValueError` in `__post_init__`):

- slot names are unique;
- every edge endpoint references a known slot.

No other invariants are enforced at construction time in PR-1. Gamma is
the verdict surface; the graph itself stays a minimal carrier.
