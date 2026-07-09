"""Runtime tests for Archimedean/Euclidean transition auditing.

Origin law          : docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md
Branch name         : X0R ArchimedeanEuclideanTransitionAudit
Constitutional chain: docs/63 -> X0R-E1 -> X0R-E2 -> Operational transition audit
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
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FIXTURE = _REPO_ROOT / "data" / "constitutional_stress_benchmark_v1.json"


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/63_ARABIC_EUCLIDEAN_LAYER_CONTRACT_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("docs/63", "X0R-E1", "X0R-E2", "OperationalAudit"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("Meaning", "Hukm", "Truth", "Certainty", "Reality"),
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
        assert item.audit.forbidden_outputs_absent
        assert all(output for output in item.audit.forbidden_outputs_absent)
