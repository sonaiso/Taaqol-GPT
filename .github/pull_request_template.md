<!--
This template is binding. See docs/13_CONSTITUTIONAL_PR_GEOMETRY.md.
A PR that omits any of the sections below is OPEN by definition and
must not be merged. Green CI is not constitutional approval.
-->

## Constitutional Origin

What constitutional law does this PR branch from?
(Cite one or more of `docs/02..18`. Provide a stable link of the
form `docs/NN_FILE.md#section`.)

- Origin law:
- Origin law reference (file#section):

## Branch Scope

What single branch does this PR implement or document?

- Branch:
- Branch of origin (the constitutional branch, not just the local
  label):

## Chain Position

Where is this PR located in `docs/14_PR_CHAIN_ROADMAP.md`?

- Previous required PR:
- Current PR (PR-N from docs/14):
- Next permitted PR:

## Allowed Scope

This PR may touch:

-

## Forbidden Scope

This PR must not touch:

-

## Output Boundary

This PR is allowed to produce:

-

This PR is forbidden from producing (proven absent in the diff):

-

## Rank / Residual / Trace Impact

- Does this PR introduce rank behavior? yes/no
- Does this PR introduce residual behavior? yes/no
- Does this PR introduce trace behavior? yes/no
- If any answer is yes, where is it covered by a constitutional test?

## Constitutional Tests

List tests proving the PR branch remains inside its origin law.
These are tests written under
`docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md`, not bare unit tests. For
any test that exercises a link of the Identity-to-Truth Licensing
Chain (`docs/16`) or the SlotGraph Generation Law (`docs/17`), the
test must use `ConstitutionalChainTestCase` (`docs/12` §9), not
bare `ConstitutionalTestCase`.

-

## Negative Tests

List tests proving the forbidden neighbours of this branch remain
forbidden (the `even_if` shape, plus the
`forbidden_shortcut_assertions` field of any chain-test case).

-

## Residuals After Merge

What is intentionally left open, and which future PR closes each
residual?

-

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
