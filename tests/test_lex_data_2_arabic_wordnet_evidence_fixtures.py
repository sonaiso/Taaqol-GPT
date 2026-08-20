"""Constitutional tests for LEX-DATA-2 Arabic WordNet witness fixtures.

Origin law          : docs/81 + docs/99 + docs/100
Branch name         : LEX-DATA-2 Arabic WordNet lexical evidence witness
Constitutional chain: docs/81 -> docs/99 -> docs/100 -> data/lexical_evidence
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

import json
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalChainTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC_81 = _REPO_ROOT / "docs" / "81_LEXICAL_EVIDENCE_DATA_LAW.md"
_DOC_99 = _REPO_ROOT / "docs" / "99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md"
_DATA_FILE = _REPO_ROOT / "data" / "lexical_evidence" / "lex_data_2_arabic_wordnet_samples.json"


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/81_LEXICAL_EVIDENCE_DATA_LAW.md + "
            "docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md + "
            "docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md"
        ),
        branch_name=f"LEX-DATA-2 Arabic WordNet witness ({branch_note})",
        constitutional_chain=("docs/81", "docs/99", "docs/100", "LEX-DATA-2"),
        chain_position="LEX-DATA-2 external lexical witness fixtures",
        origin_law_ref="docs/81_LEXICAL_EVIDENCE_DATA_LAW.md#7-external-lexical-witness-extension-lex-data-2",
        branch_of_origin=(
            "External Arabic WordNet rows enter as witness-bound lexical evidence "
            "candidates with mandatory provenance and visible residuals."
        ),
        forbidden_shortcut_assertions=(
            "RawArabic -> WordNet -> FinalMeaning",
            "WordNetRelation -> LicensedConceptualRelation",
            "WordNetEvidence -> Hukm",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("FinalMeaning", "Ifadah", "Hukm", "Truth", "Certainty", "Reality"),
        max_rank=Rank.ZERO,
        required_trace=True,
        required_residual_visibility=True,
    )
    result = ConstitutionalChainResult(
        state=ClosureState.MINIMALLY_CLOSED,
        failure_code=None,
        rank=Rank.ZERO,
        residual_visibility=True,
        trace_present=True,
        produced_outputs=frozenset(),
    )
    assert_constitutional_case(case, result)


def _load() -> list[dict[str, object]]:
    return json.loads(_DATA_FILE.read_text(encoding="utf-8"))


def test_lex_data_2_file_exists_and_rows_preserve_required_provenance() -> None:
    _declare("file/provenance")
    assert _DATA_FILE.exists()
    rows = _load()
    assert rows

    required = {
        "source_id",
        "source_version",
        "source_license",
        "query_form_id",
        "query_lemma",
        "query_pos",
        "synset_id",
        "trace_ref",
        "provenance",
    }
    for row in rows:
        assert required.issubset(set(row))
        assert row["source_id"] == "ArabicWordNet"
        assert str(row["trace_ref"]).startswith("lex-data-2:wordnet:")
        provenance = row["provenance"]
        assert isinstance(provenance, dict)
        assert provenance["retrieval_source_url"] == "https://arabic-wordnet.vercel.app/wordnet_arabic.html"


def test_lex_data_2_is_candidate_only_with_forbidden_authority_outputs() -> None:
    _declare("candidate-only authority ceiling")
    rows = _load()
    for row in rows:
        assert row["allowed_output"] == "LexicalEvidenceCandidate"
        forbidden = set(row["forbidden_outputs"])
        assert {"FinalMeaning", "Ifadah", "Hukm", "Truth", "Certainty", "Reality"}.issubset(
            forbidden
        )


def test_lex_data_2_ambiguity_for_same_query_remains_visible() -> None:
    _declare("ambiguity visibility")
    rows = _load()
    ayn_rows = [row for row in rows if row["query_form_id"] == "WQ-AYN-001"]
    assert len(ayn_rows) > 1
    for row in ayn_rows:
        residual_kinds = {res["kind"] for res in row["residuals"]}
        assert "WORDNET_MULTIPLE_SENSES" in residual_kinds
        assert "WORDNET_EXTERNAL_AUTHORITY_LIMIT" in residual_kinds


def test_docs_81_and_docs_99_define_wordnet_as_witness_not_authority() -> None:
    _declare("law markers")
    body81 = _DOC_81.read_text(encoding="utf-8")
    body99 = _DOC_99.read_text(encoding="utf-8")

    assert "LEX_DATA_2_ALLOWED_EXTERNAL_SOURCE = {ArabicWordNet}" in body81
    assert "WordNetSynset NOT_EQUAL MadlulIdentity" in body81
    assert "WordNetRelation NOT_EQUAL LicensedConceptualRelation" in body81
    assert "External lexical resources (including Arabic WordNet when used)" in body99
