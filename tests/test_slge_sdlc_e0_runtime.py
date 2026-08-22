"""Constitutional tests for SLGE-SDLC-E0 lifecycle execution runtime.

Origin law     :
    docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md
Branch         : SLGE-SDLC-E0
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from pathlib import Path

from jsonschema import Draft202012Validator

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.governance import repo_org_projection as projector
from taaqqul_slot_geometry.governance.slge_sdlc_e0_runtime import (
    HistoricalTransitionStatus,
    LegacyBaselineAnchor,
    LegacyRemapDecision,
    SLGEE0DecisionState,
    SLGEE0FailureCode,
    TransitionAttempt,
    evaluate_transition_attempt,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_GOVERNANCE = _REPO_ROOT / "governance"
_REGISTRY = _GOVERNANCE / "registry"
_SCHEMAS = _REPO_ROOT / "schemas" / "governance"
_DOCS = _REPO_ROOT / "docs"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        ),
        branch_name=f"SLGE-SDLC-E0 ({branch_note})",
        constitutional_chain=(
            "docs/124",
            "docs/126",
            "docs/127",
            "schemas/governance/slge_sdlc_e0_runtime.schema.json",
            "governance/registry/slge_sdlc_e0_runtime.json",
            "src/taaqqul_slot_geometry/governance/slge_sdlc_e0_runtime.py",
            "src/taaqqul_slot_geometry/governance/repo_org_projection.py",
            "governance/projections/current_state.json",
        ),
        chain_position="SLGE-SDLC-E0",
        origin_law_ref=(
            "docs/124_SLOT_LICENSED_GEOMETRICAL_ENGINEERING_"
            "PROJECT_DEVELOPMENT_LIFECYCLE_CONSTITUTION.md"
        ),
        branch_of_origin=(
            "Runtime admission of current/future lifecycle transitions with "
            "temporal-cut discipline and explicit non-retroactive-historical boundary."
        ),
        forbidden_shortcut_assertions=(
            "CurrentRuntimeAdmission -> HistoricalCertification",
            "ResidualConsumption -> ResidualResolution",
            "Rebuild -> HistoricalPastRepair",
            "SuccessfulTransition -> RankPromotion",
            "TraceLoss -> Approval",
            "CurrentStateProjection -> E0Approval",
            "Merge -> Closure",
            "GreenCI -> Closure",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "GlobalCurrentLifecycleStateComputation",
            "HistoricalCertificationPromotion",
            "P0ProjectorOpening",
            "G0PREnforcementOpening",
            "C0ClosureOpening",
            "OBSRuntimeOpening",
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


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _base_attempt() -> TransitionAttempt:
    return TransitionAttempt(
        attempt_id="ATTEMPT-E0-1",
        artifact_id="DOC-126",
        lineage_ref="lineage://legacy/doc-126",
        transition_contract_ref="TX-SLGE-M0-TO-E0-001",
        from_slot_ref="SLGE-SDLC-M0",
        to_slot_ref="SLGE-SDLC-E0",
        temporal_epoch_ref="T_SLGE::EPOCH-0001",
        governance_order=1290,
        dependency_order=1290,
        identity_proof_ref="proof://identity/doc-126",
        origin_proof_ref="proof://origin/doc-126",
        domain_scope_proof_ref="proof://domain/governance",
        evidence_refs=("EVR-M0-DOC-126",),
        residual_refs=("HISTORICAL_MCLT_NOT_PROVEN",),
        blocking_residual_refs=(),
        trace_ref="trace://slge/e0/attempt-1",
        backward_proof_ref="proof://backward/slge-m0",
        forward_readiness_ref="proof://forward/slge-p0",
        triangle_coherence_ref="proof://triangle/slge",
        legacy_baseline_ref="baseline://doc-126",
        source_is_legacy=True,
        identity_preserved=True,
        origin_preserved=True,
        domain_scope_valid=True,
        temporal_policy_valid=True,
        source_state_admissible=True,
        transition_contract_valid=True,
        preconditions_satisfied=True,
        evidence_adequate=True,
        gate_approved=True,
        rank_authority_bounded=True,
        residual_policy_satisfied=True,
        trace_reconstructible=True,
        backward_proof_valid=True,
        forward_readiness_valid=True,
        triangle_coherence_valid=True,
    )


def _baseline(
    *,
    remap_decision: LegacyRemapDecision = LegacyRemapDecision.KEEP,
    status: HistoricalTransitionStatus = HistoricalTransitionStatus.UNKNOWN,
    historical_mclt_ref: str | None = None,
    uncertain_mapping: bool = False,
) -> LegacyBaselineAnchor:
    return LegacyBaselineAnchor(
        baseline_id="BASELINE-DOC-126",
        artifact_id="DOC-126",
        lineage_ref="lineage://legacy/doc-126",
        remap_record_id="REMAP-DOC-126",
        remap_decision=remap_decision,
        historical_transition_status=status,
        historical_mclt_ref=historical_mclt_ref,
        unresolved_residual_refs=("HISTORICAL_MCLT_NOT_PROVEN",),
        uncertain_legacy_slot_mapping=uncertain_mapping,
        trace_ref="trace://slge/m0/remap-doc-126",
    )


def test_slge_e0_registry_validates_against_schema() -> None:
    _declare("schema surface validation")
    schema = _load_json(_SCHEMAS / "slge_sdlc_e0_runtime.schema.json")
    payload = _load_json(_REGISTRY / "slge_sdlc_e0_runtime.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda e: list(e.path))
    assert not errors, [e.message for e in errors]


def test_slge_e0_semantic_contract_integrity_passes() -> None:
    _declare("semantic contract integrity")
    inputs = projector.load_governance_inputs(_REPO_ROOT)
    projector._validate_semantics(_REPO_ROOT, inputs)


def test_non_proven_legacy_history_never_gains_historical_mclt_ref() -> None:
    _declare("historical-mclt no-fabrication boundary")
    decision = evaluate_transition_attempt(
        _base_attempt(),
        legacy_baseline=_baseline(historical_mclt_ref="MCLT-FAKE-1"),
    )
    assert SLGEE0FailureCode.HISTORICAL_MCLT_FABRICATION_FORBIDDEN in decision.failure_codes
    assert decision.state is SLGEE0DecisionState.REFUSED


def test_successful_current_transition_does_not_promote_historical_proof() -> None:
    _declare("runtime admission is not historical certification")
    decision = evaluate_transition_attempt(_base_attempt(), legacy_baseline=_baseline())
    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.historical_status_preserved is True
    assert decision.rank_promotion_granted is False


def test_rebuild_requires_new_lineage() -> None:
    _declare("rebuild lineage boundary")
    attempt = replace(_base_attempt(), new_lineage_ref=None)
    decision = evaluate_transition_attempt(
        attempt,
        legacy_baseline=_baseline(remap_decision=LegacyRemapDecision.REBUILD),
    )
    assert SLGEE0FailureCode.REBUILD_REQUIRES_NEW_LINEAGE in decision.failure_codes
    assert decision.state is SLGEE0DecisionState.REFUSED


def test_quarantine_blocks_normal_progression() -> None:
    _declare("quarantine suspension boundary")
    decision = evaluate_transition_attempt(
        _base_attempt(),
        legacy_baseline=_baseline(remap_decision=LegacyRemapDecision.QUARANTINE),
    )
    assert SLGEE0FailureCode.QUARANTINED_SOURCE in decision.failure_codes
    assert decision.state is SLGEE0DecisionState.SUSPENDED


def test_blocking_residual_refuses() -> None:
    _declare("blocking residual refusal")
    attempt = replace(_base_attempt(), blocking_residual_refs=("LEGACY_HISTORY_INCOMPLETE",))
    decision = evaluate_transition_attempt(attempt, legacy_baseline=_baseline())
    assert SLGEE0FailureCode.BLOCKING_RESIDUAL in decision.failure_codes
    assert decision.state is SLGEE0DecisionState.REFUSED


def test_consumed_residual_is_not_auto_resolved() -> None:
    _declare("residual consumption-not-resolution")
    attempt = replace(
        _base_attempt(),
        residual_refs=("HISTORICAL_MCLT_NOT_PROVEN", "LEGACY_TRACE_INCOMPLETE"),
        blocking_residual_refs=(),
    )
    decision = evaluate_transition_attempt(attempt, legacy_baseline=_baseline())
    assert decision.state is SLGEE0DecisionState.APPROVED
    assert "HISTORICAL_MCLT_NOT_PROVEN" in decision.consumed_residual_refs
    assert "HISTORICAL_MCLT_NOT_PROVEN" in decision.inherited_residual_refs


def test_missing_evidence_or_trace_refuses() -> None:
    _declare("missing evidence/trace refusal")
    attempt = replace(
        _base_attempt(),
        evidence_adequate=False,
        trace_reconstructible=False,
    )
    decision = evaluate_transition_attempt(attempt, legacy_baseline=_baseline())
    assert SLGEE0FailureCode.EVIDENCE_INSUFFICIENT in decision.failure_codes
    assert SLGEE0FailureCode.TRACE_LOSS in decision.failure_codes
    assert decision.state is SLGEE0DecisionState.REFUSED


def test_forbidden_slot_jump_refuses() -> None:
    _declare("forbidden slot jump refusal")
    attempt = replace(_base_attempt(), to_slot_ref="SLGE-SDLC-P0")
    decision = evaluate_transition_attempt(attempt, legacy_baseline=_baseline())
    assert SLGEE0FailureCode.TRANSITION_NOT_LICENSED in decision.failure_codes
    assert decision.state is SLGEE0DecisionState.REFUSED


def test_rank_elevation_skip_refuses() -> None:
    _declare("rank skip refusal")
    attempt = replace(
        _base_attempt(),
        rank_promotion_requested=True,
        rank_promotion_authorized=False,
        forbidden_skip_detected=True,
    )
    decision = evaluate_transition_attempt(attempt, legacy_baseline=_baseline())
    assert SLGEE0FailureCode.RANK_AUTHORITY_EXCEEDED in decision.failure_codes
    assert decision.state is SLGEE0DecisionState.REFUSED


def test_valid_post_cut_mclt_approves() -> None:
    _declare("valid post-cut mclt approval")
    decision = evaluate_transition_attempt(_base_attempt(), legacy_baseline=_baseline())
    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.next_openings == ("SLGE-SDLC-P0",)


def test_valid_legacy_baseline_opens_post_cut_transition_preserving_uncertainty() -> None:
    _declare("legacy baseline preserves historical uncertainty")
    baseline = _baseline(
        status=HistoricalTransitionStatus.PARTIAL,
        historical_mclt_ref=None,
        uncertain_mapping=False,
    )
    decision = evaluate_transition_attempt(_base_attempt(), legacy_baseline=baseline)
    assert decision.state is SLGEE0DecisionState.APPROVED
    assert decision.historical_status_preserved is True


def test_deterministic_input_produces_deterministic_decision() -> None:
    _declare("deterministic decision")
    attempt = _base_attempt()
    baseline = _baseline()
    first = evaluate_transition_attempt(attempt, legacy_baseline=baseline)
    second = evaluate_transition_attempt(
        copy.deepcopy(attempt),
        legacy_baseline=copy.deepcopy(baseline),
    )
    assert first == second


def test_branch_and_chain_state_reflect_e0_to_p0_opening() -> None:
    _declare("chain opening boundary")
    branches = _load_json(_REGISTRY / "branches.json")["branch_statuses"]
    runtime_map = _load_json(_REGISTRY / "runtime_map.json")["runtime_map"]
    residuals = _load_json(_REGISTRY / "residuals.json")["residuals"]
    chain = (_DOCS / "14_PR_CHAIN_ROADMAP.md").read_text(encoding="utf-8")

    e0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-E0")
    p0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-P0")
    g0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-G0")
    c0 = next(item for item in branches if item["branch_id"] == "SLGE-SDLC-C0")
    e0_runtime = next(item for item in runtime_map if item["branch_id"] == "SLGE-SDLC-E0")
    e0_pending = next(
        item for item in residuals if item["residual_id"] == "SLGE_E0_ENGINE_RUNTIME_PENDING"
    )

    assert e0["constitutional_status"] == "RATIFIED"
    assert e0["runtime_status"] == "EXECUTABLE"
    assert e0["evidence_status"] == "PROVEN"
    assert e0_runtime["runtime_status"] == "EXECUTABLE"

    assert p0["runtime_status"] == "EXECUTABLE"
    assert g0["runtime_status"] == "ABSENT"
    assert c0["runtime_status"] == "ABSENT"

    assert e0_pending["disposition"] == "CLOSED"
    assert "Amendment-105 (SLGE-SDLC-E0 — Lifecycle Execution Engine Runtime)" in chain
    assert "Immediate successor after `SLGE-SDLC-E0` is" in chain
    assert "`SLGE-SDLC-P0` only." in chain
