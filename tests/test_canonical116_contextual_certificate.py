"""Constitutional tests for reproducible canonical116-to-context certificate path.

Origin law          : docs/38 + docs/39 + docs/81 + docs/99 + docs/100
Branch name         : canonical116 contextual certification replay surface
Constitutional chain: docs/38 -> docs/39 -> docs/81 -> docs/99 -> docs/100 ->
                      x0r/canonical116_contextual_certificate.py
Category            : Category 2 — Contract / surface tests (docs/52 §4)
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from taaqqul_slot_geometry import ClosureState, Rank
from taaqqul_slot_geometry.x0r.canonical116_contextual_certificate import (
    ClaimState,
    ContextualCertificate,
    LayerState,
    certify_case,
    load_fixture,
    render_arabic_report,
    run_fixture,
)
from tests.support.constitutional_case import (
    ConstitutionalChainResult,
    ConstitutionalTestCase,
    assert_constitutional_case,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FIXTURE = (
    _REPO_ROOT
    / "data"
    / "contextual_evidence"
    / "canonical116_contextual_cases.json"
)


def _declare(branch_note: str) -> None:
    case = ConstitutionalTestCase(
        origin_law=(
            "docs/38_MUTABAQAH_TADAMMUN_ILTIZAM_CANDIDATE_LAW.md + "
            "docs/39_MUFRAD_DALALAH_CLOSURE_LAW.md + "
            "docs/81_LEXICAL_EVIDENCE_DATA_LAW.md + "
            "docs/99_CONSTITUTIONAL_LEXICON_LICENSING_ARCHITECTURE_LAW.md + "
            "docs/100_LICENSED_LEXICON_SLOT_GEOMETRY_BOUNDARY_LAW.md"
        ),
        branch_name=f"canonical116 contextual certification ({branch_note})",
        constitutional_chain=("docs/38", "docs/39", "docs/81", "docs/99", "docs/100", "x0r"),
        expected_state=ClosureState.MINIMALLY_CLOSED,
        expected_failure_code=None,
        forbidden_outputs=("FinalMeaning", "Ifadah", "Hukm", "Truth", "Reality"),
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


def _load_case(case_id: str) -> tuple[dict[str, object], str, dict[str, dict[str, str]]]:
    fixture_id, sources, cases = load_fixture(_FIXTURE)
    for case in cases:
        if case.get("case_id") == case_id:
            return deepcopy(case), fixture_id, sources
    raise AssertionError(f"case not found: {case_id}")


def _claim(cert: ContextualCertificate, claim_id: str) -> ClaimState:
    for claim in cert.claims:
        if claim.claim_id == claim_id:
            return claim.state
    raise AssertionError(f"missing claim: {claim_id}")


def _layer(cert: ContextualCertificate, layer_id: str) -> LayerState:
    for layer in cert.layers:
        if layer.layer_id == layer_id:
            return layer.state
    raise AssertionError(f"missing layer: {layer_id}")


def test_replay_case_keeps_origin_gap_suspended() -> None:
    _declare("replay origin gap")
    certs = run_fixture(_FIXTURE)
    replay = next(c for c in certs if c.case_id == "replay_l329_w3_origin_gap")

    assert _claim(replay, "A_PHRASE_EXISTS_IN_SOURCE") is ClaimState.PROVEN
    assert _claim(replay, "B_UNIQUE_LOCATION_IN_SEARCH_SET") is ClaimState.PROVEN
    assert _claim(replay, "C_DATASET_ORIGIN_LINK") is ClaimState.SUSPENDED
    assert _layer(replay, "canonical116_acceptance") is LayerState.SUSPENDED
    assert _layer(replay, "encoding_normalization") is LayerState.SUSPENDED
    assert _layer(replay, "textual_reference_resolution") is LayerState.REFUSED
    assert replay.overall_state is LayerState.REFUSED


def test_fixture_origin_link_does_not_license_unverified_analysis() -> None:
    _declare("fixture origin link with unverified analysis")
    certs = run_fixture(_FIXTURE)
    verified = next(c for c in certs if c.case_id == "fixture_origin_link_only")

    assert _claim(verified, "C_DATASET_ORIGIN_LINK") is ClaimState.SUSPENDED
    assert _layer(verified, "canonical116_acceptance") is LayerState.SUSPENDED
    assert _layer(verified, "morphology_weight_analysis") is LayerState.SUSPENDED
    assert _layer(verified, "syntax_relation_analysis") is LayerState.SUSPENDED
    assert _layer(verified, "textual_reference_resolution") is LayerState.SUSPENDED
    assert verified.overall_state is LayerState.SUSPENDED


def test_same_phrase_in_two_sources_refuses_uniqueness() -> None:
    _declare("duplicate phrase across sources")
    certs = run_fixture(_FIXTURE)
    ambiguous = next(c for c in certs if c.case_id == "ambiguous_two_sources_same_phrase")

    assert _claim(ambiguous, "A_PHRASE_EXISTS_IN_SOURCE") is ClaimState.PROVEN
    assert _claim(ambiguous, "B_UNIQUE_LOCATION_IN_SEARCH_SET") is ClaimState.REFUSED


def test_wrong_origin_anchor_refuses_claim_c() -> None:
    _declare("wrong origin offset surrogate")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    case["origin_link"]["right_anchor"] = " نص_غير_موجود "

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=sources,
        previous_audit_zip_found=(),
    )
    assert _claim(cert, "C_DATASET_ORIGIN_LINK") is ClaimState.REFUSED
    assert _layer(cert, "textual_reference_resolution") is LayerState.SUSPENDED


def test_withdrawing_reference_evidence_leaves_reference_suspended() -> None:
    _declare("reference evidence withdrawal")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    case["reference"]["evidence_refs"] = []

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=sources,
        previous_audit_zip_found=(),
    )

    assert _claim(cert, "C_DATASET_ORIGIN_LINK") is ClaimState.SUSPENDED
    assert _layer(cert, "encoding_normalization") is LayerState.SUSPENDED
    assert _layer(cert, "canonical116_acceptance") is LayerState.SUSPENDED
    assert _layer(cert, "morphology_weight_analysis") is LayerState.SUSPENDED
    assert _layer(cert, "textual_reference_resolution") is LayerState.SUSPENDED


def test_tanween_role_change_refuses_morphology() -> None:
    _declare("tanween role mutation")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    case["morphology"]["tanween_role"] = "UNKNOWN"

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=sources,
        previous_audit_zip_found=(),
    )
    assert _layer(cert, "morphology_weight_analysis") is LayerState.REFUSED


def test_forced_synthetic_wasl_is_refused() -> None:
    _declare("boundary mutation")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    case["boundaries"]["wasl"] = "FORCED_TO_SYNTHETIC_TOKEN"

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=sources,
        previous_audit_zip_found=(),
    )
    assert _layer(cert, "segment_boundary_license") is LayerState.REFUSED


def test_untrusted_dataset_adjacency_is_rejected_even_with_claim_c() -> None:
    _declare("adjacency rejection")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    case["reference"]["mode"] = "UNPROVEN_DATASET_ADJACENCY"

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=sources,
        previous_audit_zip_found=(),
    )
    assert _claim(cert, "C_DATASET_ORIGIN_LINK") is ClaimState.SUSPENDED
    assert _layer(cert, "textual_reference_resolution") is LayerState.REFUSED


def test_canonical116_declarations_never_license_a_word_count() -> None:
    _declare("canonical116 declaration is not a word count")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    case["canonical116"] = {"ready": True, "unit_count": 116}

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=sources,
        previous_audit_zip_found=(),
    )

    assert _layer(cert, "canonical116_acceptance") is LayerState.SUSPENDED
    assert "CANONICAL116_DECLARATION_NOT_REVALIDATED" in next(
        layer.residuals for layer in cert.layers if layer.layer_id == "canonical116_acceptance"
    )
    assert cert.overall_state is LayerState.SUSPENDED


def test_changed_morphology_and_unresolved_refs_do_not_license_analysis() -> None:
    _declare("morphology content and evidence mutation")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    case["morphology"]["root"] = "كتب"
    case["morphology"]["weight"] = "مَفْعُول"
    case["morphology"]["evidence_refs"] = ["absent://not-a-source"]
    case["syntax"]["evidence_refs"] = ["absent://not-a-source"]
    case["reference"]["evidence_refs"] = ["absent://not-a-source"]

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=sources,
        previous_audit_zip_found=(),
    )

    assert _layer(cert, "morphology_weight_analysis") is LayerState.SUSPENDED
    assert _layer(cert, "syntax_relation_analysis") is LayerState.SUSPENDED
    assert _layer(cert, "textual_reference_resolution") is LayerState.SUSPENDED
    assert cert.overall_state is LayerState.SUSPENDED


def test_changed_candidate_referent_is_not_licensed_by_reference_string() -> None:
    _declare("candidate referent mutation")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    case["reference"]["candidate_referent"] = "الفرق بين البحر والجبل"

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=sources,
        previous_audit_zip_found=(),
    )

    assert _layer(cert, "textual_reference_resolution") is LayerState.SUSPENDED
    assert cert.overall_state is LayerState.SUSPENDED


def test_tampered_source_breaks_origin_link_but_keeps_independent_layers() -> None:
    _declare("tampered provenance")
    case, fixture_id, sources = _load_case("fixture_origin_link_only")
    tampered_sources = deepcopy(sources)
    sid = "ghitha_al_albab_j2_p296_fixture"
    tampered_sources[sid]["normalized_text"] = tampered_sources[sid]["normalized_text"].replace(
        "قال: وَفِي الْفَرْقِ نَظَرٌ .",
        "قال: وفي الفرق نظر.",
    )

    cert = certify_case(
        case,
        fixture_id=fixture_id,
        sources=tampered_sources,
        previous_audit_zip_found=(),
    )

    assert _claim(cert, "A_PHRASE_EXISTS_IN_SOURCE") is ClaimState.REFUSED
    assert _claim(cert, "C_DATASET_ORIGIN_LINK") is ClaimState.REFUSED
    assert _layer(cert, "canonical116_acceptance") is LayerState.SUSPENDED


def test_report_mentions_missing_previous_zip_when_absent() -> None:
    _declare("zip absence report")
    certs = run_fixture(_FIXTURE)
    report = render_arabic_report(certs)
    assert "أرشيف التدقيق السابق: غير موجود" in report
