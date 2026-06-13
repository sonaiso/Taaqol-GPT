"""``taaqqul_slot_geometry.weight`` — the weight branch.

PR-10 carrier surface + PR-11 path gate + PR-12 μ chain operations
and Ω residual governance + PR-13 minimal WeightFit operation
+ PR-14 lexical / samāʿ / qiyās licensing boundary
+ PR-15 DalOnlyCandidate boundary
+ PR-16 VerbalMadlulCandidate boundary
+ PR-16B unified pre-semantic chain report
+ PR-16C pre-semantic registry contract
+ PR-16C.1 registry closure discipline
+ PR-17 Dal-Madlul binding candidate
+ PR-18 ContractableUnitGeometry boundary.

* the pre-weight chain carriers (docs/20 §§4–11) —
  :class:`SyllableCandidate`, :class:`SyllableSequenceCandidate`,
  :class:`WordBoundaryCandidate`, :class:`WordCarrierCandidate`,
  the :class:`PathKind` family with :class:`PathCandidate`,
  :class:`RootStemCandidate`, :class:`LetterStanding` with
  :class:`OriginalExtraMap`, :class:`OperationTraceCandidate`,
  :class:`PreWeightSurface`, :class:`WeightReadinessCandidate`;
* the weight-image carriers (docs/19 §9) — :class:`WeightImage`,
  :class:`Mizan`, :class:`MawzunCandidate`, :class:`SlotAlignment`;
* the pre-weight path gate (PR-11, docs/22) —
  :class:`PathGateProof`, :class:`PathGateState`,
  :class:`PathGateVerdict`, :class:`PreWeightPathGate`;
* the μ chain operations + Ω governance (PR-12, docs/23) —
  :func:`omega_governance`, :func:`mu_seq`, :func:`mu_boundary`,
  :func:`mu_word_carrier`, :func:`mu_root_stem`,
  :func:`mu_original_extra`, :func:`mu_ops`,
  :func:`mu_weight_readiness`;
* the minimal WeightFit operation (PR-13, docs/24) —
  :func:`weigh`, :class:`WeightFitCandidate`,
  :class:`WeightFitResult`, :class:`WeightFitState`;
* the licensing boundary assessment (PR-14, docs/25) —
  :func:`assess_license`, :class:`LicensingBoundaryVerdict`,
  :class:`LicensingBoundaryResult`, :class:`LicensingBoundaryState`,
  :class:`BoundaryEvidence`, :class:`LicenseBoundaryKind`;
* the DalOnlyCandidate boundary (PR-15, docs/26) —
  :func:`prove_dal`, :class:`DalOnlyCandidate`,
  :class:`DalBoundaryVerdict`, :class:`DalBoundaryState`;
* the VerbalMadlulCandidate boundary (PR-16, docs/27) —
  :func:`prove_verbal_madlul`, :class:`VerbalMadlulCandidate`,
  :class:`VerbalMadlulBoundaryVerdict`, :class:`MadlulBoundaryState`;
* the unified pre-semantic chain report (PR-16B, docs/28) —
  :func:`assemble_chain_report`, :class:`PreSemanticChainReport`,
  :class:`ChainReportResult`, :class:`ChainReportState`;
* the pre-semantic registry contract (PR-16C, docs/29) —
  :func:`lookup_registry_entry`, :class:`RegistryDomain`,
  :class:`RegistryEntry`, :class:`RegistryLookupResult`,
  :class:`RegistryLookupState`;
* the registry closure discipline (PR-16C.1, docs/30) —
  :class:`RegistryScope`, :class:`RegistryClosureKind`,
  :class:`RegistryClosureState`, :class:`RegistryClosureVerdict`;
* the Dal-Madlul binding candidate (PR-17, docs/31) —
  :func:`bind_dal_madlul`, :class:`DalMadlulBindingCandidate`,
  :class:`DalMadlulBindingVerdict`, :class:`BindingState`;
* the contractable unit geometry (PR-18, docs/32) —
  :func:`prove_contractable_unit`, :class:`ContractableUnitGeometry`,
  :class:`ContractableUnitVerdict`, :class:`ContractableUnitState`,
  :class:`ContractabilityProfile`;
* the relation candidate boundary (PR-19, docs/33) —
  :func:`prove_relation_candidate`, :class:`RelationCandidate`,
  :class:`RelationVerdict`, :class:`RelationState`.

No alignment operation, no lexicon, and no meaning / agency / hukm /
reality field lives here (docs/14; docs/19 §6; docs/20 §13).
The weight branch never touches the adapter or audit layers.
"""

from __future__ import annotations

from taaqqul_slot_geometry.weight.carrier_core import (
    BIRTH_RANK_CEILING,
    WeightCarrierBase,
    WeightCarrierSchemaError,
)
from taaqqul_slot_geometry.weight.chain_report import (
    CHAIN_REPORT_RANK_CEILING,
    ChainReportResult,
    ChainReportState,
    PreSemanticChainReport,
    assemble_chain_report,
)
from taaqqul_slot_geometry.weight.contractable_unit_geometry import (
    CONTRACTABLE_UNIT_RANK_CEILING,
    ContractabilityProfile,
    ContractableUnitGeometry,
    ContractableUnitState,
    ContractableUnitVerdict,
    prove_contractable_unit,
)
from taaqqul_slot_geometry.weight.dal_madlul_binding import (
    BINDING_RANK_CEILING,
    BindingState,
    DalMadlulBindingCandidate,
    DalMadlulBindingVerdict,
    bind_dal_madlul,
)
from taaqqul_slot_geometry.weight.dal_only import (
    DAL_BOUNDARY_RANK_CEILING,
    DalBoundaryState,
    DalBoundaryVerdict,
    DalOnlyCandidate,
    prove_dal,
)
from taaqqul_slot_geometry.weight.licensing_boundary import (
    LICENSE_BOUNDARY_RANK_CEILING,
    BoundaryEvidence,
    LicenseBoundaryKind,
    LicensingBoundaryResult,
    LicensingBoundaryState,
    LicensingBoundaryVerdict,
    assess_license,
)
from taaqqul_slot_geometry.weight.mu_chain import (
    MU_CHAIN_RANK_CEILING,
    MuStepResult,
    MuStepState,
    OmegaGovernanceState,
    ResidualGovernanceVerdict,
    mu_boundary,
    mu_ops,
    mu_original_extra,
    mu_root_stem,
    mu_seq,
    mu_weight_readiness,
    mu_word_carrier,
    omega_governance,
)
from taaqqul_slot_geometry.weight.path_gate import (
    PATH_GATE_RANK_CEILING,
    PathGateProof,
    PathGateState,
    PathGateVerdict,
    PreWeightPathGate,
)
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
    PathKind,
    PreWeightSurface,
    RootStemCandidate,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
)
from taaqqul_slot_geometry.weight.registry_closure import (
    REGISTRY_CLOSURE_RANK_CEILING,
    RegistryClosureKind,
    RegistryClosureState,
    RegistryClosureVerdict,
    RegistryScope,
)
from taaqqul_slot_geometry.weight.registry_contract import (
    REGISTRY_RANK_CEILING,
    RegistryDomain,
    RegistryEntry,
    RegistryLookupResult,
    RegistryLookupState,
    lookup_registry_entry,
)
from taaqqul_slot_geometry.weight.relation_candidate import (
    RELATION_CANDIDATE_RANK_CEILING,
    RelationCandidate,
    RelationState,
    RelationVerdict,
    prove_relation_candidate,
)
from taaqqul_slot_geometry.weight.verbal_madlul import (
    MADLUL_BOUNDARY_RANK_CEILING,
    MadlulBoundaryState,
    VerbalMadlulBoundaryVerdict,
    VerbalMadlulCandidate,
    prove_verbal_madlul,
)
from taaqqul_slot_geometry.weight.weight_fit import (
    WEIGHT_FIT_RANK_CEILING,
    WeightFitCandidate,
    WeightFitResult,
    WeightFitState,
    weigh,
)
from taaqqul_slot_geometry.weight.weight_image import (
    PATTERN_SPACE,
    MawzunCandidate,
    Mizan,
    SlotAlignment,
    WeightImage,
)

__all__ = [
    "BINDING_RANK_CEILING",
    "BIRTH_RANK_CEILING",
    "CHAIN_REPORT_RANK_CEILING",
    "CONTRACTABLE_UNIT_RANK_CEILING",
    "DAL_BOUNDARY_RANK_CEILING",
    "LICENSE_BOUNDARY_RANK_CEILING",
    "MADLUL_BOUNDARY_RANK_CEILING",
    "MU_CHAIN_RANK_CEILING",
    "PATH_GATE_RANK_CEILING",
    "PATTERN_SPACE",
    "REGISTRY_CLOSURE_RANK_CEILING",
    "REGISTRY_RANK_CEILING",
    "RELATION_CANDIDATE_RANK_CEILING",
    "WEIGHT_FIT_RANK_CEILING",
    "BindingState",
    "BoundaryEvidence",
    "ChainReportResult",
    "ChainReportState",
    "ContractabilityProfile",
    "ContractableUnitGeometry",
    "ContractableUnitState",
    "ContractableUnitVerdict",
    "DalBoundaryState",
    "DalBoundaryVerdict",
    "DalMadlulBindingCandidate",
    "DalMadlulBindingVerdict",
    "DalOnlyCandidate",
    "LetterStanding",
    "LicenseBoundaryKind",
    "LicensingBoundaryResult",
    "LicensingBoundaryState",
    "LicensingBoundaryVerdict",
    "MadlulBoundaryState",
    "MawzunCandidate",
    "Mizan",
    "MuStepResult",
    "MuStepState",
    "OmegaGovernanceState",
    "OperationTraceCandidate",
    "OriginalExtraMap",
    "PathCandidate",
    "PathGateProof",
    "PathGateState",
    "PathGateVerdict",
    "PathKind",
    "PreSemanticChainReport",
    "PreWeightPathGate",
    "PreWeightSurface",
    "RegistryClosureKind",
    "RegistryClosureState",
    "RegistryClosureVerdict",
    "RegistryDomain",
    "RegistryEntry",
    "RegistryLookupResult",
    "RegistryLookupState",
    "RegistryScope",
    "RelationCandidate",
    "RelationState",
    "RelationVerdict",
    "ResidualGovernanceVerdict",
    "RootStemCandidate",
    "SlotAlignment",
    "SyllableCandidate",
    "SyllableSequenceCandidate",
    "VerbalMadlulBoundaryVerdict",
    "VerbalMadlulCandidate",
    "WeightCarrierBase",
    "WeightCarrierSchemaError",
    "WeightFitCandidate",
    "WeightFitResult",
    "WeightFitState",
    "WeightImage",
    "WeightReadinessCandidate",
    "WordBoundaryCandidate",
    "WordCarrierCandidate",
    "assemble_chain_report",
    "assess_license",
    "bind_dal_madlul",
    "lookup_registry_entry",
    "mu_boundary",
    "mu_ops",
    "mu_original_extra",
    "mu_root_stem",
    "mu_seq",
    "mu_weight_readiness",
    "mu_word_carrier",
    "omega_governance",
    "prove_contractable_unit",
    "prove_dal",
    "prove_relation_candidate",
    "prove_verbal_madlul",
    "weigh",
]
