"""Constitutional/runtime tests for DAL-A6 detailed waqf/wasl closure gates.

Origin law     : docs/58 (DalAlone Atomic Closure Law) + docs/14 DAL-A6 position
Branch         : DAL-A6 runtime (detailed waqf/wasl closure only)
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
    DAL_A6_FORBIDDEN_OUTPUTS,
    DAL_A6_RESIDUAL_VOCABULARY,
    DAL_A6_RUNTIME_VERDICT,
    DalA6RuntimeInput,
    DalA6RuntimeStatus,
    DalA6WaqfClosure,
    DalA6WaslClosure,
    prove_dal_a6_runtime_gates,
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
)
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_DAL_A6_MODULE = (
    _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "dal_a6_runtime_gates.py"
)


def _declare(branch_name: str, produced_outputs: frozenset[str]) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=DAL_A6_FORBIDDEN_OUTPUTS,
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


def _upstream_dal_a5(trace_ref: str = "trace://dal-a4/hamza/upstream"):
    dal_a4 = evaluate_hamza_resolution_gate(
        input_ref="dal-a4://hamza/input",
        identity="hamza-id",
        hamza_form=HamzaSurfaceForm.HAMZAT_QAT,
        trace_ref=trace_ref,
    )
    verdict = prove_dal_a5_runtime_gates(
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
    assert verdict.status is DalA5RuntimeStatus.RUNTIME_GATES_CLOSED
    return verdict


def test_chain_records_dal_a6_admit_done_and_dal_a7_runtime_current() -> None:
    _declare("chain registration for dal-a6 runtime", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(
        r"DAL-A6-ADMIT\s+admission boundary after DAL-A5 runtime\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A6\s+Detailed waqf / wasl closure\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A7\s+Usage / loan / unvocalized / deletion residual gates\s+→ current",
        roadmap,
    )
    assert re.search(
        r"DAL-A6\.1\s+Refusal totality corrective hardening\s+✓ done",
        roadmap,
    )
    assert re.search(
        r"DAL-A6-ADMIT\s+admission boundary after DAL-A5 runtime\s+✓ done",
        claude,
    )
    assert re.search(
        r"DAL-A6\s+Detailed waqf / wasl closure\s+✓ done",
        claude,
    )
    assert re.search(
        r"DAL-A7\s+Usage / loan / unvocalized / deletion residual gates\s+→ current",
        claude,
    )
    assert re.search(
        r"DAL-A6\.1\s+Refusal totality corrective hardening\s+✓ done",
        claude,
    )


def test_dal_a6_runtime_requires_dal_a5_runtime_trace() -> None:
    _declare("missing upstream dal-a5 trace refusal", frozenset())
    runtime_input = DalA6RuntimeInput(
        upstream_result=_upstream_dal_a5(),
        unit_ref="dal-a6://unit/trace-missing",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a6/trace-missing",
    )

    verdict = prove_dal_a6_runtime_gates(
        runtime_input=runtime_input,
        waqf_closure=DalA6WaqfClosure.WAQF_SUKUN,
        wasl_closure=DalA6WaslClosure.WASL_CONTINUE_HARAKA,
    )

    assert verdict.status is DalA6RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.TRACE_MISSING
    assert "MISSING_DAL_A5_RUNTIME_TRACE" in verdict.residuals


def test_dal_a6_accepts_only_dal_a5_runtime_output() -> None:
    _declare("accepts only dal-a5 runtime output", frozenset({"DalA6WaqfWaslCandidate"}))
    verdict = prove_dal_a6_runtime_gates(
        runtime_input=_upstream_dal_a5(),
        waqf_closure=DalA6WaqfClosure.TA_MARBUTA_STOP_HA,
        wasl_closure=DalA6WaslClosure.HAMZAT_WASL_DROP,
    )

    assert verdict.failure_code is None
    assert verdict.candidate is not None
    assert verdict.candidate.upstream_trace_ref.startswith("trace://dal-a5/")


def test_dal_a6_waqf_wasl_closure_stays_non_lexical_non_semantic() -> None:
    _declare("waqf/wasl closure only", frozenset({"WaqfGate", "WaslGate"}))
    verdict = prove_dal_a6_runtime_gates(
        runtime_input=_upstream_dal_a5(),
        waqf_closure=DalA6WaqfClosure.TANWIN_STOP_DROP,
        wasl_closure=DalA6WaslClosure.TANWIN_LINK_CONTINUE,
    )

    assert verdict.candidate is not None
    assert verdict.candidate.waqf_closure is DalA6WaqfClosure.TANWIN_STOP_DROP
    assert verdict.candidate.wasl_closure is DalA6WaslClosure.TANWIN_LINK_CONTINUE
    assert not hasattr(verdict.candidate, "word")
    assert not hasattr(verdict.candidate, "root")
    assert not hasattr(verdict.candidate, "meaning")


def test_dal_a6_runtime_verdict_has_visible_residuals_and_trace() -> None:
    _declare("verdict has visible residuals/trace", frozenset({"RuntimeVerdictGate"}))
    verdict = prove_dal_a6_runtime_gates(
        runtime_input=_upstream_dal_a5(),
        waqf_closure=DalA6WaqfClosure.WAQF_SUKUN,
        wasl_closure=DalA6WaslClosure.WASL_CONTINUE_HARAKA,
    )

    assert verdict.status is DalA6RuntimeStatus.RUNTIME_GATES_CLOSED
    assert verdict.trace_ref
    assert verdict.upstream_trace_ref
    assert "DAL_A6_LOCAL_RUNTIME_TRACE" in verdict.residuals


def test_negative_even_if_admit_merged_raw_input_cannot_enter_runtime() -> None:
    _declare("raw input bypass forbidden", frozenset())
    runtime_input = DalA6RuntimeInput(
        upstream_result=object(),
        unit_ref="dal-a6://unit/raw",
        upstream_trace_ref="trace://not-dal-a5",
        local_trace_ref="trace://dal-a6/raw",
    )
    verdict = prove_dal_a6_runtime_gates(
        runtime_input=runtime_input,
        waqf_closure=DalA6WaqfClosure.WAQF_SUKUN,
        wasl_closure=DalA6WaslClosure.WASL_CONTINUE_HARAKA,
    )

    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "RAW_INPUT_FORBIDDEN" in verdict.residuals


def test_negative_raw_input_with_blank_upstream_trace_returns_refusal_not_schema_error() -> None:
    _declare("raw input blank upstream trace refusal", frozenset())
    runtime_input = DalA6RuntimeInput(
        upstream_result=object(),
        unit_ref="dal-a6://unit/raw-blank-trace",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a6/raw-blank-trace",
    )

    verdict = prove_dal_a6_runtime_gates(
        runtime_input=runtime_input,
        waqf_closure=DalA6WaqfClosure.WAQF_SUKUN,
        wasl_closure=DalA6WaslClosure.WASL_CONTINUE_HARAKA,
    )

    assert verdict.status is DalA6RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert verdict.upstream_trace_ref is None
    assert "RAW_INPUT_FORBIDDEN" in verdict.residuals


def test_negative_dal_a5_not_closed_blank_trace_returns_deferred() -> None:
    _declare("dal-a5 deferred blank upstream trace refusal", frozenset())
    upstream = _upstream_dal_a5()
    not_closed = replace(
        upstream,
        status=DalA5RuntimeStatus.DEFERRED,
        candidate=None,
        residuals=("DAL_A5_RUNTIME_REQUIRED",),
        failure_code=FailureCode.BOUNDARY_MISSING,
    )
    runtime_input = DalA6RuntimeInput(
        upstream_result=not_closed,
        unit_ref="dal-a6://unit/deferred-blank-trace",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a6/deferred-blank-trace",
    )

    verdict = prove_dal_a6_runtime_gates(
        runtime_input=runtime_input,
        waqf_closure=DalA6WaqfClosure.WAQF_SUKUN,
        wasl_closure=DalA6WaslClosure.WASL_CONTINUE_HARAKA,
    )

    assert verdict.status is DalA6RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert verdict.upstream_trace_ref is None
    assert "DAL_A5_RUNTIME_REQUIRED" in verdict.residuals


def test_negative_even_if_dal_a5_closed_cannot_open_dal_a7() -> None:
    _declare("dal-a7 deferred", frozenset())
    verdict = prove_dal_a6_runtime_gates(
        runtime_input=DalA6RuntimeInput(
            upstream_result=_upstream_dal_a5(),
            unit_ref="dal-a6://unit/dal-a7",
            upstream_trace_ref="trace://dal-a5/upstream",
            local_trace_ref="trace://dal-a6/dal-a7",
            requested_handoff="DAL-A7",
        ),
        waqf_closure=DalA6WaqfClosure.WAQF_SUKUN,
        wasl_closure=DalA6WaslClosure.WASL_CONTINUE_HARAKA,
    )

    assert verdict.status is DalA6RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert "DAL_A7_USAGE_POLICY_REQUIRED" in verdict.residuals


@pytest.mark.parametrize("handoff", ("LAFZI_B", "DAL-A8", "PARSER", "SEMANTIC", "HUKM", "LAW-E0"))
def test_negative_dal_a6_blocks_downstream_and_semantic_handoffs(handoff: str) -> None:
    _declare("downstream handoffs forbidden", frozenset())
    verdict = prove_dal_a6_runtime_gates(
        runtime_input=DalA6RuntimeInput(
            upstream_result=_upstream_dal_a5(),
            unit_ref=f"dal-a6://unit/{handoff.lower()}",
            upstream_trace_ref="trace://dal-a5/upstream",
            local_trace_ref=f"trace://dal-a6/{handoff.lower()}",
            requested_handoff=handoff,
        ),
        waqf_closure=DalA6WaqfClosure.WAQF_SUKUN,
        wasl_closure=DalA6WaslClosure.WASL_CONTINUE_HARAKA,
    )

    assert verdict.failure_code in {
        FailureCode.FORBIDDEN_STRAIGHT_LINE,
        FailureCode.BOUNDARY_MISSING,
    }
    assert any(
        residual
        in {
            "LAFZI_OUTPUT_FORBIDDEN",
            "FORBIDDEN_DOWNSTREAM_RUNTIME",
            "SEMANTIC_OUTPUT_FORBIDDEN",
            "HUKM_OUTPUT_FORBIDDEN",
            "GLOBAL_METRIC_ENGINE_FORBIDDEN",
        }
        for residual in verdict.residuals
    )


def test_forbidden_neighbor_proof_no_dal_a7_a8_lafzi_parser_semantic_runtime_objects() -> None:
    _declare("forbidden neighbor proof", frozenset())
    text = _DAL_A6_MODULE.read_text(encoding="utf-8")
    for forbidden_object in (
        "class DalA7",
        "class DalA8",
        "class Lafzi",
        "ParserRuntimeResult",
        "SemanticVerdict",
        "HukmVerdict",
        "RealityVerdict",
        "class GlobalMetricEngine",
    ):
        assert forbidden_object not in text


def test_dal_a6_runtime_constant_verdict_matches_declared_boundary() -> None:
    _declare("declared runtime verdict", frozenset({"DAL_A6_RUNTIME_VERDICT"}))
    assert DAL_A6_RUNTIME_VERDICT == {
        "status": "RUNTIME_GATES_CLOSED",
        "scope": "DETAILED_WAQF_WASL_CLOSURE_ONLY",
        "upstream_required": "DAL_A5_RUNTIME_CLOSED",
        "dal_a7_status": "DEFERRED",
        "dal_a8_status": "DEFERRED",
        "lafzi_b_status": "DEFERRED",
        "semantic_hukm_reality_status": "FORBIDDEN",
        "next_permitted_pr": "DAL-A7 runtime gates only",
    }
    assert "DAL_A5_RUNTIME_REQUIRED" in DAL_A6_RESIDUAL_VOCABULARY
