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

## 15) Executable verification table (18 constitutional chapters)

| # | Chapter | Invariants (must always hold) | Inputs | Acceptance conditions | Rejection/Suspension conditions | Edge tests (positive/negative) |
|---|---|---|---|---|---|---|
| 1 | Goal and claim boundary | Document class is `licensed transitions constitution + relations algebra draft`; no completeness claim. | Project objective statement, scope statement, forbidden-output registry. | Scope is explicit, measurable, and non-totalizing. | Any "complete Arabic algebra" or universal-coverage claim without proof. | `+` objective stated with bounded claims; `-` completeness slogan injected into runtime/API docs. |
| 2 | Foundational postulates | Default transition state is deny; no stage jump without governor permit. | Transition request, stage map, gate registry. | Permit path includes preflight -> execution -> postflight. | Direct engine transition with missing permit or skipped gate. | `+` permitted transition with trace; `-` forged permit token or skipped preflight. |
| 3 | Separation of rank/decision/conflict/residual/verification | `Rank != Decision`, `Conflict != Residual`, `Residual != Evidence`, `Evidence != Permit`, `InternalCertificate !-> ExternalTruth`. | Candidate state tuple, evidence refs, permit refs, verification refs. | Each state field is independently populated and auditable. | Collapsed single verdict field or implicit truth from rank/certificate. | `+` same rank with different decision outcomes; `-` certificate promoted to external truth automatically. |
| 4 | Independent governor and permit cycle | Governor is structurally separate from layers/engines; cycle is total. | `LayerProposal`, governor preflight result, execution report, postflight report. | One closed cycle per transition request with immutable ids. | Layer self-licensing, engine-issued permit, missing postflight. | `+` permit -> execute -> commit; `-` execution allowed after rejection, or commit without postflight. |
| 5 | Permit taxonomy | Permit kind is explicit and not inferred from evidence alone. | License kind enum, operation kind, gate pass set, invariant set. | Permit kind matches operation and passed gate family. | Evidence-only transition, mismatched permit kind, untyped permit. | `+` lexical attestation permit for lexical step; `-` derivation run under observation-only permit. |
| 6 | Origin/branch law | No qiyas branch without origin + common universal + effective attribute + possibility + trigger + constitutive difference + absence of defeating/preventing blockers. | Derivation basis bundle, blocker refs, evidence refs. | Full basis exists and blockers are explicitly cleared. | Missing basis term, unresolved defeating difference, active preventer. | `+` branch opens with complete basis; `-` branch claimed from retrieval/matching only. |
| 7 | Proof graph and rollback | No output without proof path; invalidation is non-destructive and trace-preserving. | Proof nodes/edges, invalidation event, recomputation plan. | Active path from origin/evidence to candidate remains after recompute. | Path collapse without independent support, or history deletion. | `+` dependent revocation after origin invalidation; `-` stale approved node remains active after ancestor invalidation. |
| 8 | Global chain (trace -> external verification) | Transition order is licensed and acyclic; no skipped constitutional stage. | Stage sequence, handoff contracts, gate decisions. | Every emitted artifact references prior licensed stage and trace. | Straight-line jump (forbidden), missing upstream contract. | `+` full chain walk to verification candidate; `-` direct jump from weight/tool output to certainty/knowledge. |
| 9 | Word geometry (`WORD-L0` -> `PRECOMP-L0`) | Word pipeline is internal subgraph; `PRECOMP-L0` is boundary output, not final syntax/meaning. | Word/form/path/rootstem/aug/weight/lafzi/wadi/facet/lexeme/precomp carriers. | Precomp contracts emitted with open slots and constraints only. | Final role/binding/ifadah/hukm emitted at word branch. | `+` harf/mabni non-weight path accepted; `-` forcing root/derivation path for all tokens. |
| 10 | Genus/source/readiness fit | Weight output is readiness direction, not meaning or final role. | Formal match results, readiness labels, lexical compatibility evidence. | Readiness labels stay interface-level and remain defeasible. | Mapping pattern labels directly to final semantic roles. | `+` `SOURCE_AS_ATTRIBUTE_OF_CARRIER` emitted; `-` `فاعل -> AgentFinal` accepted. |
| 11 | Composition and ifadah boundary | Composition readiness contracts precede any closure; no ifadah before licensed composition boundary. | Composition contract, counterpart constraints, open relation slots. | Contract is bounded, typed, and trace-linked for downstream gate use. | Closed relation/ifadah/judgment emitted from precomp stage. | `+` nominal/verbal readiness contract only; `-` proposition-level closure emitted from precomp. |
| 12 | Mantūq / Mafhūm / Iqtiḍāʾ / Ishārah / Imāʾ | Mantūq explicit branch is isolated from licensed inference branches; operators (condition/number/restriction/attribute/limit) are triggers, not Mafhūm verdicts. | Explicit utterance closure, operator signals, branch gate requests, blocker checks. | Inference branch opens only through its gate with blocker audit and origin preservation. | Unified inference layer collapse; Mafhūm opened directly from operator token; denied antecedent fallacy. | `+` condition token opens gate request only; `-` condition token auto-produces Mafhūm ruling. |
| 13 | Usage, truth-types, and majāz | Lexical/customary/legal truth are usage-domain classifications; majāz requires transfer relation + positive qarīnah. | Usage mode, transfer relation candidate, qarīnah evidence, competing analyses. | Classification remains domain-typed; qarīnah is explicit evidence; residual alternatives visible. | Converting usage class into external existence claim; treating residuals as qarīnah or vice versa. | `+` majāz accepted with relation+qarīnah; `-` majāz accepted from tension alone with no positive clue. |
| 14 | Archimedean repair economy | `MinimalCost != Truth`; repair must be sufficient, licensed, and evidence-supported. | Unit of measure, alternative space, cost function, sufficiency criterion, evidence support. | Chosen repair is minimal among sufficient licensed repairs. | Unspecified metric space/cost, or accepting cheapest-but-insufficient repair. | `+` second-cheapest sufficient repair selected over cheapest insufficient one; `-` cheapest path promoted to truth verdict. |
| 15 | Engine execution interfaces | Engines consume permits and emit execution records only within declared surfaces. | Permit object, operation payload, stage contract, execution trace envelope. | Deterministic refusal on invalid permit; no hidden side channels. | Engine executes without permit, mutates permit, or emits undeclared outputs. | `+` invalid permit returns named refusal; `-` engine fabricates permit id and proceeds. |
| 16 | Constitutional positive/negative tests | Every constitutional test declares origin law, branch, chain, expected verdict, forbidden outputs, rank ceiling, residual visibility, trace expectation. | Test case schema, fixtures, expected failure codes. | Positive and negative branches both covered with named failure codes. | Bare local-success assertions with no chain/origin/forbidden-output checks. | `+` refusal test with explicit failure code; `-` only happy-path assertion for gate closure. |
| 17 | Coverage proof and no-totality claim | No completeness declaration without independent coverage proof over grammar doors, exceptions, deletion, readings, reference, conflict, dialect, historical usage, rollback/invalidation. | Coverage matrix, unresolved-gap ledger, counterexample set, replay traces. | Coverage report is independent, reproducible, and gap-aware. | Global completeness claim with unresolved or unmeasured families. | `+` report marks open gaps and blocks totality claim; `-` CI green used as completeness evidence. |
| 18 | Ratification and execution ordering | Build order starts with governor/proof kernel, then language layers; no premature opening of downstream layers. | Chain roadmap position, ratification status, implementation diff. | Proposed change respects admitted step and forbidden surface. | Bundling multiple chain steps, or implementing later layer before law admission. | `+` GOV/PROOF-first patch with layer freeze; `-` opening inference/runtime branch before gate-law ratification. |

Execution reminder: each row is valid only if the governor cycle remains explicit (`Proposal -> Preflight -> Permit/Rejection/Suspension -> Execution -> Postflight -> Commit/Revoke/Reopen`) and all refusal paths emit named failure codes with visible residuals.
