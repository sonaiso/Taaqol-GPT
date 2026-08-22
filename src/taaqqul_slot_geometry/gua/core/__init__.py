"""GUA general-core public carrier surface."""

from taaqqul_slot_geometry.gua.core.alternatives import AlternativeSet
from taaqqul_slot_geometry.gua.core.bridge import BridgeCertificate
from taaqqul_slot_geometry.gua.core.conflict import ConflictSet
from taaqqul_slot_geometry.gua.core.delta import TransitionDelta
from taaqqul_slot_geometry.gua.core.domain import DomainSpec
from taaqqul_slot_geometry.gua.core.evidence import EvidenceContract
from taaqqul_slot_geometry.gua.core.failure import GuaCoreSchemaError, TypedFailure
from taaqqul_slot_geometry.gua.core.gate import Gate, GateDecision
from taaqqul_slot_geometry.gua.core.geometry import (
    CoreFreeze,
    GeneralCoreExtraction,
    LocalGeometry,
    compute_general_core_extraction_hash,
    freeze_general_core,
)
from taaqqul_slot_geometry.gua.core.identity import IdentityContract, TypedEntity
from taaqqul_slot_geometry.gua.core.prior_matrix import PriorDomainMatrix
from taaqqul_slot_geometry.gua.core.rank_space import RankLevel, RankSpace
from taaqqul_slot_geometry.gua.core.realization import RealizationContract
from taaqqul_slot_geometry.gua.core.refinement import RefinementRelation
from taaqqul_slot_geometry.gua.core.residual import Residual, ResidualKind, ResidualSet
from taaqqul_slot_geometry.gua.core.slot import TypedSlot
from taaqqul_slot_geometry.gua.core.trace import Trace
from taaqqul_slot_geometry.gua.core.transition import TransitionContract

__all__ = [
    "AlternativeSet",
    "BridgeCertificate",
    "compute_general_core_extraction_hash",
    "ConflictSet",
    "CoreFreeze",
    "DomainSpec",
    "EvidenceContract",
    "Gate",
    "GateDecision",
    "GeneralCoreExtraction",
    "GuaCoreSchemaError",
    "IdentityContract",
    "LocalGeometry",
    "PriorDomainMatrix",
    "RankLevel",
    "RankSpace",
    "RealizationContract",
    "RefinementRelation",
    "Residual",
    "ResidualKind",
    "ResidualSet",
    "Trace",
    "TransitionContract",
    "TransitionDelta",
    "TypedEntity",
    "TypedFailure",
    "TypedSlot",
    "freeze_general_core",
]
