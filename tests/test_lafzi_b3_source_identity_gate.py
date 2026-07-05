"""Constitutional tests for LAFZI-B3 SourceIdentityGate.

Origin law     : docs/59 (Lafzi Madlul Correspondence Law)
Branch         : LAFZI-B3 (SourceIdentityGate only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import lafzi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lafzi_madlul import (
    LAFZI_B3_ALLOWED_OUTPUT,
    LAFZI_B3_RANK_CEILING,
    LafziMadlulCandidate,
    LafziMadlulCandidateSet,
    LafziMadlulState,
    LafziResidual,
    LafziResidualKind,
    LafziScope,
    MappingState,
    SourceIdentityCandidate,
    SourceIdentityGateState,
    WordKindCandidate,
    prove_source_identity_candidate_gate,
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

_FORBIDDEN_B3_OUTPUTS = (
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
_ROADMAP_B3_DONE = (
    "LAFZI-B3 SourceIdentityGate                                               ✓ done"
)
_ROADMAP_B4_CURRENT = (
    "LAFZI-B4 FormStateGate                                                    → current"
)


def _declare(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    forbidden_outputs: tuple[str, ...] = _FORBIDDEN_B3_OUTPUTS,
) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/59_LAFZI_MADLUL_CORRESPONDENCE_LAW.md",
        branch_name=branch_name,
        constitutional_chain=(
            "DAL-A8",
            "LAFZI-B0",
            "LAFZI-B1",
            "LAFZI-B2",
            "LAFZI-B3",
            "SourceIdentityGate",
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


def _word_kind_result(
    word_kind: WordKindCandidate,
    *,
    mapping_state: MappingState = MappingState.ONE_TO_ONE,
    blocking: bool = False,
) -> object:
    candidate_set = LafziMadlulCandidateSet(
        dal_alone_closed_ref="trace://dal/closed",
        mapping_state=mapping_state,
        candidates=(
            (_candidate("trace://candidate"),)
            if mapping_state is not MappingState.BLOCKED
            else ()
        ),
        lafzi_scope=_scope(),
        residuals=(
            _residual(LafziResidualKind.UNUSED_DAL_NO_LAFZI, blocking=True),
        )
        if blocking or mapping_state is MappingState.BLOCKED
        else (),
        trace_ref="trace://set",
    )
    return prove_word_kind_candidate_gate(
        candidate_set,
        proposed_word_kind=word_kind,
        trace_ref="trace://word-kind-result",
    )


def test_source_identity_gate_proves_ism_source_without_closure() -> None:
    _declare(
        "LAFZI-B3 proven source identity",
        produced_outputs=frozenset({LAFZI_B3_ALLOWED_OUTPUT}),
    )

    result = prove_source_identity_candidate_gate(
        _word_kind_result(WordKindCandidate.ISM),
        proposed_source_identity=SourceIdentityCandidate.JAMID_ENTITY,
        trace_ref="trace://gate/source-identity/proven",
    )

    assert result.state is SourceIdentityGateState.PROVEN
    assert result.source_identity is SourceIdentityCandidate.JAMID_ENTITY
    assert result.rank is LAFZI_B3_RANK_CEILING
    assert result.output == LAFZI_B3_ALLOWED_OUTPUT
    assert result.residuals == ()


def test_source_identity_gate_defers_missing_source_with_visible_residual() -> None:
    _declare("LAFZI-B3 deferred source identity")

    result = prove_source_identity_candidate_gate(
        _word_kind_result(WordKindCandidate.ISM),
        proposed_source_identity=SourceIdentityCandidate.DEFERRED_SOURCE,
        trace_ref="trace://gate/source-identity/deferred",
    )

    assert result.state is SourceIdentityGateState.DEFERRED
    assert result.source_identity is SourceIdentityCandidate.DEFERRED_SOURCE
    assert any(
        residual.kind is LafziResidualKind.SOURCE_IDENTITY_REQUIRED for residual in result.residuals
    )


def test_source_identity_gate_blocks_on_blocked_word_kind_with_visible_residual() -> None:
    _declare("LAFZI-B3 blocked source identity")

    result = prove_source_identity_candidate_gate(
        _word_kind_result(
            WordKindCandidate.BLOCKED,
            mapping_state=MappingState.BLOCKED,
            blocking=True,
        ),
        proposed_source_identity=SourceIdentityCandidate.DEFERRED_SOURCE,
        trace_ref="trace://gate/source-identity/blocked",
    )

    assert result.state is SourceIdentityGateState.BLOCKED
    assert result.source_identity is SourceIdentityCandidate.DEFERRED_SOURCE
    assert any(residual.blocking for residual in result.residuals)


def test_source_identity_gate_refuses_missing_trace_and_invalid_inputs() -> None:
    _declare("LAFZI-B3 birth guards")

    word_kind_result = _word_kind_result(WordKindCandidate.ISM)
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_source_identity_candidate_gate(
            word_kind_result,
            proposed_source_identity=SourceIdentityCandidate.JAMID_ENTITY,
            trace_ref="",
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_source_identity_candidate_gate(  # type: ignore[arg-type]
            "not-a-word-kind-result",
            proposed_source_identity=SourceIdentityCandidate.JAMID_ENTITY,
            trace_ref="trace://gate/invalid",
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        prove_source_identity_candidate_gate(  # type: ignore[arg-type]
            word_kind_result,
            proposed_source_identity="JAMID_ENTITY",
            trace_ref="trace://gate/invalid-source",
        )


def test_source_identity_gate_exports_no_later_gates_or_closed_verdict() -> None:
    _declare("LAFZI-B3 no downstream jump")

    exported = set(lafzi_madlul.__all__)
    assert {
        "SourceIdentityCandidate",
        "SourceIdentityGateState",
        "SourceIdentityGateResult",
        "prove_source_identity_candidate_gate",
    } <= exported

    forbidden_exports = {
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


def test_chain_marks_lafzi_b3_done_and_b4_current() -> None:
    _declare("chain-marker sync")

    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert _ROADMAP_B3_DONE in roadmap
    assert _ROADMAP_B4_CURRENT in roadmap
    assert "next_permitted_pr: LAFZI-B4 FormStateGate boundary," in roadmap

    assert _ROADMAP_B3_DONE in claude
    assert _ROADMAP_B4_CURRENT in claude
