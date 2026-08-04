# 104 — Carrier-Bound Transition Preflight Hardening Law (PR-D.1)

> Status: constitutional hardening boundary + bounded runtime document.
> Scope: harden transition preflight with carrier-bound input identity, evidence-instance binding, registry snapshot pins, and trace extension.
> Snapshot date: 2026-08-04.

## §1 Constitutional role

`PR-D.1` is a hardening successor to `PR-D`.
It preserves preflight-only behavior and adds carrier-bound admissibility discipline.

No execution is opened in this step.

## §2 Hardened request/result contract

```text
TransitionExecutionPreflightHardeningRequest = <
  request_id,
  contract_id,
  domain,
  input_carrier,
  evidence_refs,
  residual_kinds,
  requested_rank,
  preserved_invariants,
  expected_domain_registry_version,
  expected_contract_registry_version,
  expected_contract_digest,
  trace_ref,
  request_epoch_seconds
>

TransitionExecutionPreflightHardeningResult = <
  request_id,
  contract_id,
  state,
  failure_codes,
  visible_residual_kinds,
  contract_declared_output_types,
  granted_rank,
  request_trace_ref,
  preflight_trace_ref,
  parent_trace_ref,
  domain_registry_version,
  contract_registry_version,
  contract_digest,
  policy_digest
>
```

State vocabulary remains closed to:

```text
ADMISSIBLE / ADMISSIBLE_WITH_RESIDUALS / DEFERRED / BLOCKED / INVALID
```

## §3 Hardening guarantees

```text
No execution from preflight hardening.
No permit/certificate issuance from preflight hardening.
No hidden residuals; residual visibility remains mandatory.
No rank promotion at preflight stage (granted_rank remains Rank.ZERO).
RequestedRankValidity is checked, but GrantedRank remains Rank.ZERO.
EvidenceKindPresent is not sufficient: evidence_refs must bind to input identity and contract.
FieldNamePresent is not sufficient: required field-value references must exist.
Preflight trace must be extended: request_trace_ref -> preflight_trace_ref (parent preserved).
Decision replay requires registry versions + contract digest + policy digest.
```

## §4 Decision priority law

The runtime decision priority is explicit and closed:

```text
INVALID > BLOCKED > DEFERRED > ADMISSIBLE_WITH_RESIDUALS > ADMISSIBLE
```

## §5 Forbidden surface

RUNTIME_NOT_OPENED = {
  transition_execution,
  permit_issuance,
  certificate_issuance,
  semantic_truth_closure,
  hukm_closure,
  reality_certificate,
  rank_promotion
}

This step hardens preflight eligibility only.
