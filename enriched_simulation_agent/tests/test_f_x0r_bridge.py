"""Regression tests for the local AUX-ESA F→X0R bridge surface.

Classification note:
- This module is plain pytest regression coverage for auxiliary-local behavior.
- It is not a constitutional harness module (`ConstitutionalTestCase` /
  `ConstitutionalChainTestCase`) and does not claim admission or chain advancement.
"""

from __future__ import annotations

import ast
import inspect

from sim_agent.f_experiment import EXPECTED_MAPPING_FINGERPRINT
from sim_agent.f_x0r_bridge import (
    BRIDGE_RESIDUAL,
    CONSTITUTIONAL_PROMOTION_RESIDUAL,
    EXTERNAL_VALIDITY_RESIDUAL,
    FToX0RBridgeReport,
    LocalCandidateShapeFailureCode,
    LocalCandidateShapingResult,
    LocalContractReadinessCheckCode,
    LocalContractReadinessFailureCode,
    LocalFailureCode,
    LocalShapedX0RCandidate,
    LocalTransitionReadinessState,
    StrictX0RFieldCheckCode,
    assess_local_contract_readiness_preconditions,
    bridge_f_experiment_to_x0r_vocabulary,
    shape_f_to_x0r_local_candidates,
)


def test_bridge_maps_mapping_declaration_to_origin_branch_identity() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    assert report.declaration.origin == "i3rab_raf3"
    assert report.declaration.branch == "measured_state"
    assert report.declaration.preserved_identity
    assert report.declaration.evidence_fingerprint == EXPECTED_MAPPING_FINGERPRINT


def test_bridge_maps_accept_defer_block_to_local_euclidean_decisions() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    by_case = {case.case_name: case for case in report.cases}

    assert by_case["accept_case"].local_decision.transition_allowed
    assert by_case["accept_case"].local_decision.readiness_state is (
        LocalTransitionReadinessState.LINK_READY
    )
    assert by_case["accept_case"].local_decision.failure_code is None

    assert not by_case["defer_case"].local_decision.transition_allowed
    assert by_case["defer_case"].local_decision.readiness_state is (
        LocalTransitionReadinessState.DEFERRED
    )
    assert by_case["defer_case"].local_decision.failure_code is LocalFailureCode.GATE_REQUIRED

    assert not by_case["block_case"].local_decision.transition_allowed
    assert by_case["block_case"].local_decision.readiness_state is (
        LocalTransitionReadinessState.BLOCKED
    )
    assert by_case["block_case"].local_decision.failure_code is (
        LocalFailureCode.BLOCKING_RESIDUAL_PRESENT
    )


def test_bridge_includes_expected_auxiliary_residuals() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    assert report.bridge_residuals == (
        EXTERNAL_VALIDITY_RESIDUAL,
        CONSTITUTIONAL_PROMOTION_RESIDUAL,
        BRIDGE_RESIDUAL,
    )


def test_bridge_audit_surface_maps_condition_sabab_preventer_rank_residuals() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    by_case = {case.case_name: case for case in report.cases}
    block_case = by_case["block_case"]

    assert block_case.audit.condition
    assert block_case.audit.sabab
    assert block_case.audit.preventer
    assert block_case.audit.rank == 1
    assert "NO_LICENSED_RELATION" in block_case.audit.residuals
    assert EXTERNAL_VALIDITY_RESIDUAL in block_case.audit.residuals
    assert CONSTITUTIONAL_PROMOTION_RESIDUAL in block_case.audit.residuals


def test_bridge_strict_field_completion_audit_enforces_f3_surface() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    strict_audit = report.strict_field_completion_audit
    by_code = {check.code: check for check in strict_audit.checks}

    assert strict_audit.all_passed
    assert len(strict_audit.checks) == 10
    assert by_code[StrictX0RFieldCheckCode.ORIGIN_PRESENT].passed
    assert by_code[StrictX0RFieldCheckCode.BRANCH_PRESENT].passed
    assert by_code[StrictX0RFieldCheckCode.PRESERVED_IDENTITY_PRESENT].passed
    assert by_code[StrictX0RFieldCheckCode.EVIDENCE_FINGERPRINT_PRESENT].passed
    assert by_code[StrictX0RFieldCheckCode.CONDITION_SABAB_PREVENTER_SEPARATE].passed
    assert by_code[StrictX0RFieldCheckCode.RANK_PROJECTION_NO_KERNEL_PROMOTION].passed
    assert by_code[StrictX0RFieldCheckCode.REQUIRED_RESIDUALS_PRESERVED].passed
    assert by_code[StrictX0RFieldCheckCode.NO_KERNEL_X0R_IMPORT].passed
    assert by_code[StrictX0RFieldCheckCode.NO_EUCLIDEAN_TRANSITION_CONTRACT_MUTATION].passed
    assert by_code[StrictX0RFieldCheckCode.NO_KERNEL_CAN_TRANSITION_CALL].passed


def test_f4_shaping_produces_local_candidates_after_f3_audit() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    shaped = shape_f_to_x0r_local_candidates(report)

    assert shaped.shaped
    assert shaped.failure_code is None
    assert len(shaped.candidates) == 3
    assert shaped.auxiliary_only
    assert shaped.non_admitted
    assert shaped.non_chain_advancing


def test_f4_shaping_blocks_when_mandatory_residual_is_missing() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    report_without_bridge_residual = FToX0RBridgeReport(
        declaration=report.declaration,
        cases=report.cases,
        bridge_residuals=(
            EXTERNAL_VALIDITY_RESIDUAL,
            CONSTITUTIONAL_PROMOTION_RESIDUAL,
        ),
        strict_field_completion_audit=report.strict_field_completion_audit,
    )

    shaped = shape_f_to_x0r_local_candidates(report_without_bridge_residual)

    assert not shaped.shaped
    assert shaped.failure_code is LocalCandidateShapeFailureCode.MANDATORY_RESIDUAL_MISSING


def test_f4_shaping_has_no_kernel_transition_call_path() -> None:
    source = inspect.getsource(shape_f_to_x0r_local_candidates)
    tree = ast.parse(source)
    forbidden_name = "can_" + "transition"

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            assert node.func.id != forbidden_name
        if isinstance(node.func, ast.Attribute):
            assert node.func.attr != forbidden_name


def test_f4_shaping_has_no_euclidean_transition_contract_reference() -> None:
    source = inspect.getsource(shape_f_to_x0r_local_candidates)
    tree = ast.parse(source)
    forbidden_identifier = "EuclideanTransition" + "Contract"

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            assert node.id != forbidden_identifier
        if isinstance(node, ast.Attribute):
            assert node.attr != forbidden_identifier


def test_f4_shaping_carries_non_admission_residuals() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    shaped = shape_f_to_x0r_local_candidates(report)

    assert EXTERNAL_VALIDITY_RESIDUAL in shaped.carry_forward_residuals
    assert CONSTITUTIONAL_PROMOTION_RESIDUAL in shaped.carry_forward_residuals
    assert BRIDGE_RESIDUAL in shaped.carry_forward_residuals
    assert all(EXTERNAL_VALIDITY_RESIDUAL in candidate.residuals for candidate in shaped.candidates)
    assert all(
        CONSTITUTIONAL_PROMOTION_RESIDUAL in candidate.residuals
        for candidate in shaped.candidates
    )


def test_f4_shaping_cannot_claim_external_validity() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    shaped = shape_f_to_x0r_local_candidates(report)

    assert not shaped.external_validity_certified
    assert all(not candidate.external_validity_certified for candidate in shaped.candidates)


def test_f5_contract_readiness_preconditions_pass_with_f4_shaped_candidates() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    shaped = shape_f_to_x0r_local_candidates(report)
    readiness = assess_local_contract_readiness_preconditions(shaped)
    by_code = {check.code: check for check in readiness.checks}

    assert readiness.contract_ready
    assert readiness.failure_code is None
    assert by_code[LocalContractReadinessCheckCode.SHAPED_CANDIDATES_PRESENT].passed
    assert by_code[LocalContractReadinessCheckCode.AUXILIARY_SURFACE_LOCKED].passed
    assert by_code[LocalContractReadinessCheckCode.REQUIRED_IDENTITY_FIELDS_PRESENT].passed
    assert by_code[LocalContractReadinessCheckCode.NON_ADMISSION_RESIDUALS_VISIBLE].passed
    assert by_code[LocalContractReadinessCheckCode.NO_ADMISSION_FLAGS_IN_CANDIDATES].passed
    assert readiness.residual_matrix.admission_blocking_residuals == (
        EXTERNAL_VALIDITY_RESIDUAL,
        CONSTITUTIONAL_PROMOTION_RESIDUAL,
    )
    assert readiness.residual_matrix.bridge_deferred_residuals == (BRIDGE_RESIDUAL,)
    assert readiness.auxiliary_only
    assert readiness.non_admitted
    assert readiness.non_chain_advancing
    assert not readiness.external_validity_certified


def test_f5_contract_readiness_requires_shaped_candidates() -> None:
    unshaped = LocalCandidateShapingResult(
        shaped=False,
        failure_code=LocalCandidateShapeFailureCode.STRICT_AUDIT_REQUIRED,
        candidates=(),
        carry_forward_residuals=(
            EXTERNAL_VALIDITY_RESIDUAL,
            CONSTITUTIONAL_PROMOTION_RESIDUAL,
            BRIDGE_RESIDUAL,
        ),
        auxiliary_only=True,
        non_admitted=True,
        non_chain_advancing=True,
        external_validity_certified=False,
    )

    readiness = assess_local_contract_readiness_preconditions(unshaped)
    assert not readiness.contract_ready
    assert readiness.failure_code is LocalContractReadinessFailureCode.SHAPED_CANDIDATES_REQUIRED


def test_f5_contract_readiness_requires_successful_f4_shaping_state() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    shaped = shape_f_to_x0r_local_candidates(report)
    inconsistent = LocalCandidateShapingResult(
        shaped=True,
        failure_code=LocalCandidateShapeFailureCode.STRICT_AUDIT_REQUIRED,
        candidates=shaped.candidates,
        carry_forward_residuals=shaped.carry_forward_residuals,
        auxiliary_only=shaped.auxiliary_only,
        non_admitted=shaped.non_admitted,
        non_chain_advancing=shaped.non_chain_advancing,
        external_validity_certified=shaped.external_validity_certified,
    )

    readiness = assess_local_contract_readiness_preconditions(inconsistent)
    assert not readiness.contract_ready
    assert readiness.failure_code is LocalContractReadinessFailureCode.F4_SHAPING_NOT_SUCCESSFUL


def test_f5_contract_readiness_fails_when_required_identity_field_missing() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    shaped = shape_f_to_x0r_local_candidates(report)
    first = shaped.candidates[0]
    malformed_candidate = LocalShapedX0RCandidate(
        case_name=first.case_name,
        origin="",
        branch=first.branch,
        readiness_state=first.readiness_state,
        rank=first.rank,
        residuals=first.residuals,
        auxiliary_only=first.auxiliary_only,
        admitted=first.admitted,
        chain_advancing=first.chain_advancing,
        external_validity_certified=first.external_validity_certified,
    )
    malformed = LocalCandidateShapingResult(
        shaped=shaped.shaped,
        failure_code=shaped.failure_code,
        candidates=(malformed_candidate, *shaped.candidates[1:]),
        carry_forward_residuals=shaped.carry_forward_residuals,
        auxiliary_only=shaped.auxiliary_only,
        non_admitted=shaped.non_admitted,
        non_chain_advancing=shaped.non_chain_advancing,
        external_validity_certified=shaped.external_validity_certified,
    )

    readiness = assess_local_contract_readiness_preconditions(malformed)
    assert not readiness.contract_ready
    assert readiness.failure_code is LocalContractReadinessFailureCode.REQUIRED_FIELDS_MISSING


def test_f5_contract_readiness_fails_when_non_admission_residual_missing() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    shaped = shape_f_to_x0r_local_candidates(report)
    first = shaped.candidates[0]
    mutated_first = LocalShapedX0RCandidate(
        case_name=first.case_name,
        origin=first.origin,
        branch=first.branch,
        readiness_state=first.readiness_state,
        rank=first.rank,
        residuals=tuple(
            residual
            for residual in first.residuals
            if residual != CONSTITUTIONAL_PROMOTION_RESIDUAL
        ),
        auxiliary_only=first.auxiliary_only,
        admitted=first.admitted,
        chain_advancing=first.chain_advancing,
        external_validity_certified=first.external_validity_certified,
    )
    mutated = LocalCandidateShapingResult(
        shaped=shaped.shaped,
        failure_code=shaped.failure_code,
        candidates=(mutated_first, *shaped.candidates[1:]),
        carry_forward_residuals=shaped.carry_forward_residuals,
        auxiliary_only=shaped.auxiliary_only,
        non_admitted=shaped.non_admitted,
        non_chain_advancing=shaped.non_chain_advancing,
        external_validity_certified=shaped.external_validity_certified,
    )

    readiness = assess_local_contract_readiness_preconditions(mutated)
    assert not readiness.contract_ready
    assert readiness.failure_code is LocalContractReadinessFailureCode.MANDATORY_RESIDUAL_MISSING


def test_f5_contract_readiness_preserves_input_carry_forward_residuals() -> None:
    report = bridge_f_experiment_to_x0r_vocabulary()
    shaped = shape_f_to_x0r_local_candidates(report)
    extra_residual = "FUTURE_AUX_RESIDUAL"
    shaped_with_extra = LocalCandidateShapingResult(
        shaped=shaped.shaped,
        failure_code=shaped.failure_code,
        candidates=shaped.candidates,
        carry_forward_residuals=(*shaped.carry_forward_residuals, extra_residual),
        auxiliary_only=shaped.auxiliary_only,
        non_admitted=shaped.non_admitted,
        non_chain_advancing=shaped.non_chain_advancing,
        external_validity_certified=shaped.external_validity_certified,
    )

    readiness = assess_local_contract_readiness_preconditions(shaped_with_extra)
    assert readiness.carry_forward_residuals == shaped_with_extra.carry_forward_residuals
    assert extra_residual in readiness.carry_forward_residuals


def test_f5_contract_readiness_has_no_kernel_transition_call_path() -> None:
    source = inspect.getsource(assess_local_contract_readiness_preconditions)
    tree = ast.parse(source)
    forbidden_name = "can_" + "transition"

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            assert node.func.id != forbidden_name
        if isinstance(node.func, ast.Attribute):
            assert node.func.attr != forbidden_name


def test_f5_contract_readiness_has_no_euclidean_transition_contract_reference() -> None:
    source = inspect.getsource(assess_local_contract_readiness_preconditions)
    tree = ast.parse(source)
    forbidden_identifier = "EuclideanTransition" + "Contract"

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            assert node.id != forbidden_identifier
        if isinstance(node, ast.Attribute):
            assert node.attr != forbidden_identifier
