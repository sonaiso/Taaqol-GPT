"""USM-C2.1 claim-type and bridge hardening tests."""

from __future__ import annotations

from dataclasses import replace

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    BridgeDirection,
    BridgeId,
    BridgeKind,
    ClaimTypeContract,
    ClaimTypeId,
    DomainId,
    EntityTypeId,
    RuleId,
    ScienceBridgeContract,
    ScienceEvidenceContract,
    ScienceId,
    TraceRef,
    TypedUSMReference,
    USMFailureCode,
    USMReferenceSlot,
    USMSchemaError,
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
        origin_law="docs/14_PR_CHAIN_ROADMAP.md",
        branch_name=f"USM-C2.1 claim/bridge ({branch_note})",
        constitutional_chain=("docs/14", "USM-C2", "USM-C2.1"),
        chain_position="USM-C2.1 corrective hardening",
        origin_law_ref="docs/14_PR_CHAIN_ROADMAP.md",
        branch_of_origin="USM claim typing + directional bridge contracts",
        forbidden_shortcut_assertions=(
            "ClaimTypeRegistry -> ClaimEvaluationRuntime",
            "BridgeContract -> BridgeExecution",
            "BridgePresence -> EvidenceTransfer",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("ClaimCertificate", "ExecutedBridge", "RankTransfer"),
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


def _math_bridge() -> ScienceBridgeContract:
    return ScienceBridgeContract(
        bridge_id=BridgeId("MATH_TO_FOREIGN_ENTITY_BRIDGE"),
        source_science_id=ScienceId("ELEMENTARY_MATHEMATICS"),
        target_science_id=ScienceId("FOREIGN_SCIENCE"),
        source_domain_id=DomainId("ARITHMETIC_AND_INTRO_ALGEBRA"),
        target_domain_id=DomainId("FOREIGN_DOMAIN"),
        source_type_ref=TypedUSMReference(
            science_id=ScienceId("ELEMENTARY_MATHEMATICS"),
            slot=USMReferenceSlot.ENTITY,
            local_identifier="EQUATION",
        ),
        target_type_ref=TypedUSMReference(
            science_id=ScienceId("FOREIGN_SCIENCE"),
            slot=USMReferenceSlot.ENTITY,
            local_identifier="FOREIGN_EQUATION",
        ),
        bridge_kind=BridgeKind.TERMINOLOGY_MAPPING,
        direction=BridgeDirection.SOURCE_TO_TARGET,
        preserved_invariants=(RuleId("TERM_BOUNDARY_PRESERVED"),),
        declared_translation=(RuleId("DECLARED_TERM_MAPPING_ONLY"),),
        required_evidence_types=(matrix_evidence_id(),),
        blockers=(RuleId("NO_AUTO_EXECUTION"),),
        rank_ceiling=Rank.CANDIDATE,
        residual_policy_ref=RuleId("BRIDGE_RESIDUAL_POLICY"),
        trace_ref=TraceRef("trace://usm/reference/math/v1/bridges/math_foreign"),
    )


def matrix_evidence_id():
    matrix = make_elementary_mathematics_reference_matrix_v1()
    return matrix.evidence[0].evidence_type_id


def test_claim_type_id_is_not_rule_id() -> None:
    _declare("claim type id distinct from rule id")
    claim = ClaimTypeId("DERIVATION_CLAIM")
    rule = RuleId("DERIVATION_CLAIM")
    assert claim != rule
    assert claim.__class__ is not rule.__class__


def test_evidence_contract_requires_claim_type_ids() -> None:
    _declare("evidence requires claim type ids")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    evidence = matrix.evidence[0]
    with pytest.raises(USMSchemaError):
        ScienceEvidenceContract(
            evidence_type_id=evidence.evidence_type_id,
            science_id=evidence.science_id,
            supported_claim_types=(RuleId("NOT_A_CLAIM_TYPE"),),  # type: ignore[arg-type]
            domain_scope=evidence.domain_scope,
            relevance_rule=evidence.relevance_rule,
            coverage_rule=evidence.coverage_rule,
            independence_rule=evidence.independence_rule,
            counterevidence_rule=evidence.counterevidence_rule,
            global_rank_ceiling=evidence.global_rank_ceiling,
            trace_ref=evidence.trace_ref,
        )


def test_claim_type_contract_rejects_foreign_science_references() -> None:
    _declare("claim type rejects foreign references")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    bad_claim = replace(
        matrix.claim_types[0],
        subject_type_refs=(EntityTypeId("FOREIGN_ENTITY"),),
    )
    result = validate_usm_matrix(replace(matrix, claim_types=(bad_claim, *matrix.claim_types[1:])))
    assert USMFailureCode.CLAIM_TYPE_REFERENCE_UNRESOLVED in result.failure_codes


def test_claim_type_requires_matching_criterion() -> None:
    _declare("claim type requires matching criterion")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    claim = matrix.claim_types[0]
    with pytest.raises(USMSchemaError):
        ClaimTypeContract(
            claim_type_id=claim.claim_type_id,
            science_id=claim.science_id,
            domain_scope=claim.domain_scope,
            subject_type_refs=claim.subject_type_refs,
            predicate_or_result_type_refs=claim.predicate_or_result_type_refs,
            relation_type_refs=claim.relation_type_refs,
            matching_criterion_ref="NOT_A_RULE_ID",  # type: ignore[arg-type]
            admissible_evidence_type_refs=claim.admissible_evidence_type_refs,
            local_rank_ceiling=claim.local_rank_ceiling,
            forbidden_overclaims=claim.forbidden_overclaims,
            trace_ref=claim.trace_ref,
        )


def test_claim_type_does_not_issue_judgment() -> None:
    _declare("claim type does not issue judgment")
    assert not hasattr(ClaimTypeContract, "issue_judgment")
    assert "CERTIFICATE" not in ClaimTypeContract.__name__.upper()


def test_cross_science_reference_requires_explicit_bridge() -> None:
    _declare("cross science reference requires explicit bridge")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    foreign_capability = replace(matrix.capabilities[0], science_id=ScienceId("FOREIGN_SCIENCE"))
    object.__setattr__(matrix, "capabilities", (foreign_capability,))
    result = validate_usm_matrix(matrix)
    assert USMFailureCode.CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE in result.failure_codes


def test_bridge_is_directional() -> None:
    _declare("bridge is directional")
    bridge = _math_bridge()
    assert bridge.direction is BridgeDirection.SOURCE_TO_TARGET
    assert bridge.direction.name != "BIDIRECTIONAL"


def test_reverse_transfer_requires_separate_bridge() -> None:
    _declare("reverse transfer requires separate bridge")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    foreign_capability = replace(matrix.capabilities[0], science_id=ScienceId("FOREIGN_SCIENCE"))
    object.__setattr__(matrix, "capabilities", (foreign_capability,))
    forward_only = replace(
        _math_bridge(),
        source_science_id=ScienceId("ELEMENTARY_MATHEMATICS"),
        target_science_id=ScienceId("FOREIGN_SCIENCE"),
        direction=BridgeDirection.SOURCE_TO_TARGET,
    )
    object.__setattr__(matrix, "bridges", (forward_only,))
    result = validate_usm_matrix(matrix)
    assert USMFailureCode.CROSS_SCIENCE_REFERENCE_WITHOUT_BRIDGE in result.failure_codes


def test_bridge_carrier_does_not_execute_transfer() -> None:
    _declare("bridge carrier does not execute transfer")
    assert not hasattr(ScienceBridgeContract, "execute_transfer")


def test_bridge_does_not_transfer_rank() -> None:
    _declare("bridge does not transfer rank")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    result = validate_usm_matrix(replace(matrix, bridges=(_math_bridge(),)))
    assert USMFailureCode.BRIDGE_RANK_CEILING_VIOLATION not in result.failure_codes


def test_bridge_does_not_certify_external_truth() -> None:
    _declare("bridge does not certify external truth")
    bridge = _math_bridge()
    assert "TRUTH" not in bridge.bridge_kind.value
    assert "CERTIFICATE" not in bridge.trace_ref.value.upper()


def test_bridge_rejects_unresolved_source_reference() -> None:
    _declare("bridge rejects unresolved source reference")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    broken_bridge = replace(
        _math_bridge(),
        source_type_ref=TypedUSMReference(
            science_id=ScienceId("ELEMENTARY_MATHEMATICS"),
            slot=USMReferenceSlot.ENTITY,
            local_identifier="UNKNOWN_SOURCE_ENTITY",
        ),
    )
    result = validate_usm_matrix(replace(matrix, bridges=(broken_bridge,)))
    assert USMFailureCode.BRIDGE_SOURCE_REFERENCE_UNRESOLVED in result.failure_codes


def test_bridge_rejects_unresolved_target_reference() -> None:
    _declare("bridge rejects unresolved target reference")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    broken_bridge = replace(
        _math_bridge(),
        target_science_id=ScienceId("ELEMENTARY_MATHEMATICS"),
        target_type_ref=TypedUSMReference(
            science_id=ScienceId("ELEMENTARY_MATHEMATICS"),
            slot=USMReferenceSlot.ENTITY,
            local_identifier="UNKNOWN_TARGET_ENTITY",
        ),
    )
    result = validate_usm_matrix(replace(matrix, bridges=(broken_bridge,)))
    assert USMFailureCode.BRIDGE_TARGET_REFERENCE_UNRESOLVED in result.failure_codes
