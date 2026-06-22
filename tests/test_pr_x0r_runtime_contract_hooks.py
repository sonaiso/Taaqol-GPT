"""Constitutional tests for PR-X0R runtime contract hooks.

Origin law          : docs/14 Amendment-32 (PR-X0R)
Branch name         : PR-X0R Runtime Contract Hooks
Constitutional chain: docs/14 -> Amendment-32 -> Runtime contract hooks
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

from taaqqul_slot_geometry.core import FailureCode
from taaqqul_slot_geometry.x0r import (
    JumpTestInput,
    ResidualKind,
    TransitionContract,
)

ORIGIN_LAW = "docs/14 Amendment-32 (PR-X0R — Runtime Contract Hooks)"
BRANCH_NAME = "PR-X0R Runtime Contract Hooks"
CONSTITUTIONAL_CHAIN = ("docs/14", "Amendment-32", "Runtime contract hooks")
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"


def _contract() -> TransitionContract:
    return TransitionContract(
        declared_transitions=frozenset(
            {
                ("CellSequence", "BuiltPath", "CELL_TO_BUILT_PATH", "text_understanding"),
                (
                    "CellSequence",
                    "RootWeightPath",
                    "CELL_TO_ROOT_WEIGHT_PATH",
                    "text_understanding",
                ),
            }
        )
    )


def _valid_jump() -> JumpTestInput:
    return JumpTestInput(
        source_level="CellSequence",
        target_level="BuiltPath",
        transition_name="CELL_TO_BUILT_PATH",
        domain="text_understanding",
        trace_ref="trace://x0r/001",
        sufficiency=True,
        necessity=True,
        preserved_trace=True,
        qadih_difference=True,
        residual_kinds=(ResidualKind.NON_BLOCKING,),
        blocking_residuals=(),
    )


def test_declares_identity_fields_for_pr_x0r_surface() -> None:
    assert ORIGIN_LAW
    assert BRANCH_NAME
    assert CONSTITUTIONAL_CHAIN


def test_default_unsupported_transition_is_forbidden_straight_line() -> None:
    verdict = _contract().evaluate(
        JumpTestInput(
            source_level="Silence",
            target_level="Motion",
            transition_name="UNDECLARED_DIRECT_MOVE",
            domain="text_understanding",
            trace_ref="trace://x0r/002",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )
    )
    assert verdict.allowed is False
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_blocking_or_contradictory_residuals_refuse_transition() -> None:
    contract = _contract()

    blocking = contract.evaluate(
        JumpTestInput(
            source_level="CellSequence",
            target_level="BuiltPath",
            transition_name="CELL_TO_BUILT_PATH",
            domain="text_understanding",
            trace_ref="trace://x0r/003",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.BLOCKING,),
            blocking_residuals=(),
        )
    )
    contradictory = contract.evaluate(
        JumpTestInput(
            source_level="CellSequence",
            target_level="BuiltPath",
            transition_name="CELL_TO_BUILT_PATH",
            domain="text_understanding",
            trace_ref="trace://x0r/004",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.CONTRADICTORY,),
            blocking_residuals=(),
        )
    )

    assert blocking.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT
    assert contradictory.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


def test_five_jump_axes_are_required_for_approval() -> None:
    verdict = _contract().evaluate(
        JumpTestInput(
            source_level="CellSequence",
            target_level="BuiltPath",
            transition_name="CELL_TO_BUILT_PATH",
            domain="text_understanding",
            trace_ref="trace://x0r/005",
            sufficiency=False,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )
    )
    assert verdict.allowed is False
    assert verdict.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE


def test_domain_and_trace_are_not_optional() -> None:
    contract = _contract()
    missing_domain = contract.evaluate(
        JumpTestInput(
            source_level="CellSequence",
            target_level="BuiltPath",
            transition_name="CELL_TO_BUILT_PATH",
            domain="",
            trace_ref="trace://x0r/006",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )
    )
    missing_trace = contract.evaluate(
        JumpTestInput(
            source_level="CellSequence",
            target_level="BuiltPath",
            transition_name="CELL_TO_BUILT_PATH",
            domain="text_understanding",
            trace_ref="",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )
    )
    assert missing_domain.failure_code is FailureCode.DOMAIN_MISSING
    assert missing_trace.failure_code is FailureCode.TRACE_MISSING


def test_path_matrix_allows_multiple_declared_paths_after_cellsequence() -> None:
    contract = _contract()
    built_path = contract.evaluate(_valid_jump())
    root_weight_path = contract.evaluate(
        JumpTestInput(
            source_level="CellSequence",
            target_level="RootWeightPath",
            transition_name="CELL_TO_ROOT_WEIGHT_PATH",
            domain="text_understanding",
            trace_ref="trace://x0r/007",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=(),
        )
    )
    assert built_path.allowed is True
    assert root_weight_path.allowed is True


def test_no_silent_success_or_failure_result_surface() -> None:
    contract = _contract()
    approved = contract.evaluate(_valid_jump())
    refused = contract.evaluate(
        JumpTestInput(
            source_level="CellSequence",
            target_level="BuiltPath",
            transition_name="CELL_TO_BUILT_PATH",
            domain="text_understanding",
            trace_ref="trace://x0r/008",
            sufficiency=True,
            necessity=True,
            preserved_trace=True,
            qadih_difference=True,
            residual_kinds=(ResidualKind.NON_BLOCKING,),
            blocking_residuals=("incomplete evidence",),
        )
    )
    assert approved.trace_ref.startswith("trace://")
    assert approved.residual_kinds
    assert approved.failure_code is None

    assert refused.trace_ref.startswith("trace://")
    assert refused.failure_code is not None
    assert refused.blocking_residuals


def test_surface_stays_generic_without_linguistic_runtime_functions() -> None:
    module_dict = __import__(
        "taaqqul_slot_geometry.x0r.transition_contract", fromlist=["dummy"]
    ).__dict__
    for forbidden_name in (
        "parse_arabic",
        "detect_root",
        "detect_weight",
        "infer_meaning",
        "classify_particle",
    ):
        assert forbidden_name not in module_dict


def test_pr_x0r_is_marked_done_in_chain_table_and_claude_staging() -> None:
    doc_14 = _DOC_14.read_text(encoding="utf-8")
    claude_md = _CLAUDE_MD.read_text(encoding="utf-8")

    done_pattern = re.compile(r"PR-X0R\s+Runtime Contract Hooks\s+✓ done")

    assert done_pattern.search(doc_14) is not None
    assert done_pattern.search(claude_md) is not None
