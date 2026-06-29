"""Constitutional tests for AQD L1 audit-only contracts.

Origin law     : docs/66_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
Branch         : AQD-L1 audit-only contracts
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.L1 import (
    AQD_FORBIDDEN_OUTPUTS,
    AqdAttributeContract,
    AqdAuditContractSchemaError,
    AqdAuditResult,
    AqdInflectionAuditContract,
    AqdMorphologicalBranchContract,
    AqdPartialBranchContract,
    AqdRelationTripletContract,
    AqdReverseAuditContract,
    AqdTemporalBindingContract,
    AqdUniversalContract,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_ORIGIN = "docs/66_AQD_AUDIT_CONTRACTS_CONSTITUTION.md"
_CHAIN = ("docs/66", "AQD-L1", "AuditOnlyContracts")


def _declare(branch_name: str, produced_outputs: frozenset[str] = frozenset()) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=tuple(AQD_FORBIDDEN_OUTPUTS),
        max_rank=Rank.CANDIDATE,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.CANDIDATE,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=produced_outputs,
    )
    assert_constitutional_case(case, result)


def _universal(**overrides: object) -> AqdUniversalContract:
    values = {
        "contract_ref": "aqd://contract/universal",
        "domain_ref": "domain://aqd/l1",
        "scope_ref": "scope://aqd/audit-only",
        "trace_ref": "trace://aqd/universal",
        "proof_object_ref": "proof://aqd/universal",
    }
    values.update(overrides)
    return AqdUniversalContract(**values)


def _partial(**overrides: object) -> AqdPartialBranchContract:
    values = {
        "origin_ref": "origin://aqd/root",
        "branch_ref": "branch://aqd/partial",
        "relation_with_prev_ref": "relation://candidate/prev",
        "relation_with_next_ref": "relation://candidate/next",
        "relation_next_to_prev_ref": "relation://candidate/next-prev",
        "condition_ref": "condition://aqd/shape",
        "sabab_ref": "sabab://aqd/branch",
        "preventer_ref": "preventer://aqd/blocker",
        "trace_ref": "trace://aqd/partial",
        "proof_trace_ref": "trace://proof/aqd/partial",
    }
    values.update(overrides)
    return AqdPartialBranchContract(**values)


def _attribute(**overrides: object) -> AqdAttributeContract:
    values = {
        "carrier_ref": "carrier://aqd/attribute",
        "attribute_ref": "attribute://aqd/candidate",
        "operator_ref": "operator://aqd/effect",
        "effect_candidate_ref": "effect://aqd/candidate",
        "trace_ref": "trace://aqd/attribute",
        "proof_object_ref": "proof://aqd/attribute",
    }
    values.update(overrides)
    return AqdAttributeContract(**values)


def _relation(**overrides: object) -> AqdRelationTripletContract:
    values = {
        "previous_relation_ref": "relation://aqd/previous",
        "next_relation_ref": "relation://aqd/next",
        "next_to_previous_relation_ref": "relation://aqd/next-to-previous",
        "relation_function_candidate": "relation-function://candidate",
        "tool_surface_ref": "tool://surface/not-final",
        "license_condition_ref": "license://condition/ref",
        "trace_ref": "trace://aqd/relation",
        "proof_object_ref": "proof://aqd/relation",
    }
    values.update(overrides)
    return AqdRelationTripletContract(**values)


def _temporal(**overrides: object) -> AqdTemporalBindingContract:
    values = {
        "temporal_scope_ref": "time://scope/audit",
        "utterance_time_ref": "time://utterance/ref",
        "attribute_time_ref": "time://attribute/ref",
        "temporal_policy_ref": "policy://temporal/audit-only",
        "trace_ref": "trace://aqd/temporal",
        "proof_object_ref": "proof://aqd/temporal",
    }
    values.update(overrides)
    return AqdTemporalBindingContract(**values)


def _inflection(**overrides: object) -> AqdInflectionAuditContract:
    values = {
        "operator_ref": "operator://inflection/candidate",
        "carrier_ref": "carrier://inflection/candidate",
        "utterance_time_ref": "time://utterance/ref",
        "attribute_time_ref": "time://attribute/ref",
        "temporal_policy_ref": "policy://temporal/audit-only",
        "effect_candidate_ref": "effect://inflection/candidate",
        "trace_ref": "trace://aqd/inflection",
        "proof_object_ref": "proof://aqd/inflection",
    }
    values.update(overrides)
    return AqdInflectionAuditContract(**values)


def _morphological(**overrides: object) -> AqdMorphologicalBranchContract:
    values = {
        "surface_weight_ref": "weight://surface/candidate",
        "path_card_ref": "path-card://candidate",
        "masdar_open_ref": "masdar://open/ref",
        "denominal_branch_license_ref": "license://denominal/ref",
        "residual_policy_ref": "policy://residual/visible",
        "trace_ref": "trace://aqd/morphological",
        "proof_object_ref": "proof://aqd/morphological",
    }
    values.update(overrides)
    return AqdMorphologicalBranchContract(**values)


def _reverse(**overrides: object) -> AqdReverseAuditContract:
    values = {
        "source_stage_ref": "stage://source",
        "target_stage_ref": "stage://target",
        "reverse_policy_ref": "policy://reverse/audit-only",
        "trace_ref": "trace://aqd/reverse",
        "proof_object_ref": "proof://aqd/reverse",
    }
    values.update(overrides)
    return AqdReverseAuditContract(**values)


def test_all_contracts_are_frozen() -> None:
    _declare("frozen contracts", frozenset({"AqdUniversalContract"}))

    contracts = (
        _universal(),
        _partial(),
        _attribute(),
        _relation(),
        _temporal(),
        _inflection(),
        _morphological(),
        _reverse(),
        AqdAuditResult(
            shape_valid=True,
            status="AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
            residuals=frozenset({"ENERGY_LEAK_LABEL_VISIBLE"}),
            trace_ref="trace://aqd/audit-result",
        ),
    )

    for contract in contracts:
        with pytest.raises(FrozenInstanceError):
            contract.trace_ref = "trace://mutated"  # type: ignore[misc]


def test_rank_promotion_is_rejected() -> None:
    _declare("rank promotion refused")

    with pytest.raises(AqdAuditContractSchemaError, match="CANDIDATE"):
        _universal(rank=Rank.STRONG)


def test_authoritative_true_is_rejected() -> None:
    _declare("authority blocked")

    with pytest.raises(AqdAuditContractSchemaError, match="authoritative"):
        _universal(authoritative=True)


def test_runtime_authorized_true_is_rejected() -> None:
    _declare("runtime authorization blocked")

    with pytest.raises(AqdAuditContractSchemaError, match="runtime_authorized"):
        _universal(runtime_authorized=True)


def test_missing_trace_ref_is_rejected() -> None:
    _declare("trace required")

    with pytest.raises(AqdAuditContractSchemaError, match="trace_ref"):
        _universal(trace_ref="")


def test_missing_proof_refs_are_rejected() -> None:
    _declare("proof ref required")

    with pytest.raises(AqdAuditContractSchemaError, match="proof_object_ref or proof_trace_ref"):
        _universal(proof_object_ref="", proof_trace_ref="")


def test_missing_forbidden_outputs_are_rejected() -> None:
    _declare("forbidden outputs required")

    with pytest.raises(AqdAuditContractSchemaError, match="forbidden_outputs"):
        _universal(forbidden_outputs=frozenset())


def test_partial_branch_contract_requires_branch_boundary_refs() -> None:
    _declare("partial branch boundary refs")

    required_fields = (
        "origin_ref",
        "branch_ref",
        "relation_with_prev_ref",
        "relation_with_next_ref",
        "relation_next_to_prev_ref",
        "condition_ref",
        "sabab_ref",
        "preventer_ref",
    )
    contract = _partial()
    for field_name in required_fields:
        assert getattr(contract, field_name)
        with pytest.raises(AqdAuditContractSchemaError, match=field_name):
            _partial(**{field_name: ""})


def test_temporal_binding_validates_shape_only_and_does_not_execute_time() -> None:
    _declare("temporal shape only", frozenset({"AqdTemporalBindingContract"}))

    temporal = _temporal()

    assert temporal.rank is Rank.CANDIDATE
    assert temporal.runtime_authorized is False
    assert temporal.time_executed is False
    with pytest.raises(AqdAuditContractSchemaError, match="time_executed"):
        _temporal(time_executed=True)


def test_inflection_audit_contract_emits_no_final_irab_or_meaning() -> None:
    _declare("inflection audit only", frozenset({"AqdInflectionAuditContract"}))

    inflection = _inflection()

    assert inflection.final_irab_emitted is False
    assert inflection.final_meaning_emitted is False
    assert "FINAL_MEANING" in inflection.forbidden_outputs
    with pytest.raises(AqdAuditContractSchemaError, match="final_irab_emitted"):
        _inflection(final_irab_emitted=True)
    with pytest.raises(AqdAuditContractSchemaError, match="final_meaning_emitted"):
        _inflection(final_meaning_emitted=True)


def test_reverse_audit_requires_stage_refs_but_no_reverse_runtime() -> None:
    _declare("reverse audit refs")

    reverse = _reverse()

    assert reverse.source_stage_ref
    assert reverse.target_stage_ref
    assert reverse.reverse_runtime_opened is False
    with pytest.raises(AqdAuditContractSchemaError, match="source_stage_ref"):
        _reverse(source_stage_ref="")
    with pytest.raises(AqdAuditContractSchemaError, match="target_stage_ref"):
        _reverse(target_stage_ref="")


def test_audit_result_for_valid_shape_keeps_runtime_blocked() -> None:
    _declare("audit result runtime blocked", frozenset({"AqdAuditResult"}))

    result = AqdAuditResult(
        shape_valid=True,
        status="AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
        residuals=frozenset({"ENERGY_MISMATCH_LABEL_VISIBLE"}),
        trace_ref="trace://aqd/result/valid-shape",
    )

    assert result.shape_valid is True
    assert result.runtime_authorized is False
    assert result.authoritative is False
    assert result.rank is Rank.CANDIDATE


def test_no_parser_runtime_or_kernel_files_are_created() -> None:
    _declare("forbidden runtime files absent")

    forbidden_paths = (
        _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "aqd_parser.py",
        _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "aqd_runtime.py",
        _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "aqd_interpreter.py",
        _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "binding_kernel.py",
        _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "decision_engine.py",
        _REPO_ROOT / "coverage_matrix_v0.1.yaml",
    )

    assert not [path for path in forbidden_paths if path.exists()]
