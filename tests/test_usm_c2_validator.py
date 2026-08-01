"""USM-C2/C2.1 structural validator tests."""

from __future__ import annotations

from dataclasses import replace

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    EntityTypeId,
    EvidenceTypeId,
    KnowledgeObjectTypeId,
    ScienceId,
    USMFailureCode,
    USMResidual,
    USMResidualKind,
    USMValidationState,
    make_arabic_reference_matrix_v1,
    make_elementary_mathematics_reference_matrix_v1,
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
        branch_name=f"USM-C2.1 ({branch_note})",
        constitutional_chain=("docs/98", "USM-C1", "USM-C2", "USM-C2.1"),
        chain_position="USM-C2.1 structural validator hardening",
        origin_law_ref="docs/98_UNIVERSAL_SCIENCE_MATRIX_CONSTITUTIONAL_LAW.md",
        branch_of_origin="USM structural consistency checks",
        forbidden_shortcut_assertions=(
            "USM-C2.1 -> TransitionCertificate",
            "USM-C2.1 -> ScientificTruthProof",
            "USM-C2.1 -> RankPromotion",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "TransitionCertificate",
            "ScientificTruthProof",
            "RankPromotion",
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


def test_validator_rejects_capability_with_unknown_bearer() -> None:
    _declare("unknown capability bearer")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    broken_capability = replace(matrix.capabilities[0], bearer_type=EntityTypeId("UNKNOWN_ENTITY"))
    broken = replace(matrix, capabilities=(broken_capability,))
    result = validate_usm_matrix(broken)
    assert USMFailureCode.UNKNOWN_CAPABILITY_BEARER in result.failure_codes


def test_validator_rejects_relation_with_unknown_operand() -> None:
    _declare("unknown relation operand")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    broken_relation = replace(
        matrix.relations[0],
        operand_types=(EntityTypeId("UNKNOWN_LEFT"), EntityTypeId("UNKNOWN_RIGHT")),
    )
    broken = replace(matrix, relations=(broken_relation,))
    result = validate_usm_matrix(broken)
    assert USMFailureCode.UNKNOWN_RELATION_OPERAND in result.failure_codes


def test_validator_rejects_transformation_without_required_capability() -> None:
    _declare("unknown required capability")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    broken_transformation = replace(
        matrix.transformations[0],
        required_capabilities=(matrix.capabilities[0].capability_id.__class__("UNKNOWN_CAP"),),
    )
    broken = replace(matrix, transformations=(broken_transformation,))
    result = validate_usm_matrix(broken)
    assert USMFailureCode.UNKNOWN_TRANSFORMATION_REFERENCE in result.failure_codes


def test_validator_rejects_judgment_with_unknown_evidence_type() -> None:
    _declare("unknown judgment evidence")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    broken_judgment = replace(
        matrix.judgments[0],
        required_evidence_types=(EvidenceTypeId("UNKNOWN_EVIDENCE"),),
    )
    broken = replace(matrix, judgments=(broken_judgment,))
    result = validate_usm_matrix(broken)
    assert USMFailureCode.UNKNOWN_JUDGMENT_EVIDENCE_TYPE in result.failure_codes


def test_validator_rejects_application_with_unknown_knowledge_object() -> None:
    _declare("unknown application knowledge object")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    broken_application = replace(
        matrix.applications[0],
        knowledge_object_types=(KnowledgeObjectTypeId("UNKNOWN_KO"),),
    )
    broken = replace(matrix, applications=(broken_application,))
    result = validate_usm_matrix(broken)
    assert USMFailureCode.UNKNOWN_APPLICATION_REFERENCE in result.failure_codes


def test_validator_rejects_cross_science_reference_without_bridge() -> None:
    _declare("cross-science reference without bridge")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    foreign_capability = replace(matrix.capabilities[0], science_id=ScienceId("FOREIGN_SCIENCE"))
    object.__setattr__(matrix, "capabilities", (foreign_capability,))
    result = validate_usm_matrix(matrix)
    assert USMFailureCode.CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE in result.failure_codes
    assert USMFailureCode.REFERENCE_MATRIX_FOREIGN_SCIENCE_ID in result.failure_codes


def test_validator_preserves_blocking_residuals() -> None:
    _declare("preserves blocking residuals")
    matrix = make_arabic_reference_matrix_v1()
    forced_blocking = replace(
        matrix.residuals[0],
        residual_id="forced-blocking-residual",
        kind=USMResidualKind.KNOWLEDGE_REVISION_DEFERRED,
        blocking=True,
    )
    result = validate_usm_matrix(replace(matrix, residuals=(forced_blocking,)))
    assert any(residual.blocking for residual in result.residuals)
    assert result.state is USMValidationState.BLOCKED


def test_validator_returns_named_failure_codes() -> None:
    _declare("named failure codes")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    broken_relation = replace(
        matrix.relations[0],
        operand_types=(EntityTypeId("UNKNOWN_LEFT"), EntityTypeId("UNKNOWN_RIGHT")),
    )
    result = validate_usm_matrix(replace(matrix, relations=(broken_relation,)))
    assert result.failure_codes
    assert all(isinstance(code, USMFailureCode) for code in result.failure_codes)


def test_validator_reports_expected_state_mismatch() -> None:
    _declare("expected state mismatch")
    matrix = make_arabic_reference_matrix_v1()
    result = validate_usm_matrix(matrix, expected_state=USMValidationState.BLOCKED)
    assert result.state is USMValidationState.INVALID
    assert USMFailureCode.REFERENCE_MATRIX_EXPECTED_STATE_MISMATCH in result.failure_codes


def test_validator_deferred_state_is_explicit_and_not_implied_by_reference_residuals() -> None:
    _declare("deferred state only by deferred residual kind")
    matrix = make_arabic_reference_matrix_v1()
    deferred_residual = USMResidual(
        residual_id="deferred-review-needed",
        kind=USMResidualKind.KNOWLEDGE_REVISION_DEFERRED,
        detail="knowledge revision remains deferred",
        blocking=False,
        visible=True,
        repair_hint="review policy in next step",
    )
    result = validate_usm_matrix(replace(matrix, residuals=(deferred_residual,)))
    assert result.state is USMValidationState.DEFERRED
