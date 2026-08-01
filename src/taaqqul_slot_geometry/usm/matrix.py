"""USM matrix carrier (USM-C1 schema-only surface)."""

from __future__ import annotations

from dataclasses import dataclass

from taaqqul_slot_geometry.usm.application_contract import ApplicationContract
from taaqqul_slot_geometry.usm.bridge_contract import ScienceBridgeContract
from taaqqul_slot_geometry.usm.capability_contract import CapabilityContract
from taaqqul_slot_geometry.usm.claim_type_contract import ClaimTypeContract
from taaqqul_slot_geometry.usm.entity_contract import EntityTypeContract
from taaqqul_slot_geometry.usm.evidence_contract import ScienceEvidenceContract
from taaqqul_slot_geometry.usm.identifiers import (
    MatrixId,
    ScienceId,
    TraceRef,
    USMSchemaError,
    require_non_empty_text,
    require_tuple,
    require_tuple_of_type,
)
from taaqqul_slot_geometry.usm.judgment_contract import JudgmentContract
from taaqqul_slot_geometry.usm.knowledge_object_contract import KnowledgeObjectContract
from taaqqul_slot_geometry.usm.relation_contract import RelationContract
from taaqqul_slot_geometry.usm.residuals import USMResidual
from taaqqul_slot_geometry.usm.transformation_contract import TransformationContract


@dataclass(frozen=True, slots=True)
class UniversalScienceMatrix:
    matrix_id: MatrixId
    science_id: ScienceId
    version: str
    declared_scope: str
    entities: tuple[EntityTypeContract, ...]
    capabilities: tuple[CapabilityContract, ...]
    relations: tuple[RelationContract, ...]
    transformations: tuple[TransformationContract, ...]
    evidence: tuple[ScienceEvidenceContract, ...]
    claim_types: tuple[ClaimTypeContract, ...]
    judgments: tuple[JudgmentContract, ...]
    knowledge_objects: tuple[KnowledgeObjectContract, ...]
    applications: tuple[ApplicationContract, ...]
    bridges: tuple[ScienceBridgeContract, ...]
    residuals: tuple[USMResidual, ...]
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.matrix_id, MatrixId):
            raise USMSchemaError("UniversalScienceMatrix.matrix_id must be MatrixId")
        if not isinstance(self.science_id, ScienceId):
            raise USMSchemaError("UniversalScienceMatrix.science_id must be ScienceId")
        require_non_empty_text("UniversalScienceMatrix", "version", self.version)
        require_non_empty_text("UniversalScienceMatrix", "declared_scope", self.declared_scope)

        require_tuple_of_type(
            "UniversalScienceMatrix",
            "entities",
            self.entities,
            EntityTypeContract,
        )
        require_tuple_of_type(
            "UniversalScienceMatrix", "capabilities", self.capabilities, CapabilityContract
        )
        require_tuple_of_type(
            "UniversalScienceMatrix",
            "relations",
            self.relations,
            RelationContract,
        )
        require_tuple_of_type(
            "UniversalScienceMatrix",
            "transformations",
            self.transformations,
            TransformationContract,
        )
        require_tuple_of_type(
            "UniversalScienceMatrix", "evidence", self.evidence, ScienceEvidenceContract
        )
        require_tuple_of_type(
            "UniversalScienceMatrix", "claim_types", self.claim_types, ClaimTypeContract
        )
        require_tuple_of_type(
            "UniversalScienceMatrix", "judgments", self.judgments, JudgmentContract
        )
        require_tuple_of_type(
            "UniversalScienceMatrix",
            "knowledge_objects",
            self.knowledge_objects,
            KnowledgeObjectContract,
        )
        require_tuple_of_type(
            "UniversalScienceMatrix", "applications", self.applications, ApplicationContract
        )
        require_tuple_of_type(
            "UniversalScienceMatrix", "bridges", self.bridges, ScienceBridgeContract
        )
        require_tuple_of_type("UniversalScienceMatrix", "residuals", self.residuals, USMResidual)
        if not isinstance(self.trace_ref, TraceRef):
            raise USMSchemaError("UniversalScienceMatrix.trace_ref must be TraceRef")

        self._validate_unique_ids()
        self._validate_science_scope_alignment()
        self._validate_trace_policy()
        self._validate_slot_presence_surface()

    def _validate_unique_ids(self) -> None:
        self._assert_unique(
            "entities",
            tuple(contract.entity_type_id.value for contract in self.entities),
        )
        self._assert_unique(
            "capabilities",
            tuple(contract.capability_id.value for contract in self.capabilities),
        )
        self._assert_unique(
            "relations",
            tuple(contract.relation_type_id.value for contract in self.relations),
        )
        self._assert_unique(
            "transformations",
            tuple(contract.transformation_type_id.value for contract in self.transformations),
        )
        self._assert_unique(
            "evidence",
            tuple(contract.evidence_type_id.value for contract in self.evidence),
        )
        self._assert_unique(
            "claim_types",
            tuple(contract.claim_type_id.value for contract in self.claim_types),
        )
        self._assert_unique(
            "judgments",
            tuple(contract.judgment_type_id.value for contract in self.judgments),
        )
        self._assert_unique(
            "knowledge_objects",
            tuple(contract.knowledge_object_type_id.value for contract in self.knowledge_objects),
        )
        self._assert_unique(
            "applications",
            tuple(contract.application_type_id.value for contract in self.applications),
        )
        self._assert_unique(
            "bridges",
            tuple(contract.bridge_id.value for contract in self.bridges),
        )

    def _assert_unique(self, slot: str, ids: tuple[str, ...]) -> None:
        if len(ids) != len(set(ids)):
            raise USMSchemaError(f"UniversalScienceMatrix.{slot} has duplicate identifiers")

    def _validate_science_scope_alignment(self) -> None:
        local_contracts = (
            self.entities
            + self.capabilities
            + self.relations
            + self.transformations
            + self.evidence
            + self.claim_types
            + self.judgments
            + self.knowledge_objects
            + self.applications
        )
        for contract in local_contracts:
            if contract.science_id != self.science_id:
                raise USMSchemaError(
                    "UniversalScienceMatrix contains contract with mismatched science_id"
                )
        for bridge in self.bridges:
            if (
                bridge.source_science_id != self.science_id
                and bridge.target_science_id != self.science_id
            ):
                raise USMSchemaError(
                    "UniversalScienceMatrix bridge must include matrix science_id "
                    "as source or target"
                )

    def _validate_trace_policy(self) -> None:
        all_traces = (
            tuple(contract.trace_ref for contract in self.entities)
            + tuple(contract.trace_ref for contract in self.capabilities)
            + tuple(contract.trace_ref for contract in self.relations)
            + tuple(contract.trace_ref for contract in self.transformations)
            + tuple(contract.trace_ref for contract in self.evidence)
            + tuple(contract.trace_ref for contract in self.claim_types)
            + tuple(contract.trace_ref for contract in self.judgments)
            + tuple(contract.trace_ref for contract in self.knowledge_objects)
            + tuple(contract.trace_ref for contract in self.applications)
            + tuple(contract.trace_ref for contract in self.bridges)
        )
        for trace in all_traces:
            if not (
                trace.value == self.trace_ref.value
                or trace.value.startswith(f"{self.trace_ref.value}/")
            ):
                raise USMSchemaError(
                    "UniversalScienceMatrix contract trace_ref must equal or descend "
                    "from matrix trace_ref"
                )

    def _validate_slot_presence_surface(self) -> None:
        slots = (
            self.entities,
            self.capabilities,
            self.relations,
            self.transformations,
            self.evidence,
            self.judgments,
            self.knowledge_objects,
            self.applications,
        )
        for slot in slots:
            require_tuple("UniversalScienceMatrix", "slot", slot)
        if all(len(slot) == 0 for slot in slots) and len(self.residuals) == 0:
            raise USMSchemaError(
                "UniversalScienceMatrix cannot have all eight slots empty "
                "without explicit residuals"
            )


__all__ = ["UniversalScienceMatrix"]
