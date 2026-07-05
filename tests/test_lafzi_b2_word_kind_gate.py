"""Constitutional tests for LAFZI-B2 WordKindCandidateGate.

Origin law     : docs/59 (Lafzi Madlul Correspondence Law)
Branch         : LAFZI-B2 (WordKindCandidateGate only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import lafzi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lafzi_madlul import (
    LAFZI_B2_ALLOWED_OUTPUT,
    LAFZI_B2_RANK_CEILING,
    LafziMadlulCandidate,
    LafziMadlulCandidateSet,
    LafziMadlulState,
    LafziResidual,
    LafziResidualKind,
    LafziScope,
    MappingState,
    WordKindCandidate,
    WordKindCandidateGateState,
    prove_word_kind_candidate_gate,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"

_FORBIDDEN_B2_OUTPUTS = (
    "LafziMadlulClosed",
    "WadiMadlul",
    "Mutabaqah",
    "Tadammun",
    "Iltizam",
    "Relation",
    "Composition",
    "Ifadah",
    "Mafhum",
    "Hukm",
    "Reality",
)
_ROADMAP_B2_DONE = (
    "LAFZI-B2 WordKindCandidateGate                                            ✓ done"
)
_ROADMAP_B3_CURRENT = (
    "LAFZI-B3 SourceIdentityGate                                               → current"
)


def _declare(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    forbidden_outputs: tuple[str, ...] = _FORBIDDEN_B2_OUTPUTS,
) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/59_LAFZI_MADLUL_CORRESPONDENCE_LAW.md",
        branch_name=branch_name,
        constitutional_chain=(
            "DAL-A8",
            "LAFZI-B0",
            "LAFZI-B1",
            "LAFZI-B2",
            "WordKindCandidateGate",
        ),
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
        produced_outputs=produced_outputs,
    )
    assert_constitutional_case(case, result)


def _scope() -> LafziScope:
    return LafziScope(
        language_scope="AR",
        register_scope="GENERAL",
        usage_scope="USAGE://GENERAL",
        vocalization_scope="FULLY_VOCALIZED",
        loan_or_native_scope="NATIVE",
        trace_ref="trace://lafzi-scope",
    )


def _residual(
    kind: LafziResidualKind = LafziResidualKind.MULTIPLE_LAFZI_CANDIDATES,
    *,
    blocking: bool = False,
) -> LafziResidual:
    return LafziResidual(
        kind=kind,
        trace_ref=f"trace://residual/{kind.value.lower()}",
        message="visible residual",
        blocking=blocking,
    )


def _candidate(trace_ref: str) -> LafziMadlulCandidate:
    return LafziMadlulCandidate(
        dal_alone_closed_ref="trace://dal/closed",
        word_kind_candidate_ref="trace://word-kind",
        source_identity_candidate_ref="trace://source-identity",
        form_state_candidate_ref="trace://form-state",
        internal_word_path_candidate_ref="trace://internal-path",
        lafzi_scope=_scope(),
        residuals=(),
        state=LafziMadlulState.CANDIDATE,
        trace_ref=trace_ref,
        rank=Rank.CANDIDATE,
    )


def test_word_kind_gate_proves_single_candidate_kind_without_closure() -> None:
    _declare(
        "LAFZI-B2 proven word kind",
        produced_outputs=frozenset({LAFZI_B2_ALLOWED_OUTPUT}),
    )

    result = prove_word_kind_candidate_gate(
        LafziMadlulCandidateSet(
            dal_alone_closed_ref="trace://dal/closed",
            mapping_state=MappingState.ONE_TO_ONE,
            candidates=(_candidate("trace://candidate/one"),),
            lafzi_scope=_scope(),
            residuals=(),
            trace_ref="trace://set/one",
        ),
        proposed_word_kind=WordKindCandidate.ISM,
        trace_ref="trace://gate/word-kind/proven",
    )

    assert result.state is WordKindCandidateGateState.PROVEN
    assert result.word_kind is WordKindCandidate.ISM
    assert result.rank is LAFZI_B2_RANK_CEILING
    assert result.output == LAFZI_B2_ALLOWED_OUTPUT
    assert result.residuals == ()


def test_word_kind_gate_defers_ambiguous_or_one_to_many_paths_with_visible_residual() -> None:
    _declare("LAFZI-B2 deferred word kind")

    result = prove_word_kind_candidate_gate(
        LafziMadlulCandidateSet(
            dal_alone_closed_ref="trace://dal/closed",
            mapping_state=MappingState.ONE_TO_MANY,
            candidates=(_candidate("trace://candidate/a"), _candidate("trace://candidate/b")),
            lafzi_scope=_scope(),
            residuals=(_residual(),),
            trace_ref="trace://set/many",
        ),
        proposed_word_kind=WordKindCandidate.AMBIGUOUS,
        trace_ref="trace://gate/word-kind/deferred",
    )

    assert result.state is WordKindCandidateGateState.DEFERRED
    assert result.word_kind is WordKindCandidate.AMBIGUOUS
    assert any(
        residual.kind is LafziResidualKind.WORD_KIND_AMBIGUOUS for residual in result.residuals
    )


def test_word_kind_gate_blocks_blocked_mapping_with_visible_blocking_residual() -> None:
    _declare("LAFZI-B2 blocked word kind")

    result = prove_word_kind_candidate_gate(
        LafziMadlulCandidateSet(
            dal_alone_closed_ref="trace://dal/closed",
            mapping_state=MappingState.BLOCKED,
            candidates=(),
            lafzi_scope=_scope(),
            residuals=(_residual(LafziResidualKind.UNUSED_DAL_NO_LAFZI, blocking=True),),
            trace_ref="trace://set/blocked",
        ),
        proposed_word_kind=WordKindCandidate.BLOCKED,
        trace_ref="trace://gate/word-kind/blocked",
    )

    assert result.state is WordKindCandidateGateState.BLOCKED
    assert result.word_kind is WordKindCandidate.BLOCKED
    assert any(residual.blocking for residual in result.residuals)


def test_word_kind_gate_refuses_missing_trace_and_invalid_inputs() -> None:
    _declare("LAFZI-B2 birth guards")

    candidate_set = LafziMadlulCandidateSet(
        dal_alone_closed_ref="trace://dal/closed",
        mapping_state=MappingState.ONE_TO_ONE,
        candidates=(_candidate("trace://candidate"),),
        lafzi_scope=_scope(),
        residuals=(),
        trace_ref="trace://set",
    )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_word_kind_candidate_gate(
            candidate_set,
            proposed_word_kind=WordKindCandidate.ISM,
            trace_ref="",
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_word_kind_candidate_gate(  # type: ignore[arg-type]
            "not-a-candidate-set",
            proposed_word_kind=WordKindCandidate.ISM,
            trace_ref="trace://gate/invalid",
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        prove_word_kind_candidate_gate(  # type: ignore[arg-type]
            candidate_set,
            proposed_word_kind="ISM",
            trace_ref="trace://gate/invalid-kind",
        )


def test_word_kind_gate_exports_no_later_gates_or_closed_verdict() -> None:
    _declare("LAFZI-B2 no downstream jump")

    exported = set(lafzi_madlul.__all__)
    assert {
        "WordKindCandidate",
        "WordKindCandidateGateState",
        "WordKindCandidateGateResult",
        "prove_word_kind_candidate_gate",
    } <= exported

    forbidden_exports = {
        "SourceIdentityGate",
        "FormStateGate",
        "InternalWordPathGate",
        "LafziResidualAudit",
        "LafziMadlulClosed",
        "LafziMadlulVerdict",
        "WadiMadlul",
        "prove_lafzi_madlul_closed",
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(lafzi_madlul, name)


def test_chain_marks_lafzi_b2_done_and_b3_current() -> None:
    _declare("chain-marker sync")

    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert _ROADMAP_B2_DONE in roadmap
    assert _ROADMAP_B3_CURRENT in roadmap
    assert "next_permitted_pr: LAFZI-B3 SourceIdentityGate boundary," in roadmap

    assert _ROADMAP_B2_DONE in claude
    assert _ROADMAP_B3_CURRENT in claude
