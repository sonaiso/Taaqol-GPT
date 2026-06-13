# 21 — Carrier Declaration Is Not Verdict Law

> **Status:** Constitutional law. Ratified in PR-10B (corrective PR;
> no new layer). This document clarifies what the PR-10 carrier
> surface **is not** and prevents downstream misreading. It binds
> every PR that consumes, extends, or interprets a weight carrier.

## 1. The governing principle

```text
A declared carrier field is not a verdict.
A depicted surface is not a judgment.
A candidate name is not a license.
```

PR-10 shipped frozen carriers — depicted outputs of stages that do
not yet operate. Every carrier is a **declaration** of shape: it
says *what would need to exist* for the next stage to be requested,
not that any gate has approved it. This law fixes the reading:

```text
Declared carrier fields are not verdicts.
PathKind is not PathGateProof.
OriginalExtraMap is not ExtraLetterLicense.
WeightReadinessCandidate is not WeightFitCandidate.
Mizan is not weighing authority.
Typed residuals are not residual clearance.
TraceRef is not ledger judgment.
Candidate rank is not promotion.
```

## 2. Discriminating identities

| PR-10 carrier field               | Is                           | Is NOT                              |
|------------------------------------|------------------------------|-------------------------------------|
| `PathCandidate.kind`              | declared candidate kind      | PathGateVerdict / PathGateProof     |
| `OriginalExtraMap.assignments`    | depicted split candidate     | ExtraLetterLicense / AugmentationProof |
| `WeightReadinessCandidate`        | chain-completion declaration | WeightFitCandidate / weigh() input  |
| `Mizan`                           | image landing surface        | weighing authority / fit scorer     |
| `MawzunCandidate`                 | thing-to-be-weighed carrier  | weighed / fit / scored result       |
| `carrier.residuals`               | typed residual tuple at birth | ResidualGovernance / residual clearance |
| `carrier.trace`                   | TraceRef at birth            | TraceLedger append / audit commit   |
| `carrier.rank == CANDIDATE`       | birth rank (ceiling)         | gate rank / promotion / license     |

## 3. The constitutional reading rule

Every interpreter of a PR-10 carrier must observe:

```text
PathCandidate(kind=ROOT)
  ⇒ may request RootPathGate (PR-11)

but:

PathCandidate(kind=ROOT)
  ⇏ RootPathGateProof

OriginalExtraMap(assignments=(...))
  ⇒ depicts which letters stand as original/extra

but:

OriginalExtraMap(assignments=(...))
  ⇏ ExtraLetterLicense
  ⇏ AugmentationProof

WeightReadinessCandidate(surface=...)
  ⇒ the chain is complete

but:

WeightReadinessCandidate(surface=...)
  ⇏ WeightFitCandidate
  ⇏ WeightOpening (until Ω judges in PR-12)

Mizan(landing_space="PatternSpace")
  ⇒ the instrument exists as a carrier

but:

Mizan(landing_space="PatternSpace")
  ⇏ weigh() authority
  ⇏ fit computation
  ⇏ PatternTable lookup

carrier.residuals == ()
  ⇒ declared empty at birth

but:

carrier.residuals == ()
  ⇏ residual clearance (Ω judgment is PR-12)
  ⇏ "no residuals exist" (they may yet be discovered by gates)

carrier.rank == Rank.CANDIDATE
  ⇒ no rank promotion has occurred

but:

carrier.rank == Rank.CANDIDATE
  ⇏ gate-level rank (HYPOTHESIS, LICENSED, ...)
  ⇏ approval
  ⇏ constitutional certainty
```

## 4. Registered misreadings (forbidden interpretations)

The following readings are constitutionally invalid and must be
refused at review with the named failure:

| Misreading                                         | FailureCode                      |
|----------------------------------------------------|----------------------------------|
| PathKind value as PathGateProof                    | `FORBIDDEN_STRAIGHT_LINE`        |
| OriginalExtraMap as ExtraLetterLicense             | `FORBIDDEN_STRAIGHT_LINE`        |
| WeightReadinessCandidate as WeightFitCandidate     | `FORBIDDEN_STRAIGHT_LINE`        |
| Mizan as weighing authority                        | `RANK_PROMOTION_WITHOUT_GATE`    |
| Typed residuals as residual clearance              | `HIDDEN_RESIDUAL`                |
| TraceRef as audit ledger commit                    | `TRACE_MISSING`                  |
| Candidate rank as gate-level rank                  | `RANK_PROMOTION_WITHOUT_GATE`    |

## 5. What enters only through later PRs

```text
PR-11:  PathGateProof, PathGateVerdict, PathGateResiduals
PR-12:  Ω judgment (FunctionalClosure / WeightOpening / Residual),
        μ chain operations, residual governance
PR-13:  weigh(), WeightFitCandidate, SlotAlignmentComputation
PR-14:  PatternTable, Lexicon, SamāʿEvidence, QiyāsEvidence
```

None of these may be inferred from a PR-10 carrier alone.

## 6. Constitutional summary

```text
PR-10 لم يفتح الوزن.
بل أغلق أبواب القفز قبل الوزن.

أثبت أن هناك حوامل محفوظة:
بقيمة، ونوع، وأصل، وهوية، ومجال، ونطاق، ورتبة، وبقايا، وأثر.

لكنه لم يحكم المسار.
ولم يزن.
ولم يحسب ملاءمة.
ولم يعط مدلولًا.
ولم يثبت فئة.
ولم يرخص زيادة.

نوع المسار المصرّح به ليس حكمًا بترخيص المسار.
خريطة الأصل والزيادة ليست رخصة زيادة.
مرشح جاهزية الوزن ليس مرشح ملاءمة الوزن.
الميزان ليس سلطة وزن.
البقايا المصنّفة ليست تبرئة بقايا.
مرجع الأثر ليس حكم سجل.
رتبة المرشح ليست ترقية.
```

## 7. Binding scope

This law binds:

- Every PR that reads or extends a weight carrier (PR-11+)
- Every test that asserts over a weight carrier field
- Every review that evaluates constitutional correctness of the
  weight branch

A test, PR, or review that treats a carrier declaration as a verdict
is a `FORBIDDEN_STRAIGHT_LINE` regardless of CI status.
