"""USM bounded schema + validation surfaces (USM-L0, USM-C1, USM-C2)."""

from taaqqul_slot_geometry.usm.application_contract import ApplicationContract
from taaqqul_slot_geometry.usm.bridge_contract import (
    BridgeDirection,
    BridgeKind,
    ScienceBridgeContract,
    TypedUSMReference,
    USMReferenceSlot,
)
from taaqqul_slot_geometry.usm.capability_contract import CapabilityContract
from taaqqul_slot_geometry.usm.capability_evaluator import (
    CapabilityEvaluationEnvironment,
    CapabilityEvaluationRequest,
    CapabilityEvaluationResult,
    CapabilityEvaluationState,
    CapabilityEvaluationTrace,
    EntityInstanceContract,
    EvaluationContextContract,
    evaluate_capability,
)
from taaqqul_slot_geometry.usm.claim_type_contract import ClaimTypeContract
from taaqqul_slot_geometry.usm.entity_contract import EntityTypeContract
from taaqqul_slot_geometry.usm.enums import RelationDirection
from taaqqul_slot_geometry.usm.evidence_contract import ScienceEvidenceContract
from taaqqul_slot_geometry.usm.identifiers import (
    ApplicationTypeId,
    BridgeId,
    CapabilityEvaluationRef,
    CapabilityId,
    ClaimTypeId,
    ContextId,
    CriterionId,
    DomainId,
    EntityInstanceRef,
    EntityTypeId,
    EvidenceTypeId,
    JudgmentTypeId,
    KnowledgeObjectTypeId,
    MatrixId,
    RelationTypeId,
    RequestId,
    RoleId,
    RuleId,
    ScienceId,
    TraceRef,
    TransformationTypeId,
    USMSchemaError,
)
from taaqqul_slot_geometry.usm.judgment_contract import JudgmentContract
from taaqqul_slot_geometry.usm.knowledge_object_contract import KnowledgeObjectContract
from taaqqul_slot_geometry.usm.matrix import UniversalScienceMatrix
from taaqqul_slot_geometry.usm.reference_matrices import (
    load_reference_matrices_v1,
    make_arabic_reference_matrix_v1,
    make_elementary_mathematics_reference_matrix_v1,
    make_elementary_mechanics_reference_matrix_v1,
)
from taaqqul_slot_geometry.usm.relation_contract import RelationContract
from taaqqul_slot_geometry.usm.relation_evaluator import (
    RelationEvaluationEnvironment,
    RelationEvaluationRequest,
    RelationEvaluationResult,
    RelationEvaluationState,
    RelationEvaluationTrace,
    RelationOperandBinding,
    evaluate_relation,
)
from taaqqul_slot_geometry.usm.residuals import USMResidual, USMResidualKind
from taaqqul_slot_geometry.usm.transformation_contract import TransformationContract
from taaqqul_slot_geometry.usm.validator import (
    USMFailureCode,
    USMValidationResult,
    USMValidationState,
    initial_functional_irreducibility_evidence,
    validate_usm_matrix,
)

__all__ = [
    "ApplicationContract",
    "ApplicationTypeId",
    "BridgeDirection",
    "BridgeId",
    "BridgeKind",
    "CapabilityEvaluationRef",
    "CapabilityContract",
    "CapabilityEvaluationEnvironment",
    "CapabilityEvaluationRequest",
    "CapabilityEvaluationResult",
    "CapabilityEvaluationState",
    "CapabilityEvaluationTrace",
    "CapabilityId",
    "ClaimTypeContract",
    "ClaimTypeId",
    "ContextId",
    "CriterionId",
    "DomainId",
    "EntityInstanceRef",
    "EntityInstanceContract",
    "EntityTypeContract",
    "EntityTypeId",
    "EvaluationContextContract",
    "EvidenceTypeId",
    "JudgmentContract",
    "JudgmentTypeId",
    "KnowledgeObjectContract",
    "KnowledgeObjectTypeId",
    "MatrixId",
    "RelationContract",
    "RelationEvaluationEnvironment",
    "RelationEvaluationRequest",
    "RelationEvaluationResult",
    "RelationEvaluationState",
    "RelationEvaluationTrace",
    "RelationOperandBinding",
    "RelationDirection",
    "RelationTypeId",
    "RequestId",
    "RoleId",
    "RuleId",
    "ScienceEvidenceContract",
    "ScienceBridgeContract",
    "ScienceId",
    "TraceRef",
    "TransformationContract",
    "TransformationTypeId",
    "USMFailureCode",
    "USMReferenceSlot",
    "USMResidual",
    "USMResidualKind",
    "USMSchemaError",
    "USMValidationResult",
    "USMValidationState",
    "UniversalScienceMatrix",
    "initial_functional_irreducibility_evidence",
    "load_reference_matrices_v1",
    "make_arabic_reference_matrix_v1",
    "make_elementary_mathematics_reference_matrix_v1",
    "make_elementary_mechanics_reference_matrix_v1",
    "validate_usm_matrix",
    "evaluate_capability",
    "evaluate_relation",
    "TypedUSMReference",
]
