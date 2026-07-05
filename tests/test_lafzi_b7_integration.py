"""Constitutional/runtime tests for LAFZI-B7 LafziMadlulClosed integration.

Origin law     : docs/59 (Lafzi Madlul Correspondence Law)
Branch         : LAFZI-B7 (LafziMadlulClosed -> Wad'iMadlulGate integration only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import lafzi_b7_integration
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lafzi_b7_integration import (
    LAFZI_B7_ALLOWED_OUTPUT,
    LAFZI_B7_RANK_CEILING,
    LafziMadlulClosedState,
    WadiMadlulGateState,
    prove_lafzi_madlul_closed,
)
from taaqqul_slot_geometry.weight.lafzi_madlul import (
    FormStateCandidate,
    InternalWordPathCandidate,
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
    prove_internal_word_path_candidate_gate,
    prove_lafzi_residual_audit,
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

_FORBIDDEN_B7_OUTPUTS = (
    "WadiMadlulClosed",
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
_ROADMAP_B7_CURRENT = (
    "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration                 → current"
)


def _declare(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    forbidden_outputs: tuple[str, ...] = _FORBIDDEN_B7_OUTPUTS,
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
            "LAFZI-B5",
            "LAFZI-B6",
            "LAFZI-B7",
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


def _b6_result(
    word_kind: WordKindCandidate,
    source_identity: SourceIdentityCandidate,
    form_state: FormStateCandidate,
    proposed_internal_path: InternalWordPathCandidate,
    *,
    mapping_state: MappingState = MappingState.ONE_TO_ONE,
    blocking: bool = False,
):
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
    source_identity_result = prove_source_identity_candidate_gate(
        word_kind_result,
        proposed_source_identity=source_identity,
        trace_ref="trace://source-identity-result",
    )
    form_state_result = prove_form_state_candidate_gate(
        source_identity_result,
        proposed_form_state=form_state,
        trace_ref="trace://form-state-result",
    )
    b5_result = prove_internal_word_path_candidate_gate(
        form_state_result,
        proposed_internal_path=proposed_internal_path,
        trace_ref="trace://internal-path-result",
    )
    return prove_lafzi_residual_audit(
        b5_result,
        trace_ref="trace://lafzi-b6/result",
    )


def _proven_b6_result():
    result = _b6_result(
        WordKindCandidate.ISM,
        SourceIdentityCandidate.JAMID_ENTITY,
        FormStateCandidate.MURAB_POTENTIAL,
        InternalWordPathCandidate.JAMID,
    )
    assert result.state.name == "PROVEN"
    assert result.residuals == ()
    return result


def test_lafzi_b7_closes_clean_b6_and_opens_wadi_gate_boundary_only() -> None:
    _declare(
        "LAFZI-B7 bounded closure handoff",
        produced_outputs=frozenset({LAFZI_B7_ALLOWED_OUTPUT}),
    )
    b6_result = _proven_b6_result()

    closed = prove_lafzi_madlul_closed(
        b6_result,
        trace_ref="trace://lafzi-b7/closed",
    )

    assert closed.state is LafziMadlulClosedState.CLOSED
    assert closed.wadi_gate_state is WadiMadlulGateState.OPENED_BOUNDARY_ONLY
    assert closed.residuals == ()
    assert closed.rank is LAFZI_B7_RANK_CEILING
    assert closed.output == LAFZI_B7_ALLOWED_OUTPUT


def test_lafzi_b7_refuses_deferred_b6_surface() -> None:
    _declare("LAFZI-B7 deferred upstream refusal")
    b6_result = _b6_result(
        WordKindCandidate.ISM,
        SourceIdentityCandidate.JAMID_ENTITY,
        FormStateCandidate.MURAB_POTENTIAL,
        InternalWordPathCandidate.MUSHTAQ,
    )
    assert b6_result.internal_word_path is InternalWordPathCandidate.DEFERRED
    assert b6_result.internal_word_path_gate_ref == "trace://internal-path-result"

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_lafzi_madlul_closed(
            b6_result,
            trace_ref="trace://lafzi-b7/deferred",
        )


def test_lafzi_b7_refuses_forged_b6_with_hidden_residual() -> None:
    _declare("LAFZI-B7 anti-forgery residual visibility")
    b6_result = _proven_b6_result()
    object.__setattr__(
        b6_result,
        "residuals",
        (_residual(LafziResidualKind.MULTIPLE_LAFZI_CANDIDATES),),
    )

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        prove_lafzi_madlul_closed(
            b6_result,
            trace_ref="trace://lafzi-b7/forged-residual",
        )


def test_lafzi_b7_refuses_forged_b6_rank_above_candidate() -> None:
    _declare("LAFZI-B7 anti-forgery rank ceiling")
    b6_result = _proven_b6_result()
    object.__setattr__(b6_result, "rank", Rank.HYPOTHESIS)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.RANK_EXCEEDS_CEILING.value):
        prove_lafzi_madlul_closed(
            b6_result,
            trace_ref="trace://lafzi-b7/forged-rank",
        )


def test_lafzi_b7_exports_boundary_surface_without_wadi_crossing() -> None:
    _declare("LAFZI-B7 no downstream crossing")
    exported = set(lafzi_b7_integration.__all__)

    assert {
        "LafziMadlulClosed",
        "LafziMadlulClosedState",
        "WadiMadlulGateState",
        "prove_lafzi_madlul_closed",
    } <= exported

    forbidden_exports = {
        "WadiMadlulContract",
        "WadiMadlulClosed",
        "Mutabaqah",
        "Tadammun",
        "Iltizam",
        "Relation",
        "Composition",
        "Ifadah",
        "Hukm",
        "Reality",
        "prove_wad_kind_gate",
    }
    for name in forbidden_exports:
        assert not hasattr(lafzi_b7_integration, name)


def test_chain_still_marks_b7_current_during_opening() -> None:
    _declare("chain marker alignment")
    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")
    assert _ROADMAP_B7_CURRENT in roadmap
    assert _ROADMAP_B7_CURRENT in claude
