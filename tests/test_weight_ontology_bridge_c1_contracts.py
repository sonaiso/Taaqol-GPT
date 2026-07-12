"""Constitutional tests for WEIGHT-ONTOLOGY-BRIDGE-C1 contract surface.

Origin law     : docs/90 (section 10 bridge hardening clauses)
Branch         : WEIGHT-ONTOLOGY-BRIDGE-C1 (carrier-only contract surface)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.weight_ontology_bridge_c1 import (
    WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS,
    WEIGHT_ONTOLOGY_BRIDGE_C1_RANK_CEILING,
    WEIGHT_ONTOLOGY_BRIDGE_C1_RESIDUAL_VOCABULARY,
    AnchorKind,
    BridgeConflictState,
    BridgeDecisionState,
    BridgePathFamily,
    OntologySchemaRef,
    WeightKind,
    WeightOntologyBridgeAssessment,
    WeightOntologyBridgeRequest,
    WeightOntologyBridgeResidual,
    WeightOntologyBridgeResidualKind,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_FORBIDDEN_OUTPUTS = (
    "MEANING",
    "PREDICATION",
    "TRUTH",
    "ACTUAL_THING",
    "ACTUAL_PROPERTY",
    "ACTUAL_ATTRIBUTE",
    "ACTUAL_TRANSFORMATION",
    "ACTUAL_EVENT",
    "ACTUAL_GENUS_MEMBERSHIP",
    "ACTUAL_SPECIES_MEMBERSHIP",
    "ACTUAL_AGENT",
    "ACTUAL_PATIENT",
    "ACTUAL_RELATION",
    "RESOLVED_REFERENCE",
    "EXTERNAL_TRUTH",
)


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/90_REBUILT_CONSTITUTIONAL_GOVERNANCE_ARCHITECTURE.md",
        branch_name=branch_name,
        constitutional_chain=("docs/90", "WEIGHT-ONTOLOGY-BRIDGE-C1"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=forbidden_outputs,
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
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _valid_schema(**overrides: object) -> OntologySchemaRef:
    values: dict[str, object] = {
        "schema_id": "schema://entity/basic",
        "schema_kind": "ENTITY_SCHEMA",
        "domain": "domain://arabic-lexical-ontology",
        "admissible_properties": ("property://human", "property://writer"),
        "invariant_refs": ("inv://identity",),
        "evidence_refs": ("evidence://schema-attestation",),
        "trace_ref": "trace://bridge-c1/schema",
        "schema_status": "ACTIVE",
    }
    values.update(overrides)
    return OntologySchemaRef(**values)  # type: ignore[arg-type]


def _valid_request(**overrides: object) -> WeightOntologyBridgeRequest:
    values: dict[str, object] = {
        "request_id": "bridge-req://k1",
        "formal_weight_id": "weight://faeil",
        "ontology_schema_ref": _valid_schema(),
        "weight_kind": WeightKind.DERIVATIONAL_NOUN,
        "requested_anchor_kind": AnchorKind.WEIGHTED_ATTRIBUTE_INTERFACE,
        "path_family": BridgePathFamily.DERIVATIONAL_WEIGHT_PATH,
        "compatibility_rule_ids": ("rule://typed-compatibility",),
        "lexical_evidence_refs": ("lex://evidence/katib",),
        "residuals": (),
        "rank": Rank.CANDIDATE,
        "trace_ref": "trace://bridge-c1/request",
        "forbidden_outputs": WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS,
    }
    values.update(overrides)
    return WeightOntologyBridgeRequest(**values)  # type: ignore[arg-type]


def _valid_assessment(**overrides: object) -> WeightOntologyBridgeAssessment:
    values: dict[str, object] = {
        "request_id": "bridge-req://k1",
        "allowed_anchor_kinds": (AnchorKind.WEIGHTED_ATTRIBUTE_INTERFACE,),
        "competing_bridge_ids": (),
        "defeating_difference_refs": (),
        "blocker_refs": (),
        "decision": BridgeDecisionState.PROVEN,
        "rank": Rank.CANDIDATE,
        "conflict": BridgeConflictState.NONE,
        "residuals": (),
        "trace_ref": "trace://bridge-c1/assessment",
        "forbidden_outputs": WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS,
    }
    values.update(overrides)
    return WeightOntologyBridgeAssessment(**values)  # type: ignore[arg-type]


def test_bridge_c1_declares_local_residual_vocabulary_only() -> None:
    _declare("local residual vocabulary")

    assert (
        tuple(kind.value for kind in WeightOntologyBridgeResidualKind)
        == WEIGHT_ONTOLOGY_BRIDGE_C1_RESIDUAL_VOCABULARY
    )
    for residual_name in WEIGHT_ONTOLOGY_BRIDGE_C1_RESIDUAL_VOCABULARY:
        assert residual_name not in FailureCode.__members__


def test_bridge_c1_forbidden_outputs_are_semantic_and_truth_blockers() -> None:
    _declare("forbidden semantic outputs", _FORBIDDEN_OUTPUTS)

    assert WEIGHT_ONTOLOGY_BRIDGE_C1_FORBIDDEN_OUTPUTS == _FORBIDDEN_OUTPUTS
    assert WEIGHT_ONTOLOGY_BRIDGE_C1_RANK_CEILING is Rank.CANDIDATE


def test_schema_requires_active_ontology_with_evidence() -> None:
    _declare("active ontology schema requirement")

    _valid_schema()
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        _valid_schema(schema_status="INACTIVE")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        _valid_schema(evidence_refs=())


def test_request_requires_weight_kind_rules_and_lexical_evidence() -> None:
    _declare("typed request mandatory inputs")

    _valid_request()
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        _valid_request(weight_kind="DERIVATIONAL_NOUN")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        _valid_request(compatibility_rule_ids=())
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        _valid_request(lexical_evidence_refs=())


def test_request_blocks_harf_mabni_and_unlicensed_relation_reference_paths() -> None:
    _declare("path restrictions for bridge opening")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.FORBIDDEN_STRAIGHT_LINE.value):
        _valid_request(path_family=BridgePathFamily.HARF_PATH)
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.FORBIDDEN_STRAIGHT_LINE.value):
        _valid_request(path_family=BridgePathFamily.MABNI_PATH)
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.FORBIDDEN_STRAIGHT_LINE.value):
        _valid_request(
            requested_anchor_kind=AnchorKind.WEIGHTED_RELATION_INTERFACE,
            path_family=BridgePathFamily.OTHER_PATH,
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.FORBIDDEN_STRAIGHT_LINE.value):
        _valid_request(
            requested_anchor_kind=AnchorKind.WEIGHTED_REFERENCE_INTERFACE,
            path_family=BridgePathFamily.OTHER_PATH,
        )


def test_assessment_allows_proven_single_anchor_only() -> None:
    _declare("single-anchor proven discipline", _FORBIDDEN_OUTPUTS)

    _valid_assessment()
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.REQUIRED_SLOT_EMPTY.value):
        _valid_assessment(allowed_anchor_kinds=())
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.FORBIDDEN_STRAIGHT_LINE.value):
        _valid_assessment(
            allowed_anchor_kinds=(
                AnchorKind.WEIGHTED_ATTRIBUTE_INTERFACE,
                AnchorKind.WEIGHTED_ENTITY_ANCHOR,
            )
        )


def test_assessment_requires_underdetermined_or_suspended_for_alternatives() -> None:
    _declare("ambiguity discipline without forced winner")

    alternatives = (
        AnchorKind.WEIGHTED_ATTRIBUTE_INTERFACE,
        AnchorKind.WEIGHTED_ENTITY_ANCHOR,
    )
    _valid_assessment(
        decision=BridgeDecisionState.UNDERDETERMINED,
        allowed_anchor_kinds=alternatives,
        competing_bridge_ids=("bridge://alt-1", "bridge://alt-2"),
        conflict=BridgeConflictState.COMPETING_ALTERNATIVES,
    )
    _valid_assessment(
        decision=BridgeDecisionState.SUSPENDED,
        allowed_anchor_kinds=alternatives,
        competing_bridge_ids=("bridge://alt-1",),
        conflict=BridgeConflictState.COMPETING_ALTERNATIVES,
    )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.FORBIDDEN_STRAIGHT_LINE.value):
        _valid_assessment(
            decision=BridgeDecisionState.REFUSED,
            allowed_anchor_kinds=alternatives,
            competing_bridge_ids=("bridge://alt-1",),
            conflict=BridgeConflictState.COMPETING_ALTERNATIVES,
        )


def test_residual_visibility_is_never_hidden() -> None:
    _declare("residual visibility discipline")

    WeightOntologyBridgeResidual(
        kind=WeightOntologyBridgeResidualKind.STRUCTURAL_COMPATIBILITY_ONLY,
        trace_ref="trace://bridge-c1/residual",
        visibility="VISIBLE",
    )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        WeightOntologyBridgeResidual(
            kind=WeightOntologyBridgeResidualKind.STRUCTURAL_COMPATIBILITY_ONLY,
            trace_ref="trace://bridge-c1/residual-hidden",
            visibility="HIDDEN",  # type: ignore[arg-type]
        )
