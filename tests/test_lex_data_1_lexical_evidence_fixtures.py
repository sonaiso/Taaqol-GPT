"""Constitutional tests for LEX-DATA-1 lexical evidence fixtures.

Origin law          : docs/80 §4/§5 + docs/81
Branch name         : LEX-DATA-1 lexical evidence fixtures
Constitutional chain: docs/80 -> docs/81 -> data/lexical_evidence -> tests
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
_DATA_DIR = _REPO_ROOT / "data" / "lexical_evidence"
_DOC_81 = _REPO_ROOT / "docs" / "81_LEXICAL_EVIDENCE_DATA_LAW.md"

_JAMID_FILE = _DATA_DIR / "lex_data_1_jamid_roots.json"
_ATTR_FILE = _DATA_DIR / "lex_data_1_attribute_sources.json"
_LINK_FILE = _DATA_DIR / "lex_data_1_genus_attribute_links.json"

_FORBIDDEN = ("Meaning", "Hukm", "Truth", "Certainty", "Reality")
_ALLOWED_SOURCES = {"Maqayis", "Wasit"}


def _declare(branch_note: str) -> None:
    case = ConstitutionalChainTestCase(
        origin_law=(
            "docs/80_OPERATIONAL_STATE_TRUTH_AND_STRESS_GOVERNANCE.md + "
            "docs/81_LEXICAL_EVIDENCE_DATA_LAW.md"
        ),
        branch_name=f"LEX-DATA-1 ({branch_note})",
        constitutional_chain=("docs/80", "docs/81", "LEX-DATA-1"),
        chain_position="LEX-DATA-1 data-only lexical evidence fixtures",
        origin_law_ref="docs/81_LEXICAL_EVIDENCE_DATA_LAW.md#2-lex-data-1-surface",
        branch_of_origin=(
            "Data-only lexical evidence witnesses for jamid and attribute "
            "compatibility candidates."
        ),
        forbidden_shortcut_assertions=(
            "LexiconEntry -> Meaning",
            "LexiconEntry -> Truth",
            "LexicalDataFixture -> Hukm",
        ),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=(
            "Meaning",
            "FinalMeaning",
            "Hukm",
            "Truth",
            "Certainty",
            "Reality",
            "EssentialAttributeTruth",
        ),
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


def _load(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_lex_data_1_files_exist_and_counts_match_declared_scope() -> None:
    _declare("file existence and counts")

    assert _DOC_81.exists()
    assert _DATA_DIR.exists()
    assert _JAMID_FILE.exists()
    assert _ATTR_FILE.exists()
    assert _LINK_FILE.exists()

    jamid_rows = _load(_JAMID_FILE)
    attr_rows = _load(_ATTR_FILE)
    link_rows = _load(_LINK_FILE)

    assert len(jamid_rows) == 25
    assert len(attr_rows) == 50
    assert len(link_rows) == 100


def test_lex_data_1_jamid_schema_and_source_discipline() -> None:
    _declare("jamid schema discipline")
    jamid_rows = _load(_JAMID_FILE)

    for row in jamid_rows:
        assert set(row).issuperset(
            {
                "id",
                "surface",
                "root_or_stem",
                "class",
                "genus_family",
                "source_attestations",
                "allowed_output",
                "forbidden_outputs",
                "residuals",
                "trace_ref",
            }
        )
        assert row["class"] == "JAMID_GENUS_ANCHOR"
        assert row["allowed_output"] == "LexicalEvidenceCandidate"
        assert isinstance(row["trace_ref"], str) and str(row["trace_ref"]).startswith("lex-data-1:")

        forbidden = tuple(row["forbidden_outputs"])
        for token in _FORBIDDEN:
            assert token in forbidden

        attestations = row["source_attestations"]
        assert isinstance(attestations, list) and attestations
        for attestation in attestations:
            assert attestation["source"] in _ALLOWED_SOURCES
            assert attestation["quote_policy"] == "NO_LONG_QUOTE"
            assert "definition" not in attestation
            assert "long_quote" not in attestation

    ayn_rows = [row for row in jamid_rows if row["surface"] == "عين"]
    assert len(ayn_rows) == 1
    residual_kinds = {res["kind"] for res in ayn_rows[0]["residuals"]}
    assert "SENSE_AMBIGUITY_RESIDUAL" in residual_kinds


def test_lex_data_1_attribute_schema_and_quote_policy() -> None:
    _declare("attribute schema discipline")
    attr_rows = _load(_ATTR_FILE)

    for row in attr_rows:
        assert set(row).issuperset(
            {
                "id",
                "surface",
                "source_type",
                "attribute_family",
                "candidate_attribute",
                "source_attestations",
                "allowed_output",
                "forbidden_outputs",
                "residuals",
                "trace_ref",
            }
        )
        assert row["source_type"] == "ATTRIBUTE_SOURCE"
        assert row["allowed_output"] == "AttributeSourceCandidate"

        forbidden = tuple(row["forbidden_outputs"])
        for token in _FORBIDDEN:
            assert token in forbidden

        attestations = row["source_attestations"]
        assert len(attestations) >= 1
        for attestation in attestations:
            assert attestation["source"] in _ALLOWED_SOURCES
            assert attestation["quote_policy"] == "NO_LONG_QUOTE"
            assert "definition" not in attestation
            assert "long_quote" not in attestation


def test_lex_data_1_links_are_candidate_only_and_rank_capped() -> None:
    _declare("link candidate rank discipline")
    jamid_rows = _load(_JAMID_FILE)
    attr_rows = _load(_ATTR_FILE)
    link_rows = _load(_LINK_FILE)

    jamid_ids = {row["id"] for row in jamid_rows}
    attr_ids = {row["id"] for row in attr_rows}

    for row in link_rows:
        assert set(row).issuperset(
            {
                "id",
                "genus_anchor_id",
                "attribute_source_id",
                "relation_type",
                "compatibility_status",
                "evidence_required",
                "compatibility_reason",
                "rank_ceiling",
                "allowed_output",
                "forbidden_outputs",
                "residuals",
                "trace_ref",
            }
        )
        assert row["genus_anchor_id"] in jamid_ids
        assert row["attribute_source_id"] in attr_ids
        assert row["relation_type"] == "GENUS_ATTRIBUTE_COMPATIBILITY_CANDIDATE"
        assert row["compatibility_status"] == "CANDIDATE"
        assert row["rank_ceiling"] == "HYPOTHESIS"
        assert row["allowed_output"] == "GenusAttributeCompatibilityCandidate"

        forbidden = tuple(row["forbidden_outputs"])
        assert "EssentialAttributeTruth" in forbidden
        for token in _FORBIDDEN:
            assert token in forbidden

        residual_kinds = {res["kind"] for res in row["residuals"]}
        assert "VISIBLE_DEFERRABLE" in residual_kinds


def test_docs_81_declares_data_only_boundary_and_runtime_embargo() -> None:
    _declare("docs/81 boundary markers")
    body = _DOC_81.read_text(encoding="utf-8")

    required_markers = (
        "LEXICON_ROLE = LINGUISTIC_ATTESTATION_WITNESS",
        "LEXICON_NOT_EQUAL = {Meaning, Hukm, Truth, Certainty, Reality}",
        "LEX_DATA_1_ALLOWED_SOURCES = {Maqayis, Wasit}",
        "LEX_DATA_1_QUOTE_POLICY = NO_LONG_QUOTE",
        "LINK_RANK_CEILING = HYPOTHESIS",
        "RUNTIME_NOT_OPENED = {",
        "semantic_runtime",
        "truth_engine",
        "lexical_meaning_runtime",
    )
    for marker in required_markers:
        assert marker in body
