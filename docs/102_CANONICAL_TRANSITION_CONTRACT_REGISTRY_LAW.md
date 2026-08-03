# 102 — Canonical Transition Contract Registry Law (PR-C)

> Status: constitutional boundary + carrier-only runtime document.
> Scope: declare one canonical source-of-truth registry for transition contracts.
> Snapshot date: 2026-08-03.

## §1 Constitutional role

`PR-C` establishes a single canonical registry surface for transition-contract declarations
licensed by earlier law boundaries, including:

```text
TC-01..TC-06 (docs/99)
TC_SR..TC_SD (docs/100)
```

The registry is a typed contract declaration boundary. It is not an execution gate.

## §2 Registry contract

The canonical registry is declared as one immutable carrier:

```text
CanonicalTransitionContractRegistry = <
  version,
  trace_ref,
  contracts: tuple[CanonicalTransitionContract]
>

CanonicalTransitionContract = <
  contract_id,
  domain,
  transition_kind,
  source_slot,
  target_slot,
  required_conditions,
  required_fields,
  outputs,
  evidence_kinds,
  residual_kinds,
  allows_multi_candidate,
  law_ref,
  trace_ref
>
```

All tuples are non-empty, typed, and duplicate-free.

## §3 Constitutional guarantees

```text
No transition execution from registry declaration alone.
No permit or certificate issuance from contract rows alone.
No semantic/hukm/truth claim from contract membership.
No hidden residual vocabulary expansion.
```

The registry standardizes contract declarations and prevents drift between duplicated local tables.

## §4 Non-goals (forbidden surface)

RUNTIME_NOT_OPENED = {
  transition_execution,
  gate_approval,
  permit_issuance,
  certificate_issuance,
  semantic_truth_closure,
  hukm_closure,
  reality_certificate
}

This step does not replace branch-local gates; it supplies one canonical contract source.
