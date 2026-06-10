# 06 — Residual Policy

> **Status:** Header-only skeleton in PR-0. Bound in code in PR-3
> (`ResidualPolicy` + `ResidualEvaluation`).

Residuals are not commentary. They are part of the verdict.

## Residual kinds

- `BLOCKING` — prevents closure entirely; the gamma state becomes
  `BLOCKED`.
- `DEFERRABLE` — does not block closure, but caps the output rank at
  `HYPOTHESIS`.
- `NON_BLOCKING` — does not affect rank; closure becomes
  `PERFORATED_CLOSED` and the residual must be declared in the output.
- `EXPLANATORY` — informational; does not affect rank or closure.
- `HIDDEN_FORBIDDEN` — a residual that exists but has not been
  surfaced. This is a fatal contract violation. `Gamma` returns
  `INVALID` and no gate may approve the graph.

## The visibility law

```text
ResidualHidden → ApprovedOutput   is forbidden.
```

An approved output must carry every residual it inherited, regardless
of kind, except where the policy explicitly suppresses `EXPLANATORY`
residuals from the output surface.

## PR-3 binding

The engine lives in
[`src/taaqqul_slot_geometry/core/residual_policy.py`](../src/taaqqul_slot_geometry/core/residual_policy.py)
and is pure: it reads the declared residual surface and returns
values. It never edits, suppresses, or reclassifies a residual, and
it never promotes a rank.

- `ResidualPolicy.rank_cap(kind)` — the per-kind output-rank caps
  named above, total over `ResidualKind`:

  ```text
  BLOCKING          → ZERO
  HIDDEN_FORBIDDEN  → ZERO
  DEFERRABLE        → HYPOTHESIS
  NON_BLOCKING      → CERTIFICATE   (lattice top — no constraint)
  EXPLANATORY       → CERTIFICATE   (lattice top — no constraint)
  ```

- `ResidualPolicy.ceiling(residuals)` — `ResidualCeiling(G)`, the
  lattice `meet` of every per-kind cap (docs/11 §9). The empty
  surface yields the lattice top: *vacuously* no residual
  constraint, **not** a licence — the value only ever enters the §8
  meet, it is never an output rank by itself. `Γ` step 9 consumes
  this ceiling and refuses a carried rank above it with
  `RANK_EXCEEDS_CEILING`.
- `ResidualPolicy.evaluate(residuals)` — returns a frozen
  `ResidualEvaluation` carrying the named refusal
  (`HIDDEN_RESIDUAL` before `BLOCKING_RESIDUAL_PRESENT`, mirroring
  `Γ` steps 6–7), the ceiling, the visibility conjunction, and
  whether the surface licenses a perforated closure
  (`PERFORATING_KINDS = {NON_BLOCKING, DEFERRABLE, EXPLANATORY}`).
