# 05 — Rank Lattice

> **Status:** Header-only skeleton in PR-0. Fully written in PR-2.

The `RankLattice` is a bounded partial order over evidential strength:

```text
ZERO < TRACE < CANDIDATE < HYPOTHESIS < LICENSED < STRONG < CERTIFICATE
```

with a monotone `meet` operation used to combine the rank carried by an
input graph, the rank licensed by available evidence, the rank ceiling
imposed by residual policy, and the rank licensed by the transition
gate itself.

## The non-promotion law

```text
OutputRank ≤ meet(EvidenceRank, IdentityRank, GateRank, ResidualCeiling)
```

No code path may produce a rank higher than the `meet` of its inputs.

## What `Evidence → Certainty` actually looks like

A *single* evidence source can never license `CERTIFICATE`. The exact
ceiling per source kind is specified in PR-2.
