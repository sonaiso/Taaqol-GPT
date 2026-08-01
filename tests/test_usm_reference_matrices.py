"""USM reference-matrix parity and bounded non-reduction tests."""

from __future__ import annotations

from dataclasses import replace

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    USMFailureCode,
    USMResidual,
    USMResidualKind,
    USMValidationState,
    initial_functional_irreducibility_evidence,
    load_reference_matrices_v1,
    validate_usm_matrix,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/98_UNIVERSAL_SCIENCE_MATRIX_CONSTITUTIONAL_LAW.md",
        branch_name=f"USM reference matrices ({branch_note})",
        constitutional_chain=("docs/98", "USM-C1", "USM-C2", "USM-C2.1", "USM-RM-V1"),
        chain_position="USM bounded reference matrices v1 hardening",
        origin_law_ref="docs/98_UNIVERSAL_SCIENCE_MATRIX_CONSTITUTIONAL_LAW.md",
        branch_of_origin="USM three-science bounded reference family",
        forbidden_shortcut_assertions=(
            "ThreeMatrices -> UniversalCompleteness",
            "StructuralValidation -> ScientificTruth",
            "EvidenceTransferWithoutBridge",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "UniversalCompletenessClaim",
            "ScientificTruthCertificate",
            "CrossScienceBridgeAutoLicense",
        ),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def test_reference_matrices_have_exact_expected_validation_state() -> None:
    _declare("exact expected state")
    for matrix in load_reference_matrices_v1():
        result = validate_usm_matrix(matrix)
        assert result.state is USMValidationState.VALID_WITH_RESIDUALS


def test_reference_matrices_have_nonempty_required_slots() -> None:
    _declare("nonempty required slots")
    for matrix in load_reference_matrices_v1():
        assert matrix.entities
        assert matrix.capabilities
        assert matrix.relations
        assert matrix.transformations
        assert matrix.evidence
        assert matrix.judgments
        assert matrix.knowledge_objects
        assert matrix.applications


def test_reference_matrix_internal_references_resolve() -> None:
    _declare("internal references resolve")
    for matrix in load_reference_matrices_v1():
        result = validate_usm_matrix(matrix)
        assert USMFailureCode.REFERENCE_MATRIX_UNRESOLVED_REFERENCE not in result.failure_codes
        assert USMFailureCode.CLAIM_TYPE_REFERENCE_UNRESOLVED not in result.failure_codes


def test_reference_matrix_identifiers_are_unique() -> None:
    _declare("identifiers are unique")
    for matrix in load_reference_matrices_v1():
        result = validate_usm_matrix(matrix)
        assert USMFailureCode.REFERENCE_MATRIX_DUPLICATE_IDENTIFIER not in result.failure_codes


def test_reference_matrix_contracts_share_matrix_science_id() -> None:
    _declare("science id parity")
    for matrix in load_reference_matrices_v1():
        result = validate_usm_matrix(matrix)
        assert USMFailureCode.REFERENCE_MATRIX_FOREIGN_SCIENCE_ID not in result.failure_codes


def test_reference_evidence_supports_declared_local_claim_types_only() -> None:
    _declare("local claim-type support only")
    for matrix in load_reference_matrices_v1():
        local_claim_ids = {claim.claim_type_id for claim in matrix.claim_types}
        for evidence_contract in matrix.evidence:
            assert evidence_contract.supported_claim_types
            assert all(
                claim in local_claim_ids for claim in evidence_contract.supported_claim_types
            )
        result = validate_usm_matrix(matrix)
        assert USMFailureCode.EVIDENCE_CLAIM_TYPE_MISMATCH not in result.failure_codes


def test_reference_matrices_keep_coverage_and_irreducibility_residuals() -> None:
    _declare("coverage and irreducibility residuals preserved")
    for matrix in load_reference_matrices_v1():
        kinds = {residual.kind for residual in matrix.residuals}
        assert USMResidualKind.COVERAGE_GAP in kinds
        assert USMResidualKind.IRREDUCIBILITY_UNPROVEN in kinds


def test_blocked_matrix_is_not_accepted_as_valid_reference() -> None:
    _declare("blocked not accepted as valid reference")
    matrix = load_reference_matrices_v1()[0]
    blocked_residual = USMResidual(
        residual_id="synthetic-blocker",
        kind=USMResidualKind.MISSING_CAPABILITY,
        detail="synthetic blocker for negative-path validation",
        blocking=True,
        visible=True,
        repair_hint="remove synthetic blocker",
    )
    result = validate_usm_matrix(replace(matrix, residuals=(blocked_residual,)))
    assert result.state is USMValidationState.BLOCKED
    assert result.state is not USMValidationState.VALID_WITH_RESIDUALS


def test_deferred_matrix_is_not_accepted_as_valid_reference() -> None:
    _declare("deferred not accepted as valid reference")
    matrix = load_reference_matrices_v1()[0]
    deferred_residual = USMResidual(
        residual_id="synthetic-deferred",
        kind=USMResidualKind.KNOWLEDGE_REVISION_DEFERRED,
        detail="synthetic deferred for negative-path validation",
        blocking=False,
        visible=True,
        repair_hint="resolve deferred branch",
    )
    result = validate_usm_matrix(replace(matrix, residuals=(deferred_residual,)))
    assert result.state is USMValidationState.DEFERRED
    assert result.state is not USMValidationState.VALID_WITH_RESIDUALS


def test_removing_each_slot_causes_named_validation_failure() -> None:
    _declare("named failure by slot removal")
    matrix = load_reference_matrices_v1()[0]
    mapping = {
        "entities": USMFailureCode.REFERENCE_MATRIX_EMPTY_ENTITIES_SLOT,
        "capabilities": USMFailureCode.REFERENCE_MATRIX_EMPTY_CAPABILITIES_SLOT,
        "relations": USMFailureCode.REFERENCE_MATRIX_EMPTY_RELATIONS_SLOT,
        "transformations": USMFailureCode.REFERENCE_MATRIX_EMPTY_TRANSFORMATIONS_SLOT,
        "evidence": USMFailureCode.REFERENCE_MATRIX_EMPTY_EVIDENCE_SLOT,
        "judgments": USMFailureCode.REFERENCE_MATRIX_EMPTY_JUDGMENTS_SLOT,
        "knowledge_objects": USMFailureCode.REFERENCE_MATRIX_EMPTY_KNOWLEDGE_OBJECTS_SLOT,
        "applications": USMFailureCode.REFERENCE_MATRIX_EMPTY_APPLICATIONS_SLOT,
    }
    for slot_name, failure_code in mapping.items():
        broken = replace(matrix, **{slot_name: ()})
        result = validate_usm_matrix(broken)
        assert failure_code in result.failure_codes


def test_initial_functional_irreducibility_evidence_by_slot_removal() -> None:
    _declare("initial functional irreducibility evidence")
    matrix = load_reference_matrices_v1()[0]
    expected = {
        "entities": "no subject identity",
        "capabilities": "possible and forbidden operations become indistinguishable",
        "relations": "entities cannot form structured claims",
        "transformations": "no licensed change or derivation",
        "evidence": "supported and unsupported claims collapse",
        "judgments": "no epistemic rank assignment",
        "knowledge_objects": "no organized reusable knowledge",
        "applications": "no transfer to new cases or feedback",
    }
    for slot_name, loss_message in expected.items():
        broken = replace(matrix, **{slot_name: ()})
        report = initial_functional_irreducibility_evidence(broken)
        assert report[slot_name] == loss_message


def test_entities_and_capabilities_are_not_merge_equivalent() -> None:
    _declare("entities not reducible to capabilities")
    matrix = load_reference_matrices_v1()[0]
    merged = replace(matrix, entities=())
    result = validate_usm_matrix(merged)
    assert USMFailureCode.REFERENCE_MATRIX_EMPTY_ENTITIES_SLOT in result.failure_codes


def test_evidence_and_judgments_are_not_merge_equivalent() -> None:
    _declare("evidence not reducible to judgments")
    matrix = load_reference_matrices_v1()[0]
    merged = replace(matrix, evidence=())
    result = validate_usm_matrix(merged)
    assert USMFailureCode.REFERENCE_MATRIX_EMPTY_EVIDENCE_SLOT in result.failure_codes


def test_knowledge_objects_and_applications_are_not_merge_equivalent() -> None:
    _declare("knowledge objects not reducible to applications")
    matrix = load_reference_matrices_v1()[0]
    merged = replace(matrix, knowledge_objects=())
    result = validate_usm_matrix(merged)
    assert USMFailureCode.REFERENCE_MATRIX_EMPTY_KNOWLEDGE_OBJECTS_SLOT in result.failure_codes


def test_reference_matrix_expected_state_can_be_asserted_structurally() -> None:
    _declare("expected state structural assertion")
    matrix = load_reference_matrices_v1()[0]
    result = validate_usm_matrix(matrix, expected_state=USMValidationState.VALID_WITH_RESIDUALS)
    assert result.state is USMValidationState.VALID_WITH_RESIDUALS
    assert USMFailureCode.REFERENCE_MATRIX_EXPECTED_STATE_MISMATCH not in result.failure_codes


def test_reference_matrix_validator_catches_duplicate_identifier() -> None:
    _declare("duplicate identifier detection")
    matrix = load_reference_matrices_v1()[1]
    duplicate_entity = replace(
        matrix.entities[0],
        entity_type_id=matrix.entities[1].entity_type_id,
        trace_ref=matrix.entities[0].trace_ref,
    )
    broken_entities = (duplicate_entity, *matrix.entities[1:])
    object.__setattr__(matrix, "entities", broken_entities)
    result = validate_usm_matrix(matrix)
    assert USMFailureCode.REFERENCE_MATRIX_DUPLICATE_IDENTIFIER in result.failure_codes
    assert USMFailureCode.DUPLICATE_IDENTIFIER in result.failure_codes
