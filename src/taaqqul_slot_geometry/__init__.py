"""Root package boundary for ``taaqqul_slot_geometry``.

This module keeps a stable-kernel-first root import surface while preserving
compatibility re-exports for established downstream imports.

Primary surfaces:

- ``taaqqul_slot_geometry.core``: constitutional kernel and transition law runtime.
- ``taaqqul_slot_geometry.gua``: additive GUA pilot extraction/proof surfaces.
- ``taaqqul_slot_geometry.weight``: Arabic/signification branch runtime surfaces.
- ``taaqqul_slot_geometry.audit``: audit shell and model-client protocol.
- ``taaqqul_slot_geometry.adapters``: concrete adapter admission surfaces.

Repository governance and historical chain records live in docs/governance
artifacts, not in this module docstring.
"""
from taaqqul_slot_geometry.adapters import (
    CONFIDENCE_SURFACE_NAMES,
    LEDGER_SURFACE_NAMES,
    RANK_SURFACE_NAMES,
    SUCCESSOR_SURFACE_NAMES,
    VERDICT_SURFACE_NAMES,
    AdapterAdmission,
    AdapterGuard,
    ConcreteAdapterCandidate,
    InMemoryModelClient,
    TransportSurface,
)
from taaqqul_slot_geometry.audit import (
    AnswerAudit,
    AuditBridgeState,
    AuditedAnswer,
    AuditedTanzilBridge,
    AuditedTanzilBridgeVerdict,
    ModelClient,
    bridge_tanzil_to_audit,
    emit_successor,
)
from taaqqul_slot_geometry.core import (
    ClosureState,
    FailureCode,
    Rank,
    Residual,
    ResidualKind,
)
from taaqqul_slot_geometry.core.evidence_contract import (
    SINGLE_SOURCE_EVIDENCE_CEILING,
    EvidenceContract,
    EvidenceSource,
)
from taaqqul_slot_geometry.core.forbidden_lines import (
    CANONICAL_REGISTRY,
    FORBIDDEN_STRAIGHT_LINES,
    TERMINOLOGY_TRANSFERS,
    ForbiddenLine,
    ForbiddenLineRegistry,
    TerminologyTransfer,
    is_forbidden_direct,
)
from taaqqul_slot_geometry.core.gamma import GammaResult, gamma
from taaqqul_slot_geometry.core.rank_lattice import RankLattice
from taaqqul_slot_geometry.core.residual_policy import (
    PERFORATING_KINDS,
    ResidualEvaluation,
    ResidualPolicy,
)
from taaqqul_slot_geometry.core.slot_graph import (
    Center,
    ConstructionResult,
    EntryBoundary,
    GenerationSource,
    Layer,
    OpeningPolicy,
    OutputBoundary,
    Slot,
    SlotBoundary,
    SlotGraph,
    SlotGraphSchemaError,
    SlotState,
    TraceRef,
)
from taaqqul_slot_geometry.core.trace_ledger import TraceEntryCandidate, TraceLedger
from taaqqul_slot_geometry.core.transition_gate import (
    GATE_RANK_CEILING,
    UNGATED_RANK_CEILING,
    TransitionGate,
    TransitionVerdict,
)
from taaqqul_slot_geometry.core.transition_state import TransitionState
from taaqqul_slot_geometry.g0_c1_carriers import (
    AnchorCertificate,
    BareJamidStemCandidate,
    EntityRank,
    EpistemicRank,
    G0C1CarrierSchemaError,
    LexicalTruthStatus,
    OntologicalClass,
    StemGender,
)
from taaqqul_slot_geometry.g0_c2_hard_blocker_gates import (
    G0_C2_ALLOWED_OUTPUT,
    G0_C2_FORBIDDEN_OUTPUTS,
    G0_C2_RANK_CEILING,
    G0C2GateSchemaError,
    G0HardBlocker,
    G0HardBlockerGateResult,
    G0HardBlockerGateState,
    G0HardBlockerResidual,
    G0HardBlockerResidualKind,
    prove_g0_hard_blocker_gates,
)
from taaqqul_slot_geometry.g0_c3_bounded_epistemic_distance import (
    G0_C3_ALLOWED_OUTPUT,
    G0_C3_FORBIDDEN_OUTPUTS,
    G0_C3_RANK_CEILING,
    G0BoundedDistanceResult,
    G0C3DistanceSchemaError,
    G0DistanceBand,
    G0DistanceResidual,
    G0DistanceResidualKind,
    compute_g0_bounded_epistemic_distance,
)
from taaqqul_slot_geometry.g0_c4_ontological_classifier import (
    G0_C4_ALLOWED_OUTPUT,
    G0_C4_FORBIDDEN_OUTPUTS,
    G0_C4_RANK_CEILING,
    G0C4ClassifierSchemaError,
    G0OntologicalClassifierResult,
    G0OntologicalClassifierState,
    G0OntologicalResidual,
    G0OntologicalResidualKind,
    classify_g0_ontological_origin,
)
from taaqqul_slot_geometry.g0_c5_epistemic_ranker import (
    G0_C5_ALLOWED_OUTPUT,
    G0_C5_FORBIDDEN_OUTPUTS,
    G0_C5_RANK_CEILING,
    G0C5RankerSchemaError,
    G0EpistemicRankerResult,
    G0EpistemicRankerState,
    G0EpistemicResidual,
    G0EpistemicResidualKind,
    rank_g0_epistemic_origin,
)
from taaqqul_slot_geometry.g0_c6_anchor_gate import (
    G0_C6_CONSUMPTION_OUTPUT,
    G0_C6_FORBIDDEN_OUTPUTS,
    G0_C6_ISSUANCE_OUTPUT,
    G0_C6_RANK_CEILING,
    G0AnchorGateState,
    G0AnchorIssuanceResult,
    G0AnchorResidual,
    G0AnchorResidualKind,
    G0C6AnchorSchemaError,
    G0DownstreamConsumptionGateResult,
    enforce_g0_anchor_consumption,
    issue_g0_anchor_certificate,
)
from taaqqul_slot_geometry.weight import (
    PATTERN_SPACE,
    LetterStanding,
    MawzunCandidate,
    Mizan,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
    PathKind,
    PreWeightSurface,
    RootStemCandidate,
    SlotAlignment,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightCarrierSchemaError,
    WeightImage,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
)

# Stable root contract: kernel-first surface for direct root imports.
# Compatibility re-exports remain available through ``__all__``.
_STABLE_ROOT_API: tuple[str, ...] = (
    "ClosureState",
    "FailureCode",
    "Rank",
    "Residual",
    "ResidualKind",
    "Center",
    "ConstructionResult",
    "EntryBoundary",
    "GenerationSource",
    "Layer",
    "OpeningPolicy",
    "OutputBoundary",
    "Slot",
    "SlotBoundary",
    "SlotGraph",
    "SlotGraphSchemaError",
    "SlotState",
    "TraceRef",
    "TraceEntryCandidate",
    "TraceLedger",
    "GammaResult",
    "gamma",
    "RankLattice",
    "ResidualEvaluation",
    "ResidualPolicy",
    "EvidenceContract",
    "EvidenceSource",
    "GATE_RANK_CEILING",
    "UNGATED_RANK_CEILING",
    "TransitionGate",
    "TransitionState",
    "TransitionVerdict",
    "CANONICAL_REGISTRY",
    "ForbiddenLine",
    "ForbiddenLineRegistry",
    "is_forbidden_direct",
)

__all__: list[str] = [
    # PR-1A carriers
    "ClosureState",
    "FailureCode",
    "Rank",
    "Residual",
    "ResidualKind",
    # PR-2 SlotGraph carriers
    "Center",
    "ConstructionResult",
    "EntryBoundary",
    "GenerationSource",
    "Layer",
    "OpeningPolicy",
    "OutputBoundary",
    "Slot",
    "SlotBoundary",
    "SlotGraph",
    "SlotGraphSchemaError",
    "SlotState",
    "TraceRef",
    # PR-2 trace ledger carriers
    "TraceEntryCandidate",
    "TraceLedger",
    # PR-2 verdict function
    "GammaResult",
    "gamma",
    # PR-3 rank lattice
    "RankLattice",
    # PR-3 residual policy engine
    "PERFORATING_KINDS",
    "ResidualEvaluation",
    "ResidualPolicy",
    # PR-3 evidence carriers
    "SINGLE_SOURCE_EVIDENCE_CEILING",
    "EvidenceContract",
    "EvidenceSource",
    # PR-4 transition gate
    "GATE_RANK_CEILING",
    "UNGATED_RANK_CEILING",
    "TransitionGate",
    "TransitionState",
    "TransitionVerdict",
    # PR-5 forbidden straight-line registry
    "CANONICAL_REGISTRY",
    "FORBIDDEN_STRAIGHT_LINES",
    "TERMINOLOGY_TRANSFERS",
    "ForbiddenLine",
    "ForbiddenLineRegistry",
    "TerminologyTransfer",
    "is_forbidden_direct",
    # PR-6 audit layer
    "AnswerAudit",
    "AuditedAnswer",
    "ModelClient",
    "emit_successor",
    # PR-22-AUDIT audit bridge
    "AuditBridgeState",
    "AuditedTanzilBridge",
    "AuditedTanzilBridgeVerdict",
    "bridge_tanzil_to_audit",
    # PR-8 adapter boundary
    "CONFIDENCE_SURFACE_NAMES",
    "LEDGER_SURFACE_NAMES",
    "RANK_SURFACE_NAMES",
    "SUCCESSOR_SURFACE_NAMES",
    "VERDICT_SURFACE_NAMES",
    "AdapterAdmission",
    "AdapterGuard",
    "ConcreteAdapterCandidate",
    "InMemoryModelClient",
    "TransportSurface",
    # PR-10 weight + pre-weight carriers
    "PATTERN_SPACE",
    "LetterStanding",
    "MawzunCandidate",
    "Mizan",
    "OperationTraceCandidate",
    "OriginalExtraMap",
    "PathCandidate",
    "PathKind",
    "PreWeightSurface",
    "RootStemCandidate",
    "SlotAlignment",
    "SyllableCandidate",
    "SyllableSequenceCandidate",
    "WeightCarrierSchemaError",
    "WeightImage",
    "WeightReadinessCandidate",
    "WordBoundaryCandidate",
    "WordCarrierCandidate",
    # G0-C1 bare-stem carrier surface
    "AnchorCertificate",
    "BareJamidStemCandidate",
    "EntityRank",
    "EpistemicRank",
    "G0C1CarrierSchemaError",
    "LexicalTruthStatus",
    "OntologicalClass",
    "StemGender",
    # G0-C2 hard-blocker gates
    "G0C2GateSchemaError",
    "G0HardBlocker",
    "G0HardBlockerGateResult",
    "G0HardBlockerGateState",
    "G0HardBlockerResidual",
    "G0HardBlockerResidualKind",
    "G0_C2_ALLOWED_OUTPUT",
    "G0_C2_FORBIDDEN_OUTPUTS",
    "G0_C2_RANK_CEILING",
    "prove_g0_hard_blocker_gates",
    # G0-C3 bounded epistemic distance
    "G0BoundedDistanceResult",
    "G0C3DistanceSchemaError",
    "G0DistanceBand",
    "G0DistanceResidual",
    "G0DistanceResidualKind",
    "G0_C3_ALLOWED_OUTPUT",
    "G0_C3_FORBIDDEN_OUTPUTS",
    "G0_C3_RANK_CEILING",
    "compute_g0_bounded_epistemic_distance",
    # G0-C4 ontological classifier
    "G0_C4_ALLOWED_OUTPUT",
    "G0_C4_FORBIDDEN_OUTPUTS",
    "G0_C4_RANK_CEILING",
    "G0C4ClassifierSchemaError",
    "G0OntologicalClassifierResult",
    "G0OntologicalClassifierState",
    "G0OntologicalResidual",
    "G0OntologicalResidualKind",
    "classify_g0_ontological_origin",
    # G0-C5 epistemic ranker
    "G0_C5_ALLOWED_OUTPUT",
    "G0_C5_FORBIDDEN_OUTPUTS",
    "G0_C5_RANK_CEILING",
    "G0C5RankerSchemaError",
    "G0EpistemicRankerResult",
    "G0EpistemicRankerState",
    "G0EpistemicResidual",
    "G0EpistemicResidualKind",
    "rank_g0_epistemic_origin",
    # G0-C6 anchor issuance + downstream consumption gate
    "G0_C6_CONSUMPTION_OUTPUT",
    "G0_C6_FORBIDDEN_OUTPUTS",
    "G0_C6_ISSUANCE_OUTPUT",
    "G0_C6_RANK_CEILING",
    "G0AnchorGateState",
    "G0AnchorIssuanceResult",
    "G0AnchorResidual",
    "G0AnchorResidualKind",
    "G0C6AnchorSchemaError",
    "G0DownstreamConsumptionGateResult",
    "enforce_g0_anchor_consumption",
    "issue_g0_anchor_certificate",
]
