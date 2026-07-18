from __future__ import annotations

from sim_agent.f_experiment import EXPECTED_MAPPING_FINGERPRINT
from sim_agent.f_x0r_bridge import (
    BRIDGE_RESIDUAL,
    CONSTITUTIONAL_PROMOTION_RESIDUAL,
    EXTERNAL_VALIDITY_RESIDUAL,
    LocalFailureCode,
    LocalTransitionReadinessState,
    bridge_f_experiment_to_x0r_vocabulary,
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
