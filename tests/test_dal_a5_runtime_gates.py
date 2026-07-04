"""Constitutional/runtime tests for DAL-A5 syllable/transition/adjacency gates.

Origin law     : docs/58 (DalAlone Atomic Closure Law) + docs/14 DAL-A5 position
Branch         : DAL-A5 runtime (syllable/transition/adjacency/S1-S5 only)
Category       : Category 2 — contract/surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight.dal_a4_runtime_gates import (
    HamzaSurfaceForm,
    evaluate_hamza_resolution_gate,
)
from taaqqul_slot_geometry.weight.dal_a5_runtime_gates import (
    DAL_A5_FORBIDDEN_OUTPUTS,
    DAL_A5_RESIDUAL_VOCABULARY,
    DAL_A5_RUNTIME_VERDICT,
    DalA5AdjacencyVerdict,
    DalA5RuntimeStatus,
    DalA5SyllableInput,
    DalA5SyllableShape,
    DalA5TransitionKind,
    prove_dal_a5_runtime_gates,
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
)
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"
_DAL_A5_MODULE = _REPO_ROOT / "src" / "taaqqul_slot_geometry" / "weight" / "dal_a5_runtime_gates.py"


def _declare(branch_name: str, produced_outputs: frozenset[str]) -> None:
    case = ConstitutionalTestCase(
        origin_law=_ORIGIN,
        branch_name=branch_name,
        constitutional_chain=_CHAIN,
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=DAL_A5_FORBIDDEN_OUTPUTS,
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


def _upstream(trace_ref: str = "trace://dal-a4/hamza/upstream"):
    return evaluate_hamza_resolution_gate(
        input_ref="dal-a4://hamza/input",
        identity="hamza-id",
        hamza_form=HamzaSurfaceForm.HAMZAT_QAT,
        trace_ref=trace_ref,
    )


def test_chain_records_dal_a5_runtime_current_and_dal_a5_admit_done() -> None:
    _declare("chain registration for dal-a5 runtime", frozenset())
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert re.search(r"DAL-A5-ADMIT\s+admission boundary after DAL-A4 runtime\s+✓ done", roadmap)
    assert re.search(
        r"DAL-A5\s+Syllable / transition / adjacency / S1-S5 gates\s+→ current",
        roadmap,
    )
    assert re.search(r"DAL-A6\s+Detailed waqf / wasl closure\s+planned", roadmap)
    assert re.search(r"DAL-A5-ADMIT\s+admission boundary after DAL-A4 runtime\s+✓ done", claude)
    assert re.search(
        r"DAL-A5\s+Syllable / transition / adjacency / S1-S5 gates\s+→ current",
        claude,
    )


def test_dal_a5_runtime_requires_dal_a4_runtime_trace() -> None:
    _declare("missing upstream dal-a4 trace refusal", frozenset())
    raw_upstream = _upstream()
    runtime_input = DalA5SyllableInput(
        upstream_result=raw_upstream,
        unit_ref="dal-a5://unit/trace-missing",
        upstream_trace_ref=" ",
        local_trace_ref="trace://dal-a5/trace-missing",
    )

    verdict = prove_dal_a5_runtime_gates(
        runtime_input=runtime_input,
        syllable_shape=DalA5SyllableShape.S1,
        transition_kind=DalA5TransitionKind.OPEN_TO_CLOSED,
        adjacency_ok=True,
    )

    assert verdict.status is DalA5RuntimeStatus.REFUSED
    assert verdict.failure_code is FailureCode.TRACE_MISSING
    assert "MISSING_DAL_A4_RUNTIME_TRACE" in verdict.residuals


def test_dal_a5_accepts_only_dal_a4_closed_surface() -> None:
    _declare("accepts only dal-a4 runtime output", frozenset({"DalA5SyllableCandidate"}))
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=_upstream(),
        syllable_shape=DalA5SyllableShape.S2,
        transition_kind=DalA5TransitionKind.CLOSED_TO_OPEN,
        adjacency_ok=True,
    )

    assert verdict.failure_code is None
    assert verdict.candidate is not None
    assert verdict.candidate.upstream_trace_ref.startswith("trace://dal-a4/")


def test_dal_a5_classifies_syllable_shape_without_word_or_meaning() -> None:
    _declare("syllable classification only", frozenset({"S1", "S5"}))
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=_upstream(),
        syllable_shape=DalA5SyllableShape.S5,
        transition_kind=DalA5TransitionKind.CLOSED_TO_CLOSED,
        adjacency_ok=True,
    )

    assert verdict.candidate is not None
    assert verdict.candidate.syllable_shape is DalA5SyllableShape.S5
    assert not hasattr(verdict.candidate, "word")
    assert not hasattr(verdict.candidate, "root")
    assert not hasattr(verdict.candidate, "meaning")


def test_dal_a5_transition_gate_preserves_trace() -> None:
    _declare("transition preserves upstream trace", frozenset({"TransitionGate"}))
    upstream = _upstream("trace://dal-a4/hamza/transition")
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=upstream,
        syllable_shape=DalA5SyllableShape.S3,
        transition_kind=DalA5TransitionKind.OPEN_TO_OPEN,
        adjacency_ok=True,
    )

    assert verdict.candidate is not None
    assert verdict.upstream_trace_ref == upstream.certificate.trace_ref
    assert verdict.trace_ref.startswith(upstream.certificate.trace_ref)


def test_dal_a5_adjacency_gate_stays_local() -> None:
    _declare("adjacency stays local", frozenset({"AdjacencyGate"}))
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=_upstream(),
        syllable_shape=DalA5SyllableShape.S4,
        transition_kind=DalA5TransitionKind.CLOSED_TO_CLOSED,
        adjacency_ok=False,
    )

    assert verdict.status is DalA5RuntimeStatus.RUNTIME_GATES_CLOSED
    assert verdict.candidate is not None
    assert verdict.candidate.transition.adjacency is DalA5AdjacencyVerdict.ADJACENT_DEFERRED


def test_dal_a5_s1_s5_shapes_are_closed_vocabulary() -> None:
    _declare("closed s1-s5 vocabulary", frozenset({"S1S5VocabularyGate"}))
    assert {shape.value for shape in DalA5SyllableShape} == {"S1", "S2", "S3", "S4", "S5"}


def test_dal_a5_runtime_verdict_has_visible_residuals_and_trace() -> None:
    _declare("verdict has visible residuals/trace", frozenset({"RuntimeVerdictGate"}))
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=_upstream("trace://dal-a4/hamza/visible"),
        syllable_shape=DalA5SyllableShape.S1,
        transition_kind=DalA5TransitionKind.OPEN_TO_CLOSED,
        adjacency_ok=True,
    )

    assert verdict.status is DalA5RuntimeStatus.RUNTIME_GATES_CLOSED
    assert verdict.trace_ref
    assert verdict.upstream_trace_ref
    assert "DAL_A5_LOCAL_RUNTIME_TRACE" in verdict.residuals


def test_negative_even_if_admit_merged_raw_input_cannot_enter_runtime() -> None:
    _declare("raw input bypass forbidden", frozenset())
    runtime_input = DalA5SyllableInput(
        upstream_result=object(),
        unit_ref="dal-a5://unit/raw",
        upstream_trace_ref="trace://not-dal-a4",
        local_trace_ref="trace://dal-a5/raw",
    )
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=runtime_input,
        syllable_shape=DalA5SyllableShape.S1,
        transition_kind=DalA5TransitionKind.OPEN_TO_CLOSED,
        adjacency_ok=True,
    )

    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "RAW_INPUT_FORBIDDEN" in verdict.residuals


@pytest.mark.parametrize("handoff", ("ROOT", "WEIGHT", "ROOT_IDENTITY_GATE"))
def test_negative_even_if_dal_a4_closed_no_word_root_weight_output(handoff: str) -> None:
    _declare("root/weight output forbidden", frozenset())
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=DalA5SyllableInput(
            upstream_result=_upstream(),
            unit_ref="dal-a5://unit/root-weight",
            upstream_trace_ref="trace://dal-a4/hamza/upstream",
            local_trace_ref="trace://dal-a5/root-weight",
            requested_handoff=handoff,
        ),
        syllable_shape=DalA5SyllableShape.S1,
        transition_kind=DalA5TransitionKind.OPEN_TO_CLOSED,
        adjacency_ok=True,
    )

    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "ROOT_WEIGHT_OUTPUT_FORBIDDEN" in verdict.residuals


def test_negative_even_if_syllable_detected_no_lafzi_output() -> None:
    _declare("lafzi output forbidden", frozenset())
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=DalA5SyllableInput(
            upstream_result=_upstream(),
            unit_ref="dal-a5://unit/lafzi",
            upstream_trace_ref="trace://dal-a4/hamza/upstream",
            local_trace_ref="trace://dal-a5/lafzi",
            requested_handoff="LAFZI_B",
        ),
        syllable_shape=DalA5SyllableShape.S3,
        transition_kind=DalA5TransitionKind.CLOSED_TO_CLOSED,
        adjacency_ok=True,
    )

    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "LAFZI_OUTPUT_FORBIDDEN" in verdict.residuals


def test_negative_even_if_adjacency_accepted_cannot_open_dal_a6() -> None:
    _declare("dal-a6 deferred", frozenset())
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=DalA5SyllableInput(
            upstream_result=_upstream(),
            unit_ref="dal-a5://unit/dal-a6",
            upstream_trace_ref="trace://dal-a4/hamza/upstream",
            local_trace_ref="trace://dal-a5/dal-a6",
            requested_handoff="DAL-A6",
        ),
        syllable_shape=DalA5SyllableShape.S2,
        transition_kind=DalA5TransitionKind.CLOSED_TO_OPEN,
        adjacency_ok=True,
    )

    assert verdict.status is DalA5RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert "DAL_A6_WAQF_WASL_REQUIRED" in verdict.residuals


def test_negative_even_if_vocabulary_closed_cannot_open_dal_a7() -> None:
    _declare("dal-a7 deferred", frozenset())
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=DalA5SyllableInput(
            upstream_result=_upstream(),
            unit_ref="dal-a5://unit/dal-a7",
            upstream_trace_ref="trace://dal-a4/hamza/upstream",
            local_trace_ref="trace://dal-a5/dal-a7",
            requested_handoff="DAL-A7",
        ),
        syllable_shape=DalA5SyllableShape.S5,
        transition_kind=DalA5TransitionKind.OPEN_TO_OPEN,
        adjacency_ok=True,
    )

    assert verdict.status is DalA5RuntimeStatus.DEFERRED
    assert verdict.failure_code is FailureCode.BOUNDARY_MISSING
    assert "DAL_A7_USAGE_POLICY_REQUIRED" in verdict.residuals


def test_negative_even_if_ci_green_runtime_not_semantic_hukm_reality_proof() -> None:
    _declare("semantic/hukm/reality not opened", frozenset())
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=DalA5SyllableInput(
            upstream_result=_upstream(),
            unit_ref="dal-a5://unit/semantic",
            upstream_trace_ref="trace://dal-a4/hamza/upstream",
            local_trace_ref="trace://dal-a5/semantic",
            requested_handoff="SEMANTIC",
        ),
        syllable_shape=DalA5SyllableShape.S1,
        transition_kind=DalA5TransitionKind.OPEN_TO_CLOSED,
        adjacency_ok=True,
    )

    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "SEMANTIC_OUTPUT_FORBIDDEN" in verdict.residuals


def test_negative_even_if_transition_valid_no_parser_morphology_syntax_ifadah_output() -> None:
    _declare("parser/morphology/syntax/ifadah forbidden", frozenset())
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=DalA5SyllableInput(
            upstream_result=_upstream(),
            unit_ref="dal-a5://unit/parser",
            upstream_trace_ref="trace://dal-a4/hamza/upstream",
            local_trace_ref="trace://dal-a5/parser",
            requested_handoff="PARSER",
        ),
        syllable_shape=DalA5SyllableShape.S4,
        transition_kind=DalA5TransitionKind.CLOSED_TO_CLOSED,
        adjacency_ok=True,
    )

    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "FORBIDDEN_DOWNSTREAM_RUNTIME" in verdict.residuals


def test_negative_even_if_sukun_madd_residual_present_it_stays_local_visible() -> None:
    _declare("upstream residuals preserved locally", frozenset())
    upstream = evaluate_hamza_resolution_gate(
        input_ref="dal-a4://hamza/unresolved",
        identity="hamza-id",
        hamza_form=HamzaSurfaceForm.UNRESOLVED,
        trace_ref="trace://dal-a4/hamza/unresolved",
    )
    verdict = prove_dal_a5_runtime_gates(
        runtime_input=upstream,
        syllable_shape=DalA5SyllableShape.S2,
        transition_kind=DalA5TransitionKind.OPEN_TO_OPEN,
        adjacency_ok=False,
    )

    assert verdict.candidate is not None
    assert "HAMZA_UNRESOLVED" in verdict.candidate.residuals
    assert "DAL_A5_LOCAL_RUNTIME_TRACE" in verdict.candidate.residuals
    assert "meaning" not in " ".join(verdict.candidate.residuals).lower()


def test_forbidden_neighbor_proof_no_dal_a6_a7_a8_lafzi_parser_semantic_runtime_objects() -> None:
    _declare("forbidden neighbor proof", frozenset())
    text = _DAL_A5_MODULE.read_text(encoding="utf-8")
    for forbidden_object in (
        "class DalA6",
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


def test_dal_a5_runtime_constant_verdict_matches_declared_boundary() -> None:
    _declare("declared runtime verdict", frozenset({"DAL_A5_RUNTIME_VERDICT"}))
    assert DAL_A5_RUNTIME_VERDICT == {
        "status": "RUNTIME_GATES_CLOSED",
        "scope": "SYLLABLE_TRANSITION_ADJACENCY_S1_S5_ONLY",
        "upstream_required": "DAL_A4_RUNTIME_CLOSED",
        "dal_a6_status": "DEFERRED",
        "dal_a7_status": "DEFERRED",
        "dal_a8_status": "DEFERRED",
        "lafzi_b_status": "DEFERRED",
        "semantic_hukm_reality_status": "FORBIDDEN",
    }
    assert "MISSING_DAL_A4_RUNTIME_TRACE" in DAL_A5_RESIDUAL_VOCABULARY
