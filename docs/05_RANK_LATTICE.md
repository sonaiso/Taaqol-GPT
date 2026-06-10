# 05 — Rank Lattice

> **Status:** Header-only skeleton in PR-0. Bound in code in PR-3
> (`RankLattice` + `EvidenceContract`).

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

A *single* evidence source can never license `CERTIFICATE`. PR-3
binds that cap in code: a one-source
`EvidenceContract.evidence_rank` is the `meet` of the source's own
rank and `SINGLE_SOURCE_EVIDENCE_CEILING` (= `STRONG`). A pool of
sources aggregates by `join` — as strong as its strongest member,
never stronger; no corroboration bonus is synthesised. Only a
`TransitionGate` (PR-4) may weigh sources against each other, and
only bounded by the §8 meet.

The exact ceiling per source *kind* remains a declared residual of
PR-3: no canonical kind list exists yet (the lexicon surface is
forbidden until far later PRs), so `kind` stays an opaque non-empty
string and imposes no rank semantics.

## PR-3 binding

The lattice lives in
[`src/taaqqul_slot_geometry/core/rank_lattice.py`](../src/taaqqul_slot_geometry/core/rank_lattice.py):

- `RankLattice.meet` / `RankLattice.join` — bounded greatest-lower /
  least-upper bounds over the total `Rank` order, with
  `RankLattice.BOTTOM = ZERO` and `RankLattice.TOP = CERTIFICATE`.
- The lattice is *pure algebra*: no promotion decision lives here.
  `Γ` step 9 consumes the residual ceiling
  ([`06_RESIDUAL_POLICY.md`](06_RESIDUAL_POLICY.md)); the evidence
  rank comes from
  [`core/evidence_contract.py`](../src/taaqqul_slot_geometry/core/evidence_contract.py);
  identity and gate ranks join the meet when the gate lands (PR-4).
- An empty or ill-typed `meet`/`join` call is a programmer mistake
  refused loudly with `TypeError` (mirroring `gamma`'s domain
  guard), never a silently synthesised bound.
