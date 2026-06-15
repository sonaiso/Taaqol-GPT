# 46 — Vertical Path Closure Law

> **Status:** Constitutional law. Ratified by PR-D10 (closure PR — no new
> runtime layer, no new carrier, no new enum, no horizontal branch).
> Binds every future PR that attempts to open a horizontal branch
> (majaz, mantuq, mafhum, naql, reference expansion, conditions DAG,
> GPT-proposer) — none may proceed until this law is merged. It is
> load-bearing.
>
> This document is the **closure certificate** for the minimum vertical
> path. It ships the `ConstitutionalVerticalChainTestCase` helper under
> `tests/support/` and the vertical path closure tests under
> `tests/test_vertical_path_closure.py`. It does not create new runtime
> carriers, does not create new operations, and does not execute
> anything.

## §1 Governing principle (ما يحفظ — what it preserves)

```text
No vertical closure without trace continuity.
No vertical closure without bounded rank.
No vertical closure without visible residuals.
No vertical closure without named refusals at every layer.
No vertical closure without presentation envelope preservation.
No vertical closure without identity continuity across layers.
No candidate-to-certificate leap.
No execution.
No horizontal branch before this closure.
```

The minimum vertical path is:

```text
MufradDalalahClosure
→ RelationClosure
→ IfadahCandidate
→ HukmCandidate
→ ManatCandidate
→ TanzilCandidate
→ AuditedTanzilBridge
```

This law proves that the column is one auditable system, not
independent islands. Every layer in the chain has:

* a law (docs/38 through docs/45),
* a runtime carrier (PR-D3 through PR-22-AUDIT),
* constitutional tests (PR-D3 through PR-22-AUDIT test modules),
* trace continuity to the next layer,
* rank bounded by the lattice meet,
* residuals visible (EXPLANATORY),
* named refusals with FailureCode on every rejection.

The governing sentence:

```text
لا توسع قبل الختم.
ولا ختم بلا أثر متصل.
ولا أثر بلا رتبة وبقايا وغلاف.
```

This vertical closure is the first executable instance of licensed
thought: no layer becomes the next without proof of conditions, trace,
residuals, rank, and boundary.

## §2 What this law opens

```text
PR-D10 — Vertical Path Closure (this PR).
         ConstitutionalVerticalChainTestCase under tests/support/.
         Vertical path closure tests under tests/test_vertical_path_closure.py.
         Amendment-13 in docs/14.
         Nothing else.
```

PR-D10 is a closure PR. It opens the **post-vertical planning phase**
only. No horizontal branch is automatically licensed by this closure.
Each post-vertical branch requires its own law, scope, forbidden
surface, tests, and chain position — proposed through a separate
Amendment PR.

## §3 What this law forbids

```text
No new runtime carrier.
No new enum.
No new operation.
No adapter changes.
No ModelClient changes.
No execution.
No fatwa.
No qada.
No final authority.
No certificate.
No Majaz / MajazVerdict / MajazLicense.
No Mantuq / MantuqClosure.
No Mafhum / MafhumCandidate.
No Naql / ManqulVerdict / ManqulLicense.
No ReferenceExpansion.
No ArabicConditionsDAG.
No GPTProposer.
No GovernmentServiceEngine.
No post-vertical branch implementation.
No candidate-to-certificate leap.
No rank promotion across the vertical walk.
No hidden residual at any step.
No trace discontinuity.
No presentation envelope loss.
```

A future PR that needs any horizontal branch must declare its own chain
position and origin law through a post-vertical roadmap Amendment.

## §4 Domain (المجال — where this law applies)

```text
Vertical path closure only.

It binds:
  * The minimum vertical path:
    MufradDalalahClosure → RelationClosure → IfadahCandidate →
    HukmCandidate → ManatCandidate → TanzilCandidate →
    AuditedTanzilBridge.
  * PR-D10 (this closure PR).
  * Every future PR that attempts a horizontal branch before
    this law is merged.

It does not bind:
  * Core kernel (core/) — the vertical path is in weight/ and audit/.
  * Adapter layer (audit/model_client.py, audit/adapter_guard.py) —
    adapters are unchanged by this closure.
  * Any pre-vertical layer (PR-0 through PR-19) — those are already
    closed by their own laws.
```

## §5 Evidence (الدليل — what justifies this closure)

1. **docs/38 through docs/45**: Each layer in the vertical path has a
   ratified law that declares its boundary, its forbidden surface, its
   evidence, its domain, and its failure conditions.
2. **PR-D3 through PR-22-AUDIT**: Each layer has a runtime
   implementation that passes constitutional tests.
3. **PR-22-AUDIT (merged)**: The final bridge connects
   TanzilCandidate to the audit surface, proving the column is
   operational end-to-end.
4. **Amendment-12 (ratified)**: Declared the vertical closure path
   and forbade horizontal branches before PR-D10.
5. **docs/04 (Forbidden Straight-Line Registry)**: The transitions
   `Candidate → Certificate`, `Judgment → Application`, and
   `Audit → Authority` remain forbidden. This closure does not
   relax any of them.
6. **docs/05 (Rank Lattice)**: Rank monotonicity across the chain
   is enforced by the lattice meet at every transition.

## §6 Closure conditions (binding on the vertical walk)

The vertical path is closed if and only if:

```text
1. Every layer produces a PROVEN verdict when inputs are valid.
2. Every transition preserves identity (trace_ref chain is continuous).
3. Every transition has evidence (no layer accepts without its inputs
   being PROVEN).
4. Every transition carries rank bounded by the lattice meet.
5. Residuals remain visible (EXPLANATORY) at every layer — no
   HIDDEN_FORBIDDEN, no BLOCKING passes silently.
6. Trace_ref is continuous from MufradDalalahClosure through
   AuditedTanzilBridge.
7. Presentation envelope (TanzilPresentationEnvelope) is preserved
   through the audit bridge.
8. Every forbidden neighbor remains absent (no horizontal branch
   symbols exported).
9. Every refusal carries a named FailureCode.
10. No candidate becomes a certificate.
11. No audit bridge implies execution or authority.
```

## §7 Failure conditions (الفشل — when closure fails)

The closure fails if any of:

```text
* Trace discontinuity at any layer transition.
* Rank promotion (output rank > input rank) at any layer.
* Hidden residual (ResidualKind.HIDDEN_FORBIDDEN) at any step.
* Blocking residual passes to the next layer.
* Presentation envelope dropped or mutated in audit bridge.
* Refusal without a named FailureCode.
* Any horizontal branch symbol exported before closure.
* Any candidate carries Certificate, FinalAuthority, Execution,
  Fatwa, Qada, or any execution-equivalent state.
* Any audit bridge implies execution or authority (not_execution,
  not_fatwa, not_qada, not_final_authority are all True).
```

## §8 Effect (الأثر — what changes when this law is ratified)

* The minimum vertical path is closed.
* Amendment-13 takes effect: horizontal branches may be planned through
  separate post-vertical roadmap PRs, but none are automatically
  licensed.
* The repository enters the **post-vertical planning phase**.
* No horizontal branch may proceed until it declares its own law,
  scope, forbidden surface, tests, and chain position.

After PR-D10 only:

```text
Post-vertical roadmap planning may begin.
Each horizontal branch requires its own Amendment PR.
No branch is licensed by this closure alone.
```

## §9 Constitutional invariants (binding on PR-D10)

* Vertical closure ≠ horizontal license.
* Vertical closure ≠ execution.
* Vertical closure ≠ certificate.
* Vertical closure ≠ authority.
* AuditedTanzilBridge ≠ Certificate.
* AuditedTanzilBridge ≠ Execution.
* AuditedTanzilBridge ≠ FinalAuthority.
* TanzilCandidate ≠ Execution.
* No layer in the vertical path produces meaning, reality, or ontology.
* Every layer in the vertical path is a candidate, never a final judgment.
* The vertical path is auditable: rank, residuals, trace are visible at
  every step.
* All operations in the vertical path are pure: no I/O, no ledger
  writes, no network, no filesystem, no clock.

## §10 Forbidden surface (mirror of §3, declared explicitly)

PR-D10 **must not** export, define, instantiate, alias, or reference:

* `Execution`, `ExternalAction`, `Enforcement`
* `Fatwa`, `Qada`, `FinalAuthority`, `DivineAuthorityClaim`
* `Certificate`, `FinalCertificate`
* `MajazVerdict`, `MajazLicense`
* `MantuqClosure`, `MafhumCandidate`
* `ManqulVerdict`, `ManqulLicense`
* `ReferenceExpansion`
* `ArabicConditionsDAG`
* `GPTProposer`, `T5Proposer`
* `GovernmentServiceEngine`
* `RealityApplication`, `RealityVerification`
* `FinalMeaning`, `Meaning`, `OntologicalClaim`
* `PropositionTruthValue`, `FreeReasoning`
* `AuthorityClaim`, `NormativeJudgment`
* Any new carrier, enum, or operation not already ratified.

## §11 Amendment-13 (bundled with PR-D10)

```text
Amendment-13 — Vertical Path Closure and Horizontal Freeze Release

After PR-D10 merges:
* The minimum vertical path is constitutionally closed.
* The horizontal-branch ban (Amendment-12) is formally discharged.
* Horizontal branches may be proposed only through separate
  post-vertical roadmap PRs.
* No horizontal branch is automatically licensed by this closure.
* Each post-vertical branch requires:
  - Its own law document.
  - Its own scope declaration.
  - Its own forbidden surface.
  - Its own constitutional tests.
  - Its own chain position (declared through an Amendment PR).
```

## §12 Deferred residuals (carried by PR-D10)

| Name                                        | Note                                                  |
|---------------------------------------------|-------------------------------------------------------|
| `HORIZONTAL_BRANCHES_DEFERRED`              | All horizontal branches remain deferred post-closure. |
| `POST_VERTICAL_ROADMAP_REQUIRED`            | Post-vertical planning requires a separate Amendment. |

These residuals are EXPLANATORY: they document what remains outside the
vertical closure without blocking it.

## §13 Reviewer law (binding on PR review)

```text
PR-D10 is a closure PR.
It does not create new runtime carriers.
It does not create new enums or operations.
It does not open any horizontal branch.
It does not execute anything.
It does not convert candidates to certificates.
It does not produce meaning, reality, or ontology.
It does not modify adapters or ModelClient.
No PR-D10 may ship code under src/ beyond what is required for
   test support exports.
```

A reviewer who finds any of the following in a PR-D10 submission must
reject:

* Any new file under `src/` (beyond minimal test support if needed)
* Any new carrier dataclass
* Any new enum member not already ratified
* Any new operation function
* Any adapter or audit code change
* Any external execution, enforcement, or authority claim
* Any horizontal branch (majaz, mantuq, mafhum, naql, GPT-proposer,
  reference expansion, conditions DAG)
* Any candidate-to-certificate conversion
* Any rank promotion in tests
* Any hidden residual in tests
