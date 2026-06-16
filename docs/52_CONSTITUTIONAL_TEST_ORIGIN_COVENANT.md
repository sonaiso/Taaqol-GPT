# 52 — Constitutional Test Origin Covenant

> **Status:** Constitutional law. Ratified in PV-T0.
> Constitutional origin: docs/12 (Constitutional Test Geometry),
> docs/13 (Constitutional PR Geometry),
> docs/49 (Meta-Language Boundary Covenant).
> This document is a **law-only covenant** that extends the test
> discipline of docs/12 with a mandatory origin-and-branch declaration
> for every test in the repository.
>
> This law does **not** introduce a runtime scanner, modify existing
> tests, add any carrier, enum, operation, or FailureCode
> implementation. It defines discipline only.

---

## §1 Governing principle (الجملة المركزية)

```text
كما لا مصطلح بلا أصل وفرع،
لا اختبار بلا أصل وفرع.

As no meta-term operates without origin and branch,
no test judges without origin and branch.
```

The constitutional test is not merely a passing assertion.
It is a **licensed transition proof**: evidence that a specific
constitutional invariant holds under a named law, along a declared
branch, within a bounded chain.

Green pytest is execution health.
A constitutional test is licensed transition proof.

---

## §2 The nine mandatory declarations

Every test written after PV-T0 must declare (or inherit from a
fixture/base class) the following nine fields:

```text
1. origin_law          — which constitutional law (docs/NN) the test
                         exercises or guards.
2. branch_of_origin    — which single branch of that law the test
                         examines (one branch per test, not a bundle).
3. invariant_under_test — the specific constitutional property being
                         proven or disproven.
4. expected_state      — the expected verdict or closure state
                         (PROVEN / REFUSED / specific ClosureState).
5. forbidden_neighbour — what adjacent output must remain absent
                         (may be empty if no neighbour applies).
6. failure_code        — the named FailureCode expected if the test
                         is a refusal test (mandatory for refusal
                         tests; omitted for success tests).
7. rank_expectation    — the rank ceiling that must not be exceeded
                         (mandatory for any test touching rank).
8. residual_expectation — the residual visibility rule in force
                         (mandatory for any test touching residuals).
9. trace_expectation   — what trace entry must appear or must not
                         appear (mandatory for any test touching trace).
```

> **Note:** Field 9 (trace_expectation) is listed as a separate
> mandatory field because trace discipline is constitutionally
> independent of rank and residual discipline.

---

## §3 The governing laws

```text
No test without origin.
No origin without branch.
No branch without invariant.
No invariant without expected pass/fail.
No refusal test without named FailureCode.
No rank test without rank ceiling.
No residual test without residual visibility rule.
No trace test without trace expectation.
```

These laws are binding on all tests written after PV-T0 merges.
They do not retroactively fail existing tests (see §5).

---

## §4 Test categories

Every test in the repository belongs to exactly one of the following
categories:

```text
Category 1: Constitutional tests
    Tests that prove a constitutional chain holds under a named law.
    These must declare all nine fields of §2.
    They use ConstitutionalTestCase or ConstitutionalChainTestCase
    (docs/12 §§6–9).

Category 2: Contract / surface tests
    Tests that prove a carrier or interface surface is correct
    without exercising the full chain. These must declare:
    origin_law, branch_of_origin, invariant_under_test,
    expected_state.
    They may omit forbidden_neighbour, rank/residual/trace
    expectations only if the surface being tested does not
    involve rank, residual, or trace.

Category 3: Regression tests
    Tests that prove a previously-identified defect remains fixed.
    These must declare: origin_law (the law whose violation was
    the defect), branch_of_origin, invariant_under_test,
    expected_state, and the failure_code that was incorrectly
    produced or missed before the fix.

Category 4: Support / fixture tests
    Tests of test infrastructure (helpers, factories, base classes).
    These must declare: origin_law = docs/12,
    branch_of_origin = "test infrastructure",
    invariant_under_test = the specific helper property.

Category 5: Smoke tests
    Minimal existence tests (import succeeds, module loads).
    These must declare: origin_law = docs/12,
    branch_of_origin = "smoke",
    invariant_under_test = "module existence".

Category 6: Orphan tests
    Tests that do not declare any origin. After PV-T0, new orphan
    tests are forbidden. Existing orphan tests are acknowledged as
    a deferred audit residual (see §5).
```

---

## §5 Transition discipline

```text
PV-T0 does not fail the existing test suite.
PV-T0 does not modify existing tests.
PV-T0 does not introduce a runtime scanner.
```

The transition from the current state to full compliance follows
three stages:

```text
Stage 1 (immediate — PV-T0 merge):
    All new tests written after PV-T0 must comply with §2/§3.
    Existing tests remain as-is; they carry an implicit
    ORPHAN_AUDIT_PENDING residual.

Stage 2 (deferred — PV-T0.1, separate PR):
    A test-origin scanner/meta-test may be introduced that
    verifies new tests comply. It must not fail existing
    orphan tests but may produce a report.

Stage 3 (gradual — ongoing):
    Existing orphan tests are audited and assigned origins
    as their surrounding code is touched by new PRs.
    No PR is required to audit all orphans at once.
```

---

## §6 Relationship to docs/12

This covenant **extends** docs/12, it does not replace it.

docs/12 defines:
- what a constitutional test is (chain-aware, not bare assertion)
- the ConstitutionalTestCase schema
- the ConstitutionalChainTestCase schema

This covenant (docs/52) adds:
- mandatory origin declaration for **all** test categories
- the category taxonomy (§4)
- the transition discipline (§5)
- the governing sentence linking test-origin to meta-term-origin

The relationship:

```text
docs/12 defines what a constitutional test must prove.
docs/52 defines that every test must declare its constitutional address.
```

---

## §7 Relationship to docs/49 (Meta-Language Boundary Covenant)

The parallel is intentional and constitutive:

```text
docs/49 §2: No meta-term without origin, branch, baʿith,
            wasf_muʾaththir, farq_qadih.
docs/52 §2: No test without origin, branch, invariant,
            expected_state, failure_code, rank/residual/trace.
```

The governing analogy:

```text
A meta-term that operates without declared origin
is an unlicensed terminological transfer.

A test that judges without declared origin
is an unlicensed constitutional verdict.
```

Both are refused by the same constitutional principle:
no judgment without a licensed path from evidence to conclusion.

---

## §8 Forbidden scope of PV-T0

This law explicitly forbids:

```text
- Runtime implementation of a test scanner
- Modification of any existing test file
- Introduction of any new FailureCode enum member
- Introduction of any new carrier or operation
- Any src/ change
- Any tests/ change
- Any Mabni, Mafhūm, Majāz, Naql, or GPTProposer content
- Any ArabicConditionsDAG or GovernmentServiceEngine content
```

PV-T0 is law only. Enforcement comes later (PV-T0.1 or subsequent).

---

## §9 Reviewer law

```text
A reviewer of PV-T0 checks:
1. The covenant does not introduce runtime code.
2. The covenant does not modify existing tests.
3. The covenant is consistent with docs/12 (extends, not contradicts).
4. The covenant is consistent with docs/49 (parallel structure).
5. The chain position is correct (after PV-M0.3, before PV-M1).
6. The CLAUDE.md and docs/14 markers are correct.
```

---

## §10 Gate condition for PV-M1

```text
No PV-M1 (Mabni Stability Boundary Law) may open until PV-T0 is
merged and stable.
```

Rationale: PV-M1 will require tests for dangerous meta-terms
(مبني، معرب، حرف معنى، اسم حرف، ضمير، اسم إشارة، تصريف، إعراب).
Those tests must comply with §2/§3 from their first commit.
If the test-origin discipline is not established before PV-M1,
the Mabni tests will be orphans by construction.

---

## §11 Reserved future steps

```text
PV-T0.1 — Test Origin Scanner (meta-test, enforcement)
    May introduce a pytest plugin or conftest check that verifies
    new tests declare their origin. Must not fail existing orphans.
    Separate PR. Not part of PV-T0.

PV-T0.2 — Orphan Audit Report (optional)
    May produce a report of existing orphan tests and their
    suggested origin assignments. Advisory only.
```

---

## §12 Binding sentence

```text
هذا العهد يثبت أن الاختبار حكمٌ.
والحكم لا ينعقد بلا أصل.
ولا أصل بلا فرع.
ولا فرع بلا ثابتٍ يُمتحن.

This covenant establishes that a test is a judgment.
And no judgment is valid without an origin.
And no origin without a branch.
And no branch without an invariant under examination.
```
