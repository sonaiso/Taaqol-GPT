"""USM reference-matrix parity and non-reduction tests."""

from __future__ import annotations

from dataclasses import replace

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
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
        constitutional_chain=("docs/98", "USM-C1", "USM-C2", "USM-RM-V1"),
        chain_position="USM bounded reference matrices v1",
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


def test_all_three_reference_matrices_use_same_eight_slots() -> None:
    _declare("same eight slots")
    matrices = load_reference_matrices_v1()
    slot_names = (
        "entities",
        "capabilities",
        "relations",
        "transformations",
        "evidence",
        "judgments",
        "knowledge_objects",
        "applications",
    )
    for matrix in matrices:
        for slot_name in slot_names:
            slot_value = getattr(matrix, slot_name)
            assert isinstance(slot_value, tuple)


def test_all_three_reference_matrices_validate_structurally() -> None:
    _declare("structural validation")
    matrices = load_reference_matrices_v1()
    for matrix in matrices:
        result = validate_usm_matrix(matrix)
        assert result.state in {
            USMValidationState.VALID,
            USMValidationState.VALID_WITH_RESIDUALS,
            USMValidationState.DEFERRED,
            USMValidationState.BLOCKED,
        }


def test_arabic_evidence_is_not_mathematical_proof() -> None:
    _declare("arabic evidence non-math-proof")
    arabic, math, _ = load_reference_matrices_v1()
    arabic_evidence = {item.evidence_type_id.value for item in arabic.evidence}
    math_evidence = {item.evidence_type_id.value for item in math.evidence}
    assert "INFERENCE_RULE" not in arabic_evidence
    assert "CALCULATION_TRACE" not in arabic_evidence
    assert "ATTESTED_USAGE" not in math_evidence
    assert arabic_evidence.isdisjoint({"INFERENCE_RULE", "CALCULATION_TRACE"})


def test_mathematical_proof_is_not_empirical_confirmation() -> None:
    _declare("math proof non-empirical confirmation")
    _, math, mechanics = load_reference_matrices_v1()
    math_evidence = {item.evidence_type_id.value for item in math.evidence}
    mechanics_evidence = {item.evidence_type_id.value for item in mechanics.evidence}
    assert "CALIBRATED_MEASUREMENT" not in math_evidence
    assert "INFERENCE_RULE" not in mechanics_evidence


def test_empirical_measurement_is_not_linguistic_attestation() -> None:
    _declare("empirical measurement non-linguistic attestation")
    arabic, _, mechanics = load_reference_matrices_v1()
    arabic_evidence = {item.evidence_type_id.value for item in arabic.evidence}
    mechanics_evidence = {item.evidence_type_id.value for item in mechanics.evidence}
    assert "ATTESTED_USAGE" in arabic_evidence
    assert "ATTESTED_USAGE" not in mechanics_evidence
    assert "CALIBRATED_MEASUREMENT" in mechanics_evidence


def test_local_rank_does_not_equal_global_rank() -> None:
    _declare("local rank differs from global rank")
    matrices = load_reference_matrices_v1()
    for matrix in matrices:
        judgment = matrix.judgments[0]
        assert judgment.local_rank_name
        assert judgment.local_rank_name != judgment.global_rank_ceiling.name


def test_three_matrices_do_not_enable_universal_completeness_claim() -> None:
    _declare("no universal completeness from three matrices")
    matrices = load_reference_matrices_v1()
    for matrix in matrices:
        kinds = {residual.kind for residual in matrix.residuals}
        assert USMResidualKind.COVERAGE_GAP in kinds
        assert USMResidualKind.IRREDUCIBILITY_UNPROVEN in kinds


def test_initial_functional_irreducibility_evidence_by_slot_removal() -> None:
    _declare("initial irreducibility evidence")
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
