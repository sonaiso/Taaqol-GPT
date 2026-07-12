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
-> Commit | Revoke | Reopen
```

Layer proposes and engine executes, but only an independent governor licenses transitions and approves/revokes outcomes.

Proposed execution contract (proposal-only, non-ratified):

```text
PreflightResult =
    Permit
  | PreflightRejected
  | PreflightSuspended
```

```text
TransitionResult =
match GovernorPreflight(Proposal, CurrentProofGraph, CurrentState) with
| Permit(p) ->
    GovernorPostflight(
      StageExecute(p, InputSnapshot)
    )
| PreflightRejected(r) ->
    RejectedResult(r)
| PreflightSuspended(s) ->
    SuspendedResult(s)
```

```text
StageExecute:
Permit x InputSnapshot -> ExecutionCandidate
```

```text
NoPermit => NoEffectfulExecution
NoApprovedPostflight => NoCommit
No State Mutation Before Approved Postflight
```

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

Provisional project definitions:

```text
For this proposal, OperationalThinking(S) is provisionally defined as:
DistinguishInput
and GenerateCandidates
and TestConstraints
and LicenseOrSuspend
and PreserveTrace
and ReviseOnInvalidation

For this proposal, SystemicSelf(S) is provisionally defined as:
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
State(x) =
<Preflight(x), Postflight(x), Commit(x), Lifecycle(x), Rank(x), Conflict(x), Residuals(x), Verification(x)>
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
class PreflightDecision(str, Enum):
    PENDING = "pending"
    PERMITTED = "permitted"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
```

```python
class PostflightDecision(str, Enum):
    UNASSESSED = "unassessed"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
```

```python
class CommitState(str, Enum):
    UNCOMMITTED = "uncommitted"
    COMMITTED = "committed"
```

```python
class ArtifactLifecycle(str, Enum):
    ACTIVE = "active"
    REOPENED = "reopened"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"
```

State distinctions (proposal-only, non-ratified):

```text
REJECTED: transition was not granted.
APPROVED: postflight accepted execution candidate.
COMMITTED: approved candidate was atomically persisted in canonical state.
REVOKED: committed artifact later lost required basis.
SUPERSEDED: prior output remains historically traceable, but an updated output replaces it for active flow.
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

Residual contract (proposal-only, non-ratified):

```python
@dataclass(frozen=True)
class Residual:
    category: "ResidualCategory"
    disposition: "ResidualDisposition"
    source: str
    scope: str
    severity: "ResidualSeverity"
    rank_impact: "RankImpact"
    repair_path: tuple[str, ...]
    conflict_ref: str | None
    trace_ref: str
```

Minimal proposed residual taxonomy:

```text
ResidualCategory:
AMBIGUITY
UNDERDETERMINATION
MISSING_EVIDENCE
DOMAIN_MISMATCH
SCOPE_GAP
UNRESOLVED_REFERENCE
UNFILLED_SLOT
FAILED_VERIFICATION

ResidualDisposition:
BLOCKING
DEFERRED
REPAIRABLE
NON_BLOCKING
CONTRADICTORY
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
    governor_id: str
    source_ids: tuple[str, ...]
    operation_id: str
    operation_version: str
    target_stage: str
    operation_kind: str
    license_kind: LicenseKind
    input_snapshot_hash: str
    relevant_subgraph_hash: str
    evidence_bundle_hash: str
    identity_obligation_ids: tuple[str, ...]
    passed_gate_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    invariant_ids: tuple[str, ...]
    rank_ceiling: SupportRank
    nonce: str
    issued_at: str
    expires_at: str
    single_use: bool
    signature: str
    graph_version: int
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

Proposed validity discipline (proposal-only, non-ratified):

```text
ProposedValid(x) requires a path that is:
- active
- licensed
- domain-sound
- identity-preserving
- rank-sufficient
- free of blocking conditions
- trace-complete
```

Node validity and claim validity are not identical (proposal-only, non-ratified):

```text
ProposedValidClaim(x, c) only if there exists a ProofDerivationSubgraph H such that:
- Concludes(H, c)
- AllRequiredPremisesActive(H)
- AllRulesLicensed(H)
- DomainCompatible(H, c)
- IdentityObligationsSatisfied(H)
- TraceComplete(H)
- NoBlockingResidual(H, c)
- NoDefeatingDifference(H, c)
- RankCeiling(H) >= RequiredRank(c)
```

Proposed rank aggregation discipline:

```text
Rank(path) = meet(
  evidence_rank,
  identity_rank,
  gate_rank,
  closure_rank,
  residual_rank_ceiling,
  explicit_rank_ceiling
).
Rank(x) is not max(activePath_i) by default.
Rank(x) should use AggregateIndependentPaths(activePath_1..activePath_n)
with explicit checks for independence, domain compatibility,
duplicate-evidence suppression, and blocking conflicts.
```

Rollback discipline:

- deactivate invalid origin/evidence nodes without deleting history,
- recompute active paths and rank aggregation,
- revoke dependents lacking independent paths,
- preserve trace and recomputation history.

## 9) WORD-L0 → PRECOMP-L0 branch architecture (proposed typed directed graph)

```text
This proposal treats WORD-L0 ... PRECOMP-L0 as a typed directed graph,
not as a mandatory single linear chain.

Example licensed path (illustrative only):
WORD-L0 -> FORM-L0 -> PATH-L0 -> ROOTSTEM-L0 -> AUG-L0 -> WEIGHT-L0R
-> LAFZI-L0 -> WADI-L0 -> LEXEME-L0 -> PRECOMP-L0

Required graph controls for future ratification:
- branch predicates
- join contracts
- alternate-path licenses
- cycle prohibition
- skip-license rules
- handoff invariants
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

Relation frame is not proposition closure (proposal-only, non-ratified):

```text
RelationEdge DOES_NOT_ENTAIL Proposition
```

```text
Proposed transition:
RelationGraph
+ PredicativeClosure
+ ScopeClosure
+ ReferenceSufficiencyForProposition
-> PropositionCandidate
```

## 12) Proposed non-executable minimal pilot specification

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

Proposed commit discipline (proposal-only, non-ratified):

```text
Commit(x) only if:
- MatchingPermit(x)
- PermitAuthentic(x)
- PermitUnconsumed(x)
- PermitUnexpired(x)
- RelevantSnapshotUnchanged(x)
- ExecutionSucceeded(x)
- PostflightApproved(x)
- ProofGraphRecorded(x)
- ResidualsPreserved(x)
- NoBlockingResidual(x)
- IdentityObligationsSatisfied(x)
- TraceComplete(x)
- DependenciesRegistered(x)
- RankBounded(x)
- DomainBounded(x)
```

## 14) Final constitutional synthesis

```text
Every output has provenance/execution origin.
Every committed epistemic claim has evidentiary support.
Not every output is derivational branch.
No layer self-licenses transition.
No execution without preflight.
No approval without postflight.
No approved epistemic output without proof/dependency graph.
No meaning from weight.
No role-finalization from pattern labels.
No external truth from internal certificate.
Maqam DOES_NOT_ENTAIL InventedLexicalMeaning.
```

This document is a design target for staged implementation. It does not amend ratified chain status by itself.

Maqam constraint discipline (proposal-only, non-ratified):

```text
MaqamConstraint = CandidateFilter + CompatibilityEvidence + ScopeConstraint + SelectionPreference
```

Maqam can restrict, prioritize, and resolve scope/reference under evidence.
Maqam cannot create lexical meaning outside licensed usage/transfer paths.
Maqam cannot directly promote rank outside gate discipline.

Four-cycle architectural summary (proposal-only, non-ratified):

```text
Formation cycle:
Carrier -> Form -> PathGate
PathGate -> RootStemPath -> AugmentationAnalysis -> WeightReadiness
PathGate -> NonWeightPath -> Mabni/Harf/Jamid/Proper/BorrowedReadiness
{WeightReadiness | NonWeightReadiness} -> LafziPotential -> WadCandidate
-> MufradMadlulCandidate -> AnchorCandidates -> LexemeCandidate -> PrecompReadiness

Relation cycle:
Anchors -> RelationFrame -> BindingRequest -> Permit -> RelationEdge

Utterance-signification cycle:
StructuralRelationCandidate -> CouplingHypotheses <-> MaqamConstraints
-> StabilityGate -> SemanticRelationCandidate -> IfadahCandidate
-> {STABLE | SUSPENDED | CONTRADICTORY | LIMIT_REACHED}

Certification cycle:
Proposition -> Evidence -> RankedJudgment -> ExternalVerification
```

Proposed minimal implementation nucleus for staged implementation:

```text
Contracts:
- GovernedState
- Proposal
- Permit
- Residual
- ProofNode
- ProofEdge
- RelationFrameCandidate
- CommittedRelation

Operations:
- preflight()
- execute_binding()
- postflight()
- invalidate_and_recompute()
```

Proposed constitutional golden cases:

```text
- nominal_predication_success
- intransitive_verbal_predication_success
- open_attachment_without_predication
- origin_invalidation_revokes_dependent_relation
```

Proposed constitutional failure cases:

```text
- binding_without_permit
- self_approval_by_engine
- relation_from_compatibility_only
- dependent_survives_without_independent_path
```

## 15) Non-executable constitutional review matrix (18 verification domains)

Status: human-review checklist only. This matrix is not machine-executable, is not CI-enforced, and has no runtime, rank, transition, or certificate effect.

These labels are documentation proposals only and have no runtime, rank, transition, or certificate effect.

| ReviewItemID | Domain | DocumentStatus | ConstitutionalOriginStatus | ProposedInvariant | RequiredDocumentationInputs | HumanAcceptanceCriterion | HumanRejectionCriterion | HumanSuspensionCriterion | ProposedFailureCode | FailureCodeRegistryStatus | RequiredSupportRank | ProposedBlockingConditionLabels | TraceSpecificationStatus | RuntimeMappingStatus | ProposedPositiveTest | ProposedNegativeTest | OpenResidual |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DOC-R01 | Goal and claim boundary | PROPOSAL_ONLY | EDITORIAL_RESTATEMENT | Document is proposal-only and non-totalizing. | Scope statement, objective statement. | Scope is bounded and non-totalizing. | Any ratified/runtime/completeness claim appears. | Scope remains ambiguous. | DOC90_PFC_01 | UNREGISTERED | NOT_APPLICABLE | SCOPE_AMBIGUITY,TOTALITY_CLAIM | PROSE_ONLY | NOT_MAPPED | Bounded-claim wording preserved. | Completeness claim injected. | Still prose-only and non-executable. |
| GOV-R01 | Foundational postulates | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | Default transition is deny unless licensed. | Transition-cycle proposal text. | Preflight->permit/reject/suspend->execution->postflight path is explicit in text. | Direct execution described without license path. | Missing preflight or postflight evidence in description. | DOC90_PFC_02 | UNREGISTERED | NOT_APPLICABLE | MISSING_PERMIT,MISSING_PREFLIGHT | PROSE_ONLY | NOT_MAPPED | Licensed transition example remains proposal-only. | Forged permit scenario accepted. | No parser or gate runtime exists. |
| STATE-R01 | State-space separation | PROPOSAL_ONLY | DERIVED_FROM_EXISTING_LAW | Rank/decision/conflict/residual/verification stay separated. InternalCertificate DOES_NOT_ENTAIL ExternalTruth. | State-space definitions, distinction list. | Separation wording remains explicit with no entailment claim. | Any truth entailment from internal certificate appears. | External verification conditions not documented. | DOC90_PFC_03 | UNREGISTERED | NOT_APPLICABLE | STATE_COLLAPSE,TRUTH_LEAP | PROSE_ONLY | NOT_MAPPED | Same rank, different decision paths documented. | Certificate promoted to external truth. | No executable state validator exists. |
| GOV-R02 | Independent governor cycle | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | Governor is structurally independent from layers and engine. | Governor-cycle section, permit section. | One explicit independent cycle per request in prose. | Self-licensing or engine-issued permit in prose. | Postflight not documented. | DOC90_PFC_04 | UNREGISTERED | NOT_APPLICABLE | GOVERNOR_INDEPENDENCE_BREACH | PROSE_ONLY | NOT_MAPPED | Independent cycle wording retained. | Layer self-licenses transition. | No permit authenticity mechanism is implemented. |
| GOV-R03 | Permit taxonomy | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | Permit kind is explicit and distinct from evidence. | License taxonomy, permit dataclass proposal. | Kind is typed in proposal and bound to operation in prose. | Evidence-only transition claim appears. | Kind matching criteria not fully specified. | DOC90_PFC_05 | UNREGISTERED | NOT_APPLICABLE | PERMIT_KIND_AMBIGUOUS | PROSE_ONLY | NOT_MAPPED | Typed permit proposal remains explicit. | Untyped permit accepted in prose. | Permit fields are still non-registered proposal fields. |
| PROOF-R01 | Proof-graph validity and rollback | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | ProposedValid requires active, licensed, domain-sound, identity-preserving, rank-sufficient, blocking-free, trace-complete path. | Proof-node/edge proposal and rollback section. | Proposed validity conditions are all present in prose. | Active-path-only wording is reintroduced. | Any condition is missing or unclear. | DOC90_PFC_06 | UNREGISTERED | NOT_APPLICABLE | PROOF_PATH_INVALID,RECOMPUTE_PENDING | PROSE_ONLY | NOT_MAPPED | Full proposed condition list preserved. | Validity reduced to active-path-only claim. | Path soundness remains non-executable. |
| CHAIN-R01 | Global transition order | PROPOSAL_ONLY | DERIVED_FROM_EXISTING_LAW | No unlicensed skip; licensed alternates may exist. | Transition-order section and path section. | Unlicensed skip forbidden, licensed alternates allowed. | Absolute no-skip wording or straight-line jump accepted. | Alternate-path licensing unspecified. | DOC90_PFC_07 | UNREGISTERED | NOT_APPLICABLE | UNLICENSED_SKIP | PROSE_ONLY | NOT_MAPPED | Licensed alternate path example remains. | Direct jump accepted as normal. | Join contracts still not formalized. |
| WORD-R01 | WORD-L0 to PRECOMP-L0 graph | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | WORD-L0...PRECOMP-L0 is a proposed typed directed graph. | Branch-architecture section. | Graph framing and required controls are explicit. | Mandatory linear chain claim appears. | Required controls are partially specified. | DOC90_PFC_08 | UNREGISTERED | NOT_APPLICABLE | LINEAR_CHAIN_COLLAPSE | PROSE_ONLY | NOT_MAPPED | Graph controls list retained. | Linear must-pass chain asserted. | Branch predicates and joins remain unspecified. |
| WEIGHT-R01 | Weight readiness boundary | PROPOSAL_ONLY | DERIVED_FROM_EXISTING_LAW | Weight emits readiness only, not final semantic role. | Weight section and forbidden-leap examples. | Readiness-only wording preserved. | Pattern-to-final-role mapping accepted. | Readiness criteria unclear. | DOC90_PFC_09 | UNREGISTERED | NOT_APPLICABLE | WEIGHT_ROLE_FINALIZATION | PROSE_ONLY | NOT_MAPPED | Readiness label example kept as proposal. | AgentFinal-style shortcut allowed. | No runtime gate enforces this in docs/90. |
| COMP-R01 | Composition boundary | PROPOSAL_ONLY | DERIVED_FROM_EXISTING_LAW | PRECOMP emits readiness contracts only, no closure. | PRECOMP section and disallowed outputs list. | Closure remains disallowed in PRECOMP prose. | Ifadah/judgment output is allowed in PRECOMP prose. | Counterpart constraints remain incomplete. | DOC90_PFC_10 | UNREGISTERED | NOT_APPLICABLE | PRECOMP_IFADAH_LEAP | PROSE_ONLY | NOT_MAPPED | Readiness-only composition contract preserved. | Proposition-level closure emitted from PRECOMP. | Contract constraints still prose-only. |
| DALALA-R01 | Mantuq/Mafhum operator discipline | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | Operator signals open requests only; they do not auto-emit verdicts. | Matrix rows on operator discipline and branch gating. | Gate-request discipline remains explicit in prose. | Operator-to-verdict shortcut appears. | Blocker audit expectations are incomplete. | DOC90_PFC_11 | UNREGISTERED | NOT_APPLICABLE | OPERATOR_SHORTCUT,BLOCKER_AUDIT_MISSING | PROSE_ONLY | NOT_MAPPED | Request-only operator behavior documented. | Direct operator verdict accepted. | Branch semantics remain unratified in this doc. |
| USAGE-R01 | Usage and majaz classification | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | Usage classes are domain classifications, not truth claims. | Usage/majaz section. | Domain-typing and qarinah evidence stay explicit. | Usage class treated as external truth. | Evidence for classification remains incomplete. | DOC90_PFC_12 | UNREGISTERED | NOT_APPLICABLE | CLASSIFICATION_TRUTH_LEAP | PROSE_ONLY | NOT_MAPPED | Domain-typed classification wording retained. | Majaz accepted without positive qarinah. | No formal evidence schema is provided. |
| REPAIR-R01 | Repair economy | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | MinimalCost DOES_NOT_ENTAIL Truth; repair must be sufficient and licensed. | Repair section inputs and criteria. | Sufficiency and licensing remain required in prose. | Cheapest path treated as truth. | Sufficiency proof conditions incomplete. | DOC90_PFC_13 | UNREGISTERED | NOT_APPLICABLE | INSUFFICIENT_REPAIR | PROSE_ONLY | NOT_MAPPED | Sufficient-over-cheapest example retained. | Cheapest-only acceptance appears. | No formal metric contract exists here. |
| ENGINE-R01 | Engine interface boundary | PROPOSAL_ONLY | NEW_UNRATIFIED_HYPOTHESIS | Engine consumes permit and emits declared outputs only. | Engine interface section and permit proposal. | Invalid permit refusal requirement remains explicit in prose. | Engine executes without permit or mutates permit. | Permit integrity checks remain unspecified. | DOC90_PFC_14 | UNREGISTERED | NOT_APPLICABLE | PERMIT_INTEGRITY_UNRESOLVED | PROSE_ONLY | NOT_MAPPED | Invalid-permit refusal scenario documented. | Engine fabricates permit and proceeds. | No runtime mapping or schema enforcement exists. |
| TEST-R01 | Constitutional test obligations | PROPOSAL_ONLY | DERIVED_FROM_EXISTING_LAW | Tests must declare origin, branch, chain, and forbidden outputs. | Test-geometry references and matrix row. | Positive/negative obligations remain explicitly documented. | Happy-path-only local assertion treated as constitutional. | Expected refusal metadata is incomplete. | DOC90_PFC_15 | UNREGISTERED | NOT_APPLICABLE | TEST_ORIGIN_MISSING,TEST_CHAIN_MISSING | PROSE_ONLY | NOT_MAPPED | Refusal-surface proposal remains explicit. | Bare local success counted as constitutional. | No test harness added by this doc. |
| COVERAGE-R01 | Coverage posture | PROPOSAL_ONLY | EDITORIAL_RESTATEMENT | No completeness claim without independent coverage evidence and open-gap ledger. | Coverage row and no-totality statements. | Coverage claims remain gap-aware. | Completeness declared while gaps remain. | Independent evidence remains pending. | DOC90_PFC_16 | UNREGISTERED | NOT_APPLICABLE | COVERAGE_GAP_OPEN | PROSE_ONLY | NOT_MAPPED | Gap-aware coverage statement retained. | CI green used as completeness proof. | Coverage model remains proposal-level. |
| CHAIN-R02 | Ratification ordering | PROPOSAL_ONLY | DERIVED_FROM_EXISTING_LAW | Changes must stay inside admitted chain position. | Chain-position references and boundary language. | Admitted-step discipline remains explicit in prose. | Multi-step bundled leap is described as acceptable. | Admission dependency unresolved. | DOC90_PFC_17 | UNREGISTERED | NOT_APPLICABLE | FORBIDDEN_LEAP | PROSE_ONLY | NOT_MAPPED | Step-bounded ordering statement preserved. | Premature downstream opening accepted. | This document cannot ratify chain movement. |
| DOC-R02 | Proposal bundle map | PROPOSAL_ONLY | EDITORIAL_RESTATEMENT | This file contains multiple proposal scopes and must not be treated as one ratified branch. | Section mapping below and index classification. | Bundle map stays explicit and non-ratifying. | File is described as one ratified constitutional branch. | Scope partition remains unclear. | DOC90_PFC_18 | UNREGISTERED | NOT_APPLICABLE | SCOPE_COLLAPSE | PROSE_ONLY | NOT_MAPPED | Proposal-family map is present. | Single-branch ratification claim appears. | Proposal split to `docs/9x_*` remains optional future cleanup. |

## 16) Proposal bundle map (non-ratified)

- Governor proposal: sections 4, 6, 7.
- Proof-graph proposal: section 8.
- Word architecture proposal: sections 9, 11.
- Weight proposal: section 10.
- Human review matrix: section 15.

## 17) Terminology Policy

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
