"""USM-C1 carrier-only constitutional tests."""

from __future__ import annotations

from dataclasses import replace

import pytest

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.usm import (
    CapabilityContract,
    EntityTypeContract,
    RelationTypeId,
    UniversalScienceMatrix,
    USMResidual,
    USMResidualKind,
    USMSchemaError,
    make_elementary_mathematics_reference_matrix_v1,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law="docs/98_UNIVERSAL_SCIENCE_MATRIX_CONSTITUTIONAL_LAW.md",
        branch_name=f"USM-C1 ({branch_note})",
        constitutional_chain=("docs/98", "USM-C1"),
        chain_position="USM-C1 schema/carrier-only surface",
        origin_law_ref="docs/98_UNIVERSAL_SCIENCE_MATRIX_CONSTITUTIONAL_LAW.md",
        branch_of_origin="USM bounded carrier surfaces",
        forbidden_shortcut_assertions=(
            "USM-C1 -> TransitionExecution",
            "USM-C1 -> CertificateIssuance",
            "USM-C1 -> ExternalTruthCertification",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "TransitionExecution",
            "CertificateIssuance",
            "ExternalTruthCertification",
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


def test_usm_matrix_requires_all_eight_slots() -> None:
    _declare("requires all slots")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    with pytest.raises(USMSchemaError):
        UniversalScienceMatrix(
            matrix_id=matrix.matrix_id,
            science_id=matrix.science_id,
            version=matrix.version,
            declared_scope=matrix.declared_scope,
            entities=(),
            capabilities=(),
            relations=(),
            transformations=(),
            evidence=(),
            claim_types=(),
            judgments=(),
            knowledge_objects=(),
            applications=(),
            bridges=(),
            residuals=(),
            trace_ref=matrix.trace_ref,
        )


def test_usm_matrix_rejects_duplicate_ids() -> None:
    _declare("duplicate id refusal")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    duplicate_entity = replace(
        matrix.entities[0],
        entity_type_id=matrix.entities[1].entity_type_id,
    )
    with pytest.raises(USMSchemaError):
        UniversalScienceMatrix(
            matrix_id=matrix.matrix_id,
            science_id=matrix.science_id,
            version=matrix.version,
            declared_scope=matrix.declared_scope,
            entities=(duplicate_entity,) + matrix.entities[1:],
            capabilities=matrix.capabilities,
            relations=matrix.relations,
            transformations=matrix.transformations,
            evidence=matrix.evidence,
            claim_types=matrix.claim_types,
            judgments=matrix.judgments,
            knowledge_objects=matrix.knowledge_objects,
            applications=matrix.applications,
            bridges=matrix.bridges,
            residuals=matrix.residuals,
            trace_ref=matrix.trace_ref,
        )


def test_usm_contracts_reject_cross_typed_identifiers() -> None:
    _declare("cross-typed identifier refusal")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    capability = matrix.capabilities[0]
    with pytest.raises(USMSchemaError):
        CapabilityContract(
            capability_id=capability.capability_id,
            science_id=capability.science_id,
            bearer_type=RelationTypeId("EQUALITY"),  # type: ignore[arg-type]
            permitted_operations=capability.permitted_operations,
            permitted_relation_roles=capability.permitted_relation_roles,
            required_conditions=capability.required_conditions,
            blockers=capability.blockers,
            evidence_requirements=capability.evidence_requirements,
            rank_ceiling=capability.rank_ceiling,
            residual_policy_ref=capability.residual_policy_ref,
            trace_ref=capability.trace_ref,
        )


def test_usm_residuals_must_be_visible() -> None:
    _declare("visible residual rule")
    with pytest.raises(USMSchemaError):
        USMResidual(
            residual_id="hidden",
            kind=USMResidualKind.COVERAGE_GAP,
            detail="hidden residual is forbidden",
            blocking=True,
            visible=False,
            repair_hint="set visible true",
        )


def test_usm_carriers_do_not_execute_transitions() -> None:
    _declare("no transition execution")
    assert not hasattr(UniversalScienceMatrix, "execute_transition")
    assert not hasattr(EntityTypeContract, "execute_transition")


def test_usm_carriers_do_not_issue_certificates() -> None:
    _declare("no certificate surface")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    assert "CERTIFICATE" not in repr(matrix)
    assert "CERTIFIED" not in matrix.declared_scope.upper()


def test_usm_carriers_do_not_claim_external_truth() -> None:
    _declare("no external truth claim")
    matrix = make_elementary_mathematics_reference_matrix_v1()
    assert "external truth" not in matrix.declared_scope.lower()
    assert any(
        residual.kind is USMResidualKind.IRREDUCIBILITY_UNPROVEN
        for residual in matrix.residuals
    )
