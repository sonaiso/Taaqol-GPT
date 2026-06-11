# 08 — Transition Gate

> **Status:** Header-only skeleton in PR-0. Bound in PR-4.

A `TransitionGate` is the only legal cross-layer or cross-slot move.

## Signature

```text
gate.decide(input_graph, target_layer, evidence) -> TransitionVerdict
```

## Verdicts

- `APPROVED` — the move is licensed; the new graph carries a rank no
  higher than the lattice meet of all inputs.
- `DEFERRED` — preconditions are not yet met; retry is permitted once
  more evidence arrives.
- `BLOCKED` — a blocking residual prevents the move.
- `REJECTED` — the move is well-formed but unlicensed for this gate.
- `FORBIDDEN_LEAP` — the source/target pair is in the forbidden
  straight-line registry and no bridge gate is being used. Fatal.

## Required preconditions

Every gate, before returning anything other than a refusal, must:

1. Confirm `evidence` is non-empty and carries an `evidence_rank`.
2. Call `RankLattice.meet` over all inputs.
3. Call `ResidualPolicy.evaluate` and respect the ceiling it returns.
4. Emit a `TraceEntryCandidate` for the caller to append.
5. Return a typed `FailureCode` on any refusal; never raise.

## PR-4 binding

The gate lives in
[`src/taaqqul_slot_geometry/core/transition_gate.py`](../src/taaqqul_slot_geometry/core/transition_gate.py)
and is pure: `decide` reads values and returns a frozen
`TransitionVerdict`. It never appends to a `TraceLedger`, never
mutates the input graph, and never constructs the successor graph
(emission through `SlotGraph.construct` with
`GenerationSource.TRANSITION_VERDICT` is the audit wrapper's job,
PR-6).

`decide(input_graph, target_layer, evidence)` walks an ordered law;
a refusal at step *k* short-circuits the rest:

1. **Γ first** (docs/11 §11): a graph that does not close cannot
   move. A `Γ` refusal maps onto the transition vocabulary with
   `Γ`'s own `FailureCode` carried through —
   `INVALID → REJECTED`, `FORBIDDEN_LEAP → FORBIDDEN_LEAP`,
   `BLOCKED → BLOCKED`, `OPEN → DEFERRED`.
2. **Forbidden Straight-Line Registry consultation** (docs/04;
   docs/10; docs/16 §4 — bound in PR-5): the declared
   `source → target` layer pair is looked up in
   `CANONICAL_REGISTRY`; any `CERTIFICATE` target additionally
   meets the canonical *Evidence → Certainty* row. A registered
   line is `FORBIDDEN_LEAP` / `FORBIDDEN_STRAIGHT_LINE`, fatal
   before any retryable refusal, regardless of evidence strength.
3. **No ungated promotion** (docs/16 link 9): a graph not born from
   `TRANSITION_VERDICT` carrying a rank above
   `UNGATED_RANK_CEILING = HYPOTHESIS` claims a licence no gate
   granted — `REJECTED` / `RANK_PROMOTION_WITHOUT_GATE`.
4. **Evidence present** (precondition 1): an empty
   `EvidenceContract` is retryable — `DEFERRED` / `GATE_REQUIRED`.
5. **The §8 meet** (preconditions 2–3): the granted rank is exactly
   `RankLattice.meet(evidence_rank, input_graph.rank, gate_rank,
   ResidualPolicy.evaluate(residuals).ceiling)` — never higher,
   never synthesised.
6. **`APPROVED`** with that granted rank and no `FailureCode`.

Every verdict — approval or refusal — carries a `stage="gate"`
`TraceEntryCandidate` for the caller to append (precondition 4).
Constitutional refusals return named `FailureCode` values
(precondition 5); only programmer mistakes outside the declared
domain (`SlotGraph` / `Layer` / `EvidenceContract`, malformed gate
birth) raise `TypeError`, mirroring `gamma`'s domain guard.

`TransitionGate.gate_rank` is capped at
`GATE_RANK_CEILING = STRONG`: a `CERTIFICATE`-granting gate is the
`CertificationGate` (docs/04), reserved for a dedicated future PR.
With every meet input so bounded, `CERTIFICATE` is structurally
ungrantable through this gate.

Declared residuals of PR-4: successor-graph emission and the audit
wrapper stay in PR-6.

## PR-5 binding

PR-5 replaced the hard-coded `CERTIFICATE`-layer bar of step 2 with
the typed Forbidden Straight-Line Registry: `decide` consults
`CANONICAL_REGISTRY` from
[`src/taaqqul_slot_geometry/core/forbidden_lines.py`](../src/taaqqul_slot_geometry/core/forbidden_lines.py)
(docs/04 — PR-5 binding), so *every* registered line — not only the
certificate bar — binds fatally before the retryable evidence check.
The registry consultation refuses only registered lines: an
unregistered pair passes step 2 untouched and meets normally.

PR-5 names forbidden lines but opens no bridge: the
`CertificationGate` and every other `required_bridge` the rows name
remain declared residuals of their own future PRs, and
`CERTIFICATE` remains structurally ungrantable through this gate.

## PR-6 binding

PR-6 binds the emission half this document reserved. The pure
function `emit_successor(verdict, input_graph)` in
[`src/taaqqul_slot_geometry/audit/successor.py`](../src/taaqqul_slot_geometry/audit/successor.py)
is the only place a `TransitionVerdict` becomes a successor
`SlotGraph` (docs/17 §1, source 3): an `APPROVED` verdict yields
`SlotGraph.construct` with `GenerationSource.TRANSITION_VERDICT`,
the granted rank (never higher — emission cannot promote), the
declared `target_layer`, and a trace anchor that names the gate
(`{parent_anchor}/gate/{gate_name}`). Every non-`APPROVED` verdict
yields a refusal carrying the verdict's own `FailureCode`: only an
audit record remains. An approval about a *different* graph is
refused as `IDENTITY_BROKEN` (docs/16 link 2).

To support that anchor, the verdict now carries `gate_name` and
`target_layer`, and its `TraceEntryCandidate` records the split
`consulted_gamma_state` / `gate_transition_state` pair (docs/07 —
PR-6 binding). `TransitionState` moved to its own leaf module
(`core/transition_state.py`) so the ledger can type the split
without an import cycle. The gate itself is unchanged: `decide`
still never constructs the successor, never appends to a ledger,
and the `CertificationGate` and every other `required_bridge`
remain reserved for their own future PRs.
