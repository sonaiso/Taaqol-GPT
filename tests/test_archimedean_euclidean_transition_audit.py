"""Runtime tests for Archimedean/Euclidean transition auditing.

Origin law          : docs/11 + docs/13 + docs/63 + docs/80
Branch name         : X0R ArchimedeanEuclideanTransitionAudit
Constitutional chain: docs/11 -> docs/13 -> docs/63 -> docs/80 -> Operational audit
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.core import FailureCode
from taaqqul_slot_geometry.x0r import (
    ArchimedeanStatus,
    ConstitutionalStressBenchmarkRunner,
    EuclideanStatus,
    StressCaseStatus,
    audit_transition,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FIXTURE = _REPO_ROOT / "data" / "constitutional_stress_benchmark_v1.json"


def _declare(branch_name: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md + "
            "docs/13_CONSTITUTIONAL_PR_GEOMETRY.md + "
            "docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md + "
            "docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md"
        ),
        branch_name=branch_name,
        constitutional_chain=("docs/11", "docs/13", "docs/63", "docs/80", "OperationalAudit"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("Meaning", "Hukm", "Truth", "Certainty", "Reality"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
        chain_position="X0R-E2 operational audit hardening",
        origin_law_ref="docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md#x0r-runtime-contract",
        branch_of_origin="X0R ArchimedeanEuclideanTransitionAudit",
        forbidden_shortcut_assertions=(
            "SurfaceText -> Truth",
            "Evidence -> Certainty",
            "Signifier -> Meaning",
        ),
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


def test_surface_text_to_truth_is_non_decomposable_blocked_jump() -> None:
    _declare("surface-text truth leap rejection")
    verdict = audit_transition(
        origin="SurfaceText",
        target="Truth",
        domain="arabic_surface",
        trace_ref="trace://audit/surface-truth/1",
        provided_steps=(),
        required_units=(
            "DIACRITIZATION_CANDIDATE",
            "SENSE_DISAMBIGUATION_CANDIDATE",
            "RELATION_CANDIDATE",
            "IFADAH_CANDIDATE",
            "EXTERNAL_EVIDENCE_BUNDLE",
        ),
        provided_gates=(),
        required_gates=("ARCHIMEDEAN_EUCLIDEAN_GATE",),
        provided_evidence=(),
        required_evidence=("EXTERNAL_EVIDENCE_BUNDLE",),
        forbidden_outputs=("Meaning", "Hukm", "Truth", "Certainty", "Reality"),
        produced_outputs=(),
        trace_replay_available=False,
        trace_snapshot_only=False,
    )

    assert verdict.archimedean_status is ArchimedeanStatus.FAIL_NON_DECOMPOSABLE
    assert verdict.euclidean_status is EuclideanStatus.FAIL_UNCONSTRUCTED_STEP
    assert verdict.final_status is StressCaseStatus.BLOCKED
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert verdict.missing_units == (
        "DIACRITIZATION_CANDIDATE",
        "SENSE_DISAMBIGUATION_CANDIDATE",
        "RELATION_CANDIDATE",
        "IFADAH_CANDIDATE",
        "EXTERNAL_EVIDENCE_BUNDLE",
    )
    assert verdict.forbidden_outputs_absent == ("Meaning", "Hukm", "Truth", "Certainty", "Reality")
    assert verdict.forbidden_output_violations == ()
    assert verdict.no_forbidden_outputs_produced is True


def test_truth_target_blocked_even_with_all_units_gates_and_evidence() -> None:
    _declare("surface-text truth leap rejection with complete prerequisites")
    verdict = audit_transition(
        origin="SurfaceText",
        target="Truth",
        domain="arabic_surface",
        trace_ref="trace://audit/surface-truth/all-present",
        provided_steps=("DIACRITIZATION_CANDIDATE", "IFADAH_CANDIDATE"),
        required_units=("DIACRITIZATION_CANDIDATE", "IFADAH_CANDIDATE"),
        provided_gates=("ARCHIMEDEAN_EUCLIDEAN_GATE",),
        required_gates=("ARCHIMEDEAN_EUCLIDEAN_GATE",),
        provided_evidence=("EXTERNAL_EVIDENCE_BUNDLE",),
        required_evidence=("EXTERNAL_EVIDENCE_BUNDLE",),
        forbidden_outputs=("Meaning", "Hukm", "Truth", "Certainty", "Reality"),
        produced_outputs=(),
        requested_rank=2,
        evidence_rank=2,
        trace_replay_available=True,
        trace_snapshot_only=False,
    )

    assert verdict.final_status is StressCaseStatus.BLOCKED
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert verdict.archimedean_status is ArchimedeanStatus.FAIL_NON_DECOMPOSABLE
    assert verdict.euclidean_status is EuclideanStatus.FAIL_UNCONSTRUCTED_STEP


def test_forbidden_output_violation_is_detected_and_blocks() -> None:
    _declare("forbidden output leakage detection")
    verdict = audit_transition(
        origin="BenchmarkCase",
        target="SurfaceResolution",
        domain="arabic_surface",
        trace_ref="trace://audit/forbidden-output/1",
        provided_steps=("MULTI_IRAB_CANDIDATE",),
        required_units=("MULTI_IRAB_CANDIDATE",),
        provided_gates=("MULTI_IRAB_GATE",),
        required_gates=("MULTI_IRAB_GATE",),
        provided_evidence=("GRAMMAR_EVIDENCE",),
        required_evidence=("GRAMMAR_EVIDENCE",),
        forbidden_outputs=("Meaning", "Hukm", "Truth"),
        produced_outputs=("Truth",),
        requested_rank=2,
        evidence_rank=2,
        trace_replay_available=True,
        trace_snapshot_only=False,
    )

    assert verdict.forbidden_output_violations == ("Truth",)
    assert verdict.no_forbidden_outputs_produced is False
    assert verdict.final_status is StressCaseStatus.BLOCKED
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_benchmark_runner_executes_fixture_and_matches_expected_statuses() -> None:
    _declare("fixture benchmark execution")
    runner = ConstitutionalStressBenchmarkRunner(_FIXTURE)
    results = runner.run()

    assert len(results) == 6
    assert all(item.matches_expected for item in results)
    assert {item.actual_status for item in results} == {
        StressCaseStatus.LICENSED,
        StressCaseStatus.BLOCKED,
        StressCaseStatus.PENDING,
        StressCaseStatus.EXCEPTIONAL,
        StressCaseStatus.RESIDUAL,
        StressCaseStatus.OUT_OF_SCOPE,
    }


def test_benchmark_runner_preserves_forbidden_output_absence() -> None:
    _declare("forbidden output absence")
    runner = ConstitutionalStressBenchmarkRunner(_FIXTURE)

    for item in runner.run():
        assert item.audit.no_forbidden_outputs_produced is True
        assert item.audit.forbidden_output_violations == ()
        assert item.audit.forbidden_outputs_absent
