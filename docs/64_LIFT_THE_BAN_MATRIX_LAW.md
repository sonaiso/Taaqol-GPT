# 64 — Lift-the-Ban Matrix Law (مصفوفة رفع الحظر)

> **Status:** Constitutional law document. Registered as `CLOSE-3.1` in the
> authoritative chain in `docs/14_PR_CHAIN_ROADMAP.md`. Law-only: no runtime
> code, no carriers, no enums, no new global `FailureCode` members, no
> adapter/audit mutation, no new ranks, no new residual kinds, and no
> opening of any horizontal branch.
>
> Constitutional origin: `docs/14` (admission rule / Amendment-14),
> `docs/47` (post-vertical admission rule), `docs/51` (Maʿqūl branch
> discipline), `docs/52` (test origin covenant), `docs/53` (project
> methodology, objectives, and KPI plan), and `docs/13`
> (constitutional PR geometry).
>
> Position in the closure family:
> `CLOSE-3 → CLOSE-3.1 → CLOSE-4 → CLOSE-5 → CLOSE-6`. The matrix is
> the *protocol* a future lift event must follow; it is **not** itself
> a lift, an audit, or a release.

---

## §1 Origin and authority

The repository forbids two distinct kinds of move:

1. **A constitutional ban** on opening the *next* horizontal branch (or
   any new layer) without an origin law, chain position, scope and
   forbidden surface, constitutional tests, residual policy, and
   rank/trace discipline — see `docs/14` §Amendment-14 admission rule
   and `docs/47` §Admission rule for post-vertical branches.
2. **A practical ban** on declaring the project *publicly ready* (a
   tagged release, an external "ready for use" claim) without a
   coherent README/roadmap state, a `LICENSE`, a published release,
   and a readiness audit.

These two bans live in different domains. Conflating them — by, for
example, treating a green CI run as permission to open a new branch,
or by treating an open branch as readiness for release — is a
*FORBIDDEN_STRAIGHT_LINE* on the discipline itself.

This document declares the **lift-the-ban matrix** that any future
proposer must populate before either ban is lifted. The matrix does
not itself lift any ban; it makes the lift event auditable.

---

## §2 The two ban classes

```text
ban_class ∈ { CONSTITUTIONAL_BRANCH , PUBLIC_READINESS }

CONSTITUTIONAL_BRANCH : controls the opening of a new horizontal
                        branch or chain step. Owner: chain author.
                        Audited by a ConstitutionalChainTestCase.
                        Lifted only when every Table A condition
                        is LIFT_PERMITTED for the named branch.

PUBLIC_READINESS      : controls the act of declaring the project
                        publicly ready (release tag, public
                        readiness statement). Owner: release
                        manager. Audited by CLOSE-5 (readiness
                        audit) and CLOSE-6 (release). Lifted only
                        when every Table B condition is
                        LIFT_PERMITTED.
```

The two classes do not share rows. A row that decides a constitutional
lift may not be cited as evidence of public readiness, and vice versa
(see §10 refusal table, MATRIX_BAN_CLASS_LEAK).

---

## §3 Matrix schema (fixed columns)

Every row of the matrix has exactly the following columns, in this
order, with no extras and no omissions:

```text
condition_id      | ban_class
condition_text    | evidence_kind
evidence_locator  | owner
test_kind         | failure_code
rank_ceiling      | residual_policy
decision
```

A row is constitutionally well-formed iff:

- every column is present and drawn from the closed vocabularies in
  §4, and
- `failure_code` is either `NONE` or a member of the project's
  existing `FailureCode` inventory
  (`src/taaqqul_slot_geometry/core/failure_taxonomy.py`), and
- `evidence_locator` is a `path` or `path:line` reachable from the
  repository root, and
- `decision` is consistent with §5.

---

## §4 Closed vocabularies for matrix columns

```text
ban_class ∈ {
    CONSTITUTIONAL_BRANCH ,
    PUBLIC_READINESS
}

evidence_kind ∈ {
    RATIFIED_LAW ,
    CHAIN_TABLE_ROW ,
    PER_STEP_BOUNDARY_BLOCK ,
    CONSTITUTIONAL_TEST ,
    RUNTIME_ARTIFACT ,
    DOC_SECTION ,
    PUBLISHED_RELEASE ,
    LICENSE_FILE
}

owner ∈ {
    chain-author ,
    maintainer ,
    release-manager
}

test_kind ∈ {
    CONSTITUTIONAL_CHAIN_TEST ,
    DOC_PRESENCE_TEST ,
    SCANNER ,
    REGISTRY_TEST ,
    OPERATIONAL_AUDIT ,
    RELEASE_CHECK ,
    NONE
}

rank_ceiling ∈ {
    ZERO , ONE , TWO , THREE
}

residual_policy ∈ {
    STRICT_VISIBLE ,
    DEFERRED_VISIBLE
}

decision ∈ {
    LIFT_PERMITTED ,
    LIFT_BLOCKED ,
    LIFT_DEFERRED_TO_LAW(<step>) ,
    NOT_APPLICABLE
}

failure_code ∈ FailureCode ∪ { NONE }
    where FailureCode is the existing enum in
    src/taaqqul_slot_geometry/core/failure_taxonomy.py .
    Introducing a new global FailureCode member is out of scope
    for this matrix and requires its own ratified law.
```

---

## §5 Decision discipline

A `decision` value is a verdict on *one* condition for *one* ban
class. It is not a verdict on the ban as a whole.

```text
LIFT_PERMITTED          : The condition is satisfied today, as
                          witnessed by the named evidence_locator
                          and (where required) test_kind. This is
                          permission to open the next law-only PR
                          that addresses the ban class, never
                          permission to ship runtime code or to
                          tag a release.

LIFT_BLOCKED            : The condition is not satisfied. The
                          named failure_code names the refusal a
                          gate would emit if the ban were lifted
                          anyway. No bundling, no workaround.

LIFT_DEFERRED_TO_LAW(X) : The condition's satisfaction depends on
                          another, named chain step X that is not
                          yet ratified or merged. The lift
                          decision is deferred until X is done.

NOT_APPLICABLE          : The condition does not apply to this
                          ban class for this branch (e.g., an
                          upstream-origin condition for a branch
                          that has no upstream).
```

A ban class is lifted only when *every* row in its table is
`LIFT_PERMITTED`. A single `LIFT_BLOCKED` or
`LIFT_DEFERRED_TO_LAW(...)` row blocks the whole class.

A `LIFT_PERMITTED` decision is never carried across ban classes.
A Table A row's `LIFT_PERMITTED` does not lift any Table B
condition, and vice versa (§10).

---

## §6 Forbidden surface

```text
This matrix MUST NOT:
- open, license, or pre-license any horizontal branch
  (including PV-A5, ḥaqīqah, majāz, naql, lexical relations).
- ship runtime code, carriers, enums, parsers, gates, or
  audit-layer changes.
- promote a Rank, hide a Residual, or skip a Trace.
- introduce a new global FailureCode member.
- assert that any branch is closed or that the project is
  publicly ready. Closure of CLOSE-3.1 is closure of the
  *protocol*, not closure of any branch or release.
- substitute for the readiness audit (CLOSE-5) or the release
  tag (CLOSE-6).
- be used as a certificate or as authority. Per docs/13 and
  docs/56, candidate-to-certificate promotion remains forbidden.
```

A PR that attempts any of the above under the cover of "populating
the matrix" is a `FORBIDDEN_LEAP` regardless of CI status.

---

## §7 Local residual vocabulary

These residual names are local to `CLOSE-3.1` and do **not** extend
any global `ResidualKind` enum. They name what a matrix audit must
expose as visible residuals if a row fails to satisfy §3 or §5.

```text
MATRIX_EVIDENCE_MISSING       : evidence_locator does not resolve
                                to a file or line in the repository.
MATRIX_OWNER_UNNAMED          : owner is empty or outside the §4
                                vocabulary.
MATRIX_DECISION_UNSUPPORTED   : decision asserts LIFT_PERMITTED but
                                evidence_locator and/or test_kind
                                do not yet exist.
MATRIX_BAN_CLASS_LEAK         : a row in one ban class is cited as
                                evidence of a lift in the other.
MATRIX_FAILURE_CODE_UNKNOWN   : failure_code is neither NONE nor a
                                member of FailureCode.
MATRIX_LIFT_WITHOUT_ORIGIN_LAW: a CONSTITUTIONAL_BRANCH row decides
                                LIFT_PERMITTED for a branch whose
                                origin law is not on disk.
```

These residuals must be **visible** (per docs/06) when emitted: a
matrix audit that hides them violates `HIDDEN_RESIDUAL`.

---

## §8 Test expectations

A `ConstitutionalChainTestCase`-backed acceptance suite for this law
(`tests/test_lift_the_ban_matrix_law.py`) must prove:

1. `docs/64` exists and declares §1 through §10.
2. Every row in §9 (Tables A and B) has all eleven schema columns
   populated and drawn from §4's closed vocabularies.
3. Every `failure_code` referenced in §9 is either `NONE` or a
   member of the existing `FailureCode` enum.
4. Every `evidence_locator` in §9 resolves to a file (or
   `file:line`) that exists in the repository.
5. No Table A row asserts `LIFT_PERMITTED` for a branch whose
   origin law is not on disk.
6. No Table A row is cited inside Table B's decisions, and no
   Table B row is cited inside Table A's decisions.
7. The roadmap (`docs/14`) and `CLAUDE.md` both register
   `CLOSE-3.1` strictly between `CLOSE-3` and `CLOSE-4`.

The tests must themselves declare `origin_law`, `branch_name`, and
`constitutional_chain` per `docs/52`.

---

## §9 Worked rows

The following tables instantiate §3's schema for the conditions
already enumerated by the project's discipline. Each row is
auditable on disk and may be re-verified by the §8 tests.

### Table A — Constitutional branch-opening ban

```text
A1
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The branch has a ratified origin law of its own.
  evidence_kind    : RATIFIED_LAW
  evidence_locator : docs/47_POST_VERTICAL_ROADMAP.md
  owner            : chain-author
  test_kind        : CONSTITUTIONAL_CHAIN_TEST
  failure_code     : UNLICENSED_OPENING
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

A2
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The branch has an explicit chain position in
                     docs/14 and CLAUDE.md.
  evidence_kind    : CHAIN_TABLE_ROW
  evidence_locator : docs/14_PR_CHAIN_ROADMAP.md
  owner            : chain-author
  test_kind        : DOC_PRESENCE_TEST
  failure_code     : OUTPUT_EXCEEDS_LAYER
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

A3
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The branch declares its scope and its forbidden
                     surface in a per-step boundary block.
  evidence_kind    : PER_STEP_BOUNDARY_BLOCK
  evidence_locator : docs/14_PR_CHAIN_ROADMAP.md
  owner            : chain-author
  test_kind        : DOC_PRESENCE_TEST
  failure_code     : UNLICENSED_OPENING
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

A4
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The branch has constitutional tests
                     (ConstitutionalTestCase or
                     ConstitutionalChainTestCase) covering its
                     boundary, not just unit tests.
  evidence_kind    : CONSTITUTIONAL_TEST
  evidence_locator : tests/support/constitutional_case.py
  owner            : chain-author
  test_kind        : CONSTITUTIONAL_CHAIN_TEST
  failure_code     : UNLICENSED_OPENING
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

A5
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The branch declares its residual policy and
                     keeps residuals visible (no HIDDEN_RESIDUAL).
  evidence_kind    : DOC_SECTION
  evidence_locator : docs/06_RESIDUAL_POLICY.md
  owner            : chain-author
  test_kind        : CONSTITUTIONAL_CHAIN_TEST
  failure_code     : HIDDEN_RESIDUAL
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

A6
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The branch declares its rank ceiling and its
                     trace expectation; rank promotion only via a
                     licensed TransitionGate.
  evidence_kind    : DOC_SECTION
  evidence_locator : docs/05_RANK_LATTICE.md
  owner            : chain-author
  test_kind        : CONSTITUTIONAL_CHAIN_TEST
  failure_code     : TRACE_MISSING
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

A7
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The single-open-branch rule is respected:
                     no second horizontal branch is open while
                     this one is being opened (docs/47).
  evidence_kind    : DOC_SECTION
  evidence_locator : docs/47_POST_VERTICAL_ROADMAP.md
  owner            : chain-author
  test_kind        : DOC_PRESENCE_TEST
  failure_code     : UNLICENSED_OPENING
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

A8
  ban_class        : CONSTITUTIONAL_BRANCH
  condition_text   : The upstream origin of this branch is preserved
                     and closed before this branch opens (e.g.,
                     ManṭūqClosure before any post-manṭūq branch).
  evidence_kind    : RATIFIED_LAW
  evidence_locator : docs/48_MANTUQ_BOUNDARY_LAW.md
  owner            : chain-author
  test_kind        : CONSTITUTIONAL_CHAIN_TEST
  failure_code     : MAFHUM_BEFORE_MANTUQ
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED
```

### Table B — Public readiness ban

```text
B1
  ban_class        : PUBLIC_READINESS
  condition_text   : README and the authoritative roadmap report
                     the same chain state (no stale "current"
                     marker, no missing step, no contradictory
                     status line).
  evidence_kind    : DOC_SECTION
  evidence_locator : README.md
  owner            : maintainer
  test_kind        : DOC_PRESENCE_TEST
  failure_code     : NONE
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

B2
  ban_class        : PUBLIC_READINESS
  condition_text   : A LICENSE file is present at the repository
                     root and names an OSI-approved license.
  evidence_kind    : LICENSE_FILE
  evidence_locator : LICENSE
  owner            : maintainer
  test_kind        : DOC_PRESENCE_TEST
  failure_code     : NONE
  rank_ceiling     : ZERO
  residual_policy  : STRICT_VISIBLE
  decision         : LIFT_PERMITTED

B3
  ban_class        : PUBLIC_READINESS
  condition_text   : A tagged release exists on the repository
                     (e.g., v0.1.0).
  evidence_kind    : PUBLISHED_RELEASE
  evidence_locator : CHANGELOG.md
  owner            : release-manager
  test_kind        : RELEASE_CHECK
  failure_code     : NONE
  rank_ceiling     : ZERO
  residual_policy  : DEFERRED_VISIBLE
  decision         : LIFT_DEFERRED_TO_LAW(CLOSE-6)

B4
  ban_class        : PUBLIC_READINESS
  condition_text   : A readiness/audit report is published naming
                     what is closed, what remains forbidden, and
                     what is next.
  evidence_kind    : DOC_SECTION
  evidence_locator : docs/14_PR_CHAIN_ROADMAP.md
  owner            : maintainer
  test_kind        : OPERATIONAL_AUDIT
  failure_code     : NONE
  rank_ceiling     : ZERO
  residual_policy  : DEFERRED_VISIBLE
  decision         : LIFT_DEFERRED_TO_LAW(CLOSE-5)
```

The `LIFT_PERMITTED` decisions in Table A reflect that the
*matrix-side* conditions on opening a new branch are formally
declared in the cited laws. They do **not** open any branch by
themselves: opening a branch still requires its own origin law,
its own chain step, and its own ratified Amendment per `docs/14`
§Amendment discipline.

---

## §10 Refusal table

A row of the matrix is **inadmissible** (the matrix audit must
refuse it and emit a visible residual) when any of the following
holds:

```text
inadmissibility                 | emitted residual                   | named failure_code
--------------------------------+-------------------------------------+-----------------------------
column missing or empty         | MATRIX_EVIDENCE_MISSING            | UNLICENSED_OPENING
column value outside §4         | MATRIX_EVIDENCE_MISSING            | UNLICENSED_OPENING
owner outside §4 vocabulary     | MATRIX_OWNER_UNNAMED               | UNLICENSED_OPENING
failure_code not in FailureCode | MATRIX_FAILURE_CODE_UNKNOWN        | UNLICENSED_OPENING
evidence_locator does not exist | MATRIX_EVIDENCE_MISSING            | UNLICENSED_OPENING
LIFT_PERMITTED without origin   | MATRIX_LIFT_WITHOUT_ORIGIN_LAW     | UNLICENSED_OPENING
Table A row decides Table B     | MATRIX_BAN_CLASS_LEAK              | FORBIDDEN_STRAIGHT_LINE
Table B row decides Table A     | MATRIX_BAN_CLASS_LEAK              | FORBIDDEN_STRAIGHT_LINE
decision asserts closure of     | MATRIX_DECISION_UNSUPPORTED        | OUTPUT_EXCEEDS_LAYER
  a branch / readiness as a     |                                    |
  whole                         |                                    |
matrix used as certificate or   | MATRIX_DECISION_UNSUPPORTED        | OUTPUT_EXCEEDS_LAYER
  authority                     |                                    |
```

A refused row is not silently dropped: the matrix audit must record
the inadmissibility, the residual, and the named `FailureCode`, and
must refuse the lift event of the affected ban class.

---

## §11 Exit

`CLOSE-3.1` closes when:

- `docs/64` is on disk in the form above,
- `docs/14` and `CLAUDE.md` register `CLOSE-3.1` between `CLOSE-3`
  and `CLOSE-4`,
- the `tests/test_lift_the_ban_matrix_law.py` acceptance suite
  enforces §8, and
- no row in §9 silently violates §10.

`CLOSE-3.1` does **not** close any branch, lift any ban, or
declare the project ready. The next implementation step in the
chain remains `CLOSE-3` (PV-T0.1 test-origin scanner) until
`CLOSE-3` itself is marked done; this matrix law lives alongside
`CLOSE-3` as the *protocol* the later `CLOSE-4`, `CLOSE-5`, and
`CLOSE-6` steps must honour when they are themselves opened.
