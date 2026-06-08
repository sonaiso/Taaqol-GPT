# 13 — Constitutional PR Geometry

> **Status:** Constitutional law. Ratified in PR-1B. Every later PR
> opened against this repository is bound by this document. No PR may
> be merged that violates these rules, regardless of CI status.

This document closes a loophole that neither the
[Mathematical Slot Geometry Laws](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md)
nor the
[Constitutional Test Geometry](12_CONSTITUTIONAL_TEST_GEOMETRY.md)
can close on their own:

```text
A pull request can be locally well-formed,
have green CI, and still be a constitutional leap.
```

The remedy is the same shape as the kernel itself:

```text
A PR is a SlotGraph.
It has a center, a boundary, a rank, residuals, and a trace.
It is subject to a Gamma-like verdict.
```

The governing statement:

```text
No PR without an Origin.
No PR without a Branch.
No PR without a Chain position.
No PR without a declared Boundary.
No PR without Constitutional Tests.
No green CI as Constitutional Success.
```

---

## 1. PR as a constitutional object

Conceptually, every PR is a tuple:

```text
PRSlotGraph = ⟨
    center               — the single branch the PR exists to prove,
    openings             — the files/layers the PR is allowed to touch,
    closure              — what the PR actually closes,
    boundary             — the declared allowed and forbidden scope,
    rank                 — the maturity of the contribution
                           (docs, carrier, kernel, gate, adapter),
    residuals            — what is intentionally left open after merge,
    trace                — commits, tests, docs, and the chain
                           position they claim,
⟩
```

A "Γ for PRs" is implicit in the review checklist below. A PR is:

```text
OPEN                — does not yet declare origin/branch/chain.
MINIMALLY_CLOSED    — exact branch implemented with no leaking residuals.
PERFORATED_CLOSED   — exact branch implemented with declared,
                      non-blocking residuals.
BLOCKED             — touches a forbidden layer or names.
INVALID             — claims completion that is not in fact implemented,
                      or mixes layers.
FORBIDDEN_LEAP      — implements a future PR or jumps a layer.
```

This is identical in spirit to the closure verdicts in
[`03_GAMMA_CLOSURE_CONTRACT.md`](03_GAMMA_CLOSURE_CONTRACT.md). The
analogy is not decorative; it is the reason the project requires the
same discipline on the development process that it requires on the
runtime engine.

## 2. Required declarations on every PR

Every PR description must declare, in this order:

```text
1.  Constitutional Origin
       The named law (from docs/02..14) the PR branches from.
2.  Branch Scope
       The single branch the PR implements or documents.
3.  Chain Position
       Previous required PR; current layer; next permitted PR.
4.  Allowed Scope
       Files, directories, and constitutional layers this PR may
       touch.
5.  Forbidden Scope
       Files, directories, and constitutional layers this PR must
       not touch.
6.  Output Boundary
       Concrete outputs (modules, exports, behaviors, docs) the PR
       is allowed to produce, and the symmetric list of outputs it
       must not produce.
7.  Rank / Residual / Trace Impact
       Does this PR introduce rank behavior? residual behavior?
       trace behavior? If yes, where is each covered by a
       constitutional test?
8.  Constitutional Tests
       Tests proving the PR branch stays inside its origin law.
9.  Negative Tests
       Tests proving the forbidden neighbours remain forbidden.
10. Residuals After Merge
       What is intentionally left open, and which future PR closes
       each residual.
```

A PR description that omits any of these sections is **OPEN** by
definition and must not be merged.

The mandatory template lives in
[`.github/pull_request_template.md`](../.github/pull_request_template.md).

## 3. Chain position is binding

A PR may only implement its **declared** chain position. The
authoritative chain lives in
[`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md).

```text
A PR that ships work belonging to a later position
is a FORBIDDEN_LEAP, not a "bonus".
```

The only licit way to change the chain is to open an **Amendment
PR** whose entire branch is the chain change. Amendment PRs are
themselves bound by this document.

## 4. Scope discipline

The allowed and forbidden scopes are not advisory. They are part of
the PR's identity.

```text
A PR that touches a forbidden file or a forbidden constitutional
layer is BLOCKED, regardless of how clean its diff looks.
```

In particular, until the PR-2 kernel lands no PR may introduce a
`SlotGraph`, `Slot`, `gamma`, `TraceLedger`, or `TransitionGate`
binding. The PR-1 carriers are already guarded by the existing
`tests/test_package_imports.py`.

## 5. Tests, not assertions, are the contract

A PR's constitutional tests must obey
[`12_CONSTITUTIONAL_TEST_GEOMETRY.md`](12_CONSTITUTIONAL_TEST_GEOMETRY.md).
A PR with green CI but no constitutional tests for the branches it
claims is **INVALID**.

```text
Green CI ≠ Constitutional Approval.
CI is a trace artifact. The verdict is review against this document.
```

## 6. Residuals must be declared

A PR that closes its branch but leaves work undone must enumerate
the residuals it leaves and the PR that owns each residual. Hiding
work that is "almost done" is the PR-level analogue of a hidden
residual under [`06_RESIDUAL_POLICY.md`](06_RESIDUAL_POLICY.md) and
collapses the verdict to `INVALID`.

## 7. Reviewer checklist

The reviewer checklist that the PR template binds to:

```text
- [ ] The PR has a constitutional origin.
- [ ] The PR is a branch, not a bundle.
- [ ] The PR is in the declared chain position.
- [ ] The PR does not exceed its allowed scope.
- [ ] The PR does not touch any forbidden scope.
- [ ] The PR has constitutional tests, not only unit tests.
- [ ] Every rejection has a named FailureCode where applicable.
- [ ] No hidden residual can pass.
- [ ] No rank promotion happens outside a Gate.
- [ ] Green CI is not treated as constitutional approval.
```

## 8. Verdict shorthand

```text
PR.center      = the single branch under test
PR.boundary    = allowed and forbidden scope declarations
PR.rank        = layer reached (docs, carriers, kernel, gates, adapters)
PR.residuals   = declared open work after merge
PR.trace       = commits + constitutional tests + docs
Γ(PR)          = the reviewer checklist applied honestly
```

A merged PR is a `TraceEntryCandidate` whose closure is the merge
itself. The repository's value depends on that closure being
verifiable, not merely green.

---

## Cross-references

- The kernel laws: [`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md).
- The test-side discipline: [`12_CONSTITUTIONAL_TEST_GEOMETRY.md`](12_CONSTITUTIONAL_TEST_GEOMETRY.md).
- The chain roadmap: [`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md).
- The PR template that enforces this document at submission time:
  [`../.github/pull_request_template.md`](../.github/pull_request_template.md).
- The agent operating instructions in [`../CLAUDE.md`](../CLAUDE.md).
