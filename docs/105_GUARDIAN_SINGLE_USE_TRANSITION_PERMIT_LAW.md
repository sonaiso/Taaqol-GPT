# 105 — Guardian Single-Use Transition Permit Law (PR-E)

> Status: constitutional execution-governor boundary + bounded runtime document.
> Scope: issue a guardian permit from hardened preflight outcomes without opening execution.
> Snapshot date: 2026-08-04.

## §1 Constitutional role

`PR-E` is the post-`PR-D.1` successor step.
It opens permit issuance only, with single-use and bounded trace discipline.

This step does not open execution, postflight, commit, or canonical mutation.

## §2 Permit issuance contract

```text
TransitionPermitIssuanceRequest = <
  permit_request_id,
  preflight_result,
  requested_output_types,
  ttl_seconds,
  issue_at_epoch_seconds,
  trace_ref
>

TransitionPermit = <
  permit_id,
  permit_nonce,
  request_id,
  contract_id,
  allowed_output_types,
  consumption_limit: 1,
  issued_rank,
  issued_at_epoch,
  expires_at_epoch,
  preflight_trace_ref,
  permit_trace_ref,
  contract_digest,
  policy_digest
>

TransitionPermitIssuanceResult = <
  permit_request_id,
  state,
  failure_codes,
  permit,
  trace_ref
>
```

State vocabulary is closed to:

```text
GRANTED / DEFERRED / REFUSED
```

## §3 Issuance guarantees

```text
Permit issuance requires admissible PR-D.1 preflight output.
Permit output types must be a subset of preflight contract_declared_output_types.
Permit is single-use by schema (consumption_limit: 1).
Permit rank remains Rank.ZERO in this branch.
Permit issuance emits a dedicated permit trace.
No execution from permit issuance.
No postflight or commit from permit issuance.
No semantic/hukm/truth/reality closure from permit issuance.
```

## §4 Forbidden surface

RUNTIME_NOT_OPENED = {
  transition_execution,
  postflight_evaluation,
  commit_decision,
  canonical_mutation,
  semantic_truth_closure,
  hukm_closure,
  reality_certificate
}

This step opens permit issuance only.
