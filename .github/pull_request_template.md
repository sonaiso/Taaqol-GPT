<!--
This template is binding. See docs/13_CONSTITUTIONAL_PR_GEOMETRY.md.
A PR that omits any of the sections below is OPEN by definition and
must not be merged. Green CI is not constitutional approval.
-->

## Constitutional Origin

What constitutional law does this PR branch from?
(Cite one or more of `docs/02..14`.)

- Origin law:

## Branch Scope

What single branch does this PR implement or document?

- Branch:

## Chain Position

Where is this PR located in `docs/14_PR_CHAIN_ROADMAP.md`?

- Previous required PR:
- Current layer:
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

This PR is forbidden from producing:

-

## Rank / Residual / Trace Impact

- Does this PR introduce rank behavior? yes/no
- Does this PR introduce residual behavior? yes/no
- Does this PR introduce trace behavior? yes/no
- If any answer is yes, where is it covered by a constitutional test?

## Constitutional Tests

List tests proving the PR branch remains inside its origin law.
These are tests written under
`docs/12_CONSTITUTIONAL_TEST_GEOMETRY.md`, not bare unit tests.

-

## Negative Tests

List tests proving the forbidden neighbours of this branch remain
forbidden (the `even_if` shape).

-

## Residuals After Merge

What is intentionally left open, and which future PR closes each
residual?

-

## Reviewer Checklist

- [ ] The PR has a constitutional origin.
- [ ] The PR is a branch, not a bundle.
- [ ] The PR is in the declared chain position.
- [ ] The PR does not exceed its allowed scope.
- [ ] The PR does not touch any forbidden scope.
- [ ] The PR has constitutional tests, not only unit tests.
- [ ] Every rejection has a named `FailureCode` where applicable.
- [ ] No hidden residual can pass.
- [ ] No rank promotion happens outside a `TransitionGate`.
- [ ] Green CI is not treated as constitutional approval.
