# 12 — Constitutional Test Geometry

> **Status:** Constitutional law. Ratified in PR-1B. Every later PR
> writes tests under these rules; no later PR may relax them.

This document closes a loophole that the [Mathematical Slot Geometry
Laws](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md) cannot close on their own:

```text
A piece of code can pass a small local test
and still fail constitutionally in the full chain.
```

That failure mode is the test-side mirror of agent hallucination: a
single green assertion gets treated as proof that a whole layer is
sound. The repository refuses that move. Constitutional success is
**not** the success of one function. It is the success of a
**licensed transition inside a constitutional chain**.

The governing statement is:

```text
No test without an origin.
No test without a branch.
No test without a constitutional chain.
No partial pass counts as constitutional success.
```

---

## 1. Why unit success is not constitutional success

A unit test that does the following is **not** a constitutional test:

```text
build a SlotGraph
call gamma(graph)
assert state == MINIMALLY_CLOSED
```

Even if the assertion holds, it does not answer:

```text
Is this SlotGraph itself licit?
Does it carry a Center?
Does it carry a Boundary?
Is its layer correct?
Did the output rank jump above the ceiling?
Are residuals visible?
Was a trace candidate produced?
Is this success part of a chain, or a free-standing fact?
```

A constitutional test must answer every one of these for the branch
under examination, or it must not claim a constitutional verdict.

The repository rule:

```text
Green pytest ≠ constitutional success
until the test proves the whole chain it claims.

A partial pass is not a constitutional pass,
even when the asserted value is correct.
A test that asserts the right verdict on one axis
while dropping any other required axis collapses
to INVALID by §6 (anti-agent-hallucination tests).
```

## 2. Origin / Branch law for tests

Every test is a **branch of an origin law**. There are no orphan
tests.

```text
Origin law:
    A named constitutional law from docs/02..11.

Branch:
    The specific case under that law that this test exercises.

Forbidden:
    A test that asserts behavior without naming the origin law
    and branch it claims to exercise.
```

Examples of valid origin/branch pairings:

```text
Origin: "No SlotGraph without Center."
Branch: "SlotGraph constructed without a center is INVALID
         with FailureCode.CENTER_MISSING."

Origin: "Perforated closure licenses a candidate, not a certificate."
Branch: "SlotGraph with required slots closed and a visible
         non-blocking residual is PERFORATED_CLOSED with rank
         no higher than CANDIDATE."

Origin: "No closure with hidden residuals."
Branch: "SlotGraph with a hidden-forbidden residual is INVALID
         with FailureCode.HIDDEN_RESIDUAL even if required slots
         appear closed."
```

## 3. `ConstitutionalTestCase` schema

A constitutional test case is the tuple

```text
ConstitutionalTestCase = ⟨
    origin_law,
    branch_name,
    constitutional_chain,
    expected_state,
    expected_failure_code,
    forbidden_outputs,
    max_rank,
    required_trace,
    required_residual_visibility,
⟩
```

with meaning:

```text
origin_law                    — short name of the constitutional law
                                this test branches from.
branch_name                   — the single branch the test exercises.
constitutional_chain          — ordered sequence of layers the test
                                walks (e.g. SlotGraph → Gamma → Rank
                                → ResidualVisibility → Trace →
                                OutputBoundary).
expected_state                — the ClosureState verdict the chain
                                must produce (OPEN, MINIMALLY_CLOSED,
                                PERFORATED_CLOSED, BLOCKED, INVALID,
                                FORBIDDEN_LEAP).
expected_failure_code         — a FailureCode name when the verdict
                                is a refusal, or None when the verdict
                                is a licit closure.
forbidden_outputs             — outputs the test guarantees do *not*
                                appear (e.g. "CERTIFICATE",
                                "APPROVED_OUTPUT", "MINIMALLY_CLOSED").
max_rank                      — the rank ceiling the chain must not
                                exceed (e.g. "ZERO", "TRACE",
                                "CANDIDATE", ...).
required_trace                — True iff the chain must produce a
                                trace-entry candidate.
required_residual_visibility  — True iff the chain must make residuals
                                explicit (the "no hidden residuals"
                                law).
```

The schema lives in [`tests/support/constitutional_case.py`](../tests/support/constitutional_case.py).
It is intentionally a frozen dataclass with no behavior — the schema
is law; the assertions are the next section.

## 4. Required assertion chain

A constitutional test must walk a single chain in a fixed order. The
chain is:

```text
1.  Origin law named.
2.  Branch named.
3.  Input SlotGraph constructed (or refused at construction).
4.  Gamma applied (or refused before Gamma).
5.  Rank ceiling checked.
6.  Residual visibility checked.
7.  Trace candidate verified (presence or absence per the schema).
8.  Output boundary verified.
9.  Forbidden outputs proven absent.
10. Named failure or named closure proven present.
```

The chain is not optional. A test that proves only step 4 is a
partial pass and is not a constitutional test, even if it is green.

The helper `assert_constitutional_case(case, result)` (in
[`tests/support/constitutional_case.py`](../tests/support/constitutional_case.py))
enforces the schema-side discipline as soon as the executable kernel
arrives in PR-2.

## 5. Negative tests precede positive tests

Constitutional refusals are higher-priority than constitutional
closures. The reason is the same one the
[Forbidden Straight Lines](04_FORBIDDEN_STRAIGHT_LINES.md) document
gives for the kernel itself: the value of the system is precisely
that it refuses certain transitions even when they look locally
attractive.

```text
For every origin law, the negative branch is written first.
A positive branch may only be added once its forbidden neighbours
are already proven forbidden.
```

A common shape:

```text
test_<law>_<branch>_is_forbidden_even_if_<looks_attractive>
```

Examples (their bodies land with the layers they exercise):

```text
test_weight_to_agency_direct_is_forbidden_even_if_weight_slot_closed
test_evidence_to_certainty_direct_is_forbidden_even_with_strong_evidence
test_lexicon_to_candidate_direct_is_forbidden_even_with_valid_entry
test_tool_number_to_knowledge_is_forbidden_even_if_score_high
```

The phrase `even_if` is load-bearing: it states that strength of
input does not license bypassing a Gate.

## 6. Anti-agent-hallucination tests

These tests forbid an agent from labelling a partial pass as a
constitutional pass.

```text
test_gamma_success_without_trace_is_not_constitutional_success
test_closed_required_slots_without_rank_is_not_constitutional_success
test_approved_state_without_residual_visibility_is_invalid
test_candidate_without_origin_law_reference_is_invalid_test_fixture
test_unit_success_without_chain_assertions_is_not_accepted
```

The intent is structural: even if a chain emits a licit state on one
axis, dropping any other required axis collapses the verdict to
`INVALID`.

## 7. Test acceptance rules

A test is accepted as constitutional **only if** it declares:

```text
- origin law
- branch case
- constitutional chain
- expected verdict (ClosureState)
- forbidden outputs
- rank ceiling
- residual visibility expectation
- trace expectation
- named failure code if the verdict is a refusal
```

Equivalently, in the project shorthand:

```text
A test is not accepted because it is green.
It is accepted only when it proves its origin, its branch,
its chain, its boundary, and its forbidden neighbours.
```

This rule binds reviewers as much as it binds authors. A green
pytest run is evidence; it is not approval.

## 8. Examples

### 8.1 Negative example — hidden residual branch

```text
ConstitutionalTestCase(
    origin_law="No closure with hidden residuals.",
    branch_name="hidden-residual branch",
    constitutional_chain=(
        "SlotGraph",
        "Gamma",
        "ResidualVisibility",
        "FailureTaxonomy",
        "TraceCandidate",
    ),
    expected_state="INVALID",
    expected_failure_code="HIDDEN_RESIDUAL",
    forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
    max_rank="ZERO",
    required_trace=True,
    required_residual_visibility=True,
)
```

### 8.2 Positive example — minimally-closed branch

```text
ConstitutionalTestCase(
    origin_law="Closure without hidden residuals is minimally closed.",
    branch_name="all-required-slots-closed branch",
    constitutional_chain=(
        "SlotGraph",
        "Gamma",
        "RankCeiling",
        "ResidualVisibility",
        "Trace",
        "OutputBoundary",
    ),
    expected_state="MINIMALLY_CLOSED",
    expected_failure_code=None,
    forbidden_outputs=("CERTIFICATE",),
    max_rank="CANDIDATE",
    required_trace=True,
    required_residual_visibility=True,
)
```

### 8.3 Negative example — forbidden straight line

```text
ConstitutionalTestCase(
    origin_law="No straight line from Evidence to Certainty.",
    branch_name="evidence-to-certificate direct branch",
    constitutional_chain=(
        "SlotGraph",
        "TransitionGate",
        "ForbiddenStraightLineRegistry",
        "FailureTaxonomy",
    ),
    expected_state="FORBIDDEN_LEAP",
    expected_failure_code="FORBIDDEN_STRAIGHT_LINE",
    forbidden_outputs=("CERTIFICATE", "APPROVED_OUTPUT"),
    max_rank="ZERO",
    required_trace=True,
    required_residual_visibility=True,
)
```

---

## 9. `ConstitutionalChainTestCase` — chain-position binding

> Added in PR-1C. Every test that exercises any layer downstream of
> `DeclaredEntry`, the Identity-to-Truth Licensing Chain
> ([`16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md`](16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md)),
> or the SlotGraph Generation Law
> ([`17_SLOTGRAPH_GENERATION_LAW.md`](17_SLOTGRAPH_GENERATION_LAW.md))
> must declare its identity through `ConstitutionalChainTestCase`,
> not bare `ConstitutionalTestCase`.

A `ConstitutionalChainTestCase` is a `ConstitutionalTestCase`
extended with four mandatory declarations:

```text
chain_position
    The single position in the full constitutional chain that
    this test exercises. Examples:
        "DeclaredEntry"
        "SlotGraph.Generation"
        "IdentityChain.link.5.Potentiality"
        "Gamma.step.6.HiddenResidual"
        "TransitionGate.EvidenceToCertainty"

origin_law_ref
    A textual reference of the form
        "docs/NN_FILE.md#section-or-anchor"
    naming the file (and where useful the section) that the test
    branches from. A test whose origin_law_ref does not resolve
    to an actual file in the repository is a schema violation.

branch_of_origin
    The named branch derived from the origin law. This is the
    single behaviour the test exercises and must not be a
    paraphrase of `branch_name`. `branch_name` is the local
    identifier; `branch_of_origin` is the constitutional one.

forbidden_shortcut_assertions
    The ordered tuple of direct transitions the test guarantees
    remain forbidden. Examples:
        ("TextEntry → Meaning",)
        ("Identity → Truth", "Matching → Meaning")
        ("Opening → Closure", "Closure → Certificate",
         "Candidate → Truth")
        ("NoError → Approval",)
    For a closure verdict (MINIMALLY_CLOSED, PERFORATED_CLOSED)
    this tuple must be non-empty: a green chain that does not
    prove its forbidden neighbours is a partial pass.
```

The schema rule:

```text
A test that exercises any link of the Identity-to-Truth Licensing
Chain (docs/16 §2) or any obligation of the SlotGraph Generation
Law (docs/17 §1–§3) and does not declare itself through
`ConstitutionalChainTestCase` is rejected as a schema violation,
even if its assertions are correct.
```

The executable schema lives alongside `ConstitutionalTestCase` in
[`../tests/support/constitutional_case.py`](../tests/support/constitutional_case.py).
`ConstitutionalChainTestCase` extends, not replaces,
`ConstitutionalTestCase`: every chain case is also a constitutional
case, and `assert_constitutional_case` accepts both. When a chain
case is passed, the helper additionally enforces that no
`forbidden_shortcut_assertions` row appears in the produced output
surface of the chain result.

### 9.1 Why the four extra fields are mandatory

```text
chain_position
    forces the test to name where in the full chain it lives,
    so a reviewer can refuse a test that drifts upward or
    downward.

origin_law_ref
    forces the test to ground itself in a present document
    file. A floating origin is the test-side mirror of a
    floating Center.

branch_of_origin
    forces the test to declare the constitutional branch, not
    just an implementation-side label. Two tests with the same
    `branch_name` may exercise different `branch_of_origin`
    and must remain distinguishable at review.

forbidden_shortcut_assertions
    forces every chain test to enumerate the direct transitions
    it proves are still refused. A closure result is not a
    constitutional success until the relevant straight-line
    bypasses are proven absent in the same chain result.
```

### 9.2 Anti-shortcut assertion in the helper

When `assert_constitutional_case(case, result)` is called with a
`ConstitutionalChainTestCase`, the helper performs all the
`ConstitutionalTestCase` checks and then performs one additional
step:

```text
11. Forbidden shortcuts proven absent.
    For every entry s in case.forbidden_shortcut_assertions,
    s must not appear in result.produced_outputs. A test whose
    result claims `Identity → Truth` as an emitted output is
    forbidden, even when result.state is a closure.
```

### 9.3 Examples

A chain-test against the SlotGraph Generation Law (docs/17 §3
*Center missing* row):

```text
ConstitutionalChainTestCase(
    origin_law="docs/17_SLOTGRAPH_GENERATION_LAW.md §3",
    branch_name="ctor-refuses-missing-center",
    constitutional_chain=("SlotGraph.Generation", "FailureTaxonomy"),
    expected_state=ClosureState.INVALID,
    expected_failure_code=FailureCode.CENTER_MISSING,
    forbidden_outputs=("APPROVED_OUTPUT", "MINIMALLY_CLOSED"),
    max_rank=Rank.ZERO,
    required_trace=True,
    required_residual_visibility=True,
    chain_position="SlotGraph.Generation.center",
    origin_law_ref="docs/17_SLOTGRAPH_GENERATION_LAW.md#3-the-constructor-refusal-table",
    branch_of_origin="No SlotGraph from raw value (missing-center sub-branch).",
    forbidden_shortcut_assertions=(
        "Identity → Truth",
        "Candidate → Truth",
    ),
)
```

A chain-test against the Identity-to-Truth Licensing Chain link 7
(*Closure*) proving a positive branch:

```text
ConstitutionalChainTestCase(
    origin_law="docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md §2 link 7",
    branch_name="closure-without-residuals-is-minimal",
    constitutional_chain=(
        "SlotGraph",
        "IdentityChain.link.7.Closure",
        "Gamma",
        "RankCeiling",
        "ResidualVisibility",
        "Trace",
        "OutputBoundary",
    ),
    expected_state=ClosureState.MINIMALLY_CLOSED,
    expected_failure_code=None,
    forbidden_outputs=("CERTIFICATE",),
    max_rank=Rank.CANDIDATE,
    required_trace=True,
    required_residual_visibility=True,
    chain_position="IdentityChain.link.7.Closure",
    origin_law_ref="docs/16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md#2-the-ten-licensing-links",
    branch_of_origin="Closure is established (link 7 of 10).",
    forbidden_shortcut_assertions=(
        "Closure → Certificate",
        "Candidate → Truth",
    ),
)
```

---

## Cross-references

- The Mathematical Slot Geometry Laws live in
  [`11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`](11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md).
- The Constitutional PR Geometry (the same discipline applied to
  pull requests) lives in
  [`13_CONSTITUTIONAL_PR_GEOMETRY.md`](13_CONSTITUTIONAL_PR_GEOMETRY.md).
- The PR chain roadmap lives in
  [`14_PR_CHAIN_ROADMAP.md`](14_PR_CHAIN_ROADMAP.md).
- The Textual Communication Entry Law (PR-1C):
  [`15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md`](15_TEXTUAL_COMMUNICATION_ENTRY_LAW.md).
- The Identity-to-Truth Licensing Chain (PR-1C):
  [`16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md`](16_IDENTITY_TO_TRUTH_LICENSING_CHAIN.md).
- The SlotGraph Generation Law (PR-1C):
  [`17_SLOTGRAPH_GENERATION_LAW.md`](17_SLOTGRAPH_GENERATION_LAW.md).
- The agent operating rules in [`../CLAUDE.md`](../CLAUDE.md) bind
  every contributor (human or agent) to this document.
