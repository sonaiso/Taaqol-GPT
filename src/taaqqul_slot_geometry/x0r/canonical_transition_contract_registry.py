"""PR-C canonical transition contract registry (carrier-only contract source of truth)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.x0r.canonical_domain_registry import (
    DomainId,
    EvidenceKind,
    ResidualKind,
    TransitionKind,
)


class CanonicalTransitionContractRegistrySchemaError(TypeError):
    """Raised when the canonical transition contract registry surface is malformed."""


class TransitionContractId(StrEnum):
    """Canonical transition-contract identifiers."""

    TC_01 = "TC-01"
    TC_02 = "TC-02"
    TC_03 = "TC-03"
    TC_04 = "TC-04"
    TC_05 = "TC-05"
    TC_06 = "TC-06"
    TC_SR = "TC_SR"
    TC_RI = "TC_RI"
    TC_IL = "TC_IL"
    TC_LW = "TC_LW"
    TC_WS = "TC_WS"
    TC_SD = "TC_SD"


@dataclass(frozen=True, slots=True)
class CanonicalTransitionContract:
    """Immutable contract declaration row in the canonical registry."""

    contract_id: TransitionContractId
    domain: DomainId
    transition_kind: TransitionKind
    source_slot: str
    target_slot: str
    required_conditions: tuple[str, ...]
    required_fields: tuple[str, ...]
    outputs: tuple[str, ...]
    evidence_kinds: tuple[EvidenceKind, ...]
    residual_kinds: tuple[ResidualKind, ...]
    allows_multi_candidate: bool
    law_ref: str
    trace_ref: str

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        if not isinstance(self.contract_id, TransitionContractId):
            raise CanonicalTransitionContractRegistrySchemaError(
                f"{cls}.contract_id must be TransitionContractId"
            )
        if not isinstance(self.domain, DomainId):
            raise CanonicalTransitionContractRegistrySchemaError(f"{cls}.domain must be DomainId")
        if not isinstance(self.transition_kind, TransitionKind):
            raise CanonicalTransitionContractRegistrySchemaError(
                f"{cls}.transition_kind must be TransitionKind"
            )
        _require_str(cls, "source_slot", self.source_slot)
        _require_str(cls, "target_slot", self.target_slot)
        _validate_unique_non_empty_str_tuple(cls, "required_conditions", self.required_conditions)
        _validate_unique_non_empty_str_tuple(cls, "required_fields", self.required_fields)
        _validate_unique_non_empty_str_tuple(cls, "outputs", self.outputs)
        _validate_enum_tuple(cls, "evidence_kinds", self.evidence_kinds, EvidenceKind)
        _validate_enum_tuple(cls, "residual_kinds", self.residual_kinds, ResidualKind)
        if not isinstance(self.allows_multi_candidate, bool):
            raise CanonicalTransitionContractRegistrySchemaError(
                f"{cls}.allows_multi_candidate must be bool"
            )
        _require_str(cls, "law_ref", self.law_ref)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)


@dataclass(frozen=True, slots=True)
class CanonicalTransitionContractRegistry:
    """Immutable canonical registry for transition-contract declarations."""

    version: str
    trace_ref: str
    contracts: tuple[CanonicalTransitionContract, ...]

    def __post_init__(self) -> None:
        cls = self.__class__.__name__
        _require_str(cls, "version", self.version)
        _require_trace_ref(cls, "trace_ref", self.trace_ref)
        if not isinstance(self.contracts, tuple) or not self.contracts:
            raise CanonicalTransitionContractRegistrySchemaError(
                f"{cls}.contracts must be a non-empty tuple"
            )
        for contract in self.contracts:
            if not isinstance(contract, CanonicalTransitionContract):
                raise CanonicalTransitionContractRegistrySchemaError(
                    f"{cls}.contracts entries must be CanonicalTransitionContract"
                )
        ids = tuple(contract.contract_id for contract in self.contracts)
        if len(set(ids)) != len(ids):
            raise CanonicalTransitionContractRegistrySchemaError(
                f"{cls}.contracts must have unique contract_id values"
            )

    def includes_contract(self, contract_id: TransitionContractId) -> bool:
        return any(contract.contract_id is contract_id for contract in self.contracts)

    def contract_by_id(self, contract_id: TransitionContractId) -> CanonicalTransitionContract:
        for contract in self.contracts:
            if contract.contract_id is contract_id:
                return contract
        raise KeyError(contract_id.value)

    def lexicon_contracts(self) -> tuple[CanonicalTransitionContract, ...]:
        lexicon_ids = (
            TransitionContractId.TC_SR,
            TransitionContractId.TC_RI,
            TransitionContractId.TC_IL,
            TransitionContractId.TC_LW,
            TransitionContractId.TC_WS,
            TransitionContractId.TC_SD,
        )
        return tuple(self.contract_by_id(contract_id) for contract_id in lexicon_ids)


def canonical_transition_contract_registry() -> CanonicalTransitionContractRegistry:
    """Return the immutable canonical transition-contract registry singleton."""

    return _CANONICAL_TRANSITION_CONTRACT_REGISTRY_V1


def _validate_enum_tuple(
    cls_name: str, field_name: str, value: object, expected_type: type[StrEnum]
) -> None:
    if not isinstance(value, tuple) or not value:
        raise CanonicalTransitionContractRegistrySchemaError(
            f"{cls_name}.{field_name} must be a non-empty tuple"
        )
    for entry in value:
        if not isinstance(entry, expected_type):
            raise CanonicalTransitionContractRegistrySchemaError(
                f"{cls_name}.{field_name} entries must be {expected_type.__name__}"
            )
    if len(set(value)) != len(value):
        raise CanonicalTransitionContractRegistrySchemaError(
            f"{cls_name}.{field_name} entries must be unique"
        )


def _validate_unique_non_empty_str_tuple(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, tuple) or not value:
        raise CanonicalTransitionContractRegistrySchemaError(
            f"{cls_name}.{field_name} must be a non-empty tuple"
        )
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise CanonicalTransitionContractRegistrySchemaError(
                f"{cls_name}.{field_name} entries must be non-empty strings"
            )
    if len(set(value)) != len(value):
        raise CanonicalTransitionContractRegistrySchemaError(
            f"{cls_name}.{field_name} entries must be unique"
        )


def _require_str(cls_name: str, field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CanonicalTransitionContractRegistrySchemaError(
            f"{cls_name}.{field_name} must be a non-empty string"
        )


def _require_trace_ref(cls_name: str, field_name: str, value: object) -> None:
    _require_str(cls_name, field_name, value)
    assert isinstance(value, str)
    if not value.startswith("trace://"):
        raise CanonicalTransitionContractRegistrySchemaError(
            f"{cls_name}.{field_name} must start with 'trace://'"
        )


_CANONICAL_TRANSITION_CONTRACT_REGISTRY_V1 = CanonicalTransitionContractRegistry(
    version="canonical-transition-contract-registry-v1",
    trace_ref="trace://x0r/pr-c/canonical-transition-contract-registry/v1",
    contracts=(
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_01,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.LINKING,
            source_slot="SourceCarrier",
            target_slot="IdentityCarrier",
            required_conditions=(
                "preserved_source",
                "identity_stability",
                "trace_recorded",
                "no_blocking_residual",
            ),
            required_fields=("source_ref", "identity_ref", "trace_ref"),
            outputs=("IdentityCarrier",),
            evidence_kinds=(EvidenceKind.SOURCE_TEXT, EvidenceKind.STRUCTURAL_VALIDATION),
            residual_kinds=(
                ResidualKind.BLOCKING,
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
            ),
            allows_multi_candidate=True,
            law_ref="docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md#71-transition-contract-registry-tc-01tc-06",
            trace_ref="trace://lexicon-l1/tc-01",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_02,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.LINKING,
            source_slot="IdentityCarrier",
            target_slot="LexicalConstitutionCarrier",
            required_conditions=(
                "identity_verified",
                "attested_lexical_placement",
                "unresolved_lexical_conflict_absent",
            ),
            required_fields=("identity_ref", "placement_evidence", "trace_ref"),
            outputs=("LexicalMeaning",),
            evidence_kinds=(EvidenceKind.STRUCTURAL_VALIDATION, EvidenceKind.RULE_PROOF),
            residual_kinds=(
                ResidualKind.BLOCKING,
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
            ),
            allows_multi_candidate=True,
            law_ref="docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md#71-transition-contract-registry-tc-01tc-06",
            trace_ref="trace://lexicon-l1/tc-02",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_03,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.LINKING,
            source_slot="LexicalConstitutionCarrier",
            target_slot="OntologicalConstitutionCarrier",
            required_conditions=(
                "genus_declared",
                "species_declared_if_available",
                "essential_properties_extracted",
                "capabilities_extracted",
                "potential_blockers_recorded",
            ),
            required_fields=("lexical_identity", "ontological_profile", "trace_ref"),
            outputs=("OntologicalProfile",),
            evidence_kinds=(EvidenceKind.RULE_PROOF, EvidenceKind.STRUCTURAL_VALIDATION),
            residual_kinds=(
                ResidualKind.BLOCKING,
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
            ),
            allows_multi_candidate=True,
            law_ref="docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md#71-transition-contract-registry-tc-01tc-06",
            trace_ref="trace://lexicon-l1/tc-03",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_04,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.LINKING,
            source_slot="OntologicalConstitutionCarrier",
            target_slot="SemanticConstitutionCarrier",
            required_conditions=(
                "genus_proven",
                "essential_properties_proven",
                "capability_conditions_satisfied",
                "blocking_residual_absent_for_transition",
            ),
            required_fields=("ontological_ref", "semantic_frame", "trace_ref"),
            outputs=("CorrespondenceCandidate", "ContainmentCandidate", "CommitmentCandidate"),
            evidence_kinds=(EvidenceKind.RULE_PROOF, EvidenceKind.CROSS_SOURCE_CORROBORATION),
            residual_kinds=(
                ResidualKind.BLOCKING,
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
            ),
            allows_multi_candidate=True,
            law_ref="docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md#71-transition-contract-registry-tc-01tc-06",
            trace_ref="trace://lexicon-l1/tc-04",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_05,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.LINKING,
            source_slot="SemanticConstitutionCarrier",
            target_slot="IfadahConstitutionCarrier",
            required_conditions=(
                "compositional_relations_complete",
                "isnad_verified",
                "relation_graph_closed",
                "non_blocking_residuals_visible",
            ),
            required_fields=("semantic_graph", "ifadah_context", "trace_ref"),
            outputs=("IfadahCandidate",),
            evidence_kinds=(
                EvidenceKind.STRUCTURAL_VALIDATION,
                EvidenceKind.CROSS_SOURCE_CORROBORATION,
            ),
            residual_kinds=(
                ResidualKind.BLOCKING,
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
            ),
            allows_multi_candidate=True,
            law_ref="docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md#71-transition-contract-registry-tc-01tc-06",
            trace_ref="trace://lexicon-l1/tc-05",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_06,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.LINKING,
            source_slot="IfadahConstitutionCarrier",
            target_slot="JudgmentConstitutionCarrier",
            required_conditions=(
                "sufficient_evidence",
                "no_blocking_residual",
                "review_passed",
                "judgment_scope_declared",
            ),
            required_fields=("ifadah_ref", "judgment_scope", "trace_ref"),
            outputs=("JudgmentCandidate",),
            evidence_kinds=(EvidenceKind.RULE_PROOF, EvidenceKind.CROSS_SOURCE_CORROBORATION),
            residual_kinds=(
                ResidualKind.BLOCKING,
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
            ),
            allows_multi_candidate=False,
            law_ref="docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md#71-transition-contract-registry-tc-01tc-06",
            trace_ref="trace://lexicon-l1/tc-06",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_SR,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.CARRIER_DECLARATION,
            source_slot="SourceSlot",
            target_slot="ReadingCandidate",
            required_conditions=(
                "source_available",
                "span_declared",
                "trace_recorded",
            ),
            required_fields=("source_ref", "span_ref", "raw_text", "reading_evidence", "trace_ref"),
            outputs=("ReadingCandidate",),
            evidence_kinds=(EvidenceKind.SOURCE_TEXT, EvidenceKind.STRUCTURAL_VALIDATION),
            residual_kinds=(
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
                ResidualKind.REPAIRABLE,
            ),
            allows_multi_candidate=True,
            law_ref="docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md#5-contract-only-transition-surface",
            trace_ref="trace://lexicon-slot-l0/tc-sr",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_RI,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.CARRIER_DECLARATION,
            source_slot="ReadingCandidate",
            target_slot="IdentityCarrier",
            required_conditions=(
                "reading_candidate_present",
                "identity_axes_preserved",
                "trace_recorded",
            ),
            required_fields=(
                "graphic_identity",
                "phonological_identity",
                "token_boundary",
                "trace_ref",
            ),
            outputs=("IdentityCarrier",),
            evidence_kinds=(EvidenceKind.STRUCTURAL_VALIDATION, EvidenceKind.RULE_PROOF),
            residual_kinds=(
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
                ResidualKind.REPAIRABLE,
            ),
            allows_multi_candidate=True,
            law_ref="docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md#5-contract-only-transition-surface",
            trace_ref="trace://lexicon-slot-l0/tc-ri",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_IL,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.CARRIER_DECLARATION,
            source_slot="IdentityCarrier",
            target_slot="LexicalEntitySlot",
            required_conditions=(
                "identity_verified",
                "entity_classification_present",
                "trace_recorded",
            ),
            required_fields=(
                "lexeme_identity",
                "entity_type",
                "classification_evidence",
                "trace_ref",
            ),
            outputs=("LexicalEntitySlot",),
            evidence_kinds=(EvidenceKind.STRUCTURAL_VALIDATION, EvidenceKind.RULE_PROOF),
            residual_kinds=(
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
                ResidualKind.REPAIRABLE,
            ),
            allows_multi_candidate=True,
            law_ref="docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md#5-contract-only-transition-surface",
            trace_ref="trace://lexicon-slot-l0/tc-il",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_LW,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.CARRIER_DECLARATION,
            source_slot="LexicalEntitySlot",
            target_slot="WadCandidate",
            required_conditions=(
                "wad_kind_declared",
                "authority_recorded",
                "trace_recorded",
            ),
            required_fields=("wad_kind", "authority_ref", "usage_scope", "trace_ref"),
            outputs=("WadCandidate",),
            evidence_kinds=(EvidenceKind.RULE_PROOF, EvidenceKind.CROSS_SOURCE_CORROBORATION),
            residual_kinds=(
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
                ResidualKind.REPAIRABLE,
            ),
            allows_multi_candidate=True,
            law_ref="docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md#5-contract-only-transition-surface",
            trace_ref="trace://lexicon-slot-l0/tc-lw",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_WS,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.CARRIER_DECLARATION,
            source_slot="WadCandidate",
            target_slot="LexicalSenseSlot",
            required_conditions=(
                "sense_identity_declared",
                "sense_boundary_declared",
                "trace_recorded",
            ),
            required_fields=("sense_identity", "sense_boundary", "usage_evidence", "trace_ref"),
            outputs=("LexicalSenseSlot",),
            evidence_kinds=(
                EvidenceKind.CROSS_SOURCE_CORROBORATION,
                EvidenceKind.STRUCTURAL_VALIDATION,
            ),
            residual_kinds=(
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
                ResidualKind.REPAIRABLE,
            ),
            allows_multi_candidate=True,
            law_ref="docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md#5-contract-only-transition-surface",
            trace_ref="trace://lexicon-slot-l0/tc-ws",
        ),
        CanonicalTransitionContract(
            contract_id=TransitionContractId.TC_SD,
            domain=DomainId.LEXICON,
            transition_kind=TransitionKind.CARRIER_DECLARATION,
            source_slot="LexicalSenseSlot",
            target_slot="DalalahCandidateSlot",
            required_conditions=(
                "dalalah_candidate_declared",
                "rank_vector_present",
                "trace_recorded",
            ),
            required_fields=("candidate_kind", "candidate_label", "rank_vector", "trace_ref"),
            outputs=("DalalahCandidateSlot",),
            evidence_kinds=(EvidenceKind.STRUCTURAL_VALIDATION, EvidenceKind.RULE_PROOF),
            residual_kinds=(
                ResidualKind.DEFERRED,
                ResidualKind.NON_BLOCKING,
                ResidualKind.REPAIRABLE,
            ),
            allows_multi_candidate=True,
            law_ref="docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md#5-contract-only-transition-surface",
            trace_ref="trace://lexicon-slot-l0/tc-sd",
        ),
    ),
)


__all__ = [
    "CanonicalTransitionContract",
    "CanonicalTransitionContractRegistry",
    "CanonicalTransitionContractRegistrySchemaError",
    "TransitionContractId",
    "canonical_transition_contract_registry",
]
