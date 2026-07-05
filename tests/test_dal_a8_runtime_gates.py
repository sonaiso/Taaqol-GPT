"""Constitutional/runtime tests for DAL-A8 integration gates.

Origin law     : docs/58 (DalAlone Atomic Closure Law) + docs/14 DAL-A8 position
Branch         : DAL-A8 runtime (DalAloneClosed -> LafziMadlulGate integration only)
Category       : Category 2 — contract/surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re
from dataclasses import replace

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight.dal_a4_runtime_gates import (
    HamzaSurfaceForm,
    evaluate_hamza_resolution_gate,
)
from taaqqul_slot_geometry.weight.dal_a5_runtime_gates import (
    DalA5RuntimeStatus,
    DalA5SyllableInput,
    DalA5SyllableShape,
    DalA5TransitionKind,
    prove_dal_a5_runtime_gates,
)
from taaqqul_slot_geometry.weight.dal_a6_runtime_gates import (
    DalA6RuntimeInput,
    DalA6RuntimeStatus,
    DalA6WaqfClosure,
    DalA6WaslClosure,
    prove_dal_a6_runtime_gates,
)
from taaqqul_slot_geometry.weight.dal_a7_runtime_gates import (
    DalA7DeletionStatus,
    DalA7LoanStatus,
    DalA7RuntimeInput,
    DalA7RuntimeStatus,
    DalA7UnvocalizedStatus,
    DalA7UsageStatus,
    prove_dal_a7_runtime_gates,
)
from taaqqul_slot_geometry.weight.dal_a8_runtime_gates import (
    DAL_A8_FORBIDDEN_OUTPUTS,
    DAL_A8_RESIDUAL_VOCABULARY,
    DAL_A8_RUNTIME_VERDICT,
    DalA8LafziGateState,
    DalA8RuntimeInput,
    DalA8RuntimeStatus,
    prove_dal_a8_runtime_gates,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_ORIGIN = "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"
_CHAIN = (
    "DalOnlyCandidate",
    "DAL-A1",
    "DAL-A2",
    "DAL-A3",
    "DAL-A4",
    "DAL-A5",
    "DAL-A6",
    "DAL-A7",
    "DAL-A8",
)
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_DAL_A8_MODULE = (
    _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "dal_a8_runtime_gates.py"
)


def _declare(branch_name: str, produced_outputs: frozenset[str]) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=DAL_A8_FORBIDDEN_OUTPUTS,
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


def _upstream_dal_a7(trace_ref: str = "trace://dal-a4/hamza/upstream"):
    dal_a4 = evaluate_hamza_resolution_gate(
        input_ref="dal-a4://hamza/input",
        identity="hamza-id",
        hamza_form=HamzaSurfaceForm.HAMZAT_QAT,
        trace_ref=trace_ref,
    )
    dal_a5 = prove_dal_a5_runtime_gates(
        runtime_input=DalA5SyllableInput(
            upstream_result=dal_a4,
            unit_ref="dal-a5://unit/upstream",
            upstream_trace_ref=trace_ref,
            local_trace_ref="trace://dal-a5/upstream",
        ),
        syllable_shape=DalA5SyllableShape.S2,
        transition_kind=DalA5TransitionKind.CLOSED_TO_OPEN,
        adjacency_ok=True,
    )
    assert dal_a5.status is DalA5RuntimeStatus.RUNTIME_GATES_CLOSED
    dal_a6 = prove_dal_a6_runtime_gates(
        runtime_input=DalA6RuntimeInput(
            upstream_result=dal_a5,
            unit_ref="dal-a6://unit/upstream",
            upstream_trace_ref=dal_a5.trace_ref,
            local_trace_ref="trace://dal-a6/upstream",
        ),
        waqf_closure=DalA6WaqfClosure.WAQF_SUKUN,
        wasl_closure=DalA6WaslClosure.WASL_CONTINUE_HARAKA,
    )
    assert dal_a6.status is DalA6RuntimeStatus.RUNTIME_GATES_CLOSED
    dal_a7 = prove_dal_a7_runtime_gates(
        runtime_input=DalA7RuntimeInput(
            upstream_result=dal_a6,
            unit_ref="dal-a7://unit/upstream",
            upstream_trace_ref=dal_a6.trace_ref,
            local_trace_ref="trace://dal-a7/upstream",
        ),
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )
    assert dal_a7.status is DalA7RuntimeStatus.RUNTIME_GATES_CLOSED
    return dal_a7


def test_chain_records_dal_a7_1_done_and_dal_a8_current() -> None:
    _declare("chain registration for dal-a8 runtime", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(
        r"DAL-A7\s+Usage / loan / unvocalized / deletion residual gates\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A7\.1\s+Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A8\s+DalAloneClosed -> LafziMadlulGate integration\s+→ current",
        roadmap,
    )
    assert re.search(
        r"DAL-A7\s+Usage / loan / unvocalized / deletion residual gates\s+✓ done",
        claude,
    )
    assert re.search(
        r"DAL-A7\.1\s+Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics\s+✓ done",
        claude,
    )
    assert re.search(
        r"DAL-A8\s+DalAloneClosed -> LafziMadlulGate integration\s+→ current",
        claude,
    )


def test_dal_a8_runtime_requires_dal_a7_runtime_trace() -> None:
    _declare("missing upstream dal-a7 trace refusal", frozenset())
    runtime_input = DalA8RuntimeInput(
        upstream_result=_upstream_dal_a7(),
        unit_ref="dal-a8://unit/trace-missing",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a8/trace-missing",
    )

    verdict = prove_dal_a8_runtime_gates(runtime_input=runtime_input)

    assert verdict.status is DalA8RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.TRACE_MISSING
    assert "MISSING_DAL_A7_RUNTIME_TRACE" in verdict.residuals


def test_dal_a8_accepts_only_dal_a7_runtime_output() -> None:
    _declare("accepts only dal-a7 runtime output", frozenset({"DalA8IntegrationCandidate"}))
    verdict = prove_dal_a8_runtime_gates(runtime_input=_upstream_dal_a7())

    assert verdict.failure_code is None
    assert verdict.candidate is not None
    assert verdict.candidate.upstream_trace_ref.startswith("trace://dal-a7/")


def test_dal_a8_opens_lafzi_gate_boundary_without_crossing() -> None:
    _declare("lafzi gate boundary opening only", frozenset({"LafziMadlulGateBoundaryGate"}))
    verdict = prove_dal_a8_runtime_gates(
        runtime_input=DalA8RuntimeInput(
            upstream_result=_upstream_dal_a7(),
            unit_ref="dal-a8://unit/lafzi-boundary",
            upstream_trace_ref="trace://dal-a7/upstream",
            local_trace_ref="trace://dal-a8/lafzi-boundary",
            requested_handoff="LAFZI",
        )
    )

    assert verdict.status is DalA8RuntimeStatus.RUNTIME_GATES_CLOSED
    assert verdict.candidate is not None
    assert verdict.candidate.lafzi_gate_state is DalA8LafziGateState.OPENED_BOUNDARY_ONLY
    assert not hasattr(verdict.candidate, "lafzi_candidate_set")
    assert not hasattr(verdict.candidate, "meaning")


def test_dal_a8_runtime_verdict_has_visible_residuals_and_trace() -> None:
    _declare("verdict has visible residuals/trace", frozenset({"RuntimeVerdictGate"}))
    verdict = prove_dal_a8_runtime_gates(runtime_input=_upstream_dal_a7())

    assert verdict.status is DalA8RuntimeStatus.RUNTIME_GATES_CLOSED
    assert verdict.trace_ref
    assert verdict.upstream_trace_ref
    assert "DAL_A8_LOCAL_RUNTIME_TRACE" in verdict.residuals


def test_negative_even_if_dal_a7_closed_lafzi_b0_runtime_is_deferred() -> None:
    _declare("lafzi-b0 remains law-only deferred", frozenset())
    verdict = prove_dal_a8_runtime_gates(
        runtime_input=DalA8RuntimeInput(
            upstream_result=_upstream_dal_a7(),
            unit_ref="dal-a8://unit/lafzi-b0",
            upstream_trace_ref="trace://dal-a7/upstream",
            local_trace_ref="trace://dal-a8/lafzi-b0",
            requested_handoff="LAFZI-B0",
        )
    )

    assert verdict.status is DalA8RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert "LAFZI_B0_LAW_REQUIRED" in verdict.residuals


def test_negative_even_if_admit_merged_raw_input_cannot_enter_runtime() -> None:
    _declare("raw input bypass forbidden", frozenset())
    runtime_input = DalA8RuntimeInput(
        upstream_result=object(),
        unit_ref="dal-a8://unit/raw",
        upstream_trace_ref="trace://not-dal-a7",
        local_trace_ref="trace://dal-a8/raw",
    )
    verdict = prove_dal_a8_runtime_gates(runtime_input=runtime_input)

    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "RAW_INPUT_FORBIDDEN" in verdict.residuals


def test_negative_raw_input_with_blank_upstream_trace_returns_refusal_not_schema_error() -> None:
    _declare("raw input blank upstream trace refusal", frozenset())
    runtime_input = DalA8RuntimeInput(
        upstream_result=object(),
        unit_ref="dal-a8://unit/raw-blank-trace",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a8/raw-blank-trace",
    )

    verdict = prove_dal_a8_runtime_gates(runtime_input=runtime_input)

    assert verdict.status is DalA8RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert verdict.upstream_trace_ref is None
    assert "RAW_INPUT_FORBIDDEN" in verdict.residuals


def test_negative_dal_a7_not_closed_blank_trace_returns_deferred() -> None:
    _declare("dal-a7 deferred blank upstream trace refusal", frozenset())
    upstream = _upstream_dal_a7()
    not_closed = replace(
        upstream,
        status=DalA7RuntimeStatus.DEFERRED,
        candidate=None,
        residuals=("DAL_A7_RUNTIME_REQUIRED",),
        failure_code=FailureCode.BOUNDARY_MISSING,
    )
    runtime_input = DalA8RuntimeInput(
        upstream_result=not_closed,
        unit_ref="dal-a8://unit/deferred-blank-trace",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a8/deferred-blank-trace",
    )

    verdict = prove_dal_a8_runtime_gates(runtime_input=runtime_input)

    assert verdict.status is DalA8RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert verdict.upstream_trace_ref is None
    assert "DAL_A7_RUNTIME_REQUIRED" in verdict.residuals


@pytest.mark.parametrize(
    "handoff,residual",
    (
        ("PARSER", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("MORPHOLOGY", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("SYNTAX", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("LAFZI_RUNTIME", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("LAFZI_OUTPUT", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("LAFZI_MADLUL", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("LAFZI_OBJECT", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("LAFZI_CANDIDATE_SET", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("LAFZI_B1", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("SEMANTIC", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("IFADAH", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("MAFHUM", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("HUKM", "HUKM_OUTPUT_FORBIDDEN"),
        ("LAW-E0", "GLOBAL_METRIC_ENGINE_FORBIDDEN"),
    ),
)
def test_negative_dal_a8_blocks_direct_downstream_and_semantic_output_handoffs(
    handoff: str, residual: str
) -> None:
    _declare("direct downstream output handoffs forbidden", frozenset())
    verdict = prove_dal_a8_runtime_gates(
        runtime_input=DalA8RuntimeInput(
            upstream_result=_upstream_dal_a7(),
            unit_ref=f"dal-a8://unit/{handoff.lower()}",
            upstream_trace_ref="trace://dal-a7/upstream",
            local_trace_ref=f"trace://dal-a8/{handoff.lower()}",
            requested_handoff=handoff,
        )
    )

    assert verdict.status is DalA8RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert residual in verdict.residuals


def test_forbidden_neighbor_proof_no_lafzi_b_runtime_or_semantic_runtime_objects() -> None:
    _declare("forbidden neighbor proof", frozenset())
    text = _DAL_A8_MODULE.read_text(encoding="utf-8")
    for forbidden_object in (
        "class LafziMadlulCandidateSet",
        "class Wad'iMadlul",
        "ParserRuntimeResult",
        "SemanticVerdict",
        "HukmVerdict",
        "RealityVerdict",
        "class GlobalMetricEngine",
    ):
        assert forbidden_object not in text


def test_dal_a8_runtime_constant_verdict_matches_declared_boundary() -> None:
    _declare("declared runtime verdict", frozenset({"DAL_A8_RUNTIME_VERDICT"}))
    assert DAL_A8_RUNTIME_VERDICT == {
        "status": "RUNTIME_GATES_CLOSED",
        "scope": "DAL_ALONE_CLOSED_TO_LAFZI_GATE_INTEGRATION_ONLY",
        "upstream_required": "DAL_A7_RUNTIME_CLOSED",
        "lafzi_gate_status": "OPENED_BOUNDARY_ONLY",
        "lafzi_candidate_set_status": "NOT_OPENED",
        "semantic_hukm_reality_status": "FORBIDDEN",
        "next_permitted_pr": "LAFZI-B0 law-only only",
    }
    assert "DAL_A7_RUNTIME_REQUIRED" in DAL_A8_RESIDUAL_VOCABULARY
