"""Constitutional/runtime tests for DAL-A7 usage/loan residual gates.

Origin law     : docs/58 (DalAlone Atomic Closure Law) + docs/14 DAL-A7 position
Branch         : DAL-A7 runtime (usage/loan/unvocalized/deletion residual gates only)
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
    DAL_A7_FORBIDDEN_OUTPUTS,
    DAL_A7_RESIDUAL_VOCABULARY,
    DAL_A7_RUNTIME_VERDICT,
    DalA7DeletionStatus,
    DalA7LoanStatus,
    DalA7RuntimeInput,
    DalA7RuntimeStatus,
    DalA7UnvocalizedStatus,
    DalA7UsageStatus,
    prove_dal_a7_runtime_gates,
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
)
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_DAL_A7_MODULE = (
    _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "dal_a7_runtime_gates.py"
)


def _declare(branch_name: str, produced_outputs: frozenset[str]) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=DAL_A7_FORBIDDEN_OUTPUTS,
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


def _upstream_dal_a6(trace_ref: str = "trace://dal-a4/hamza/upstream"):
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
    return dal_a6


def test_chain_records_dal_a7_done_and_dal_a7_1_current() -> None:
    _declare("chain registration for dal-a7 runtime", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(
        r"DAL-A6\s+Detailed waqf / wasl closure\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A7\s+Usage / loan / unvocalized / deletion residual gates\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A7\.1\s+Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics\s+→ current",
        roadmap,
    )
    assert re.search(
        r"DAL-A6\.1\s+Refusal totality corrective hardening\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A6\s+Detailed waqf / wasl closure\s+✓ done",
        claude,
    )
    assert re.search(
        r"DAL-A7\s+Usage / loan / unvocalized / deletion residual gates\s+✓ done",
        claude,
    )
    assert re.search(
        r"DAL-A7\.1\s+Harden DAL-A7 LAFZI/LAFZI-B handoff deferral semantics\s+→ current",
        claude,
    )
    assert re.search(
        r"DAL-A6\.1\s+Refusal totality corrective hardening\s+✓ done",
        claude,
    )


def test_dal_a7_runtime_requires_dal_a6_runtime_trace() -> None:
    _declare("missing upstream dal-a6 trace refusal", frozenset())
    runtime_input = DalA7RuntimeInput(
        upstream_result=_upstream_dal_a6(),
        unit_ref="dal-a7://unit/trace-missing",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a7/trace-missing",
    )

    verdict = prove_dal_a7_runtime_gates(
        runtime_input=runtime_input,
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.status is DalA7RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.TRACE_MISSING
    assert "MISSING_DAL_A6_RUNTIME_TRACE" in verdict.residuals


def test_dal_a7_accepts_only_dal_a6_runtime_output() -> None:
    _declare("accepts only dal-a6 runtime output", frozenset({"DalA7ResidualCandidate"}))
    verdict = prove_dal_a7_runtime_gates(
        runtime_input=_upstream_dal_a6(),
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.LOAN_VISIBLE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.failure_code is None
    assert verdict.candidate is not None
    assert verdict.candidate.upstream_trace_ref.startswith("trace://dal-a6/")


def test_dal_a7_runtime_verdict_has_visible_residuals_and_trace() -> None:
    _declare("verdict has visible residuals/trace", frozenset({"RuntimeVerdictGate"}))
    verdict = prove_dal_a7_runtime_gates(
        runtime_input=_upstream_dal_a6(),
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.status is DalA7RuntimeStatus.RUNTIME_GATES_CLOSED
    assert verdict.trace_ref
    assert verdict.upstream_trace_ref
    assert "DAL_A7_LOCAL_RUNTIME_TRACE" in verdict.residuals


def test_negative_even_if_admit_merged_raw_input_cannot_enter_runtime() -> None:
    _declare("raw input bypass forbidden", frozenset())
    runtime_input = DalA7RuntimeInput(
        upstream_result=object(),
        unit_ref="dal-a7://unit/raw",
        upstream_trace_ref="trace://not-dal-a6",
        local_trace_ref="trace://dal-a7/raw",
    )
    verdict = prove_dal_a7_runtime_gates(
        runtime_input=runtime_input,
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "RAW_INPUT_FORBIDDEN" in verdict.residuals


def test_negative_raw_input_with_blank_upstream_trace_returns_refusal_not_schema_error() -> None:
    _declare("raw input blank upstream trace refusal", frozenset())
    runtime_input = DalA7RuntimeInput(
        upstream_result=object(),
        unit_ref="dal-a7://unit/raw-blank-trace",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a7/raw-blank-trace",
    )

    verdict = prove_dal_a7_runtime_gates(
        runtime_input=runtime_input,
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.status is DalA7RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert verdict.upstream_trace_ref is None
    assert "RAW_INPUT_FORBIDDEN" in verdict.residuals


def test_negative_dal_a6_not_closed_blank_trace_returns_deferred() -> None:
    _declare("dal-a6 deferred blank upstream trace refusal", frozenset())
    upstream = _upstream_dal_a6()
    not_closed = replace(
        upstream,
        status=DalA6RuntimeStatus.DEFERRED,
        candidate=None,
        residuals=("DAL_A6_RUNTIME_REQUIRED",),
        failure_code=FailureCode.BOUNDARY_MISSING,
    )
    runtime_input = DalA7RuntimeInput(
        upstream_result=not_closed,
        unit_ref="dal-a7://unit/deferred-blank-trace",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a7/deferred-blank-trace",
    )

    verdict = prove_dal_a7_runtime_gates(
        runtime_input=runtime_input,
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.status is DalA7RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert verdict.upstream_trace_ref is None
    assert "DAL_A6_RUNTIME_REQUIRED" in verdict.residuals


@pytest.mark.parametrize(
    ("loan_status", "unvocalized_status", "deletion_status", "expected_residual"),
    (
        (
            DalA7LoanStatus.LOAN_REQUIRED,
            DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
            DalA7DeletionStatus.LICENSED,
            "LOAN_PATH_REQUIRED",
        ),
        (
            DalA7LoanStatus.NATIVE,
            DalA7UnvocalizedStatus.CANDIDATE_SET_ONLY,
            DalA7DeletionStatus.LICENSED,
            "UNVOCALIZED_SURFACE",
        ),
        (
            DalA7LoanStatus.NATIVE,
            DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
            DalA7DeletionStatus.UNLICENSED,
            "DELETION_UNLICENSED",
        ),
    ),
)
def test_negative_local_residual_conditions_defer_closure(
    loan_status: DalA7LoanStatus,
    unvocalized_status: DalA7UnvocalizedStatus,
    deletion_status: DalA7DeletionStatus,
    expected_residual: str,
) -> None:
    _declare("local residual policy deferred", frozenset())
    verdict = prove_dal_a7_runtime_gates(
        runtime_input=_upstream_dal_a6(),
        usage_status=DalA7UsageStatus.USED,
        loan_status=loan_status,
        unvocalized_status=unvocalized_status,
        deletion_status=deletion_status,
    )

    assert verdict.status is DalA7RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert expected_residual in verdict.residuals


def test_negative_even_if_dal_a6_closed_cannot_open_dal_a8() -> None:
    _declare("dal-a8 deferred", frozenset())
    verdict = prove_dal_a7_runtime_gates(
        runtime_input=DalA7RuntimeInput(
            upstream_result=_upstream_dal_a6(),
            unit_ref="dal-a7://unit/dal-a8",
            upstream_trace_ref="trace://dal-a6/upstream",
            local_trace_ref="trace://dal-a7/dal-a8",
            requested_handoff="DAL-A8",
        ),
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.status is DalA7RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert "DAL_A8_INTEGRATION_REQUIRED" in verdict.residuals


@pytest.mark.parametrize("handoff", ("LAFZI_B", "LAFZI"))
def test_negative_lafzi_boundary_handoff_is_deferred_until_dal_a8(handoff: str) -> None:
    _declare("lafzi boundary handoff deferred", frozenset())
    verdict = prove_dal_a7_runtime_gates(
        runtime_input=DalA7RuntimeInput(
            upstream_result=_upstream_dal_a6(),
            unit_ref=f"dal-a7://unit/{handoff.lower()}",
            upstream_trace_ref="trace://dal-a6/upstream",
            local_trace_ref=f"trace://dal-a7/{handoff.lower()}",
            requested_handoff=handoff,
        ),
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.status is DalA7RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert "DAL_A8_INTEGRATION_REQUIRED" in verdict.residuals
    assert verdict.trace_ref == f"trace://dal-a7/{handoff.lower()}"
    assert verdict.upstream_trace_ref == "trace://dal-a6/upstream"
    assert verdict.candidate is None


@pytest.mark.parametrize(
    "handoff,residual",
    (
        ("PARSER", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("MORPHOLOGY", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("SYNTAX", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("DAL-A8-RUNTIME", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("LAFZI_RUNTIME", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("LAFZI_OUTPUT", "FORBIDDEN_DOWNSTREAM_RUNTIME"),
        ("SEMANTIC", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("MEANING", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("IFADAH", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("MAFHUM", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("HUKM", "HUKM_OUTPUT_FORBIDDEN"),
        ("TRUTH", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("CERTAINTY", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("REALITY", "SEMANTIC_OUTPUT_FORBIDDEN"),
        ("LAW-E0", "GLOBAL_METRIC_ENGINE_FORBIDDEN"),
    ),
)
def test_negative_dal_a7_blocks_direct_downstream_and_semantic_output_handoffs(
    handoff: str, residual: str
) -> None:
    _declare("direct downstream output handoffs forbidden", frozenset())
    verdict = prove_dal_a7_runtime_gates(
        runtime_input=DalA7RuntimeInput(
            upstream_result=_upstream_dal_a6(),
            unit_ref=f"dal-a7://unit/{handoff.lower()}",
            upstream_trace_ref="trace://dal-a6/upstream",
            local_trace_ref=f"trace://dal-a7/{handoff.lower()}",
            requested_handoff=handoff,
        ),
        usage_status=DalA7UsageStatus.USED,
        loan_status=DalA7LoanStatus.NATIVE,
        unvocalized_status=DalA7UnvocalizedStatus.RESOLVED_BY_EVIDENCE,
        deletion_status=DalA7DeletionStatus.LICENSED,
    )

    assert verdict.status is DalA7RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert residual in verdict.residuals


def test_forbidden_neighbor_proof_no_dal_a8_lafzi_parser_semantic_runtime_objects() -> None:
    _declare("forbidden neighbor proof", frozenset())
    text = _DAL_A7_MODULE.read_text(encoding="utf-8")
    for forbidden_object in (
        "class DalA8",
        "class Lafzi",
        "ParserRuntimeResult",
        "SemanticVerdict",
        "HukmVerdict",
        "RealityVerdict",
        "class GlobalMetricEngine",
    ):
        assert forbidden_object not in text


def test_dal_a7_runtime_constant_verdict_matches_declared_boundary() -> None:
    _declare("declared runtime verdict", frozenset({"DAL_A7_RUNTIME_VERDICT"}))
    assert DAL_A7_RUNTIME_VERDICT == {
        "status": "RUNTIME_GATES_CLOSED",
        "scope": "USAGE_LOAN_UNVOCALIZED_DELETION_RESIDUAL_GATES_ONLY",
        "upstream_required": "DAL_A6_RUNTIME_CLOSED",
        "dal_a8_status": "DEFERRED",
        "lafzi_b_status": "DEFERRED",
        "semantic_hukm_reality_status": "FORBIDDEN",
        "next_permitted_pr": "DAL-A8 integration gates only",
    }
    for residual in ("LOAN_PATH_REQUIRED", "UNVOCALIZED_SURFACE", "DELETION_UNLICENSED"):
        assert residual in DAL_A7_RESIDUAL_VOCABULARY
