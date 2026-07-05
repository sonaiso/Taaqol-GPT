"""Constitutional tests for LAFZI-B4 FormStateGate.

Origin law     : docs/59 (Lafzi Madlul Correspondence Law)
Branch         : LAFZI-B4 (FormStateGate only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import lafzi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lafzi_madlul import (
    LAFZI_B4_ALLOWED_OUTPUT,
    LAFZI_B4_RANK_CEILING,
    FormStateCandidate,
    FormStateGateState,
    LafziMadlulCandidate,
    LafziMadlulCandidateSet,
    LafziMadlulState,
    LafziResidual,
    LafziResidualKind,
    LafziScope,
    MappingState,
    SourceIdentityCandidate,
    WordKindCandidate,
    prove_form_state_candidate_gate,
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

_FORBIDDEN_B4_OUTPUTS = (
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
_ROADMAP_B4_DONE = (
    "LAFZI-B4 FormStateGate                                                    ✓ done"
)
_ROADMAP_B5_CURRENT = (
    "LAFZI-B5 InternalWordPathGate                                             ✓ done"
)
_ROADMAP_B6_CURRENT = (
    "LAFZI-B6 LafziResidualAudit                                               → current"
)


def _declare(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    forbidden_outputs: tuple[str, ...] = _FORBIDDEN_B4_OUTPUTS,
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
            "LAFZI-B4",
            "FormStateGate",
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


def _source_identity_result(
    word_kind: WordKindCandidate,
    source_identity: SourceIdentityCandidate,
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
    word_kind_result = prove_word_kind_candidate_gate(
        candidate_set,
        proposed_word_kind=word_kind,
        trace_ref="trace://word-kind-result",
    )
    return prove_source_identity_candidate_gate(
        word_kind_result,
        proposed_source_identity=source_identity,
        trace_ref="trace://source-identity-result",
    )


def test_form_state_gate_proves_ism_form_without_closure() -> None:
    _declare(
        "LAFZI-B4 proven form state",
        produced_outputs=frozenset({LAFZI_B4_ALLOWED_OUTPUT}),
    )

    result = prove_form_state_candidate_gate(
        _source_identity_result(WordKindCandidate.ISM, SourceIdentityCandidate.JAMID_ENTITY),
        proposed_form_state=FormStateCandidate.MURAB_POTENTIAL,
        trace_ref="trace://gate/form-state/proven",
    )

    assert result.state is FormStateGateState.PROVEN
    assert result.form_state is FormStateCandidate.MURAB_POTENTIAL
    assert result.rank is LAFZI_B4_RANK_CEILING
    assert result.output == LAFZI_B4_ALLOWED_OUTPUT
    assert result.residuals == ()


def test_form_state_gate_defers_missing_form_with_visible_residual() -> None:
    _declare("LAFZI-B4 deferred form state")

    result = prove_form_state_candidate_gate(
        _source_identity_result(WordKindCandidate.ISM, SourceIdentityCandidate.JAMID_ENTITY),
        proposed_form_state=FormStateCandidate.DEFERRED,
        trace_ref="trace://gate/form-state/deferred",
    )

    assert result.state is FormStateGateState.DEFERRED
    assert result.form_state is FormStateCandidate.DEFERRED
    assert any(
        residual.kind is LafziResidualKind.FORM_STATE_REQUIRED for residual in result.residuals
    )


def test_form_state_gate_blocks_on_blocked_source_identity_with_visible_residual() -> None:
    _declare("LAFZI-B4 blocked form state")

    result = prove_form_state_candidate_gate(
        _source_identity_result(
            WordKindCandidate.BLOCKED,
            SourceIdentityCandidate.DEFERRED_SOURCE,
            mapping_state=MappingState.BLOCKED,
            blocking=True,
        ),
        proposed_form_state=FormStateCandidate.DEFERRED,
        trace_ref="trace://gate/form-state/blocked",
    )

    assert result.state is FormStateGateState.BLOCKED
    assert result.form_state is FormStateCandidate.DEFERRED
    assert any(residual.blocking for residual in result.residuals)


def test_form_state_gate_refuses_missing_trace_and_invalid_inputs() -> None:
    _declare("LAFZI-B4 birth guards")

    source_identity_result = _source_identity_result(
        WordKindCandidate.ISM,
        SourceIdentityCandidate.JAMID_ENTITY,
    )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_form_state_candidate_gate(
            source_identity_result,
            proposed_form_state=FormStateCandidate.MABNI,
            trace_ref="",
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_form_state_candidate_gate(  # type: ignore[arg-type]
            "not-a-source-identity-result",
            proposed_form_state=FormStateCandidate.MABNI,
            trace_ref="trace://gate/invalid",
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        prove_form_state_candidate_gate(  # type: ignore[arg-type]
            source_identity_result,
            proposed_form_state="MABNI",
            trace_ref="trace://gate/invalid-form-state",
        )


def test_form_state_gate_exports_no_later_gates_or_closed_verdict() -> None:
    _declare("LAFZI-B4 no downstream jump")

    exported = set(lafzi_madlul.__all__)
    assert {
        "FormStateCandidate",
        "FormStateGateState",
        "FormStateGateResult",
        "prove_form_state_candidate_gate",
    } <= exported

    forbidden_exports = {
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


def test_chain_marks_lafzi_b4_done_and_b5_current() -> None:
    _declare("chain-marker sync")

    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert _ROADMAP_B4_DONE in roadmap
    assert _ROADMAP_B5_CURRENT in roadmap
    assert _ROADMAP_B6_CURRENT in roadmap
    assert "next_permitted_pr: LAFZI-B6 LafziResidualAudit boundary," in roadmap

    assert _ROADMAP_B4_DONE in claude
    assert _ROADMAP_B5_CURRENT in claude
    assert _ROADMAP_B6_CURRENT in claude
