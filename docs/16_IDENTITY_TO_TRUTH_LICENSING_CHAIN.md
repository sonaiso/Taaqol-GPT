# 16 — Identity-to-Truth Licensing Chain

> **Status:** Constitutional law. Ratified in PR-1C. Every later PR
> that introduces internal processing inside a `SlotGraph` is bound
> by this document; no later PR may relax it.

This document closes a loophole that the
[Mathematical Slot Geometry Laws](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md)
state in §2–§7 but do not chain explicitly:

```text
A SlotGraph can be well-formed,
its slots can be filled,
and an implementation can still slide
from identity straight to truth.
```

The remedy is to fix a single, ordered licensing chain that every
entity inside a `SlotGraph` must traverse. Each link in the chain
licenses the next; no link is allowed to deliver the next without
its predecessor being satisfied.

The governing statement:

```text
الهوية تُحفظ.
الثبات يُصان.
المطابقة تُعيَّن.
التضمن يُكشف.
الكمون يُرخَّص.
الانفتاح يُضبط.
الإغلاق يُثبت.
الالتزام يُستخرج.
المرشح يُختبر.
والحقيقة لا تثبت إلا بدليل.
```

In English:

```text
Identity is preserved.
Stability is maintained.
Matching is assigned.
Inclusion is uncovered.
Potentiality is licensed.
Opening is controlled.
Closure is established.
Implication is extracted.
Candidate is tested.
Truth holds only by evidence.
```

---

## 1. Why an explicit chain is needed

A construction that builds a `SlotGraph` and then asserts a verdict
like `MINIMALLY_CLOSED` without traversing the licensing chain
collapses several distinct moves into one. Each collapse is a
forbidden straight line.

Without an explicit chain, the following slides become tempting:

```text
Identity     → Truth
Matching     → Meaning
Potentiality → Actuality
Opening      → Closure
Closure      → Certificate
Candidate    → Truth
```

Each of these is a constitutional refusal. They must be enumerated
in the registry that lands in PR-5, and they must be detectable as
named refusals in any binding implementation of `Γ` or `Gate`.

## 2. The ten licensing links

The chain is fixed and ordered. An implementation **must not** skip
or re-order links.

```text
1.  Identity            — the entity's identity claim is preserved.
2.  Stability           — the identity is stable under licensed ops.
3.  Matching            — the entity is matched to its declared role.
4.  Inclusion           — the entity's containment relations are
                          made explicit.
5.  Potentiality        — the entity's admissible fillings are
                          declared and licensed.
6.  Opening             — an opening is controlled by its boundary.
7.  Closure             — closure is established under §5 of doc 11.
8.  Implication         — implications licensed by closure are
                          extracted, never assumed.
9.  Candidate           — a candidate is produced and tested.
10. Evidence-bound Truth — truth holds only by evidence through a
                          TransitionGate that satisfies Rank and
                          Residual policy.
```

This chain is the entity-level dual of `Γ` in
`docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md` §7. `Γ` orders the
verdict; this chain orders the *internal processing* that leads
to a verdict.

## 3. Per-link refusal mapping

Each link binds to one or more `FailureCode` members already declared
in `core/failure_taxonomy.py` (PR-1A). Where no current carrier
exists, the chain only **names** the refusal; the PR-2+ amendment
that introduces the matching carrier must keep the name stable.

```text
1.  Identity
       Failure carrier (PR-1A): IDENTITY_BROKEN, CENTER_MISSING.
       Forbidden line:           Identity → Truth.

2.  Stability
       Failure carrier (PR-1A): IDENTITY_BROKEN.
       Forbidden line:           Stability → Truth.

3.  Matching
       Failure carrier (PR-1A): BOUNDARY_MISSING, SCOPE_MISSING.
       Forbidden line:           Matching → Meaning.

4.  Inclusion
       Failure carrier (PR-1A): DOMAIN_MISSING.
       Forbidden line:           Inclusion → Meaning.

5.  Potentiality
       Failure carrier (PR-1A): UNLICENSED_OPENING.
       Forbidden line:           Potentiality → Actuality.

6.  Opening
       Failure carrier (PR-1A): UNLICENSED_OPENING,
                                REQUIRED_SLOT_EMPTY.
       Forbidden line:           Opening → Closure (without Γ).

7.  Closure
       Failure carrier (PR-1A): HIDDEN_RESIDUAL,
                                BLOCKING_RESIDUAL_PRESENT,
                                OUTPUT_EXCEEDS_LAYER.
       Forbidden line:           Closure → Certificate.

8.  Implication
       Failure carrier (PR-1A): RANK_EXCEEDS_CEILING.
       Forbidden line:           Implication → Truth (without Gate).

9.  Candidate
       Failure carrier (PR-1A): RANK_PROMOTION_WITHOUT_GATE.
       Forbidden line:           Candidate → Truth.

10. Evidence-bound Truth
       Failure carrier (PR-1A): FORBIDDEN_STRAIGHT_LINE,
                                GATE_REQUIRED.
       Forbidden line:           Evidence → Certainty (the canonical
                                 forbidden straight line of doc 04).
```

A link whose failure carrier above is marked *(reserved for PR-2+)*
must not be invented in PR-1C: this PR is docs-only and the
`FailureCode` enum is frozen against unrelated additions until PR-2.

If a future PR needs a more specific carrier (for instance, a
distinct `IMPLICATION_WITHOUT_LICENSE` code), it must extend the
enum in the PR whose branch is exactly that extension, never as a
side-effect of another PR.

## 4. The six new forbidden straight lines

The following lines are introduced by this chain and must be merged
into the registry that lands in PR-5. None of them may be
implemented as a direct transition.

```text
| Forbidden transition       | Why it is forbidden                           | Required bridge                  |
| Identity → Truth           | Identity preservation is not a truth verdict. | Gamma + Gate + Evidence + Rank.   |
| Matching → Meaning         | Role assignment is not meaning.                | Signification chain + Gate.        |
| Potentiality → Actuality   | Admissibility is not filling.                  | Opening control + Closure + Gate.  |
| Opening → Closure          | An opening is not its closure without Γ.       | Γ then Gate.                       |
| Closure → Certificate      | Closure is boundary satisfaction, not truth.   | Rank lattice + Gate.               |
| Candidate → Truth          | A candidate is not a certificate.              | Certification gate + Evidence.     |
```

Each row above is `FORBIDDEN_STRAIGHT_LINE` until the row's required
bridge is opened by a future PR. Until then, the matching transition
must return that `FailureCode`.

## 5. Where the chain runs

The chain runs inside every `SlotGraph` for every entity that:

- is declared as a `Slot` value,
- is declared in the `Center` as the identity claim,
- is computed by an `Operation` (`Ω`),
- is consumed by a `TransitionGate` (when the gate lands in PR-4).

It does not run outside `SlotGraph`. Pre-`SlotGraph` data is governed
by the Textual Communication Entry Law (`docs/15`) and the SlotGraph
Generation Law (`docs/17`).

## 6. Anti-collapse rules

These rules are mandatory. A PR that violates any of them is
`BLOCKED` regardless of CI status.

```text
no-shortcut:    No implementation may bind link N to link N+2
                without binding N+1.
no-rename:      A link may not be renamed away from the ten names
                listed in §2.
no-merge:       Two links may not be merged into a single function
                whose return value is the union of their refusals.
no-promotion:   A link may not promote its output's rank; only a
                TransitionGate may, and only bounded by the lattice
                meet (docs/11 §8).
named-refusal:  Every refusal returns a FailureCode member.
no-silence:     A link may not silently return None to skip its
                successor; missing = refuse.
```

## 7. Test-side obligation

Every constitutional test that exercises any link of this chain must
declare it explicitly via the `ConstitutionalChainTestCase` schema
introduced in PR-1C (see `docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md`
§9). The declared `chain_position` field must name the link under
test, and the `forbidden_shortcut_assertions` field must list the
direct transitions the test proves remain forbidden.

A test that exercises link N without proving the forbidden N → N+2
shortcut remains forbidden is a partial pass, not a constitutional
pass.

## 8. Short constitutional summary

```text
الهوية لا تساوي الحقيقة.
المطابقة لا تساوي المعنى.
الكمون لا يساوي الفعل.
الانفتاح لا يساوي الإغلاق.
الإغلاق لا يساوي اليقين.
المرشح لا يساوي الشهادة.
ولا حقيقة إلا بدليل عبر بوّابة.
```

In English:

```text
Identity is not truth.
Matching is not meaning.
Potentiality is not actuality.
Opening is not closure.
Closure is not certainty.
Candidate is not certificate.
And no truth holds without evidence through a Gate.
```

---

## Cross-references

- The mathematical statement: [`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md)
  §2–§10.
- The `Γ` ordering this chain mirrors:
  [`03_GAMMA_CLOSURE_CONTRACT.md`](03_GAMMA_CLOSURE_CONTRACT.md) and
  [`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md) §7.
- The textual entry that feeds this chain:
  [`15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md`](15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md).
- The SlotGraph generation law that builds the host of this chain:
  [`17_SLOTGRAPH_GENERATION_LAW.md`](17_SLOTGRAPH_GENERATION_LAW.md).
- The test-side schema for chain-tests:
  [`12_CONSTITUTIONAL_TEST_GEOMETRY.md`](12_CONSTITUTIONAL_TEST_GEOMETRY.md) §9.
- The forbidden straight-line surface:
  [`04_FORBIDDEN_STRAIGHT_LINES.md`](04_FORBIDDEN_STRAIGHT_LINES.md).
- The PR-chain position of this document:
  [`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md) — PR-1C.
