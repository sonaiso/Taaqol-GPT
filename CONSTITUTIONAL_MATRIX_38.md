# CONSTITUTIONAL_MATRIX_38

This document declares the executable data surface for the 38 constitutional operations matrix used by `ConstitutionalMatrixEngine`.

## Files

- `data/constitutional_matrix_38.json`: canonical matrix data.
- `src/taaqqul_slot_geometry/x0r/constitutional_matrix_engine.py`: runtime loader, verifier, and transition evaluator.

## Required Per-Operation Fields

Each operation declares the seven mandatory constitutional fields:

1. `origins`
2. `inputs`
3. `slots`
4. `licensing`
5. `local_closure`
6. `residuals`
7. `handoff_gate`

In addition, each operation carries:

- `operation_id`
- `name`
- `next_operations`

## Engine I/O

Input:

- `current_operation_id`
- `inputs`
- `evidence`

Output:

- `next_operation_id`
- `closure_verdict` (`CLOSED`, `DEFERRED`, `REFUSED`)
- `residuals`
- `trace_entry`

## Verification Surface

`ConstitutionalMatrixEngine.verify()` checks:

- all origins defined (operation IDs or declared origins)
- no cycles (acyclic DAG)
- no orphans (every operation has at least one origin)
- Euclidean progression (child level strictly after origin level)
- residual vocabulary cardinality
