# 23 — Pre-Weight Chain Operations Law

> **Status:** Constitutional law. Ratified in PR-12; chain position
> ratified by Amendment-3
> ([`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) §2). This
> document is the law the pre-weight μ chain operations and the Ω
> residual governance implement.
>
> PR-10 gave the carrier.
> PR-10B forbade the carrier from claiming a verdict.
> PR-11 established the path court.
> PR-11B clarified visible carry is not Ω clearance.
> PR-12 introduces transition authority.

## 1. The governing principle

```text
PR-11 = visibility without governance.
PR-12 = governance without weighing.

VisibleResidual is audit visibility.
ΩResidualGovernance is transition authority.

PR-11 sees and carries.
PR-12 judges and governs.

PR-12 does not discover weight.
PR-12 prepares the lawful object that later weight discovery may inspect.
```

## 2. The Ω residual governance

The Ω judgment is a pure function over a `PreWeightSurface` that
classifies every residual and determines whether transition authority
is granted:

```text
Ω : (residuals, surface_rank) → ResidualGovernanceVerdict
```

### 2.1 The five Ω classifications

```text
BLOCKING          — the residual blocks transition entirely.
                    No forward movement is licensed.

DEFERRABLE        — the residual may be carried forward as a
                    deferred bounded candidate. It does not block
                    but constrains.

NON_BLOCKING      — the residual does not prevent transition.
                    It is carried visibly but without authority.

HIDDEN_FORBIDDEN  — the residual was hidden or invisible.
                    Transition is rejected/blocked. A hidden
                    residual may never pass silently.

EXPLANATORY       — an audit-only residual. It carries no
                    transition authority by itself but remains
                    visible for trace purposes.
```

### 2.2 The governance verdicts

```text
GRANTED           — transition authority is granted. All residuals
                    are non-blocking or explanatory. The μ chain
                    may proceed.

DEFERRED          — transition is deferred. At least one DEFERRABLE
                    residual constrains the output. Only a deferred
                    bounded candidate is produced.

BLOCKED           — transition is blocked. At least one BLOCKING
                    residual prevents forward movement.

REJECTED          — transition is rejected. A HIDDEN_FORBIDDEN
                    residual was detected or a constitutional
                    violation is present.
```

### 2.3 The governance invariants

```text
1. Visible residual is not Ω clearance.
   Seeing a residual (PR-11) is not clearing it (PR-12).

2. HIDDEN_FORBIDDEN cannot pass silently.
   A hidden residual results in REJECTED, never GRANTED.

3. BLOCKING prevents transition.
   A blocking residual results in BLOCKED, never GRANTED.

4. DEFERRABLE produces deferred bounded candidate only.
   It does not block, but constrains the output.

5. NON_BLOCKING may pass visibly.
   It does not block and does not constrain.

6. EXPLANATORY has no transition authority by itself.
   It is visible for audit, never an input to transition logic.

7. Ω is pure: no I/O, no ledger writes, no time reads.

8. Ω applies the same taxonomy as ResidualKind (docs/06).
   No new classification beyond the five above.
```

## 3. The μ chain operations

The μ chain is the ordered implementation of docs/20 §§4–11:

```text
μ_seq              → SyllableSequenceCandidate
μ_boundary         → WordBoundaryCandidate
μ_word_carrier     → WordCarrierCandidate
μ_root_stem        → RootStemCandidate (ROOT path) or continuation
μ_original_extra   → OriginalExtraMap
μ_ops              → OperationTraceCandidate
μ_weight_readiness → WeightReadinessCandidate (Ω = WeightOpening only)
```

### 3.1 Per-step invariants

Every μ step must:

```text
1. Accept only the previous licensed output, not raw declarations.
2. Require PathGateVerdict where applicable (μ_root_stem).
3. Apply ΩResidualGovernance before transition.
4. Return a bounded candidate or named refusal.
5. Never raise rank beyond the permitted ceiling.
6. Preserve trace references without becoming audit ledger commits.
7. Expose residual decisions visibly.
8. Map every refusal onto a named FailureCode from the existing
   taxonomy (no new codes).
```

### 3.2 The rank ceiling

```text
PR-12 operates within the pre-weight rank space:
the μ chain rank ceiling is HYPOTHESIS (the same as
PATH_GATE_RANK_CEILING from PR-11).

No μ step may promote rank. The bounded meet at the path gate
(PR-11) is the only rank-setting authority in the pre-weight chain.
```

## 4. Forbidden forms

```text
forbidden: weigh()
forbidden: WeightFitCandidate
forbidden: LicensedWeight
forbidden: DiscoverWeightAlgorithm (unless strictly deferred)
forbidden: lexical / samāʿ / qiyās licensing
forbidden: extra-letter licensing
forbidden: meaning, agency, hukm, or reality fields
forbidden: new runtime dependencies
forbidden: audit ledger implementation
forbidden: new FailureCode members
forbidden: new forbidden-line registry rows
forbidden: adapter or audit layer changes
```

## 5. What PR-12 produces and what it does not

```text
PR-12 produces:
  - ResidualGovernanceVerdict (the Ω verdict)
  - μ step result candidates
  - WeightReadinessCandidate (pre-weighing readiness, not weight fit)
  - Named refusals using existing FailureCode taxonomy
  - Constitutional tests for each μ step and Ω behavior

PR-12 does not produce:
  - Weight fit
  - Weight discovery
  - Licensed weight
  - Meaning, semantics, or ontological claims
  - Lexical or grammatical licenses
```

## 6. The golden formulation

```text
VisibleResidual is audit visibility.
ΩResidualGovernance is transition authority.

ظهور البقايا شرط تتبع.
وحكم Ω شرط انتقال.

PR-12 لا يكتشف الوزن.
بل يهيئ حاملًا مرخصًا يمكن أن يُفحص وزنيًا لاحقًا.
```

## 7. Binding scope

This law binds:

- Every PR that reads, extends, or consumes the μ chain output
- Every PR that invokes or extends Ω governance
- Every test that asserts over μ or Ω behavior
- Every review that evaluates PR-12 constitutional correctness

A test, PR, or review that confuses visible carry with Ω clearance,
or that treats a μ step output as a weight fit, is a
`FORBIDDEN_STRAIGHT_LINE` regardless of CI status.
