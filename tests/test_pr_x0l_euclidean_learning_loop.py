"""Constitutional tests for PR-X0L Euclidean learning-loop runtime.

Origin law          : docs/14 PR-X0L (Euclidean Learning Loop over X0R)
Branch name         : PR-X0L Euclidean Learning Loop
Constitutional chain: docs/14 -> PR-X0L -> learn/refine/promote
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib
import re

from taaqqul_slot_geometry.core import FailureCode
from taaqqul_slot_geometry.x0r import (
    EuclideanLearningEvidence,
    EuclideanLearningState,
    EuclideanTransitionContract,
    MinimalCompleteRequirement,
    learn_failure,
    learn_success,
    promote_rank_if_evidence_sufficient,
    refine_contract,
)

ORIGIN_LAW = "docs/14 PR-X0L (Euclidean Learning Loop over X0R)"
BRANCH_NAME = "PR-X0L Euclidean Learning Loop"
CONSTITUTIONAL_CHAIN = ("docs/14", "PR-X0L", "learn/refine/promote")
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"


def _contract(
    *,
    rank: int = 3,
    residuals: tuple[str, ...] = ("visible:deferred",),
    condition: bool = True,
    preventer: bool = False,
) -> EuclideanTransitionContract:
    return EuclideanTransitionContract(
        origin="asl/base_rule",
        branch="far/derived_case",
        preserved_identity=True,
        common_illah="shared causal bridge",
        effective_description="effective operational descriptor",
        qadih_difference=True,
        condition=condition,
        sabab=True,
        preventer=preventer,
        residuals=residuals,
        rank=rank,
        minimal_complete_requirement=MinimalCompleteRequirement(
            current_stage_rank=4,
            max_required_stage_rank=3,
            requested_state="candidate",
            candidate_or_deferred_sufficient=True,
            missing_requirements=(),
            rank_ceiling=4,
        ),
        handoff="handoff://x0l/euclidean",
        origin_to_branch_linked=True,
        branch_to_origin_linked=True,
    )


def _evidence(ref: str, *, rank_hint: int | None = None) -> EuclideanLearningEvidence:
    return EuclideanLearningEvidence(
        evidence_ref=ref,
        source="evidence://x0l/runtime",
        observations=("visible learning observation",),
        rank_hint=rank_hint,
    )


def test_declares_identity_fields_for_pr_x0l_surface() -> None:
    assert ORIGIN_LAW
    assert BRANCH_NAME
    assert CONSTITUTIONAL_CHAIN


def test_learn_success_records_visible_evidence_without_verdict_leak() -> None:
    result = learn_success(
        _contract(),
        _evidence("evidence://x0l/success/1"),
        trace_ref="trace://x0l/learn-success/1",
    )

    assert result.state is EuclideanLearningState.SUCCESS_RECORDED
    assert result.failure_code is None
    assert result.evidence_refs == ("evidence://x0l/success/1",)
    assert "learning:success:evidence:evidence://x0l/success/1" in result.residuals
    assert not hasattr(result, "reasonableness_verdict")
    assert not hasattr(result, "truth")


def test_learn_failure_records_blocking_residual_and_named_failure() -> None:
    result = learn_failure(
        _contract(),
        _evidence("evidence://x0l/failure/1"),
        failure_note="conflict with preserved identity",
        trace_ref="trace://x0l/learn-failure/1",
    )

    assert result.state is EuclideanLearningState.FAILURE_RECORDED
    assert result.failure_code is not None
    assert "blocking:learning:failure:conflict with preserved identity" in result.residuals


def test_refine_contract_updates_description_and_keeps_evidence_visible() -> None:
    result = refine_contract(
        _contract(),
        (_evidence("evidence://x0l/refine/1"), _evidence("evidence://x0l/refine/2")),
        refinement_note="tighten effective descriptor",
        trace_ref="trace://x0l/refine/1",
    )

    assert result.state is EuclideanLearningState.CONTRACT_REFINED
    assert result.failure_code is None
    assert result.evidence_refs == ("evidence://x0l/refine/1", "evidence://x0l/refine/2")
    assert "refine:tighten effective descriptor" in result.contract.effective_description
    assert "learning:refine:evidence:evidence://x0l/refine/1" in result.residuals


def test_rank_promotion_requires_sufficient_visible_evidence() -> None:
    result = promote_rank_if_evidence_sufficient(
        _contract(rank=3),
        (_evidence("evidence://x0l/promote/1", rank_hint=4),),
        trace_ref="trace://x0l/promote/insufficient",
    )

    assert result.state is EuclideanLearningState.REFUSED
    assert result.failure_code is FailureCode.RANK_PROMOTION_WITHOUT_GATE


def test_rank_promotion_succeeds_with_sufficient_evidence_and_gate_safe_contract() -> None:
    result = promote_rank_if_evidence_sufficient(
        _contract(rank=3),
        (
            _evidence("evidence://x0l/promote/1", rank_hint=4),
            _evidence("evidence://x0l/promote/2", rank_hint=4),
        ),
        trace_ref="trace://x0l/promote/success",
    )

    assert result.state is EuclideanLearningState.RANK_PROMOTED
    assert result.failure_code is None
    assert result.contract.rank == 4
    assert "learning:promotion:rank:4" in result.residuals


def test_rank_promotion_refuses_when_contract_gate_is_not_satisfied() -> None:
    result = promote_rank_if_evidence_sufficient(
        _contract(rank=3, condition=False),
        (
            _evidence("evidence://x0l/promote/refused/1", rank_hint=4),
            _evidence("evidence://x0l/promote/refused/2", rank_hint=4),
        ),
        trace_ref="trace://x0l/promote/refused",
    )

    assert result.state is EuclideanLearningState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED


def test_pr_x0l_is_marked_done_in_chain_table_and_claude_staging() -> None:
    doc_14 = _DOC_14.read_text(encoding="utf-8")
    claude_md = _CLAUDE_MD.read_text(encoding="utf-8")

    done_pattern = re.compile(r"PR-X0L\s+Euclidean Learning Loop over X0R Contract\s+✓ done")

    assert done_pattern.search(doc_14) is not None
    assert done_pattern.search(claude_md) is not None
