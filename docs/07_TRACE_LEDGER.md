# 07 — Trace Ledger

> **Status:** Header-only skeleton in PR-0. Fully written in PR-1.

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

The ledger itself is in-memory in PR-1 and stays in-memory through
PR-5. Persistence is out of scope for the staged roadmap.
