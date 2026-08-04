# 106 — Permit Consumption and Execution Candidate Law (PR-F)

> Status: constitutional execution-governor boundary + bounded runtime document.
> Scope: consume one issued permit atomically and emit `ExecutionCandidate` only.
> Snapshot date: 2026-08-04.

## §1 Constitutional role

`PR-F` is the post-`PR-E` successor step.
It opens single-atomic permit consumption plus bounded execution-candidate emission.

This step does not open postflight approval, commit, canonical mutation, or semantic/hukm/truth closure.

## §2 Consumption/execution contract

```text
PermitLifecycleSnapshot = <
  permit_id,
  state in {ISSUED, CONSUMED, EXPIRED, REVOKED, SUPERSEDED},
  consumed_nonces,
  revoked_permit_ids
>

CurrentRegistrySnapshot = <
  expected_contract_registry_version
>

TransitionExecutionRequest = <
  execution_request_id,
  permit,
  permit_lifecycle,
  input_carrier_snapshot,
  input_identity_pin,
  executor_identity,
  authorized_executors,
  requested_operation,
  requested_output_type,
  output_candidate_ref,
  observed_invariants,
  observed_residual_kinds,
  current_time_epoch_seconds,
  current_registry_snapshot,
  trace_ref
>

ExecutionCandidate = <
  execution_id,
  permit_id,
  input_identity,
  requested_operation,
  requested_output_type,
  output_candidate_ref,
  operation_trace_ref,
  observed_invariants,
  observed_residual_kinds,
  execution_status: EXECUTED,
  postflight_required: True,
  rank: Rank.ZERO
>

TransitionExecutionResult = <
  execution_request_id,
  state,
  failure_codes,
  consumed_nonce,
  lifecycle_transition,
  execution_candidate,
  trace_ref
>
```

State vocabulary is closed to:

```text
EXECUTED / DEFERRED / REFUSED
```

## §3 Boundary guarantees

```text
Permit must be in ISSUED lifecycle state to execute.
Permit nonce replay is refused.
Permit expiry is enforced at consumption time.
Contract digest pin must match current canonical registry computation.
Input identity pin must match the provided input carrier snapshot.
Requested operation must match the permit contract transition kind.
Requested output type must be permitted by the issued permit.
Executor must be in authorized_executors.
Successful consumption is atomic in decision form: ISSUED -> CONSUMED.
Execution output in PR-F is candidate-only (ExecutionCandidate).
No postflight approval from PR-F.
No commit decision from PR-F.
No rank promotion in PR-F (rank remains Rank.ZERO).
```

## §4 Forbidden surface

RUNTIME_NOT_OPENED = {
  postflight_approval,
  commit_decision,
  canonical_mutation,
  certificate_issuance,
  semantic_truth_closure,
  hukm_closure,
  reality_certificate,
  rank_promotion
}

This step opens permit consumption and execution-candidate emission only.
