# 07 — Trace Ledger

> **Status:** Header skeleton in PR-0. Constitutional purity rule
> ratified in PR-1. The executable `TraceLedger` and
> `TraceEntryCandidate` land in PR-2 alongside `SlotGraph` + `Γ`.

The `TraceLedger` is an append-only record of every verdict the engine
has produced.

## Entries

Each `TraceEntry` carries:

```text
trace_id
parent_id
stage           (e.g., "gamma", "gate", "audit")
input_ref       (hash or id of the input SlotGraph)
snapshot        (the verdict and its key fields)
timestamp
```

## The purity rule

Core verdict functions do **not** append to the ledger. They return a
`TraceEntryCandidate` inside their result. The outer caller (the audit
wrapper, the gate runner, a test harness) decides when and where to
append. This keeps `core/` pure and free of I/O.

```text
gamma(graph) -> GammaResult(trace_event=TraceEntryCandidate(...))
ledger.append(result.trace_event)
```

The ledger itself is in-memory in PR-2 and stays in-memory through
PR-6. Persistence is out of scope for the staged roadmap.

## PR-2 binding (forward reference)

PR-2 will ship `TraceEntryCandidate` (frozen) and `TraceLedger`
(minimal in-memory container with `append(entry)` and an `entries`
view) inside `core/trace_ledger.py`. `gamma.py` must not import
`TraceLedger`; the constitutional purity rule above will be enforced
by a static guard in the PR-2 test suite.

## PR-6 binding

PR-6 splits the verdict snapshot that PR-2's `TraceEntryCandidate`
carried in one field: every candidate now records
`consulted_gamma_state` (the `ClosureState` that `Γ` returned) and
`gate_transition_state` (the `TransitionState` of the gate verdict —
`None` exactly when `stage="gamma"`, required for `stage="gate"` and
`stage="audit"`). The mixed `snapshot_state` field is gone; a gamma
state can no longer impersonate a gate verdict in the ledger.

The audit wrapper
([`src/taaqqul_slot_geometry/audit/answer_audit.py`](../src/taaqqul_slot_geometry/audit/answer_audit.py))
is the designated impure shell that owns the ledger: it appends the
`gamma` candidate, the `gate` candidate, and its own `audit`-stage
candidate, in that order. Core verdict functions and the pure
emission half (`emit_successor`) still never touch a `TraceLedger`;
the static guards that enforce this now cover the audit package
too. The ledger stays in-memory: no persistence, no network, no
filesystem I/O.
