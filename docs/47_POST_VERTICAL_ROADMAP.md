# 47 — Post-Vertical Roadmap

> **Status:** Constitutional planning document. Ratified in PV0.
> Constitutional origin: PR-D10 Vertical Path Closure Law (docs/46),
> Amendment-13 (horizontal-branch ban discharge).
>
> This document plans; it does not implement. No post-vertical runtime
> branch may start before this document is merged.

---

## 1. Closure statement

The minimum vertical path is constitutionally closed:

```text
MufradDalalahClosure
→ RelationClosure
→ IfadahCandidate
→ HukmCandidate
→ ManatCandidate
→ TanzilCandidate
→ AuditedTanzilBridge
```

This path was closed by PR-D10 (docs/46) and verified by
`ConstitutionalVerticalChainTestCase` (45 tests in 9 groups).
The closure proves:

- trace continuity across all layers
- rank monotonicity (no rank exceeds its predecessor's ceiling)
- residual visibility (no hidden residual passes through)
- envelope preservation (candidate ≠ certificate ≠ execution)
- named refusals at every rejection point
- no horizontal-branch leakage

The vertical closure is the first executable instance of the
governing principle:

> No output without a SlotGraph.
> No SlotGraph without Constitutional Geometry.
> No Closure without Gamma.
> No Output without Trace.

---

## 2. No automatic branch license

PR-D10 does **not** automatically license any horizontal branch.

```text
الإقفال لا يفتح الفروع تلقائيًا.
بل يجعل فتحها مسؤولًا.
```

The horizontal-branch ban (Amendment-12) is formally discharged by
Amendment-13, but this discharge means only that proposing a branch
is no longer a `FORBIDDEN_LEAP`. It does **not** mean any branch is
pre-approved.

Every post-vertical branch still requires:

- its own law document (docs/N)
- a declared chain position (in docs/14)
- a bounded scope
- a forbidden surface
- constitutional tests (under docs/12 rules)
- named refusals (FailureCode taxonomy)
- rank / residual / trace discipline
- a separate Amendment PR to register it in the chain

---

## 3. Branch families

The deferred branches are organized into families. No family opens
entirely at once; each individual branch within a family requires its
own law-first step.

### Family A — Dalālah and Bayān branches

```text
PV-A1  Manṭūq Boundary Law (docs/N, law only)
PV-A2  Manṭūq Closure Candidate
PV-A3  Mafhūm Boundary Law (docs/N, law only)
PV-A4  Mafhūm Candidate
PV-A5  Haqīqah Attempt Law (docs/N, law only)
PV-A6  Haqīqah / Majāz Transfer Gate
PV-A7  Naql Transfer Gate
PV-A8  Qarīnah Gate
```

Prerequisite: closed vertical path (PR-D10). These branches operate
on the existing column; they do not create new layers below Tanzīl.

### Family B — Reference and Composition Expansion

```text
PV-B1  Reference Expansion Law (docs/N, law only)
PV-B2  Pronoun Resolution Candidate
PV-B3  Operator Expansion Candidate
PV-B4  Relation Type Expansion
PV-B5  Iʿrāb Relation Expansion
```

Prerequisite: closed vertical path + at least one Family A branch
closed (relation expansion presupposes knowing whether mantūq or
mafhūm is active).

### Family C — Arabic Conditions Infrastructure

```text
PV-C1  Arabic Cognitive Constraint Detection Law (docs/N, law only)
PV-C2  Arabic Conditions DAG Design
PV-C3  Carrier / Gate Expansion
PV-C4  Weight Geometry Expansion
PV-C5  57-Condition Detector (or subset)
```

Prerequisite: at least Family A fully closed and Family B started.
These branches widen the constitutional surface; they must not be
attempted until the dalālah/bayān branches prove the horizontal
pattern stable.

### Family D — AI-Assisted Proposer

```text
PV-D1  GPT Proposer Boundary Law (docs/N, law only)
PV-D2  Proposer Protocol (ModelClient-derived)
PV-D3  Residual Suggestion Assistant
PV-D4  Trace Explanation Generator
```

Prerequisite: closed vertical path + Adapter Boundary Law (docs/18)
already ratified. These operate strictly under:

```text
AI proposes.
Algebra governs.
Audit records.
```

No proposer may produce a verdict, approve a rank promotion, hide a
residual, or write a trace entry.

### Family E — Industrial Applications

```text
PV-E1  Application Layer Boundary Law (docs/N, law only)
PV-E2  Rule DSL Design
PV-E3  Government Service Declarative Engine
PV-E4  Public-Sector Workflow Generator
```

Prerequisite: Family A + Family B closed, Family D started. These
consume the full vertical path and must not modify it.

---

## 4. Admission rule

Every post-vertical branch requires **all** of the following before
its implementation PR may be opened:

1. **Law document** — a numbered `docs/N_*.md` file declaring the
   branch's constitutional origin, scope, forbidden surface, and
   refusal taxonomy.
2. **Chain position** — an Amendment PR adding the branch to
   `docs/14_PR_CHAIN_ROADMAP.md` with explicit predecessor and
   successor.
3. **Scope declaration** — what files, modules, and layers the
   branch is allowed to touch.
4. **Forbidden surface** — what the branch may never produce,
   touch, or assume.
5. **Constitutional tests** — tests under `docs/12` rules with
   origin, branch, chain, expected verdict, forbidden outputs,
   rank ceiling, residual visibility, trace, and FailureCode.
6. **Residual policy** — what residuals the branch leaves open and
   which future step closes them.
7. **Rank / trace discipline** — the branch must declare its
   maximum rank and prove trace continuity with the vertical path.

A branch that omits any of these is constitutionally OPEN and must
not be merged.

---

## 5. WIP rule

```text
Only one post-vertical branch may be open at a time.
```

This prevents fragmentation. The governing principle:

> لا تعالج التفكك بمزيد من التفكيك.
> (Do not treat fragmentation with more fragmentation.)

A branch is "open" from the moment its law-only PR is merged until
its closure PR (or integration PR) is merged. While a branch is
open, no other branch's law-only PR may be merged.

Exception: corrective PRs (`.1`, `.2` suffix) to the currently-open
branch are always permitted.

---

## 6. Suggested first branch

The recommended first post-vertical branch is **PV-A1: Manṭūq
Boundary Law** — the closest horizontal extension to the existing
vertical path. Manṭūq (explicit indication) operates directly on
IfādahCandidate output and has the smallest distance from the
existing audit surface.

This is a suggestion, not a binding decision. The actual first
branch will be chosen by the maintainer after PV0 is merged.

---

## 7. What PV0 does NOT license

PV0 does **not** license:

- any `src/` code
- any new carriers, enums, or operations
- any GPT integration
- any government service engine code
- any majāz, mafhūm, or mantūq implementation
- any Arabic Conditions DAG runtime
- any new proof-theory runtime
- any adapter or audit change
- any schema expansion

PV0 plans; it does not implement.

---

## 8. Governing sentences

```text
بعد الختم لا يبدأ التوسع،
بل يبدأ ترتيب التوسع.

After closure, expansion does not begin —
the ordering of expansion begins.
```

```text
أغلقنا العمود.
لا نكسر الإغلاق بالاستعجال.
نكتب خارطة ما بعد الإقفال أولًا.

We closed the column.
We do not break the closure by haste.
We write the post-closure roadmap first.
```
