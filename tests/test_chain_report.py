"""Constitutional tests for PR-16B: Unified Pre-Semantic Chain Report.

Origin: docs/28_PRE_SEMANTIC_CHAIN_REPORT_LAW.md, docs/14 (chain integrity).

Coverage:

1.  docs/28 origin law is present.
2.  assemble_chain_report() requires a VerbalMadlulCandidate.
3.  Report does not promote rank.
4.  Report does not hide residuals.
5.  Report does not assert meaning.
6.  Report carries no binding, relation, ifadah, hukm, reality.
7.  Rank monotonicity is verified across layers.
8.  Residual continuity is verified.
9.  Forbidden output absence is attested.
10. Trace coverage is complete (all refs non-empty).
11. Every refusal has a named FailureCode.
12. Full end-to-end chain produces an ASSEMBLED report.
13. Report source_surface_identity matches dal signifier_identity.
14. PR-16B module does not import forbidden types.
"""

from __future__ import annotations

import ast
import pathlib

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual, ResidualKind
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    BoundaryEvidence,
    DalBoundaryState,
    DalOnlyCandidate,
    LicenseBoundaryKind,
    LicensingBoundaryState,
    PathKind,
    PreWeightSurface,
    ResidualGovernanceVerdict,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightFitCandidate,
    WeightFitState,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
    assess_license,
    omega_governance,
    prove_dal,
    weigh,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.chain_report import (
    CHAIN_REPORT_RANK_CEILING,
    ChainReportState,
    PreSemanticChainReport,
    assemble_chain_report,
)
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
)
from taaqqul_slot_geometry.weight.verbal_madlul import (
    MadlulBoundaryState,
    VerbalMadlulCandidate,
    prove_verbal_madlul,
)

_DOC_28 = "docs/28_PRE_SEMANTIC_CHAIN_REPORT_LAW.md"


# ---------------------------------------------------------------------------
# Test fixtures — build the full chain through lawful operations
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr16b-chain-report-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr16b/qatala", kind="DECLARED_ENTRY"),
    }


def _syllable() -> SyllableCandidate:
    return SyllableCandidate(**_base("syllable", "syll-qa", "qa"), units=(("q", "a"),))


def _syllables() -> tuple[SyllableCandidate, ...]:
    return (
        _syllable(),
        SyllableCandidate(**_base("syllable", "syll-ta", "ta"), units=(("t", "a"),)),
        SyllableCandidate(**_base("syllable", "syll-la", "la"), units=(("l", "a"),)),
    )


def _sequence() -> SyllableSequenceCandidate:
    return SyllableSequenceCandidate(
        **_base("syllable_sequence", "seq-qatala", "qa-ta-la"),
        syllables=_syllables(),
    )


def _boundary() -> WordBoundaryCandidate:
    return WordBoundaryCandidate(
        **_base("word_boundary", "wb-qatala", "qatala"), sequence=_sequence()
    )


def _word_carrier() -> WordCarrierCandidate:
    return WordCarrierCandidate(
        **_base("word_carrier", "wc-qatala", "qatala"), bounded_surface=_boundary()
    )


def _original_extra() -> OriginalExtraMap:
    return OriginalExtraMap(
        **_base("original_extra_map", "oem-qatala", "qatala"),
        underlying_form="qatala",
        assignments=(
            ("q", LetterStanding.ORIGINAL),
            ("t", LetterStanding.ORIGINAL),
            ("l", LetterStanding.ORIGINAL),
        ),
    )


def _operations() -> OperationTraceCandidate:
    return OperationTraceCandidate(
        **_base("operation_trace", "ops-qatala", "declared-steps"),
        steps=("declared_seq", "declared_boundary"),
    )


def _surface() -> PreWeightSurface:
    carrier = _word_carrier()
    return PreWeightSurface(
        **_base("pre_weight_surface", "pws-qatala", "qatala"),
        carrier=carrier,
        path=PathCandidate(
            **_base("path", "path-qatala", "root_path"),
            kind=PathKind.ROOT,
            carrier=carrier,
        ),
        original_extra=_original_extra(),
        operations=_operations(),
    )


def _weight_readiness() -> WeightReadinessCandidate:
    return WeightReadinessCandidate(
        **_base("weight_readiness", "wr-qatala", "qatala"),
        surface=_surface(),
    )


def _weight_fit_candidate() -> WeightFitCandidate:
    """Produce a valid WeightFitCandidate through the lawful chain."""
    candidate = _weight_readiness()
    governance = omega_governance((), Rank.CANDIDATE)
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED
    assert result.candidate is not None
    return result.candidate


def _granted_governance() -> ResidualGovernanceVerdict:
    return omega_governance((), Rank.CANDIDATE)


def _lexical_evidence() -> BoundaryEvidence:
    return BoundaryEvidence(
        kind=LicenseBoundaryKind.LEXICAL,
        attestation="lexical_root_attested",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
    )


def _licensing_verdict():
    """Produce a valid LicensingBoundaryVerdict through the lawful chain."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = _lexical_evidence()
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    return result.verdict


def _dal_only_candidate() -> DalOnlyCandidate:
    """Produce a valid DalOnlyCandidate through the lawful chain."""
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


def _verbal_madlul_candidate() -> VerbalMadlulCandidate:
    """Produce a valid VerbalMadlulCandidate through the lawful chain."""
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(dal, "wad:lexical_root_qatala")
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


# ---------------------------------------------------------------------------
# 0. Origin law must be present
# ---------------------------------------------------------------------------


def test_pr16b_constitutional_document_is_present() -> None:
    """docs/28 — PR-16B origin law must exist."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    path = repo_root / _DOC_28
    assert path.exists(), f"{_DOC_28} must exist for PR-16B to be constitutional"


# ---------------------------------------------------------------------------
# 1. assemble_chain_report() requires a VerbalMadlulCandidate
# ---------------------------------------------------------------------------


def test_chain_report_requires_verbal_madlul_candidate() -> None:
    """docs/28 §3 — assemble_chain_report accepts ONLY VerbalMadlulCandidate."""
    # Invalid: raw string
    result = assemble_chain_report("raw_surface")  # type: ignore[arg-type]
    assert result.state is ChainReportState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: DalOnlyCandidate (not terminal)
    dal = _dal_only_candidate()
    result = assemble_chain_report(dal)  # type: ignore[arg-type]
    assert result.state is ChainReportState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: None
    result = assemble_chain_report(None)  # type: ignore[arg-type]
    assert result.state is ChainReportState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED


# ---------------------------------------------------------------------------
# 2. Report does not promote rank
# ---------------------------------------------------------------------------


def test_chain_report_does_not_promote_rank() -> None:
    """docs/28 §7 — report rank ceiling does not exceed the chain ceiling."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None
    assert result.report.chain_rank_ceiling <= CHAIN_REPORT_RANK_CEILING
    assert result.report.madlul_rank <= CHAIN_REPORT_RANK_CEILING
    assert result.report.dal_rank <= CHAIN_REPORT_RANK_CEILING
    assert result.report.weight_fit_rank <= CHAIN_REPORT_RANK_CEILING
    assert result.report.licensing_eligibility_rank <= CHAIN_REPORT_RANK_CEILING


# ---------------------------------------------------------------------------
# 3. Report does not hide residuals
# ---------------------------------------------------------------------------


def test_chain_report_does_not_hide_residuals() -> None:
    """docs/28 §5 — all residuals from the terminal are carried."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None
    # The report residuals must equal the terminal residuals
    assert result.report.residuals == terminal.residuals


# ---------------------------------------------------------------------------
# 4. Report does not assert meaning
# ---------------------------------------------------------------------------


def test_chain_report_does_not_assert_meaning() -> None:
    """docs/28 §6/§9 — report has no meaning/ifadah/hukm/reality fields."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None

    # Check that no field name suggests meaning/hukm/ifadah/reality
    field_names = {f.name for f in result.report.__dataclass_fields__.values()}
    forbidden_substrings = {"meaning", "ifadah", "hukm", "reality", "ontolog", "reference_cert"}
    for name in field_names:
        for forbidden in forbidden_substrings:
            assert forbidden not in name, (
                f"PreSemanticChainReport must not carry a '{forbidden}' field"
            )


# ---------------------------------------------------------------------------
# 5. Report carries no binding/relation/ifadah/hukm/reality
# ---------------------------------------------------------------------------


def test_chain_report_carries_no_forbidden_types() -> None:
    """docs/28 §6 — forbidden output attestation is True."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None
    assert result.report.forbidden_outputs_absent is True


# ---------------------------------------------------------------------------
# 6. Rank monotonicity is verified
# ---------------------------------------------------------------------------


def test_chain_report_verifies_rank_monotonicity() -> None:
    """docs/28 §4 — rank does not increase between layers."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None

    ranks = [
        result.report.weight_fit_rank,
        result.report.licensing_eligibility_rank,
        result.report.dal_rank,
        result.report.madlul_rank,
    ]
    for i in range(len(ranks) - 1):
        assert ranks[i + 1] <= ranks[i], (
            f"Rank monotonicity violated: {ranks[i + 1]} > {ranks[i]}"
        )


# ---------------------------------------------------------------------------
# 7. Residual continuity
# ---------------------------------------------------------------------------


def test_chain_report_residual_continuity() -> None:
    """docs/28 §5 — residuals do not disappear between layers."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None
    # All residuals from the input are in the report
    assert result.report.residuals == terminal.residuals


# ---------------------------------------------------------------------------
# 8. Forbidden output absence attestation
# ---------------------------------------------------------------------------


def test_chain_report_forbidden_outputs_absent() -> None:
    """docs/28 §6 — forbidden_outputs_absent must be True."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None
    assert result.report.forbidden_outputs_absent is True

    # Cannot construct a report with forbidden_outputs_absent=False
    with pytest.raises(WeightCarrierSchemaError, match="FORBIDDEN_STRAIGHT_LINE"):
        PreSemanticChainReport(
            source_surface_identity="test",
            weight_readiness_ref="ref",
            weight_fit_ref="ref",
            weight_fit_rank=Rank.CANDIDATE,
            licensing_boundary_ref="ref",
            licensing_boundary_kind="LEXICAL",
            licensing_eligibility_rank=Rank.CANDIDATE,
            dal_ref="ref",
            signifier_identity="test",
            dal_rank=Rank.CANDIDATE,
            verbal_madlul_ref="ref",
            wad_usage_boundary="wad:test",
            correspondence_candidate="",
            inclusion_candidate="",
            iltizam_condition="",
            madlul_rank=Rank.CANDIDATE,
            chain_rank_ceiling=Rank.CANDIDATE,
            residuals=(),
            named_refusals=(),
            trace_refs=("ref1", "ref2"),
            forbidden_outputs_absent=False,
        )


# ---------------------------------------------------------------------------
# 9. Trace coverage is complete
# ---------------------------------------------------------------------------


def test_chain_report_trace_coverage_complete() -> None:
    """docs/28 §2 — all trace_refs are non-empty."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None
    assert len(result.report.trace_refs) >= 4
    for t in result.report.trace_refs:
        assert isinstance(t, str)
        assert t.strip(), "Every trace_ref must be non-empty"


# ---------------------------------------------------------------------------
# 10. Every refusal has a named FailureCode
# ---------------------------------------------------------------------------


def test_chain_report_every_refusal_has_failure_code() -> None:
    """docs/28 §8 — every refusal carries a named FailureCode."""
    # Test with invalid input
    result = assemble_chain_report("invalid")  # type: ignore[arg-type]
    assert result.state is ChainReportState.REFUSED
    assert result.failure_code is not None
    assert isinstance(result.failure_code, FailureCode)


# ---------------------------------------------------------------------------
# 11. Full end-to-end chain produces ASSEMBLED report (KPI-6)
# ---------------------------------------------------------------------------


def test_full_end_to_end_chain_produces_assembled_report() -> None:
    """docs/28 §10 KPI-6 — one canonical end-to-end fixture."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)

    assert result.state is ChainReportState.ASSEMBLED
    assert result.failure_code is None
    assert result.report is not None
    assert isinstance(result.report, PreSemanticChainReport)

    # Verify the report reflects the full chain
    assert result.report.source_surface_identity == "qatala"
    assert result.report.signifier_identity == "qatala"
    assert result.report.wad_usage_boundary == "wad:lexical_root_qatala"
    assert result.report.licensing_boundary_kind == "LEXICAL"
    assert result.report.forbidden_outputs_absent is True
    assert len(result.report.trace_refs) >= 4


# ---------------------------------------------------------------------------
# 12. Report source_surface_identity matches dal signifier_identity
# ---------------------------------------------------------------------------


def test_chain_report_source_matches_signifier() -> None:
    """docs/28 §2 — source_surface_identity == signifier_identity."""
    terminal = _verbal_madlul_candidate()
    result = assemble_chain_report(terminal)
    assert result.state is ChainReportState.ASSEMBLED
    assert result.report is not None
    assert result.report.source_surface_identity == result.report.signifier_identity


# ---------------------------------------------------------------------------
# 13. PR-16B module does not import forbidden types
# ---------------------------------------------------------------------------


def test_pr16b_module_does_not_import_forbidden_types() -> None:
    """docs/28 §9 — chain_report.py must not import forbidden types."""
    module_path = (
        pathlib.Path(__file__).resolve().parent.parent
        / "src"
        / "taaqqul_slot_geometry"
        / "weight"
        / "chain_report.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_names = {
        "DalMadlulBindingCandidate",
        "RelationCandidate",
        "ContractableUnitGeometry",
        "IfadahCandidate",
        "HukmCandidate",
        "TanzilCandidate",
        "ExtraLetterLicense",
        "C_Aug",
        "LicensedWeight",
        "Meaning",
        "Reality",
    }

    imported_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            for alias in node.names:
                imported_names.add(alias.asname if alias.asname else alias.name)

    violations = imported_names & forbidden_names
    assert not violations, (
        f"chain_report.py must not import forbidden types: {violations}"
    )


# ---------------------------------------------------------------------------
# 14. Hidden-forbidden residual causes REFUSED
# ---------------------------------------------------------------------------


def test_chain_report_refuses_on_hidden_residual() -> None:
    """docs/28 §5 — hidden-forbidden residual causes refusal.

    Tests the assemble_chain_report's own guard (lines 360–367) by
    constructing a VerbalMadlulCandidate directly with a hidden
    residual, bypassing prove_verbal_madlul which would normally
    refuse such construction.
    """
    hidden = Residual(
        name="hidden_test",
        kind=ResidualKind.HIDDEN_FORBIDDEN,
        visible=False,
    )

    # Build a valid dal (without hidden residuals) so we can construct
    # a VerbalMadlulCandidate manually with hidden residual injected.
    verdict = _licensing_verdict()
    clean_dal = DalOnlyCandidate(
        signifier_identity="test_hidden",
        phonetic_trace_ref="phonetic://test",
        graphic_trace_ref="graphic://test",
        prior_licensing_verdict=verdict,
        dal_rank=Rank.CANDIDATE,
        residuals=(),
        trace_ref="prove_dal/test_hidden",
    )

    # Directly construct VerbalMadlulCandidate with hidden residual
    # (bypassing prove_verbal_madlul's own guard — simulating a
    # governance bypass scenario that the report must catch).
    madlul_with_hidden = VerbalMadlulCandidate(
        dal_only=clean_dal,
        wad_usage_boundary="wad:test",
        correspondence_candidate="correspondence/test",
        inclusion_candidate="inclusion/test",
        iltizam_condition="iltizam/test",
        existence_carrier_candidate="existence/test",
        event_carrier_candidate="event/test",
        relation_affordance_candidate="relation/test",
        madlul_rank=Rank.CANDIDATE,
        residuals=(hidden,),
        trace_ref="prove_verbal_madlul/test_hidden",
    )

    # assemble_chain_report must refuse due to its own hidden-residual guard
    result = assemble_chain_report(madlul_with_hidden)
    assert result.state is ChainReportState.REFUSED
    assert result.failure_code is FailureCode.HIDDEN_RESIDUAL
    assert result.report is None
