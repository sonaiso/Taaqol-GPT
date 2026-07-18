from __future__ import annotations

from sim_agent.f_experiment import (
    EXPECTED_MAPPING_FINGERPRINT,
    FVerdict,
    MappingDeclaration,
    TenConditionAuditor,
    TenConditionCode,
    build_f_experiment,
    run_f_experiment,
)


def test_baseline_structural_valid_true() -> None:
    experiment = build_f_experiment()
    assert experiment.structural_valid()


def test_baseline_mapping_fingerprint_constant() -> None:
    report = run_f_experiment()
    assert report.mapping_fingerprint == EXPECTED_MAPPING_FINGERPRINT


def test_baseline_verdict_flow_accept_defer_block() -> None:
    experiment = build_f_experiment()
    assert experiment.accept_case.evaluate() == FVerdict.ACCEPT
    assert experiment.defer_case.evaluate() == FVerdict.DEFER
    assert experiment.block_case.evaluate() == FVerdict.BLOCK


def test_nontrivial_feature_flags_present() -> None:
    experiment = build_f_experiment()
    assert "abstract_surface_distinction" in experiment.non_trivial_features
    assert "carrier_protocol_dependency" in experiment.non_trivial_features
    assert "same_state_multiple_realizations" in experiment.non_trivial_features
    assert "same_surface_not_sufficient" in experiment.non_trivial_features


def test_audit_suite_passes_all_ten_conditions() -> None:
    report = run_f_experiment()
    assert report.structural_valid
    assert report.ten_condition_passed
    assert len(report.results) == 10
    assert all(result.passed for result in report.results)


def test_condition_01_accept_to_block_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[0]
    assert result.code == TenConditionCode.ACCEPT_TO_BLOCK
    assert result.passed


def test_condition_02_block_to_accept_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[1]
    assert result.code == TenConditionCode.BLOCK_TO_ACCEPT
    assert result.passed


def test_condition_03_operation_collapse_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[2]
    assert result.code == TenConditionCode.OPERATION_COLLAPSE
    assert result.passed


def test_condition_04_composition_failure_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[3]
    assert result.code == TenConditionCode.COMPOSITION_FAILURE
    assert result.passed


def test_condition_05_intermediate_layer_deleted_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[4]
    assert result.code == TenConditionCode.INTERMEDIATE_LAYER_DELETED
    assert result.passed


def test_condition_06_rank_inflation_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[5]
    assert result.code == TenConditionCode.RANK_INFLATION
    assert result.passed


def test_condition_07_identity_loss_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[6]
    assert result.code == TenConditionCode.IDENTITY_LOSS
    assert result.passed


def test_condition_08_blocking_residual_loss_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[7]
    assert result.code == TenConditionCode.BLOCKING_RESIDUAL_LOSS
    assert result.passed


def test_condition_09_post_hoc_mapping_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[8]
    assert result.code == TenConditionCode.POST_HOC_MAPPING
    assert result.passed


def test_condition_10_random_symbolic_equivalence_detected() -> None:
    result = TenConditionAuditor(build_f_experiment()).run().results[9]
    assert result.code == TenConditionCode.RANDOM_SYMBOLIC_EQUIVALENCE
    assert result.passed


def test_mapping_declaration_detects_post_hoc_mutation() -> None:
    declaration = MappingDeclaration(
        state_map={"a": "b"},
        operation_map={"o1": "o2"},
    )
    assert not declaration.has_post_hoc_mutation()
    declaration.state_map["a"] = "c"
    assert declaration.has_post_hoc_mutation()


def test_same_state_can_have_multiple_realizations() -> None:
    experiment = build_f_experiment()
    realizations = experiment.state_multiple_realizations["i3rab_raf3"]
    assert len(realizations) > 1
    assert "waw" in realizations


def test_surface_alone_not_sufficient_to_recover_state() -> None:
    experiment = build_f_experiment()
    accept = experiment.accept_case
    defer_with_same_surface = type(accept)(
        abstract_state=experiment.defer_case.abstract_state,
        carrier=experiment.defer_case.carrier,
        protocol=experiment.defer_case.protocol,
        realization=accept.realization,
        identity=experiment.defer_case.identity,
        state_licensed=experiment.defer_case.state_licensed,
        carrier_known=experiment.defer_case.carrier_known,
        protocol_licensed=experiment.defer_case.protocol_licensed,
        surface_visible=experiment.defer_case.surface_visible,
        carrier_limited=experiment.defer_case.carrier_limited,
        rank=experiment.defer_case.rank,
        rank_ceiling=experiment.defer_case.rank_ceiling,
        residuals=experiment.defer_case.residuals,
    )
    assert accept.realization == defer_with_same_surface.realization
    assert accept.abstract_state != defer_with_same_surface.abstract_state
    assert accept.evaluate() != defer_with_same_surface.evaluate()


def test_pipeline_contains_required_intermediate_layer() -> None:
    layers = build_f_experiment().accept_case.pipeline_layers()
    assert len(layers) == 3
    assert all(layers)
