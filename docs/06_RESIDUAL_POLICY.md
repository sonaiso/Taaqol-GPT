# 06 — Residual Policy

> **Status:** Header-only skeleton in PR-0. Fully written in PR-2.

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
