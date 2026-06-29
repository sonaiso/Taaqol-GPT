# 67 — Golden Closure Fixtures Law (مصفوفة الإغلاق الذهبية)

> **Status:** Constitutional law document. Registered as `CLOSE-4` in the
> authoritative chain in `docs/14_PR_CHAIN_ROADMAP.md`. Operationalises
> the closure-family discipline declared in the `CLOSE-3 through CLOSE-6`
> boundary block: this step publishes a *curated, evidence-bearing
> fixture pack* over the chain steps that are already constitutionally
> closed.
>
> **Forbidden surface.** This law and its companion fixture pack must
> not introduce any runtime behaviour, any new global `FailureCode`
> member, any new `ResidualKind` member, any new rank, any adapter or
> audit mutation, any opening or pre-licensing of a horizontal branch
> (PV-A5, ḥaqīqah, majāz, naql, lexical relations, DAL-A1+, LAFZI-B0+,
> LAW-E0), any rank promotion outside a gate, any hidden residual,
> any certificate or authority semantics, and any release-readiness
> claim. The fixture pack is **not** a certificate of correctness; it
> is an *auditable snapshot of declared chain truth* — what was
> ratified, where its origin law lives, where its runtime lives (if
> any), and where its constitutional tests live.
>
> Constitutional origin: `docs/12` (Constitutional Test Geometry),
> `docs/13` (Constitutional PR Geometry), `docs/14`
> (PR chain roadmap), `docs/52` (Constitutional Test Origin Covenant),
> `docs/53` (Project Methodology / KPI Plan), and `docs/64`
> (Lift-the-Ban Matrix Law). The fixture pack reuses the
> chain-truth surfaces those laws already declare; it adds no new
> truth claim of its own.
>
> Position in the closure family:
> `CLOSE-3 → CLOSE-3.1 → CLOSE-4 → CLOSE-5 → CLOSE-6`. The fixtures
> are the *closure snapshot* a future audit (`CLOSE-5`) and release
> announcement (`CLOSE-6`) may cite; they are **not** the audit and
> **not** the release.

---

## §1 Origin and authority

The chain (`docs/14`) and the methodology plan (`docs/53`) already
declare which steps are ratified, where their laws live, where their
runtime modules live, and where their constitutional tests live.
However, that information is *narrative*: it is spread across the
roadmap table, per-step boundary blocks, amendments, and the
`CLAUDE.md` staging table. Nothing today gives a reviewer, a future
agent, or an audit step a *single machine-readable, locator-checked
snapshot* of the closed chain.

`CLOSE-4` fills that gap by publishing two artefacts:

1. **This law (`docs/67`)** — declares the schema, vocabularies,
   curation rule, refusal table, residual policy, and forbidden
   surface for the fixture pack.
2. **The fixture pack** — `data/golden_closure_fixtures.json` —
   one entry per *constitutional landmark* (one representative
   step per chain family). Each entry is bounded by the schema in
   §3 below, drawn from the closed vocabularies in §4, and
   accompanied by on-disk evidence locators that the §8
   acceptance suite verifies.

The fixture pack is *curated*, not exhaustive. Exhaustively listing
every ratified step would duplicate `docs/14`, not verify it. The
curation rule (§5) selects one landmark per family so that the
fixture pack is small, stable, and re-readable end-to-end.

---

## §2 The truth this law verifies

The fixture pack asserts exactly one kind of proposition:

```text
For each landmark step S in the curated set:
    S is registered as ratified in docs/14 and CLAUDE.md;
    S's declared origin law(s) exist on disk;
    S's declared runtime module(s) exist on disk (if S has runtime);
    S's declared constitutional test module(s) exist on disk;
    S's declared forbidden output names are non-empty.
```

It does **not** assert that:

- a runtime module is *correct* — that is the role of the test
  module's own `ConstitutionalTestCase` / `ConstitutionalChainTestCase`;
- a closure verdict is *true* — that is the role of `gamma()`, the
  appropriate gate, and the appropriate audit;
- the project is *publicly ready* — that is the role of `CLOSE-5`
  (closure audit) and `CLOSE-6` (release).

Treating the fixture pack as a certificate would itself be a
`FORBIDDEN_STRAIGHT_LINE` (snapshot → correctness, snapshot →
release). The law forbids that move in §6.

---

## §3 Fixture schema

Every entry in `data/golden_closure_fixtures.json` is a JSON object
with **exactly** the following nine keys. No additional keys are
permitted; missing keys are a schema violation.

```text
{
    "chain_step_id"   : string drawn from §4.A
    "family"          : string drawn from §4.B
    "status"          : string drawn from §4.C
    "origin_law_locators"  : non-empty array of strings (file paths)
    "runtime_locators"     : array of strings (file paths) — may be empty
                             only when status == "DONE_LAW_ONLY"
    "test_locators"        : non-empty array of strings (file paths)
    "forbidden_outputs"    : non-empty array of strings
                             (declared forbidden surface names)
    "residual_kind"        : string drawn from §4.D
    "evidence_note"        : non-empty string (1–240 characters) —
                             single-line human-readable trace into
                             docs/14 explaining why this step is a
                             landmark for its family
}
```

Every path string is repository-relative POSIX (e.g.
`docs/56_GPT_R8_AUDIT_INTEGRATION_LAW.md`,
`src/taaqqul_slot_geometry/audit/answer_audit.py`,
`tests/test_answer_audit.py`).

---

## §4 Closed vocabularies

### §4.A `chain_step_id`

Every value must be an exact identifier currently registered in
the `docs/14` chain table *and* the `CLAUDE.md` PR staging table.
The fixture pack does not invent new identifiers.

### §4.B `family`

```text
family ∈ {
    KERNEL,                  # core/ (slot graph, gamma, rank, residual,
                             # evidence, forbidden lines, gate, trace)
    AUDIT,                   # audit/ (model client, successor, audit)
    ADAPTER,                 # adapters/ (adapter boundary, in-memory)
    WEIGHT,                  # weight/ (pre-weight + weight)
    PRE_SEMANTIC,            # signifier-signified chain (PR-15..PR-19)
    FORMAL_SHAPE,            # PR-F1..PR-F8 formal shape registry
    MUFRAD_DALALAH,          # PR-D1..PR-D4 mufrad dalālah closure
    VERTICAL,                # PR-D5..PR-D10 vertical column
    POST_VERTICAL,           # PV0..PV-A4.1 post-vertical
    GPT_REASONABLENESS,      # GPT-R0..GPT-R8 + GPT-K0..K2
    EUCLIDEAN,               # PR-X0..PR-X0L
    WADI,                    # LAFZI-C0..C8 wadʿī chain
    COUPLED_DALALAH,         # LAFZI-D0..D6 coupled dalālah matrix
    CLOSURE,                 # CLOSE-1..CLOSE-6 closure-family steps
    LAW_ONLY_RECORD          # standalone law-only records (e.g. WEB-M0)
}
```

### §4.C `status`

```text
status ∈ {
    DONE_RUNTIME,            # step shipped runtime code + tests
    DONE_LAW_ONLY,           # step shipped a ratified law document only
    DONE_CORRECTIVE          # step corrected an earlier surface;
                             # no new layer
}
```

### §4.D `residual_kind`

Drawn from the existing `ResidualKind` enum in
`src/taaqqul_slot_geometry/core/residual_policy.py`:

```text
residual_kind ∈ {
    BLOCKING,
    DEFERRABLE,
    NON_BLOCKING,
    EXPLANATORY,
    HIDDEN_FORBIDDEN
}
```

A fixture entry must declare `EXPLANATORY` as its residual kind:
the fixture pack itself is an *explanatory* residual against the
chain — it surfaces what was already ratified, without blocking
or deferring anything. Any other kind would be a category
confusion (e.g. `BLOCKING` would imply the fixture pack can
refuse a gate; it cannot). The §8 acceptance suite enforces this.

---

## §5 Curation rule

The fixture pack lists **one landmark step per family**. The
landmark is chosen as the most recent ratified step in its family
whose runtime (or, for `LAW_ONLY_RECORD` and `DONE_LAW_ONLY`
families, whose law) is the *capstone* of that family — i.e. the
step at which the family reached its current declared closure
state. Examples (not exhaustive — see the pack for the actual
choices):

- `KERNEL` → `PR-6` (`AnswerAudit` is the kernel-shaped capstone
  that closes the pure `gamma → gate → audit` ledger sequence).
- `WADI` → `LAFZI-C8` (`Wad'iMadlulClosed → CoupledDalalahGate`).
- `COUPLED_DALALAH` → `LAFZI-D6` (`DalalahMatrixClosed →
  WordCapability`).
- `GPT_REASONABLENESS` → `GPT-R8` (audit integration).
- `VERTICAL` → `PR-D10` (Vertical Path Closure Law).
- `POST_VERTICAL` → `PV-A4.1` (Maʿqūl Branch Discipline Law).
- `CLOSURE` → `CLOSE-3.1` (Lift-the-Ban Matrix Law).
- `LAW_ONLY_RECORD` → `WEB-M0`.

A fixture pack that selects a non-capstone step for a family is
schema-valid but constitutionally weaker; reviewers should refuse
such a pack as a *non-representative snapshot* and request a
re-curation rather than a new branch.

---

## §6 Forbidden surface

The following moves are forbidden inside the fixture pack, this
law, and the §8 acceptance suite. Each is named so that a future
reviewer can refuse it precisely.

```text
ForbiddenInFixturePack = {
    "PromotionWithoutGate",          # treating a fixture as rank-promoting
    "HiddenResidual",                # claiming closure without naming
                                     # forbidden outputs
    "OpenedBranch",                  # opening a new horizontal branch
                                     # under cover of "extending the pack"
    "BranchLicense",                 # licensing a future branch from a
                                     # fixture
    "ReadinessCertificate",          # treating the pack as readiness
    "ReleaseTag",                    # treating the pack as a release
    "ChainTruthOverride",            # asserting truth not already in
                                     # docs/14 + CLAUDE.md
    "FabricatedLocator",             # listing a path that does not exist
                                     # on disk
    "NewFailureCode",                # extending the FailureCode enum
    "NewResidualKind",               # extending the ResidualKind enum
    "AdapterMutation",               # mutating ModelClient / AdapterGuard
    "AuditMutation"                  # mutating AnswerAudit /
                                     # AuditedAnswer
}
```

These forbidden names are declared so that the §8 acceptance suite
can verify each fixture entry's `forbidden_outputs` field is drawn
from this set.

---

## §7 Residual policy

The fixture pack carries **one** explanatory residual at the
chain-truth surface: the pack itself is an `EXPLANATORY`
residual against `docs/14`, surfacing the closure landmarks
without altering them. It carries no `BLOCKING`, `DEFERRABLE`,
`NON_BLOCKING`, or `HIDDEN_FORBIDDEN` residuals; if any such
residual would be implied by adding an entry, the entry is
refused. The pack therefore cannot delay, block, or promote any
chain decision.

The acceptance suite (§8) is the operative guard for this rule.

---

## §8 Acceptance suite

The acceptance suite for this law lives at
`tests/test_golden_closure_fixtures.py` and must, as a
`ConstitutionalChainTestCase`-backed module declaring its
`origin_law`, `branch_name`, and `constitutional_chain` per
`docs/52`, prove the following propositions:

1. `docs/67` (this law) exists and declares §1 through §10.
2. `data/golden_closure_fixtures.json` exists and is valid JSON.
3. The pack is a non-empty list and every entry is a JSON object
   with **exactly** the nine keys in §3 and no others.
4. Every `chain_step_id` is unique within the pack and appears
   verbatim as a ratified row in both `docs/14_PR_CHAIN_ROADMAP.md`
   and `CLAUDE.md` (with a `✓ done` marker).
5. Every `family` value is drawn from §4.B; every `status` value
   from §4.C; every `residual_kind` value from §4.D.
6. For every `status == "DONE_RUNTIME"` entry, `runtime_locators`
   is non-empty.
7. For every `status == "DONE_LAW_ONLY"` entry, `runtime_locators`
   is empty.
8. Every path in `origin_law_locators`, `runtime_locators`, and
   `test_locators` resolves to a file that exists on disk
   (`FabricatedLocator` refusal).
9. Every entry's `forbidden_outputs` is a non-empty list drawn
   entirely from the §6 `ForbiddenInFixturePack` set.
10. Every entry's `residual_kind` is `"EXPLANATORY"` (§7).
11. Every `family` listed in §4.B appears at least once in the
    pack (the curation rule is *one per family*; the pack must
    cover every declared family).
12. The roadmap (`docs/14`) and `CLAUDE.md` both register
    `CLOSE-4` as `✓ done` and `CLOSE-5` as `→ current`, strictly
    in that order.
13. The `FailureCode` enum in
    `src/taaqqul_slot_geometry/core/failure_taxonomy.py` is
    not extended by this PR (no new member is introduced).
14. The `ResidualKind` enum in
    `src/taaqqul_slot_geometry/core/residual_policy.py` is not
    extended by this PR (no new member is introduced).

Failures 1–11 refuse the fixture pack itself; failures 12–14
refuse the closure step.

---

## §9 Refusal table

```text
Refusal name                     Cause
-------------------------------- ----------------------------------------
SchemaShapeViolation              fixture missing or extra key (§3)
UnknownFamily                     family ∉ §4.B
UnknownStatus                     status ∉ §4.C
UnknownResidualKind               residual_kind ∉ §4.D
NonRepresentativePack             a family in §4.B has no entry (§5)
NonUniqueChainStepId              duplicate chain_step_id (§8.4)
ChainStepIdNotInRoadmap           chain_step_id not registered as ✓ done
                                  in docs/14 + CLAUDE.md (§8.4)
FabricatedLocator                 path in *_locators does not exist (§8.8)
EmptyRuntimeLocatorsForRuntime    DONE_RUNTIME with empty runtime_locators
NonEmptyRuntimeLocatorsForLawOnly DONE_LAW_ONLY with non-empty runtime
EmptyTestLocators                 test_locators is empty (§3)
EmptyForbiddenOutputs             forbidden_outputs is empty (§3)
ForbiddenOutOfVocabulary          forbidden_outputs item ∉ §6
ResidualKindNotExplanatory        residual_kind ≠ EXPLANATORY (§7)
EvidenceNoteOutOfBounds           evidence_note empty or > 240 chars (§3)
CloseFourStatusMissing            docs/14 or CLAUDE.md still marks
                                  CLOSE-4 as current after this PR (§8.12)
CloseFiveCurrentMissing           docs/14 or CLAUDE.md does not mark
                                  CLOSE-5 as the next current step (§8.12)
NewFailureCodeIntroduced          FailureCode enum extended (§8.13)
NewResidualKindIntroduced         ResidualKind enum extended (§8.14)
```

None of these refusals is a member of the global `FailureCode`
enum; they are *local* refusal labels for this law, audited by
test logic, exactly as the local residual vocabulary in `docs/56`
§7 and the local matrix vocabulary in `docs/64` §4 are. This
keeps the fixture pack from leaking into the global taxonomy.

---

## §10 Effect on the chain

`CLOSE-4` becomes `✓ done`. `CLOSE-5` becomes the next
`→ current` step. No other chain status changes. No horizontal
branch opens. `docs/14` chain table, `docs/14` per-step
boundary block, and `CLAUDE.md` PR staging table are
synchronized in one PR per the chain-recording discipline.

The fixture pack remains in `data/` precisely so that future
closure steps (`CLOSE-5` audit, `CLOSE-6` release) can cite it as
a snapshot — never as a certificate.

---

*End of `docs/67_GOLDEN_CLOSURE_FIXTURES_LAW.md`.*
