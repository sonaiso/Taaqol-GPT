# 90 — Rebuilt Constitutional Governance Architecture (WORD-L0 → PRECOMP-L0)

> Status: architectural design document (proposal-only, non-ratified chain step).
> Scope: independent constitutional governor kernel for licensed transitions and proof-graph-based invalidation/revision.
> Snapshot date: 2026-07-11.

## 1) Core separation law

```text
Proposal != Licensing != Execution != Approval
```

Licensed cycle:

```text
LayerProposal
-> GovernorPreflight
-> TransitionPermit
-> EngineExecution
-> GovernorPostflight
-> ProofGraphCommit
```

Layer proposes and engine executes, but only an independent governor licenses transitions and approves/revokes outcomes.

## 2) Scientific correction of "Arabic thinks"

Operational statement:

```text
A licensed computational model for Arabic can realize operational thinking
and systemic self-governance if it has:
- stable system identity
- independent governor
- proof memory
- explicit revision/invalidation policy
```

Operational predicates:

```text
OperationalThinking(S) iff
DistinguishInput
and GenerateCandidates
and TestConstraints
and LicenseOrSuspend
and PreserveTrace
and ReviseOnInvalidation

SystemicSelf(S) iff
StableSystemIdentity
and ExplicitState
and IndependentGovernor
and ProofMemory
and RevisionPolicy
```

Systemic self here is a formal system property, not human consciousness.

## 3) Diagnosis of current architecture

- `AFJGGovernor` is scoped to LLM proposal governance with coarse verdict levels and is not a full linguistic constitutional governor.
- `LayerSovereigntyRegistry` behaves as policy naming/ordering, not a transition-request governor with permit lifecycle.
- The current global pipeline is linear/coarse and should not be demolished immediately; the rebuilt word architecture should enter as an internal subgraph under word/morphology boundaries.
- Existing AFU rank normalization is acceptable for external answer interfaces but insufficient for internal linguistic engine distinctions.
- Current weight-role vectors that map patterns directly to semantic roles are the critical forbidden leap to remove.
- Existing low-level wazn matching remains reusable as formal geometry tooling if decoupled from semantic closure.

## 4) Constitutional kernel model

Kernel tuple:

```text
K = <D, U, O, G, L, E, R, C, B, T, V>
```

Where:

- `D`: domains
- `U`: units/candidates
- `O`: operation kinds
- `G`: independent governor
- `L`: licenses/gates
- `E`: evidence and dependency graph
- `R`: support ranks
- `C`: conflict states
- `B`: residuals
- `T`: execution trace
- `V`: external verification

Object state cannot collapse into one verdict:

```text
State(x) = <Decision(x), Rank(x), Conflict(x), Residuals(x), Verification(x)>
```

## 5) Required state spaces

```python
class SupportRank(IntEnum):
    ZERO = 0
    POSSIBILITY = 1
    CANDIDATE = 2
    HYPOTHESIS = 3
    STRONG_HYPOTHESIS = 4
    CERTIFICATE = 5
```

```python
class DecisionState(str, Enum):
    PENDING = "pending"
    PERMITTED = "permitted"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
```

```python
class ConflictState(str, Enum):
    NONE = "none"
    COMPATIBLE_ALTERNATIVES = "compatible_alternatives"
    UNDERDETERMINED = "underdetermined"
    TENSION = "tension"
    CONTRADICTION = "contradiction"
```

```python
class VerificationState(str, Enum):
    UNASSESSED = "unassessed"
    INTERNAL_ONLY = "internal_only"
    EVIDENCE_SUPPORTED = "evidence_supported"
    EXTERNALLY_VERIFIED = "externally_verified"
```

Binding distinctions:

```text
Rank != Decision
Conflict != Residual
Residual != Rank
CertificateRank does not imply ExternalTruth
```

`FINAL_JUDGMENT` is decision-space semantics, not support-rank semantics.

## 6) License taxonomy (evidence != permit)

```python
class LicenseKind(str, Enum):
    OBSERVATION = "observation"
    NORMALIZATION = "normalization"
    SEGMENTATION = "segmentation"
    PATH_SELECTION = "path_selection"
    FORMAL_TRANSFORMATION = "formal_transformation"
    DERIVATION = "derivation"
    LEXICAL_ATTESTATION = "lexical_attestation"
    COMPATIBILITY = "compatibility"
    BINDING = "binding"
    REFERENCE_RESOLUTION = "reference_resolution"
    COMPOSITION = "composition"
    EPISTEMIC_PROMOTION = "epistemic_promotion"
    EXTERNAL_VERIFICATION = "external_verification"
    REPAIR = "repair"
    EXCEPTION = "exception"
```

Permit object (governor-issued only):

```python
@dataclass(frozen=True)
class TransitionPermit:
    permit_id: str
    request_id: str
    source_ids: tuple[str, ...]
    target_stage: str
    operation_kind: str
    license_kind: LicenseKind
    passed_gate_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    invariant_ids: tuple[str, ...]
    rank_ceiling: SupportRank
    graph_version: int
    _governor_token: object
```

## 7) Origin/branch law

```text
Every output has evidentiary/execution origin.
Not every output is derivational branch.
```

Separate two difference classes:

- `ConstitutiveDifference`: required branch-forming difference.
- `DefeatingDifference`: invalidating difference that blocks transfer/license.

Derivation basis:

```python
@dataclass(frozen=True)
class DerivationBasis:
    origin_id: str
    common_universal_id: str
    effective_attribute: str
    possibility_condition: str
    trigger_cause: str
    constitutive_difference: str
    defeating_difference_refs: tuple[str, ...]
    branch_preventer_refs: tuple[str, ...]
    repair_preventer_refs: tuple[str, ...]
    preserved_invariants: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    rank_ceiling: SupportRank
```

## 8) Proof graph and rollback

Node kinds:

```text
EvidenceNode, RuleNode, CandidateNode, LicenseNode,
TransitionNode, DecisionNode, VerificationNode
```

Edge kinds:

```text
SUPPORTS, DERIVES_FROM, LICENSES, DEPENDS_ON, PRESERVES,
CONTRADICTS, BLOCKS, SUPERSEDES, INVALIDATES, REPAIRS, VERIFIES
```

Validity law:

```text
Valid(branch) iff there exists an active proof path from origin/evidence to branch.
```

Rollback discipline:

- deactivate invalid origin/evidence nodes without deleting history,
- recompute active paths and rank aggregation,
- revoke dependents lacking independent paths,
- preserve trace and recomputation history.

## 9) WORD-L0 → PRECOMP-L0 branch architecture

```text
WORD-L0
-> FORM-L0
-> PATH-L0
-> ROOTSTEM-L0 / NonWeightPath
-> AUG-L0
-> WEIGHT-L0R
-> LAFZI-L0
-> WADI-L0
-> NOUN/VERB/MABNI/HARF/ZARF/REFERENCE facets
-> LEXEME-L0
-> PRECOMP-L0
```

Discipline:

- keep this chain as an internal subgraph under current word/morphology boundaries,
- pass only `PRECOMP-L0` contracts to higher composition boundary,
- do not force root/derivation paths for harf/mabni tracks.

## 10) Weight re-foundation

Functional split:

```text
FormalWeightMatch -> WeightOntologicalInterface -> Lexical/Relational Licensing
```

`WEIGHT-L0R` emits readiness directions, not final semantic roles.

Examples of admissible readiness labels:

```text
SOURCE_AS_ATTRIBUTE_OF_CARRIER
CARRIER_AS_RECEIVER_OF_TRANSFORMATION
SOURCE_FRAMED_BY_PLACE_OR_TIME
SOURCE_LINKED_TO_INSTRUMENT_INTERFACE
AUGMENTED_DIRECTION_ALTERNATIVES
```

Forbidden leap examples:

```text
فاعل -> AgentFinal
مفعول -> PatientFinal
مَفْعَل -> PlaceFinal
PastPattern -> MujarradBabFinal
استفعل -> RequestMeaningFinal
```

## 11) Pre-composition contract model

```python
@dataclass(frozen=True)
class CompositionReadinessContract:
    contract_id: str
    lexeme_id: str
    target_composition_kind: str
    counterpart_constraints: tuple[str, ...]
    open_relation_slots: tuple[str, ...]
    allowed_bindings: tuple[str, ...]
    forbidden_bindings: tuple[str, ...]
    field_assessments: tuple["FieldAssessment", ...]
    dependency_refs: tuple[str, ...]
    trace_refs: tuple[str, ...]
    graph_version: int
    assessment: "Assessment"
```

Admissible first contract kinds:

```text
NOMINAL_PREDICATION
VERBAL_PREDICATION
ADJECTIVAL_MODIFICATION
IDAFA
PREPOSITIONAL_BINDING
REFERENCE_BINDING
ZARF_BINDING
CONDITIONAL_BINDING
EXCEPTION_RESTRICTION
```

`PRECOMP-L0` may not emit:

```text
FinalSyntacticRole
ActualBinding
ClosedRelation
Ifadah
Judgment
ExternalTruth
```

## 12) Minimal executable constitutional pilot

Bootstrapping set:

- `كاتِبٌ`: root/stem/augment/weight readiness -> lexical attestation -> noun facet -> isolated lexeme -> nominal/adjectival precomp readiness.
- `فِي`: harf/mabni path -> derivational weight blocked -> operator identity/open slot -> prepositional readiness.
- `كَتَبَ`: bab readiness may remain `SUSPENDED` with `PAST_PRESENT_PAIR_REQUIRED`.

Mandatory invalidation test:

- invalidate root evidence of `كاتِبٌ`,
- preserve word/form artifacts,
- recompute dependent candidates,
- revoke dependent weight/lexical/precomp contracts if proof path collapses,
- allow reactivation only through independent evidence,
- never delete historical trace.

## 13) Migration strategy from current implementation

- Keep `AFJGGovernor` strictly for LLM-proposal governance.
- Recast `LayerSovereigntyRegistry` semantics as policy registry (no implicit governance authority by name alone).
- Keep `analyzer/wazn/matcher.py` as low-level formal matcher through adapter boundary.
- Replace direct pattern-role vectors with non-final readiness interfaces.
- Move from folded word semantics toward explicit proof-graph separation between form/weight/wadi/relation.
- Keep AFU compatibility adapter so public answer surfaces can stay coarse while internal ranks remain granular.

## 14) Final constitutional synthesis

```text
Every output has evidentiary origin.
Not every output is derivational branch.
No layer self-licenses transition.
No execution without preflight.
No approval without postflight.
No output without proof graph.
No meaning from weight.
No role-finalization from pattern labels.
No external truth from internal certificate.
```

This document is a design target for staged implementation. It does not amend ratified chain status by itself.

## 15) Non-executable constitutional review matrix (18 verification domains)

Status: human-review checklist only. This matrix is not machine-executable, is not CI-enforced, does not ratify runtime behavior, and does not itself prove coverage.

| RuleID | Domain | Invariant | Required Inputs | Acceptance | Rejection | Suspension | FailureCode | Required Rank | Blocking Residuals | Trace Requirement | Proposed Positive Test | Proposed Negative Test | Runtime Mapping Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GOV-R01 | Goal and claim boundary | Document class remains proposal-only and non-totalizing. | Objective statement, scope statement, forbidden-output registry. | Scope is explicit and bounded. | Runtime/ratification/completeness claim appears without admitted law step. | Scope remains ambiguous pending boundary declaration. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | SCOPE_AMBIGUITY, TOTALITY_CLAIM | Section + row trace references are present. | Bounded claims only. | Universal completeness claim inserted. | NOT_MAPPED |
| GOV-R02 | Foundational postulates | Default transition is deny unless explicitly licensed. | Transition request, stage map, gate registry. | Permit path explicitly includes preflight -> execution -> postflight. | Direct execution with no permit or missing gate stage. | Permit evidence incomplete and cannot clear preflight. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | MISSING_PERMIT, MISSING_PREFLIGHT | Transition trace references request and gate path. | Licensed transition path documented. | Forged permit or skipped preflight accepted. | NOT_MAPPED |
| GOV-R03 | State-space separation | `Rank != Decision`, `Conflict != Residual`, `Residual != Evidence`, `Evidence != Permit`. InternalCertificate alone does not entail ExternalTruth (`InternalCertificate \nRightarrow ExternalTruth`). | Candidate tuple, evidence refs, permit refs, verification refs. | State fields remain independent and auditable. | Single-field collapse or truth implied from internal certificate alone. | Verification deferred pending independent external evidence. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | STATE_COLLAPSE, TRUTH_LEAP | Trace links each field decision to source evidence. | Same rank can lead to different decisions. | Internal certificate auto-promoted to external truth. | NOT_MAPPED |
| GOV-R04 | Independent governor cycle | Layer does not self-license; engine does not issue permits. | Proposal, preflight report, execution report, postflight report. | One complete cycle per request with immutable identifiers. | Self-licensing, engine-issued permit, or commit without postflight. | Request paused while postflight evidence is unresolved. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | GOVERNOR_INDEPENDENCE_BREACH | Trace captures full cycle (proposal -> commit/revoke/reopen). | Valid cycle with external governor approval recorded. | Execution proceeds after rejection or without postflight. | NOT_MAPPED |
| GOV-R05 | Permit taxonomy | Permit kind is explicit artifact, not inferred from evidence alone. | License kind, operation kind, gate pass set, invariant set. | Permit kind matches operation and gate family. | Evidence-only transition or permit-kind mismatch. | Transition paused when kind cannot be resolved safely. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | PERMIT_KIND_AMBIGUOUS | Trace includes permit_id and governing gate set. | Lexical step under lexical permit kind. | Derivation accepted under observation-only permit. | NOT_MAPPED |
| GOV-R06 | Origin/branch law | Branch requires full derivation basis + blocker clearance. | Derivation basis bundle, blocker refs, evidence refs. | Basis complete and blockers explicitly cleared. | Missing basis term or active defeating/preventing blocker. | Branch held while blocker status is unresolved. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | DEFEATING_DIFFERENCE_ACTIVE, PREVENTER_ACTIVE | Trace links branch to basis components and blockers. | Branch opens with complete basis. | Branch claimed from retrieval/matching only. | NOT_MAPPED |
| GOV-R07 | Proof-graph validity and rollback | Approved claim requires valid proof path; all artifacts require provenance path. | Proof nodes/edges, invalidation event, recomputation plan. | Active, sound proof path remains after recomputation for approved claims. | Approved claim has collapsed/invalid proof path or history is deleted. | Claim status deferred while recomputation is incomplete. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | PROOF_PATH_INVALID, RECOMPUTE_PENDING | Provenance and proof references are both present when required. | Dependent revocation after ancestor invalidation. | Approved node remains active after upstream invalidation. | NOT_MAPPED |
| GOV-R08 | Global transition order | No unlicensed skip across constitutional stages. | Stage sequence, handoff contracts, gate decisions. | Transition follows a licensed path (including licensed alternate paths). | Straight-line forbidden jump or missing licensed handoff. | Alternate-path request waits for explicit license. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | UNLICENSED_SKIP | Trace shows licensed path edges for each transition. | Licensed alternate path accepted. | Unlicensed direct jump accepted. | NOT_MAPPED |
| GOV-R09 | Word geometry (`WORD-L0` -> `PRECOMP-L0`) | Word branch emits readiness contracts only, never final closure. | Word/form/path/rootstem/aug/weight/lafzi/wadi/facet/lexeme/precomp carriers. | Precomp contracts include open slots and constraints only. | Final role/binding/ifadah/hukm emitted in word branch. | Contract deferred when counterpart constraints are unresolved. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | PRECOMP_CLOSURE_LEAP | Trace links PRECOMP output to upstream word subgraph. | Harf/mabni non-weight path remains admissible. | Root/derivation forced for all tokens. | NOT_MAPPED |
| GOV-R10 | Weight readiness boundary | Weight output is readiness direction, not final meaning/role. | Formal match results, readiness labels, lexical compatibility evidence. | Interface-level readiness remains defeasible. | Pattern labels mapped directly to final semantic roles. | Weight readiness held pending lexical licensing. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | WEIGHT_ROLE_FINALIZATION | Trace records readiness labels and compatibility evidence. | `SOURCE_AS_ATTRIBUTE_OF_CARRIER` emitted as readiness only. | `فاعل -> AgentFinal` accepted as final role. | NOT_MAPPED |
| GOV-R11 | Composition boundary | Composition readiness precedes closure; no ifadah in precomp. | Composition contract, counterpart constraints, relation slots. | Contract remains typed, bounded, and trace-linked. | Closed relation/ifadah/judgment emitted from PRECOMP stage. | Composition waits for missing counterpart evidence. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | PRECOMP_IFADAH_LEAP | Trace links contract to downstream gate request. | Nominal/verbal readiness contract only. | Proposition-level closure emitted from precomp. | NOT_MAPPED |
| GOV-R12 | Mantuq/Mafhum operator discipline | Operator tokens trigger branch requests; they do not auto-emit Mafhum verdicts. | Explicit closure, operator signals, gate request, blocker audit. | Inference branch opens only through licensed gate and blocker audit. | Unified inference collapse or direct operator-to-verdict jump. | Branch request paused when blocker audit is incomplete. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | OPERATOR_SHORTCUT, BLOCKER_AUDIT_MISSING | Trace preserves explicit origin and branch-open request. | Operator opens request only. | Operator auto-produces Mafhum ruling. | NOT_MAPPED |
| GOV-R13 | Convention-domain classification | Linguistic/customary/shar'i convention classes are usage-domain classes, not external truth claims. | Usage mode, transfer relation candidate, qarinah evidence, alternatives. | Classification stays domain-typed with explicit evidence. | Usage class converted into external existence/truth claim. | Classification held pending positive qarinah/evidence. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | CLASSIFICATION_TRUTH_LEAP | Trace separates usage-class evidence from truth verification. | Majaz accepted with transfer relation plus positive qarinah. | Majaz accepted from tension alone. | NOT_MAPPED |
| GOV-R14 | Repair economy | `MinimalCost != Truth`; repair must be sufficient and licensed. | Metric space, alternatives, cost function, sufficiency criterion, evidence support. | Minimal sufficient licensed repair selected. | Cheapest-but-insufficient repair promoted to truth. | Repair decision paused while sufficiency proof is incomplete. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | INSUFFICIENT_REPAIR | Trace records alternatives and sufficiency rationale. | Second-cheapest sufficient repair selected over cheapest insufficient one. | Cheapest path promoted as truth verdict. | NOT_MAPPED |
| GOV-R15 | Engine interface boundary | Engines consume permits and emit declared execution records only. | Permit object, operation payload, stage contract, trace envelope. | Invalid permit deterministically refused; no undeclared outputs. | Engine executes without permit, mutates permit, or emits hidden outputs. | Execution paused while permit integrity is unresolved. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | PERMIT_INTEGRITY_UNRESOLVED | Trace binds execution record to permit_id and stage contract. | Invalid permit returns refusal path. | Engine fabricates permit id and proceeds. | NOT_MAPPED |
| GOV-R16 | Constitutional test obligations | Constitutional tests declare origin, branch, chain, forbidden outputs, and trace expectation. | Test schema, fixtures, expected failures. | Positive and negative obligations are both declared. | Bare local-success assertion with no constitutional declaration. | Test status pending until constitutional metadata is complete. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | TEST_ORIGIN_MISSING, TEST_CHAIN_MISSING | Trace expectation declared in test case metadata. | Refusal test includes named failure surface. | Happy-path only test accepted as constitutional. | NOT_MAPPED |
| GOV-R17 | Coverage posture | No completeness declaration without independent coverage proof and unresolved-gap ledger. | Coverage matrix, unresolved-gap ledger, counterexamples, replay traces. | Coverage reporting is reproducible and explicitly gap-aware. | Completeness claim emitted with unresolved gaps. | Coverage claim suspended while independent evidence is pending. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | COVERAGE_GAP_OPEN | Trace links each claim to reproducible coverage evidence. | Report blocks totality claim while gaps are open. | CI green treated as completeness proof. | NOT_MAPPED |
| GOV-R18 | Ratification ordering | Implementation ordering follows admitted chain position only. | Chain roadmap position, ratification status, implementation diff. | Change stays inside admitted step and declared boundary. | Bundled multi-step chain leap or premature downstream opening. | Change paused pending dedicated admission/ratification step. | UNREGISTERED - requires dedicated ratification PR | PROPOSAL_ONLY | FORBIDDEN_LEAP | Trace includes chain-position and boundary justification. | Governor/proof-first ordering preserved. | Downstream runtime opened before law admission. | NOT_MAPPED |

Execution reminder: rows in this matrix are review obligations, not executable runtime gates.

## 16) Terminology Policy

Each term should carry a stable canonical identifier, an Arabic form, an ASCII identifier, a scholarly transliteration, and deprecated spellings where relevant.

| canonical_id | Arabic term | ASCII identifier | scholarly transliteration | deprecated spellings |
|---|---|---|---|---|
| IFADAH | الإفادة | ifadah | ifādah | ifadāh |
| MANTUQ | المنطوق | mantuq | mantuq | - |
| MAFHUM | المفهوم | mafhum | mafhum | - |
| IQTIDA | الاقتضاء | iqtida | iqtida | iqtida' |
| ISHARAH | الإشارة | isharah | isharah | - |
| IMA | الإيماء | ima | ima | ima' |
| MAJAZ | المجاز | majaz | majaz | - |
| QARINAH | القرينة | qarinah | qarinah | qarinah |
| WAZN | الوزن | wazn | wazn | - |
| MABNI | المبني | mabni | mabni | - |
| HARF | الحرف | harf | harf | - |
