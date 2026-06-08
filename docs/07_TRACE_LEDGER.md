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
