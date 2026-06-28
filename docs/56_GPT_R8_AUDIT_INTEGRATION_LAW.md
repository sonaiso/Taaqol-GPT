# 56 — GPT-R8 Audit Integration Law

> **Status:** Constitutional law document. Ratified in **GPT-R8L**.
> This is a **law-only** document. It defines how
> `GPTAnswerReasonablenessVerdict` (GPT-R7) is to be carried by
> `AuditedAnswer` (PR-6 / docs/01) **without** breaking the
> `ModelClient` black-box boundary (docs/01) or the Adapter Boundary
> Law (docs/18). It does **not** add runtime code, does **not**
> mutate `AnswerAudit.audit()`, and does **not** introduce new
> `FailureCode` members in the global registry. Those changes,
> if any, belong to the runtime PR (**GPT-R8**) that this law licenses.
>
> Constitutional origin:
> - docs/01 (Black-Box Boundary)
> - docs/07 (Trace Ledger)
> - docs/18 (Adapter Boundary Law)
> - docs/46 (Vertical Path Closure Law)
> - docs/47 (Post-Vertical Roadmap)
> - docs/54 (GPT Answer Reasonableness Objective Law)
> - docs/55 (Knowledge Origins Boundary Law)

---

## §1 What GPT-R8L Closes and What It Opens

```text
GPT-R8L closes:
  The licensing question for how a bounded GPT-R7
  reasonableness verdict may be carried by the AnswerAudit
  shell.

GPT-R8L opens:
  GPT-R8 (the runtime PR) — and only GPT-R8. No other branch
  is licensed by this law.

GPT-R8L does NOT close:
  - The runtime integration itself (that is GPT-R8).
  - Certificate / authority semantics (forbidden at every layer).
  - The hallucination leak ports (those remain governed by
    src/taaqqul_slot_geometry/gpt/hallucination_leak_closure.py
    pre-audit surfaces and the existing FailureCode entries).
```

This document is binding for the GPT-R8 runtime PR and for any
later PR that touches `AnswerAudit`, `AuditedAnswer`, or any
`ModelClient` adapter while a GPT reasonableness verdict is in
play.

---

## §2 The Six Inviolable Integration Boundaries

GPT-R8 (runtime) **must** preserve all six of the following
boundaries. A runtime PR that violates any one of them is a
`FORBIDDEN_LEAP` regardless of CI status.

```text
B1  ModelClient stays a black box.
    The verdict is computed from claim-graph + evidence + R6 gates
    only. The model's hidden reasoning, confidence, logits, or
    internal state never participate (docs/01).

B2  AnswerAudit owns the only TraceLedger writes.
    GPT-R8 must not move ledger writes into core/ or gpt/.
    The audit shell appends, the kernel returns candidates.

B3  AuditedAnswer keeps its existing birth invariants.
    The successor / gate_state / failure_code / rank invariants
    defined by AuditedAnswer.__post_init__ remain unchanged.
    Any reasonableness field is additive and must respect the
    same successor-iff-APPROVED discipline.

B4  No certificate, no authority, no truth.
    REASONABLE is procedural reasonableness, not truth (docs/55
    §1.2). GPT-R8 must reject any code path that promotes a
    reasonableness verdict into a certificate or an absolute
    truth claim. `certificate_allowed` stays False, always.

B5  Residuals stay visible.
    Every reasonableness residual carried by AuditedAnswer must
    be enumerable and printable; none may be silently dropped
    by the audit shell.

B6  Trace continuity is mandatory.
    The reasonableness verdict's trace_ref must be appended in
    constitutional order (after `gamma`, after `gate`, before or
    inside the existing `audit` entry — never replacing them).
```

---

## §3 The Adapter Boundary (docs/18) Stays Intact

```text
ADAPTER LAW (docs/18) declares ModelClient as the only seam
between the audit shell and any concrete LLM. GPT-R8L extends
this declaration with the following clarifications:

  - A reasonableness verdict is NEVER produced by a ModelClient
    adapter. The adapter still returns a string answer; the
    verdict is computed downstream of the adapter, inside
    AnswerAudit (or a caller of AnswerAudit), from declared
    R6 inputs.

  - AdapterGuard contract continues to hold: judging stays
    static, adapters stay swap-equivalent under the contract,
    and no adapter may inspect or override a reasonableness
    verdict to license its own output.

  - The runtime PR (GPT-R8) MUST NOT add a new method to the
    ModelClient protocol. The protocol surface stays exactly
    one method: complete(prompt: str) -> str.
```

---

## §4 Licensed Integration Shapes for GPT-R8

GPT-R8 (runtime) is free to choose exactly **one** of the
following two integration shapes. Both are licensed by this law;
no third shape is licensed.

### §4.1 Shape A — Additive Field on `AuditedAnswer`

```text
AuditedAnswer gains one additional immutable field carrying a
licensed GPT-R7 verdict surface. The field is OPTIONAL at the
type level (None when reasonableness was not run) and is
checked by AuditedAnswer.__post_init__ with the same
schema-error discipline used today.

When the field is present:
  - its integration_status is PRE_AUDIT_VERDICT (R7) being
    consumed by R8: the runtime PR must declare the consumption
    transition explicitly;
  - its trace_ref must be present;
  - its certificate_allowed must remain False;
  - its rank must not exceed the AuditedAnswer.rank;
  - its residuals augment, not replace, the audit residuals.
```

### §4.2 Shape B — Sibling Wrapper Over `AuditedAnswer`

```text
A separate carrier (for example `ReasonablenessAuditedAnswer`)
wraps an existing AuditedAnswer plus a GPTAnswerReasonablenessVerdict.

The wrapper is born only from a fully constructed AuditedAnswer
and a fully constructed verdict; it never re-runs gamma, never
re-runs the gate, never re-runs R6, and never mutates the
underlying AuditedAnswer. It exposes the same residual-visibility
and trace-continuity guarantees defined in §2.
```

Either shape is acceptable. The runtime PR must declare which
shape it adopts and must justify the choice with a short
trade-off note in its Amendment entry in `docs/14`.

---

## §5 Forbidden Outputs

GPT-R8 (runtime) **may not** produce any of the following:

```text
- AnswerCertificate, ReasonablenessCertificate, TruthCertificate
- AuthorityRecord, AbsoluteTruthVerdict
- A "REASONABLE → APPROVED" auto-promotion path that bypasses
  the existing TransitionGate
- A new ModelClient method or any adapter-side reasonableness hook
- A bypass that lets a model adapter override or rewrite a
  reasonableness verdict
- A ledger write that hides residuals or skips the gamma → gate
  → audit order
- A path that consumes R7 before R6 has produced a
  ReasonablenessGateReport
- A new global FailureCode that duplicates an existing R6/R7
  named refusal
```

If a new named refusal is genuinely required, it must be added
under the existing R6/R7 family (for example by extending
`ReasonablenessGateKind` semantics), not by widening the global
`FailureCode` registry from inside the audit shell.

---

## §6 Forbidden Straight Lines

GPT-R8 binds the following inverse-tests on top of the existing
Forbidden Straight-Line Registry (docs/05). The runtime PR
**must** include at least one constitutional test per line.

```text
- ModelClient.complete -> Reasonableness verdict
    (no straight line from raw text to verdict)
- Adapter -> Reasonableness verdict
    (no straight line from a swappable adapter to verdict authority)
- Reasonableness verdict -> Certificate
    (no straight line from procedural reasonableness to certified truth)
- Reasonableness verdict -> Approved successor
    (no straight line bypassing the existing TransitionGate)
- AuditedAnswer -> Reasonableness verdict
    (the audit shell does not synthesize a verdict; it carries one)
- Pre-audit verdict -> Final audit verdict
    (PRE_AUDIT_VERDICT is not the audit verdict; it is its input)
```

---

## §7 Residual Vocabulary (Local, Non-Global)

GPT-R8 **may** name local residual kinds for the integration
surface, but it **may not** widen the global residual policy. The
following names are reserved for the runtime PR's local
vocabulary and may not be used anywhere else:

```text
RESIDUAL_REASONABLENESS_DEFERRED
    The audit shell could not run R6/R7 because an upstream
    input (gate report, origin binding, evidence contract) was
    deferred.

RESIDUAL_NEEDGATE_NOT_OPENED
    The NeedGate (docs/54 §2.3) did not open the Arabic chain,
    so any Arabic-conditional residual remains explicitly
    unopened — not silently dropped.

RESIDUAL_R7_NOT_CONSUMED
    A GPT-R7 verdict was produced but not consumed by the audit
    shell (the audit ran without it). The audit record must
    declare this explicitly rather than imply silent acceptance.
```

Any other residual the runtime PR may want to introduce must be
named in its Amendment entry and must remain local to the
GPT-R8 surface.

---

## §8 Constitutional Tests Required by GPT-R8

The runtime PR (GPT-R8) **must** ship at least the following
constitutional tests (docs/12 + docs/52):

```text
T1  AuditedAnswer surface unchanged invariants:
    every existing AuditedAnswer schema-error path still fires.

T2  No ModelClient protocol mutation:
    inspecting ModelClient still reveals exactly one method
    (complete), and adapters remain swap-equivalent.

T3  Reasonableness ⇒ procedural:
    a REASONABLE verdict NEVER yields an APPROVED successor by
    itself; the TransitionGate still gates the successor.

T4  Residual visibility under integration:
    when a verdict is carried by the audit record, every
    OriginResidual on the verdict appears in an enumerable
    surface on the audit record, with no silent drops.

T5  Trace continuity under integration:
    gamma → gate → audit ordering is preserved; if a verdict
    trace_ref is appended, it is appended in an order that is
    explicitly declared by the runtime PR and asserted in tests.

T6  Forbidden-leap refusal:
    constructing an AuditedAnswer that bundles a verdict whose
    certificate_allowed is True is refused with a named
    FailureCode (no silent acceptance).

T7  Inverse test for each Forbidden Straight Line in §6.
```

Tests must follow `ConstitutionalTestCase` discipline (docs/52):
each must declare `origin_law=docs/56`, `branch_name=GPT-R8` (or a
local sub-branch), and a `constitutional_chain` that walks
gamma → gate → audit → reasonableness verdict.

---

## §9 KPI Surface for GPT-R8

The runtime PR will be measured against the existing GPT
reasonableness KPI table (docs/54 §7) plus the following
integration-specific KPIs:

| KPI | Target |
|-----|--------|
| AuditedAnswer schema invariants preserved | 100% (no existing test regresses) |
| ModelClient protocol arity unchanged | 1 method (complete) — exactly |
| Reasonableness → APPROVED auto-promotions | 0 |
| Residual silent drops at integration boundary | 0 |
| Trace continuity (gamma → gate → audit) | 100% across new and existing audits |
| Certificate / authority promotions | 0 |
| New global FailureCode members | 0 (local naming only) |

---

## §10 Binding Declarations

```text
1. This document is binding for the GPT-R8 runtime PR and for
   any later PR that touches AnswerAudit, AuditedAnswer, or the
   ModelClient protocol while a GPT reasonableness verdict is
   in play.

2. The runtime PR (GPT-R8) MUST cite this document by name in
   its commit message and in its Amendment entry in docs/14.

3. The six inviolable integration boundaries (§2), the adapter
   boundary clarifications (§3), the two licensed integration
   shapes (§4), the forbidden outputs (§5), the forbidden
   straight lines (§6), and the local residual vocabulary (§7)
   are constitutional and may not be modified without an
   Amendment PR.

4. No global FailureCode expansion is licensed by this law.
   No certificate / authority semantics are licensed by this
   law. No mutation of the ModelClient protocol is licensed by
   this law.

5. docs/53 methodology, docs/54 objective law, and docs/55
   knowledge-origins boundary remain binding — this document
   extends them with the audit-integration boundary, it does
   not replace them.

6. GPT-R8L licenses GPT-R8 and nothing else. CLOSE-3 through
   CLOSE-6, DAL-A1+, LAFZI-B0+, and LAW-E0 are NOT licensed
   by this law and remain governed by their own admission rules.
```
