"""Constitutional tests for LAFZI-B6 LafziResidualAudit.

Origin law     : docs/59 (Lafzi Madlul Correspondence Law)
Branch         : LAFZI-B6 (LafziResidualAudit only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import lafzi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lafzi_madlul import (
    LAFZI_B6_ALLOWED_OUTPUT,
    LAFZI_B6_RANK_CEILING,
    FormStateCandidate,
    InternalWordPathCandidate,
    InternalWordPathGateState,
    LafziMadlulCandidate,
    LafziMadlulCandidateSet,
    LafziMadlulState,
    LafziResidual,
    LafziResidualAuditState,
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

_FORBIDDEN_B6_OUTPUTS = (
    "LafziMadlulClosed",
    "WadiMadlul",
    "Wad'iMadlul",
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
_ROADMAP_B6_DONE = (
    "LAFZI-B6 LafziResidualAudit                                               ✓ done"
)
_ROADMAP_B7_CURRENT = (
    "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration                 → current"
)


def _declare(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    forbidden_outputs: tuple[str, ...] = _FORBIDDEN_B6_OUTPUTS,
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
            "LafziResidualAudit",
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


def _internal_word_path_result(
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
    return prove_internal_word_path_candidate_gate(
        form_state_result,
        proposed_internal_path=proposed_internal_path,
        trace_ref="trace://internal-path-result",
    )


def _proven_b5_result():
    result = _internal_word_path_result(
        WordKindCandidate.ISM,
        SourceIdentityCandidate.JAMID_ENTITY,
        FormStateCandidate.MURAB_POTENTIAL,
        InternalWordPathCandidate.JAMID,
    )
    assert result.state is InternalWordPathGateState.PROVEN
    assert result.residuals == ()
    return result


def test_lafzi_residual_audit_proves_clean_b5_surface() -> None:
    _declare(
        "LAFZI-B6 proven residual audit",
        produced_outputs=frozenset({LAFZI_B6_ALLOWED_OUTPUT}),
    )
    b5_result = _internal_word_path_result(
        WordKindCandidate.ISM,
        SourceIdentityCandidate.JAMID_ENTITY,
        FormStateCandidate.MURAB_POTENTIAL,
        InternalWordPathCandidate.JAMID,
    )
    assert b5_result.state is InternalWordPathGateState.PROVEN
    assert b5_result.residuals == ()

    result = prove_lafzi_residual_audit(
        b5_result,
        trace_ref="trace://lafzi-b6/proven",
    )

    assert result.state is LafziResidualAuditState.PROVEN
    assert result.residuals == ()
    assert result.blocking_residuals == ()
    assert result.non_blocking_residuals == ()
    assert result.rank is LAFZI_B6_RANK_CEILING
    assert result.output == LAFZI_B6_ALLOWED_OUTPUT


def test_lafzi_residual_audit_defers_on_visible_non_blocking_residuals() -> None:
    _declare("LAFZI-B6 deferred residual audit")
    b5_result = _internal_word_path_result(
        WordKindCandidate.ISM,
        SourceIdentityCandidate.JAMID_ENTITY,
        FormStateCandidate.MURAB_POTENTIAL,
        InternalWordPathCandidate.MUSHTAQ,
    )
    assert b5_result.state is InternalWordPathGateState.DEFERRED
    assert any(not residual.blocking for residual in b5_result.residuals)

    result = prove_lafzi_residual_audit(
        b5_result,
        trace_ref="trace://lafzi-b6/deferred",
    )

    assert result.state is LafziResidualAuditState.DEFERRED
    assert result.residuals == b5_result.residuals
    assert result.blocking_residuals == ()
    assert result.non_blocking_residuals == b5_result.residuals


def test_lafzi_residual_audit_blocks_on_visible_blocking_residuals() -> None:
    _declare("LAFZI-B6 blocking residual audit")
    b5_result = _internal_word_path_result(
        WordKindCandidate.BLOCKED,
        SourceIdentityCandidate.DEFERRED_SOURCE,
        FormStateCandidate.DEFERRED,
        InternalWordPathCandidate.DEFERRED,
        mapping_state=MappingState.BLOCKED,
        blocking=True,
    )
    assert b5_result.state is InternalWordPathGateState.BLOCKED

    result = prove_lafzi_residual_audit(
        b5_result,
        trace_ref="trace://lafzi-b6/blocked",
    )

    assert result.state is LafziResidualAuditState.BLOCKED
    assert result.residuals == b5_result.residuals
    assert result.non_blocking_residuals == ()
    assert all(residual.blocking for residual in result.blocking_residuals)


def test_lafzi_residual_audit_refuses_missing_trace_or_wrong_prior_gate() -> None:
    _declare("LAFZI-B6 birth guards")
    b5_result = _internal_word_path_result(
        WordKindCandidate.ISM,
        SourceIdentityCandidate.JAMID_ENTITY,
        FormStateCandidate.MABNI,
        InternalWordPathCandidate.JAMID,
    )

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_lafzi_residual_audit(b5_result, trace_ref="")
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_lafzi_residual_audit(  # type: ignore[arg-type]
            "not-b5-result",
            trace_ref="trace://lafzi-b6/invalid",
        )


def test_b6_refuses_forged_b5_proven_with_deferred_internal_path() -> None:
    _declare("LAFZI-B6 forged B5 proven deferred internal path refusal")
    b5_result = _proven_b5_result()
    object.__setattr__(b5_result, "internal_word_path", InternalWordPathCandidate.DEFERRED)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_lafzi_residual_audit(
            b5_result,
            trace_ref="trace://lafzi-b6/forged-deferred-internal-path",
        )


def test_b6_refuses_forged_b5_proven_with_blocked_word_kind() -> None:
    _declare("LAFZI-B6 forged B5 proven blocked word kind refusal")
    b5_result = _proven_b5_result()
    object.__setattr__(b5_result, "word_kind", WordKindCandidate.BLOCKED)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_lafzi_residual_audit(
            b5_result,
            trace_ref="trace://lafzi-b6/forged-blocked-word-kind",
        )


def test_b6_refuses_forged_b5_proven_with_deferred_source_identity() -> None:
    _declare("LAFZI-B6 forged B5 proven deferred source identity refusal")
    b5_result = _proven_b5_result()
    object.__setattr__(b5_result, "source_identity", SourceIdentityCandidate.DEFERRED_SOURCE)

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_lafzi_residual_audit(
            b5_result,
            trace_ref="trace://lafzi-b6/forged-deferred-source-identity",
        )


def test_b6_refuses_forged_b5_proven_with_residuals() -> None:
    _declare("LAFZI-B6 forged B5 proven residual visibility refusal")
    b5_result = _proven_b5_result()
    object.__setattr__(b5_result, "residuals", (_residual(),))

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.HIDDEN_RESIDUAL.value):
        prove_lafzi_residual_audit(
            b5_result,
            trace_ref="trace://lafzi-b6/forged-proven-with-residuals",
        )


def test_lafzi_residual_audit_exports_no_b7_or_downstream_runtime() -> None:
    _declare("LAFZI-B6 no downstream jump")

    exported = set(lafzi_madlul.__all__)
    assert {
        "LafziResidualAuditState",
        "LafziResidualAuditResult",
        "prove_lafzi_residual_audit",
    } <= exported

    forbidden_exports = {
        "LafziMadlulClosed",
        "LafziMadlulVerdict",
        "WadiMadlul",
        "Mutabaqah",
        "Tadammun",
        "Iltizam",
        "Relation",
        "Composition",
        "Ifadah",
        "Hukm",
        "Reality",
        "prove_lafzi_madlul_closed",
    }

    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(lafzi_madlul, name)


def test_lafzi_residual_audit_adds_no_global_failure_codes() -> None:
    _declare("LAFZI-B6 local residual vocabulary only")

    assert "HIDDEN_LAFZI_RESIDUAL" not in FailureCode.__members__


def test_chain_marks_lafzi_b6_done_and_b7_current() -> None:
    _declare("chain-marker sync")

    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert _ROADMAP_B6_DONE in roadmap
    assert _ROADMAP_B7_CURRENT in roadmap
    assert "next_permitted_pr: LAFZI-B7 LafziMadlulClosed integration boundary," in roadmap

    assert _ROADMAP_B6_DONE in claude
    assert _ROADMAP_B7_CURRENT in claude
