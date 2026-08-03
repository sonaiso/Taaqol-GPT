"""Constitutional tests for LEXICON-SLOT-L0 runtime contracts.

Origin law     : docs/100 (Licensed Lexicon Slot Geometry Boundary Law)
Branch         : LEXICON-SLOT-L0-RUNTIME (bounded carriers/contracts/integration)
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from taaqqul_slot_geometry import ClosureState, FailureCode, Rank
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.lexicon_slot_geometry import (
    LEXICON_SLOT_ALLOWED_OUTPUT,
    LEXICON_SLOT_FORBIDDEN_OUTPUTS,
    LEXICON_SLOT_RANK_CEILING,
    LEXICON_SLOT_RESIDUAL_VOCABULARY,
    TC_IL,
    TC_LW,
    TC_RI,
    TC_SD,
    TC_SR,
    TC_WS,
    DalalahCandidateKind,
    LexicalEntityType,
    LexicalSlot,
    LexicalTransitionContract,
    LexiconResidual,
    LexiconResidualKind,
    RankVector,
    build_vertical_lexical_candidate_set_from_source_row,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_JAMID_FIXTURES = _REPO_ROOT / "data" / "lexical_evidence" / "lex_data_1_jamid_roots.json"


def _declare(branch_name: str, forbidden_outputs: tuple[str, ...]) -> None:
    case = ConstitutionalTestCase(
        origin_law="docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md",
        branch_name=branch_name,
        constitutional_chain=("docs/100", "LEXICON-SLOT-L0-RUNTIME"),
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


def _contract_case(contract: LexicalTransitionContract) -> None:
    _declare(f"contract {contract.contract_id}", LEXICON_SLOT_FORBIDDEN_OUTPUTS)
    assert contract.rank_ceiling is Rank.CANDIDATE
    assert contract.allows_multi_candidate is True
    assert contract.required_fields


def test_rank_vector_channels_are_independent_and_rank_capped() -> None:
    _declare("RankVector channel discipline", LEXICON_SLOT_FORBIDDEN_OUTPUTS)

    rank_vector = RankVector(
        r_source=Rank.TRACE,
        r_reading=Rank.CANDIDATE,
        r_identity=Rank.CANDIDATE,
        r_root=Rank.CANDIDATE,
        r_wad=Rank.CANDIDATE,
        r_sense=Rank.CANDIDATE,
        r_usage=Rank.CANDIDATE,
        r_ontology=Rank.TRACE,
    )
    assert rank_vector.r_source is Rank.TRACE
    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.RANK_EXCEEDS_CEILING.value):
        RankVector(
            r_source=Rank["CERTIFICATE"],
            r_reading=Rank.CANDIDATE,
            r_identity=Rank.CANDIDATE,
            r_root=Rank.CANDIDATE,
            r_wad=Rank.CANDIDATE,
            r_sense=Rank.CANDIDATE,
            r_usage=Rank.CANDIDATE,
            r_ontology=Rank.TRACE,
        )


def test_lexical_slot_requires_licensed_geometry_fields() -> None:
    _declare("LexicalSlot mandatory geometry", LEXICON_SLOT_FORBIDDEN_OUTPUTS)

    rank_vector = RankVector(
        r_source=Rank.TRACE,
        r_reading=Rank.CANDIDATE,
        r_identity=Rank.CANDIDATE,
        r_root=Rank.CANDIDATE,
        r_wad=Rank.CANDIDATE,
        r_sense=Rank.CANDIDATE,
        r_usage=Rank.CANDIDATE,
        r_ontology=Rank.TRACE,
    )
    residual = LexiconResidual(kind=LexiconResidualKind.USAGE_EVIDENCE_PARTIAL, trace_ref="trace://lex")

    LexicalSlot(
        anchor="anchor://1",
        identity="identity://1",
        lexical_type=LexicalEntityType.JAMID_STEM,
        domain="LEXICON_LICENSED_BOUNDARY",
        boundary="SOURCE_READING_IDENTITY_WAD_SENSE_USAGE",
        source="source://1",
        operation="SOURCE_TO_LEXICAL_CANDIDATE",
        invariant="LEXICON_CLOSURE_IS_NOT_MEANING_CLOSURE",
        evidence=("evidence://1",),
        rank_vector=rank_vector,
        trace_ref="trace://1",
        residuals=(residual,),
        closure="LEXICAL_SENSE_CLOSED",
    )

    with pytest.raises(WeightCarrierSchemaError, match=FailureCode.REQUIRED_SLOT_EMPTY.value):
        LexicalSlot(
            anchor="anchor://1",
            identity="identity://1",
            lexical_type=LexicalEntityType.JAMID_STEM,
            domain="LEXICON_LICENSED_BOUNDARY",
            boundary="SOURCE_READING_IDENTITY_WAD_SENSE_USAGE",
            source="source://1",
            operation="SOURCE_TO_LEXICAL_CANDIDATE",
            invariant="LEXICON_CLOSURE_IS_NOT_MEANING_CLOSURE",
            evidence=(),
            rank_vector=rank_vector,
            trace_ref="trace://1",
            residuals=(residual,),
            closure="LEXICAL_SENSE_CLOSED",
        )


def test_transition_contracts_tc_sr_to_tc_sd_are_declared() -> None:
    _contract_case(TC_SR)
    assert TC_SR.input_slot == "SourceSlot"
    assert TC_SR.output_slot == "ReadingCandidate"

    _contract_case(TC_RI)
    assert TC_RI.input_slot == "ReadingCandidate"
    assert TC_RI.output_slot == "IdentityCarrier"

    _contract_case(TC_IL)
    assert TC_IL.input_slot == "IdentityCarrier"
    assert TC_IL.output_slot == "LexicalEntitySlot"

    _contract_case(TC_LW)
    assert TC_LW.input_slot == "LexicalEntitySlot"
    assert TC_LW.output_slot == "WadCandidate"

    _contract_case(TC_WS)
    assert TC_WS.input_slot == "WadCandidate"
    assert TC_WS.output_slot == "LexicalSenseSlot"

    _contract_case(TC_SD)
    assert TC_SD.input_slot == "LexicalSenseSlot"
    assert TC_SD.output_slot == "DalalahCandidateSlot"


def test_vertical_pilot_integrates_real_source_to_dalalah_with_visible_residuals() -> None:
    _declare("vertical pilot SourceSlot->DalalahCandidateSlot", LEXICON_SLOT_FORBIDDEN_OUTPUTS)

    rows = json.loads(_JAMID_FIXTURES.read_text(encoding="utf-8"))
    ayn_row = next(row for row in rows if row.get("surface") == "عين")

    candidate_set = build_vertical_lexical_candidate_set_from_source_row(ayn_row)

    assert len(candidate_set.candidates) == 1
    assert candidate_set.candidates[0].candidate_kind is DalalahCandidateKind.MUTABAQAH
    assert candidate_set.candidates[0].forbidden_outputs == LEXICON_SLOT_FORBIDDEN_OUTPUTS
    assert candidate_set.candidates[0].rank is Rank.CANDIDATE
    assert candidate_set.rank_vector.r_source is Rank.TRACE
    assert candidate_set.rank_vector.r_sense is Rank.CANDIDATE
    assert candidate_set.residuals[0].kind is LexiconResidualKind.SENSE_UNDERDETERMINED
    assert candidate_set.residuals[0].visibility == "VISIBLE"
    assert "lex-data-1:" in candidate_set.traces[0]


def test_lexicon_surface_constants_are_candidate_only() -> None:
    _declare("surface constants", LEXICON_SLOT_FORBIDDEN_OUTPUTS)

    assert LEXICON_SLOT_ALLOWED_OUTPUT == "DALALAH_CANDIDATE_SLOT"
    assert LEXICON_SLOT_RANK_CEILING is Rank.CANDIDATE
    assert tuple(kind.value for kind in LexiconResidualKind) == LEXICON_SLOT_RESIDUAL_VOCABULARY
    for residual_name in LEXICON_SLOT_RESIDUAL_VOCABULARY:
        assert residual_name not in FailureCode.__members__
