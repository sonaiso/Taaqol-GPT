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
