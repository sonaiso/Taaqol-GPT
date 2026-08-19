# 111 — Independent Postflight Guardian Law (PR-G)

> Status: constitutional execution-governor boundary document (law-only).
> Scope: evaluate `ExecutionCandidate` through an independent postflight guardian before any commit or certificate path.
> Snapshot date: 2026-08-19.

## §1 Constitutional role

`PR-G` is the post-`PR-F` successor step.
It opens independent postflight evaluation only.

This step does not open commit, canonical mutation, certificate issuance, or semantic/hukm/truth/reality closure.
This step introduces no runtime code.

## §2 Postflight guardian contract (law surface)

```text
PostflightEvaluationRequest = <
  evaluation_request_id,
  execution_candidate,
  permit_snapshot,
  contract_snapshot,
  domain_snapshot,
  evidence_snapshot,
  observed_invariants,
  observed_residual_kinds,
  trace_ref
>

PostflightVerdict = <
  verdict_id,
  state,
  failure_codes,
  residual_kinds,
  continuity_report_ref,
  trace_ref,
  rank: Rank.ZERO
>
```

## §3 Closed verdict vocabulary

`ExecutionCandidate` may transition only to:

```text
POSTFLIGHT_APPROVED
POSTFLIGHT_REJECTED
POSTFLIGHT_SUSPENDED
```

No other postflight state is licensed in this step.

## §4 Mandatory re-check surface

The independent postflight guardian must re-check at minimum:

1. `input_identity` continuity.
2. `requested_output_type` continuity.
3. invariant continuity (`observed_invariants`).
4. residual visibility continuity (`observed_residual_kinds`).
5. trace continuity (`trace_ref` extension).
6. rank discipline (`Rank.ZERO` ceiling in this branch).
7. permit/contract continuity (permit id, contract id, digest continuity).

## §5 Minimum refusal/suspension families

At minimum, the guardian names and exposes:

1. `POSTFLIGHT_INPUT_IDENTITY_MISMATCH`
2. `POSTFLIGHT_OUTPUT_TYPE_MISMATCH`
3. `POSTFLIGHT_INVARIANT_BREAK`
4. `POSTFLIGHT_TRACE_CONTINUITY_BROKEN`
5. `POSTFLIGHT_RANK_ABOVE_ZERO`
6. `POSTFLIGHT_PERMIT_CONTRACT_CONTINUITY_BROKEN`
7. `POSTFLIGHT_BLOCKING_RESIDUAL_PRESENT`
8. `POSTFLIGHT_EVIDENCE_CONTINUITY_MISSING`

## §6 Forbidden surface in PR-G

```text
FORBIDDEN_FROM_PR_G = {
  commit_decision,
  canonical_mutation,
  certificate_issuance,
  semantic_truth_closure,
  hukm_closure,
  reality_certificate,
  rank_promotion
}
```

`PR-G` is an evaluation boundary only.

## §7 Runtime admission dependency (docs/110 binding)

Opening runtime for this law remains gated by docs/110:

```text
LawRatified(111)
and ProofObjectsPass(111)
and CountermodelsPass(111)
and ReconstructionStable(111)
and NegativeRegressionStable(111)
and ResidualRegressionStable(111)
```

Admission order remains:

```text
Law -> ProofObjects -> Countermodels -> Regression -> RuntimeAdmission
```

## §8 Constitutional non-overreach theorem

```text
Not(POSTFLIGHT_APPROVED) => Not(Commit)
```

```text
NoCanonicalMutationBeforeCommit.
```

```text
ExecutionCandidate.postflight_required = True
```
