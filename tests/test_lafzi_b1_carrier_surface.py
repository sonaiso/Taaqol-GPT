"""Constitutional tests for LAFZI-B1 Lafzi carrier surface.

Origin law     : docs/59 (Lafzi Madlul Correspondence Law)
Branch         : LAFZI-B1 (carrier-only lafzi correspondence surface)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import dataclasses
import pathlib

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight import lafzi_madlul
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lafzi_madlul import (
    LAFZI_B1_FORBIDDEN_OUTPUTS,
    LAFZI_B1_RANK_CEILING,
    LAFZI_B1_RESIDUAL_VOCABULARY,
    LafziMadlulCandidate,
    LafziMadlulCandidateSet,
    LafziMadlulState,
    LafziResidual,
    LafziResidualKind,
    LafziScope,
    MappingState,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DOC_14 = _REPO_ROOT / "docs" / "14_PR_CHAIN_ROADMAP.md"
_CLAUDE = _REPO_ROOT / "CLAUDE.md"

_FORBIDDEN_B1_OUTPUTS = (
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


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...] = ()) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/59_LAFZI_MADLUL_CORRESPONDENCE_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("DAL-A8", "LAFZI-B0", "LAFZI-B1", "LafziMadlulCandidateSet"),
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
        produced_outputs=frozenset(),
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


def _candidate(
    trace_ref: str,
    **overrides: object,
) -> LafziMadlulCandidate:
    values: dict[str, object] = {
        "dal_alone_closed_ref": "trace://dal/closed",
        "word_kind_candidate_ref": "trace://word-kind",
        "source_identity_candidate_ref": "trace://source-identity",
        "form_state_candidate_ref": "trace://form-state",
        "internal_word_path_candidate_ref": "trace://internal-path",
        "lafzi_scope": _scope(),
        "residuals": (),
        "state": LafziMadlulState.CANDIDATE,
        "trace_ref": trace_ref,
        "rank": Rank.CANDIDATE,
    }
    values.update(overrides)
    return LafziMadlulCandidate(**values)  # type: ignore[arg-type]


def test_lafzi_b1_defines_local_residual_vocabulary_only() -> None:
    _declare("local residual vocabulary")

    assert tuple(kind.value for kind in LafziResidualKind) == LAFZI_B1_RESIDUAL_VOCABULARY
    for residual_name in LAFZI_B1_RESIDUAL_VOCABULARY:
        assert residual_name not in FailureCode.__members__


def test_lafzi_b1_defines_candidate_surface_only() -> None:
    _declare("candidate surface", _FORBIDDEN_B1_OUTPUTS)

    candidate = _candidate("trace://candidate")
    fields = {field.name for field in dataclasses.fields(LafziMadlulCandidate)}

    for field_name in (
        "dal_alone_closed_ref",
        "word_kind_candidate_ref",
        "source_identity_candidate_ref",
        "form_state_candidate_ref",
        "internal_word_path_candidate_ref",
        "lafzi_scope",
        "residuals",
        "state",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in fields
    assert candidate.rank is LAFZI_B1_RANK_CEILING


def test_lafzi_b1_defines_candidate_set_surface_only() -> None:
    _declare("candidate-set surface", _FORBIDDEN_B1_OUTPUTS)

    candidate_set = LafziMadlulCandidateSet(
        dal_alone_closed_ref="trace://dal/closed",
        mapping_state=MappingState.ONE_TO_ONE,
        candidates=(_candidate("trace://candidate/set"),),
        lafzi_scope=_scope(),
        residuals=(),
        trace_ref="trace://candidate-set",
    )
    fields = {field.name for field in dataclasses.fields(LafziMadlulCandidateSet)}

    for field_name in (
        "dal_alone_closed_ref",
        "mapping_state",
        "candidates",
        "lafzi_scope",
        "residuals",
        "trace_ref",
        "forbidden_outputs",
    ):
        assert field_name in fields
    assert candidate_set.rank is LAFZI_B1_RANK_CEILING


def test_lafzi_b1_candidate_requires_dal_alone_closed_ref() -> None:
    _declare("candidate birth guard")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        _candidate("trace://candidate", dal_alone_closed_ref="")


def test_lafzi_b1_candidate_set_requires_trace_ref() -> None:
    _declare("candidate-set trace guard")

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.TRACE_MISSING.value):
        LafziMadlulCandidateSet(
            dal_alone_closed_ref="trace://dal/closed",
            mapping_state=MappingState.ONE_TO_ONE,
            candidates=(_candidate("trace://candidate/set"),),
            lafzi_scope=_scope(),
            residuals=(),
            trace_ref="",
        )


def test_lafzi_b1_candidate_set_allows_one_to_many_without_closure() -> None:
    _declare("one-to-many without closure")

    candidate_set = LafziMadlulCandidateSet(
        dal_alone_closed_ref="trace://dal/closed",
        mapping_state=MappingState.ONE_TO_MANY,
        candidates=(
            _candidate("trace://candidate/a"),
            _candidate("trace://candidate/b"),
        ),
        lafzi_scope=_scope(),
        residuals=(_residual(),),
        trace_ref="trace://candidate-set/many",
    )

    assert candidate_set.mapping_state is MappingState.ONE_TO_MANY
    assert len(candidate_set.candidates) == 2


def test_lafzi_b1_empty_candidates_require_blocked_with_visible_residual() -> None:
    _declare("blocked empty candidate set")

    blocked_set = LafziMadlulCandidateSet(
        dal_alone_closed_ref="trace://dal/closed",
        mapping_state=MappingState.BLOCKED,
        candidates=(),
        lafzi_scope=_scope(),
        residuals=(
            _residual(
                LafziResidualKind.UNUSED_DAL_NO_LAFZI,
                blocking=True,
            ),
        ),
        trace_ref="trace://candidate-set/blocked",
    )
    assert blocked_set.mapping_state is MappingState.BLOCKED

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.BLOCKING_RESIDUAL_PRESENT.value):
        LafziMadlulCandidateSet(
            dal_alone_closed_ref="trace://dal/closed",
            mapping_state=MappingState.BLOCKED,
            candidates=(),
            lafzi_scope=_scope(),
            residuals=(),
            trace_ref="trace://candidate-set/blocked-missing-residual",
        )


def test_lafzi_b1_forbids_meaning_and_downstream_fields_on_carriers() -> None:
    _declare("forbidden-field absence", _FORBIDDEN_B1_OUTPUTS)

    forbidden_fields = {
        "meaning",
        "wad_i_madlul",
        "mutabaqah",
        "tadammun",
        "iltizam",
        "relation",
        "composition",
        "ifadah",
        "mafhum",
        "hukm",
        "reality",
    }

    candidate_fields = {field.name for field in dataclasses.fields(LafziMadlulCandidate)}
    candidate_set_fields = {field.name for field in dataclasses.fields(LafziMadlulCandidateSet)}

    assert candidate_fields.isdisjoint(forbidden_fields)
    assert candidate_set_fields.isdisjoint(forbidden_fields)


def test_lafzi_b1_does_not_define_gate_execution_or_closed_verdict() -> None:
    _declare("no gate execution", _FORBIDDEN_B1_OUTPUTS)

    forbidden_exports = {
        "WordKindGate",
        "SourceIdentityGate",
        "FormStateGate",
        "InternalWordPathGate",
        "LafziResidualAudit",
        "LafziMadlulClosed",
        "LafziMadlulVerdict",
        "prove_lafzi_mapping",
    }

    exported = set(lafzi_madlul.__all__)
    assert exported.isdisjoint(forbidden_exports)
    for name in forbidden_exports:
        assert not hasattr(lafzi_madlul, name)
    assert LAFZI_B1_FORBIDDEN_OUTPUTS


def test_chain_marks_lafzi_b1_done_and_b2_current() -> None:
    _declare("chain-marker sync")

    roadmap = _DOC_14.read_text(encoding="utf-8")
    claude = _CLAUDE.read_text(encoding="utf-8")

    assert "LAFZI-B1 Lafzi carrier surface + local residual vocabulary                ✓ done" in roadmap
    assert "LAFZI-B2 WordKindCandidateGate                                            → current" in roadmap
    assert "next_permitted_pr: LAFZI-B2 WordKindCandidateGate boundary," in roadmap

    assert "LAFZI-B1 Lafzi carrier surface + local residual vocabulary                ✓ done" in claude
    assert "LAFZI-B2 WordKindCandidateGate                                            → current" in claude
