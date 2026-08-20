"""Constitutional tests for WordNet -> LexicalCandidateSet bounded bridge.

Origin law     : docs/81 + docs/99 + docs/100
Branch         : LEXICON-SLOT-L0-WORDNET-BRIDGE
Category       : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.weight.lexicon_slot_geometry import (
    LEXICON_SLOT_FORBIDDEN_OUTPUTS,
    LexiconResidualKind,
    build_wordnet_lexical_candidate_set_from_rows,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_WORDNET_FIXTURES = (
    _REPO_ROOT / "data" / "lexical_evidence" / "lex_data_2_arabic_wordnet_samples.json"
)


def _declare(branch_name: str) -> None:
    case = ConstitutionalTestCase(
        origin_law=(
            "docs/81_LEXICAL_EVIDENCE_DATA_LAW.md + "
            "docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md + "
            "docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md"
        ),
        branch_name=branch_name,
        constitutional_chain=("docs/81", "docs/99", "docs/100", "LEXICON-SLOT-L0-WORDNET-BRIDGE"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=LEXICON_SLOT_FORBIDDEN_OUTPUTS,
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


def _rows() -> list[dict[str, object]]:
    return json.loads(_WORDNET_FIXTURES.read_text(encoding="utf-8"))


def test_wordnet_bridge_preserves_multi_sense_ambiguity() -> None:
    _declare("WordNet ambiguity remains visible")
    rows = [row for row in _rows() if row["query_form_id"] == "WQ-AYN-001"]
    candidate_set = build_wordnet_lexical_candidate_set_from_rows(rows)

    assert len(candidate_set.candidates) == len(rows)
    residual_kinds = {res.kind for res in candidate_set.residuals}
    assert LexiconResidualKind.WORDNET_MULTIPLE_SENSES in residual_kinds
    assert LexiconResidualKind.WORDNET_EXTERNAL_AUTHORITY_LIMIT in residual_kinds
    assert all(candidate.rank is Rank.CANDIDATE for candidate in candidate_set.candidates)
    assert all(
        output in LEXICON_SLOT_FORBIDDEN_OUTPUTS
        for candidate in candidate_set.candidates
        for output in candidate.forbidden_outputs
    )
    for row in rows:
        assert any(str(row["synset_id"]) in identity for identity in candidate_set.identity_proofs)


def test_wordnet_bridge_single_sense_stays_candidate_only() -> None:
    _declare("WordNet single sense stays candidate-only")
    rows = [row for row in _rows() if row["query_form_id"] == "WQ-KITAB-001"]
    candidate_set = build_wordnet_lexical_candidate_set_from_rows(rows)

    assert len(candidate_set.candidates) == 1
    residual_kinds = {res.kind for res in candidate_set.residuals}
    assert LexiconResidualKind.WORDNET_EXTERNAL_AUTHORITY_LIMIT in residual_kinds
    assert LexiconResidualKind.WORDNET_MULTIPLE_SENSES not in residual_kinds
    assert candidate_set.usage_scopes == ("WORDNET_POS:NOUN",)
    assert candidate_set.rank_vector.r_sense is Rank.CANDIDATE
    assert candidate_set.rank_vector.r_source is Rank.TRACE
