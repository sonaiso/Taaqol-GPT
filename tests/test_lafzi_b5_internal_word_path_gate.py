"""Constitutional tests for LAFZI-B5 InternalWordPathGate.

Origin law     : docs/59 (Lafzi Madlul Correspondence Law)
Branch         : LAFZI-B5 (InternalWordPathGate only)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import lafzi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lafzi_madlul import (
    LAFZI_B5_ALLOWED_OUTPUT,
    LAFZI_B5_RANK_CEILING,
    FormStateCandidate,
    FormStateGateResult,
    InternalWordPathCandidate,
    InternalWordPathGateState,
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

_FORBIDDEN_B5_OUTPUTS = (
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
_ROADMAP_B5_DONE = (
    "LAFZI-B5 InternalWordPathGate                                             ✓ done"
)
_ROADMAP_B6_CURRENT = (
    "LAFZI-B6 LafziResidualAudit                                               ✓ done"
)
_ROADMAP_B7_CURRENT = (
    "LAFZI-B7 LafziMadlulClosed -> Wad'iMadlulGate integration                 → current"
)


def _declare(
    branch_name: str,
    produced_outputs: frozenset[str] = frozenset(),
    forbidden_outputs: tuple[str, ...] = _FORBIDDEN_B5_OUTPUTS,
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
            "InternalWordPathGate",
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


def _form_state_result(
    word_kind: WordKindCandidate,
    source_identity: SourceIdentityCandidate,
    form_state: FormStateCandidate,
    *,
    mapping_state: MappingState = MappingState.ONE_TO_ONE,
    blocking: bool = False,
) -> FormStateGateResult:
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
    return prove_form_state_candidate_gate(
        source_identity_result,
        proposed_form_state=form_state,
        trace_ref="trace://form-state-result",
    )


def test_internal_word_path_gate_proves_ism_jamid_without_closure() -> None:
    _declare(
        "LAFZI-B5 proven ism path",
        produced_outputs=frozenset({LAFZI_B5_ALLOWED_OUTPUT}),
    )

    result = prove_internal_word_path_candidate_gate(
        _form_state_result(
            WordKindCandidate.ISM,
            SourceIdentityCandidate.JAMID_ENTITY,
            FormStateCandidate.MURAB_POTENTIAL,
        ),
        proposed_internal_path=InternalWordPathCandidate.JAMID,
        trace_ref="trace://gate/internal-word-path/ism-jamid",
    )

    assert result.state is InternalWordPathGateState.PROVEN
    assert result.internal_word_path is InternalWordPathCandidate.JAMID
    assert result.rank is LAFZI_B5_RANK_CEILING
    assert result.output == LAFZI_B5_ALLOWED_OUTPUT
    assert result.residuals == ()


def test_internal_word_path_gate_proves_ism_built_name_for_jamid_entity() -> None:
    _declare("LAFZI-B5 built-name jamid path")

    result = prove_internal_word_path_candidate_gate(
        _form_state_result(
            WordKindCandidate.ISM,
            SourceIdentityCandidate.JAMID_ENTITY,
            FormStateCandidate.MABNI,
        ),
        proposed_internal_path=InternalWordPathCandidate.BUILT_NAME,
        trace_ref="trace://gate/internal-word-path/ism-built-name-jamid",
    )

    assert result.state is InternalWordPathGateState.PROVEN
    assert result.internal_word_path is InternalWordPathCandidate.BUILT_NAME
    assert result.rank is LAFZI_B5_RANK_CEILING
    assert result.residuals == ()


def test_internal_word_path_gate_proves_ism_reference_without_external_resolution() -> None:
    _declare("LAFZI-B5 reference path")

    result = prove_internal_word_path_candidate_gate(
        _form_state_result(
            WordKindCandidate.ISM,
            SourceIdentityCandidate.PRONOUN_BUILT_REFERENCE,
            FormStateCandidate.MABNI,
        ),
        proposed_internal_path=InternalWordPathCandidate.REFERENCE,
        trace_ref="trace://gate/internal-word-path/ism-reference",
    )

    assert result.state is InternalWordPathGateState.PROVEN
    assert result.internal_word_path is InternalWordPathCandidate.REFERENCE
    assert result.word_kind is WordKindCandidate.ISM
    assert result.residuals == ()


def test_internal_word_path_gate_defers_mushtaq_without_masdar_evidence() -> None:
    _declare("LAFZI-B5 mushtaq residual")

    result = prove_internal_word_path_candidate_gate(
        _form_state_result(
            WordKindCandidate.ISM,
            SourceIdentityCandidate.JAMID_ENTITY,
            FormStateCandidate.MURAB_POTENTIAL,
        ),
        proposed_internal_path=InternalWordPathCandidate.MUSHTAQ,
        trace_ref="trace://gate/internal-word-path/mushtaq-deferred",
    )

    assert result.state is InternalWordPathGateState.DEFERRED
    assert result.internal_word_path is InternalWordPathCandidate.DEFERRED
    assert any(
        residual.kind is LafziResidualKind.MUSHTAQ_REQUIRES_MASDAR
        for residual in result.residuals
    )


def test_internal_word_path_gate_defers_fiil_without_masdar_basis() -> None:
    _declare("LAFZI-B5 fiil residual")

    result = prove_internal_word_path_candidate_gate(
        _form_state_result(
            WordKindCandidate.FIIL,
            SourceIdentityCandidate.DEFERRED_SOURCE,
            FormStateCandidate.VERB_BUILT_FORM,
        ),
        proposed_internal_path=InternalWordPathCandidate.FIIL_MASDAR_PATH,
        trace_ref="trace://gate/internal-word-path/fiil-deferred",
    )

    assert result.state is InternalWordPathGateState.DEFERRED
    assert result.internal_word_path is InternalWordPathCandidate.DEFERRED
    assert any(
        residual.kind is LafziResidualKind.FIIL_MASDAR_REQUIRED for residual in result.residuals
    )


@pytest.mark.parametrize(
    ("word_kind", "source_identity", "form_state", "proposed_internal_path", "residual_kind"),
    (
        (
            WordKindCandidate.ISM,
            SourceIdentityCandidate.MUSHTAQ_MASDAR_ROLE,
            FormStateCandidate.MURAB_POTENTIAL,
            InternalWordPathCandidate.JAMID,
            LafziResidualKind.SOURCE_IDENTITY_INTERNAL_PATH_MISMATCH,
        ),
        (
            WordKindCandidate.ISM,
            SourceIdentityCandidate.JAMID_ENTITY,
            FormStateCandidate.MURAB_POTENTIAL,
            InternalWordPathCandidate.MUSHTAQ,
            LafziResidualKind.MUSHTAQ_REQUIRES_MASDAR,
        ),
        (
            WordKindCandidate.ISM,
            SourceIdentityCandidate.JAMID_ENTITY,
            FormStateCandidate.MURAB_POTENTIAL,
            InternalWordPathCandidate.PROPER,
            LafziResidualKind.PROPER_SELF_DESIGNATION_REQUIRED,
        ),
        (
            WordKindCandidate.ISM,
            SourceIdentityCandidate.JAMID_ENTITY,
            FormStateCandidate.MURAB_POTENTIAL,
            InternalWordPathCandidate.REFERENCE,
            LafziResidualKind.REFERENCE_SOURCE_REQUIRED,
        ),
        (
            WordKindCandidate.ISM,
            SourceIdentityCandidate.PROPER_SELF_DESIGNATION,
            FormStateCandidate.MABNI,
            InternalWordPathCandidate.JAMID,
            LafziResidualKind.SOURCE_IDENTITY_INTERNAL_PATH_MISMATCH,
        ),
        (
            WordKindCandidate.HARF,
            SourceIdentityCandidate.HARF_RELATION_OPERATOR_IDENTITY,
            FormStateCandidate.MABNI,
            InternalWordPathCandidate.JAMID,
            LafziResidualKind.HARF_OPERATOR_REQUIRED,
        ),
        (
            WordKindCandidate.HARF,
            SourceIdentityCandidate.HARF_RELATION_OPERATOR_IDENTITY,
            FormStateCandidate.MABNI,
            InternalWordPathCandidate.FIIL_MASDAR_PATH,
            LafziResidualKind.HARF_OPERATOR_REQUIRED,
        ),
        (
            WordKindCandidate.FIIL,
            SourceIdentityCandidate.FIIL_MASDAR_TEMPORAL_IMAGE,
            FormStateCandidate.VERB_BUILT_FORM,
            InternalWordPathCandidate.JAMID,
            LafziResidualKind.FIIL_MASDAR_REQUIRED,
        ),
    ),
)
def test_internal_word_path_gate_never_proves_source_path_mismatch(
    word_kind: WordKindCandidate,
    source_identity: SourceIdentityCandidate,
    form_state: FormStateCandidate,
    proposed_internal_path: InternalWordPathCandidate,
    residual_kind: LafziResidualKind,
) -> None:
    _declare("LAFZI-B5 source-path mismatch hardening")

    result = prove_internal_word_path_candidate_gate(
        _form_state_result(word_kind, source_identity, form_state),
        proposed_internal_path=proposed_internal_path,
        trace_ref=f"trace://gate/internal-word-path/mismatch/{proposed_internal_path.value.lower()}",
    )

    assert result.state is InternalWordPathGateState.DEFERRED
    assert result.internal_word_path is InternalWordPathCandidate.DEFERRED
    assert result.rank is LAFZI_B5_RANK_CEILING
    assert any(residual.kind is residual_kind for residual in result.residuals)


def test_internal_word_path_gate_proves_harf_operator_need_only() -> None:
    _declare("LAFZI-B5 harf bounded path")

    result = prove_internal_word_path_candidate_gate(
        _form_state_result(
            WordKindCandidate.HARF,
            SourceIdentityCandidate.HARF_RELATION_OPERATOR_IDENTITY,
            FormStateCandidate.MABNI,
        ),
        proposed_internal_path=InternalWordPathCandidate.RELATION_NEED,
        trace_ref="trace://gate/internal-word-path/harf-relation-need",
    )

    assert result.state is InternalWordPathGateState.PROVEN
    assert result.internal_word_path is InternalWordPathCandidate.RELATION_NEED
    assert result.word_kind is WordKindCandidate.HARF


def test_internal_word_path_gate_blocks_on_blocked_form_state_with_visible_residual() -> None:
    _declare("LAFZI-B5 blocked path")

    result = prove_internal_word_path_candidate_gate(
        _form_state_result(
            WordKindCandidate.BLOCKED,
            SourceIdentityCandidate.DEFERRED_SOURCE,
            FormStateCandidate.DEFERRED,
            mapping_state=MappingState.BLOCKED,
            blocking=True,
        ),
        proposed_internal_path=InternalWordPathCandidate.DEFERRED,
        trace_ref="trace://gate/internal-word-path/blocked",
    )

    assert result.state is InternalWordPathGateState.BLOCKED
    assert result.internal_word_path is InternalWordPathCandidate.DEFERRED
    assert any(residual.blocking for residual in result.residuals)
    assert any(
        residual.kind is LafziResidualKind.UNUSED_DAL_NO_LAFZI for residual in result.residuals
    )


def test_internal_word_path_gate_refuses_missing_trace_and_invalid_inputs() -> None:
    _declare("LAFZI-B5 birth guards")

    form_state_result = _form_state_result(
        WordKindCandidate.ISM,
        SourceIdentityCandidate.JAMID_ENTITY,
        FormStateCandidate.MABNI,
    )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        prove_internal_word_path_candidate_gate(
            form_state_result,
            proposed_internal_path=InternalWordPathCandidate.JAMID,
            trace_ref="",
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.GATE_REQUIRED.value):
        prove_internal_word_path_candidate_gate(  # type: ignore[arg-type]
            "not-a-form-state-result",
            proposed_internal_path=InternalWordPathCandidate.JAMID,
            trace_ref="trace://gate/invalid",
        )
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BOUNDARY_MISSING.value):
        prove_internal_word_path_candidate_gate(  # type: ignore[arg-type]
            form_state_result,
            proposed_internal_path="JAMID",
            trace_ref="trace://gate/invalid-internal-path",
        )


def test_internal_word_path_gate_exports_b6_but_no_closure_or_crossing() -> None:
    _declare("LAFZI-B5 no downstream jump")

    exported = set(lafzi_madlul.__all__)
    assert {
        "InternalWordPathCandidate",
        "InternalWordPathGateState",
        "InternalWordPathGateResult",
        "prove_internal_word_path_candidate_gate",
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


def test_chain_marks_lafzi_b5_done_b6_done_and_b7_current() -> None:
    _declare("chain-marker sync")

    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert _ROADMAP_B5_DONE in roadmap
    assert _ROADMAP_B6_CURRENT in roadmap
    assert _ROADMAP_B7_CURRENT in roadmap
    assert "next_permitted_pr: LAFZI-B7 LafziMadlulClosed integration boundary," in roadmap

    assert _ROADMAP_B5_DONE in claude
    assert _ROADMAP_B6_CURRENT in claude
    assert _ROADMAP_B7_CURRENT in claude
