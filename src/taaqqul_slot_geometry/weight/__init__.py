"""``taaqqul_slot_geometry.weight`` — the weight branch.

PR-10 carrier surface + PR-11 path gate + PR-12 μ chain operations
and Ω residual governance + PR-13 minimal WeightFit operation
+ PR-14 lexical / samāʿ / qiyās licensing boundary
+ PR-15 DalOnlyCandidate boundary
+ PR-16 VerbalMadlulCandidate boundary.

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
  :class:`VerbalMadlulBoundaryVerdict`, :class:`MadlulBoundaryState`.

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
    "BIRTH_RANK_CEILING",
    "DAL_BOUNDARY_RANK_CEILING",
    "LICENSE_BOUNDARY_RANK_CEILING",
    "MADLUL_BOUNDARY_RANK_CEILING",
    "MU_CHAIN_RANK_CEILING",
    "PATH_GATE_RANK_CEILING",
    "PATTERN_SPACE",
    "WEIGHT_FIT_RANK_CEILING",
    "BoundaryEvidence",
    "DalBoundaryState",
    "DalBoundaryVerdict",
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
    "PreWeightPathGate",
    "PreWeightSurface",
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
    "assess_license",
    "mu_boundary",
    "mu_ops",
    "mu_original_extra",
    "mu_root_stem",
    "mu_seq",
    "mu_weight_readiness",
    "mu_word_carrier",
    "omega_governance",
    "prove_dal",
    "prove_verbal_madlul",
    "weigh",
]
