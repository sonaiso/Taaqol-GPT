# 101 — Canonical Domain Registry Law (PR-B)

> Status: constitutional boundary + carrier-only runtime document.
> Scope: unify cross-branch basic kind vocabularies without opening execution.
> Snapshot date: 2026-08-03.

## §1 Constitutional role

`PR-B` establishes a single canonical registry surface for the shared kind set:

```text
DomainId / TransitionKind / CarrierKind / EvidenceKind / ResidualKind / RankChannel
```

The registry is a typed vocabulary boundary. It is not an execution gate.

## §2 Registry contract

The canonical registry is declared as one immutable carrier:

```text
CanonicalDomainRegistry = <
  version,
  trace_ref,
  domains,
  transition_kinds,
  carrier_kinds,
  evidence_kinds,
  residual_kinds,
  rank_channels
>
```

All tuples are non-empty, typed, and duplicate-free.

## §3 Constitutional guarantees

```text
No transition execution without dedicated gate/runtime branch.
No certificate issuance from vocabulary declaration alone.
No semantic/hukm/truth claim from registry membership.
No hidden residual vocabulary expansion.
```

The registry only standardizes names; it does not authorize effects.

## §4 Non-goals (forbidden surface)

RUNTIME_NOT_OPENED = {
  transition_execution,
  permit_issuance,
  postflight_approval,
  commit_semantics,
  semantic_truth_closure,
  hukm_closure
}

This step does not replace branch-local contracts; it supplies a canonical shared index.
