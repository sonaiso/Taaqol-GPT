# PR-AUDIT Constitutional Description Template

Use the following text as the pull request description for the mandatory structural audit gate before V0.229.

```md
<!--
This template is binding. See docs/13_CONSTITUTIONAL_PR_GEOMETRY.md.
A PR that omits any of the sections below is OPEN by definition and
must not be merged. Green CI is not constitutional approval.
-->

## Constitutional Origin

What constitutional law does this PR branch from?
(Cite one or more of `docs/02..18`. Provide a stable link of the
form `docs/NN_FILE.md#section`.)

- Origin law: Constitutional PR Geometry + Constitutional Test Geometry + PR Chain Roadmap discipline
- Origin law reference (file#section): `docs/13_CONSTITUTIONAL_PR_GEOMETRY.md#constitutional-rules-for-pull-requests`, `docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md#constitutional-rules-for-tests`, `docs/14_PR_CHAIN_ROADMAP.md#pr-staging-do-not-collapse`

## Branch Scope

What single branch does this PR implement or document?

- Branch: `PR-AUDIT-STRUCTURAL-HIDDEN-ORACLE` (mandatory structural audit gate before V0.229)
- Branch of origin (the constitutional branch, not just the local
  label): Post-vertical hardening/integration discipline (no theorem extension)

## Chain Position

Where is this PR located in `docs/14_PR_CHAIN_ROADMAP.md`?

- Previous required PR: `USM-C3 Bounded Capability Evaluation Runtime` (done)
- Current PR (PR-N from docs/14): `PR-AUDIT` (pre-V0.229 admission gate; hardening PR, no theorem claim)
- Next permitted PR: `PR-127 / V0.229 Finite Quotient Foundation (FRP)` only if this audit closes as `PROVEN_FOR_MODEL`

## Allowed Scope

This PR may touch:

- Structural audit protocol only: hidden-oracle detection, forbidden-straight-line detection, gate-bypass detection, residual-visibility checks, trace-integrity checks, rank-policy checks, and explicit refusal taxonomy

## Forbidden Scope

This PR must not touch:

- FRP theorem/proof content, finite-quotient constructive proof steps, semantic/hukm layer expansion, or any runtime beyond audit boundary

## Output Boundary

This PR is allowed to produce:

- A constitutional audit verdict under bounded states: `PROVEN_FOR_MODEL` / `REFUTED` / `INCONCLUSIVE` / `BLOCKED`, with explicit trace and visible residuals

This PR is forbidden from producing (proven absent in the diff):

- Any FRP theorem claim, any cutoff theorem claim, any hidden residual pass, any direct tool/number-to-knowledge shortcut, any unlicensed rank promotion

## Rank / Residual / Trace Impact

- Does this PR introduce rank behavior? yes
- Does this PR introduce residual behavior? yes
- Does this PR introduce trace behavior? yes
- If any answer is yes, where is it covered by a constitutional test? Covered by constitutional audit tests that assert rank-ceiling enforcement, residual visibility invariants, and trace continuity/break refusal cases

## Constitutional Tests

List tests proving the PR branch remains inside its origin law.
These are tests written under
`docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md`, not bare unit tests. For
any test that exercises a link of the Identity-to-Truth Licensing
Chain (`docs/16`) or the SlotGraph Generation Law (`docs/17`), the
test must use `ConstitutionalChainTestCase` (`docs/12` §9), not
bare `ConstitutionalTestCase`.

- Structural pass test: full audit path executes through licensed gates only and returns bounded verdict with trace
- Hidden-oracle injection test: forced oracle shortcut is refused with named failure code
- Gate-bypass test: direct evidence-to-verdict path is refused with named failure code
- Residual-visibility test: hidden residual attempt is refused; residuals remain explicit
- Trace-integrity test: trace break attempt is refused; no approved output without trace
- Rank-policy test: out-of-gate rank promotion attempt is refused

## Negative Tests

List tests proving the forbidden neighbours of this branch remain
forbidden (the `even_if` shape, plus the
`forbidden_shortcut_assertions` field of any chain-test case).

- Even if all green unit checks pass, approve-state is denied when hidden-oracle signal appears
- Even if local outputs look correct, refusal is mandatory on forbidden straight-line path
- Even if evidence payload exists, refusal is mandatory when trace chain is incomplete
- Even if parser/runtime remains stable, refusal is mandatory on residual suppression attempt
- Forbidden shortcut assertions: no `Tool/Number -> Knowledge` jump; no `Evidence -> Certainty` jump

## Residuals After Merge

What is intentionally left open, and which future PR closes each
residual?

- FRP theorem for Arabic lower layers remains open; closed by `PR-127 / V0.229`
- Finite representative witness bounds remain open; closed by `PR-127`
- Cutoff theorem derivation for morphology/syntax remains open; closed by post-PR-127 theorem PRs

## Reviewer Checklist

- [ ] The PR has a constitutional origin (and a resolvable
      `origin law reference`).
- [ ] The PR is a branch, not a bundle.
- [ ] The PR is in the declared chain position.
- [ ] The PR does not exceed its allowed scope.
- [ ] The PR does not touch any forbidden scope.
- [ ] The PR has constitutional tests, not only unit tests.
- [ ] Every chain-test uses `ConstitutionalChainTestCase` where
      `docs/12` §9 requires it.
- [ ] Every rejection has a named `FailureCode` where applicable.
- [ ] No hidden residual can pass.
- [ ] No rank promotion happens outside a `TransitionGate`.
- [ ] Green CI is not treated as constitutional approval.
- [ ] **No runtime behavior is added before its law is ratified in
      `docs/`** (binds PR-2+ to docs 15/16/17).
```
