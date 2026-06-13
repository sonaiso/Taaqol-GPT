"""Constitutional tests for PR-15: DalOnlyCandidate Boundary.

Origin: docs/25, docs/26_DAL_ONLY_CANDIDATE_BOUNDARY_LAW.md, docs/04.

Coverage of the 10 required constitutional tests:

1.  DalOnlyCandidate is not VerbalMadlulCandidate.
2.  DalOnlyCandidate carries no meaning field.
3.  DalOnlyCandidate carries no ifadah/hukm/reality fields.
4.  DalOnlyCandidate cannot be created from raw surface without prior
    boundary verdicts.
5.  Rank is bounded.
6.  Residual governance is respected.
7.  TraceRef remains reference, not ledger commit.
8.  PR-15 does not import or define ContractableUnitGeometry,
    ExtraLetterLicense, C_Aug, RelationCandidate, or VerbalMadlulCandidate.
9.  Any refusal has named FailureCode.
10. Candidate declaration is not semantic verdict.
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
    DAL_BOUNDARY_RANK_CEILING,
    LICENSE_BOUNDARY_RANK_CEILING,
    BoundaryEvidence,
    DalBoundaryState,
    DalBoundaryVerdict,
    DalOnlyCandidate,
    LicenseBoundaryKind,
    LicensingBoundaryState,
    LicensingBoundaryVerdict,
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
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
)

_DOC_26 = "docs/26_DAL_ONLY_CANDIDATE_BOUNDARY_LAW.md"


# ---------------------------------------------------------------------------
# Test fixtures — build a LicensingBoundaryVerdict through the lawful chain
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr15-dal-only-boundary-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr15/qatala", kind="DECLARED_ENTRY"),
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
    """A GRANTED omega governance verdict with no residuals."""
    return omega_governance((), Rank.CANDIDATE)


def _lexical_evidence() -> BoundaryEvidence:
    return BoundaryEvidence(
        kind=LicenseBoundaryKind.LEXICAL,
        attestation="lexical_root_attested",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
    )


def _licensing_verdict() -> LicensingBoundaryVerdict:
    """Produce a valid LicensingBoundaryVerdict through the lawful chain."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = _lexical_evidence()
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    return result.verdict


# ---------------------------------------------------------------------------
# 0. Origin law must be present
# ---------------------------------------------------------------------------


def test_pr15_constitutional_document_is_present() -> None:
    """docs/26 — PR-15 origin law must exist."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    path = repo_root / _DOC_26
    assert path.is_file(), f"missing PR-15 origin document: {_DOC_26}"
    assert path.read_text(encoding="utf-8").strip(), f"PR-15 origin document is empty: {_DOC_26}"


# ---------------------------------------------------------------------------
# 1. DalOnlyCandidate is not VerbalMadlulCandidate
# ---------------------------------------------------------------------------


def test_dal_only_candidate_is_not_verbal_madlul_candidate() -> None:
    """docs/26 §1 — DalOnlyCandidate != VerbalMadlulCandidate.

    The signifier-alone carrier is categorically distinct from the
    verbal signified carrier. No VerbalMadlulCandidate class exists
    in PR-15.
    """
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    assert isinstance(result.candidate, DalOnlyCandidate)

    # DalOnlyCandidate has no 'verbal_signified' or 'madlul' field
    fields = set(result.candidate.__dataclass_fields__.keys())
    assert "verbal_signified" not in fields
    assert "madlul" not in fields
    assert "verbal_madlul" not in fields

    # The type is specifically DalOnlyCandidate, not VerbalMadlulCandidate
    assert type(result.candidate).__name__ == "DalOnlyCandidate"


# ---------------------------------------------------------------------------
# 2. DalOnlyCandidate carries no meaning field
# ---------------------------------------------------------------------------


def test_dal_only_candidate_carries_no_meaning_field() -> None:
    """docs/26 §2.2 — DalOnlyCandidate does NOT carry meaning.

    No field named meaning, dalalah, conceptual_meaning, lexical_meaning,
    or semantic_content exists on DalOnlyCandidate.
    """
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    fields = set(candidate.__dataclass_fields__.keys())
    forbidden_meaning_fields = {
        "meaning", "dalalah", "conceptual_meaning", "lexical_meaning",
        "semantic_content", "madlul", "verbal_signified", "reference",
        "denotation",
    }
    found = fields & forbidden_meaning_fields
    assert not found, f"DalOnlyCandidate carries forbidden meaning fields: {found}"


# ---------------------------------------------------------------------------
# 3. DalOnlyCandidate carries no ifadah/hukm/reality fields
# ---------------------------------------------------------------------------


def test_dal_only_candidate_carries_no_ifadah_hukm_reality() -> None:
    """docs/26 §2.2 — DalOnlyCandidate does NOT carry ifadah/hukm/reality.

    No field named ifadah, hukm, reality, judgment, proposition,
    application, tanzil, or truth_value exists on DalOnlyCandidate.
    """
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    fields = set(candidate.__dataclass_fields__.keys())
    forbidden_fields = {
        "ifadah", "hukm", "reality", "judgment", "proposition",
        "application", "tanzil", "truth_value", "agency", "patienthood",
    }
    found = fields & forbidden_fields
    assert not found, f"DalOnlyCandidate carries forbidden fields: {found}"


# ---------------------------------------------------------------------------
# 4. DalOnlyCandidate cannot be created from raw surface without prior
#    boundary verdicts
# ---------------------------------------------------------------------------


def test_dal_only_requires_prior_licensing_verdict() -> None:
    """docs/26 §3 — DalOnlyCandidate requires a LicensingBoundaryVerdict.

    prove_dal() refuses any input that is not a LicensingBoundaryVerdict.
    """
    # Valid — should succeed
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN

    # Invalid: raw string
    result = prove_dal("raw_surface", "qatala", "phonetic://qatala")  # type: ignore[arg-type]
    assert result.verdict_state is DalBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: WeightFitCandidate (must pass through assess_license first)
    result = prove_dal(_weight_fit_candidate(), "qatala", "phonetic://qatala")  # type: ignore[arg-type]
    assert result.verdict_state is DalBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: None
    result = prove_dal(None, "qatala", "phonetic://qatala")  # type: ignore[arg-type]
    assert result.verdict_state is DalBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: WeightReadinessCandidate
    result = prove_dal(_weight_readiness(), "qatala", "phonetic://qatala")  # type: ignore[arg-type]
    assert result.verdict_state is DalBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Birth guard: DalOnlyCandidate refuses construction with non-verdict prior
    with pytest.raises(WeightCarrierSchemaError, match="GATE_REQUIRED"):
        DalOnlyCandidate(
            signifier_identity="qatala",
            phonetic_trace_ref="phonetic://qatala",
            graphic_trace_ref="graphic://qatala",
            prior_licensing_verdict="not_a_verdict",  # type: ignore[arg-type]
            dal_rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="trace://test",
        )


# ---------------------------------------------------------------------------
# 5. Rank is bounded
# ---------------------------------------------------------------------------


def test_dal_rank_is_bounded() -> None:
    """docs/26 §5 — DalOnlyCandidate.dal_rank <= DAL_BOUNDARY_RANK_CEILING.

    No rank promotion beyond the ceiling, mirroring PR-14.
    """
    assert DAL_BOUNDARY_RANK_CEILING == LICENSE_BOUNDARY_RANK_CEILING
    assert DAL_BOUNDARY_RANK_CEILING == Rank.HYPOTHESIS

    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    assert result.candidate.dal_rank <= DAL_BOUNDARY_RANK_CEILING
    assert result.verdict_rank <= DAL_BOUNDARY_RANK_CEILING

    # Birth guard: constructing with rank above ceiling fails
    with pytest.raises(WeightCarrierSchemaError, match="RANK_EXCEEDS_CEILING"):
        DalOnlyCandidate(
            signifier_identity="qatala",
            phonetic_trace_ref="phonetic://qatala",
            graphic_trace_ref="graphic://qatala",
            prior_licensing_verdict=verdict,
            dal_rank=Rank.LICENSED,  # above HYPOTHESIS ceiling
            residuals=(),
            trace_ref="trace://test",
        )


# ---------------------------------------------------------------------------
# 6. Residual governance is respected
# ---------------------------------------------------------------------------


def test_residual_governance_is_respected() -> None:
    """docs/26 §6 — residual governance from PR-14 is inherited.

    HIDDEN_FORBIDDEN and BLOCKING residuals refuse the candidate.
    """
    # Produce a WeightFitCandidate with a HIDDEN_FORBIDDEN residual
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = _lexical_evidence()

    # First get a valid verdict
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    verdict = result.verdict
    assert verdict is not None

    # Now build a verdict whose source carries HIDDEN_FORBIDDEN residual
    # We need to test prove_dal's governance handling
    hidden_residual = Residual(
        name="hidden_test", kind=ResidualKind.HIDDEN_FORBIDDEN, visible=False
    )
    blocking_residual = Residual(
        name="blocking_test", kind=ResidualKind.BLOCKING, visible=True
    )

    # Create a WeightFitCandidate with hidden residual for testing
    readiness = _weight_readiness()
    # omega_governance with HIDDEN_FORBIDDEN will reject — test prove_dal directly

    # Construct a verdict manually whose source has bad residuals
    # The real check: LicensingBoundaryVerdict.source carries the residuals
    # and prove_dal checks them
    from taaqqul_slot_geometry.weight.weight_fit import WeightFitCandidate as WFC

    # Build a fit candidate with hidden residuals for testing
    bad_fit = WFC(
        value="qatala",
        type="weight_fit",
        origin="declared_fixture",
        identity="wf-hidden-test",
        domain="arabic_morphophonology",
        scope="test",
        rank=Rank.CANDIDATE,
        residuals=(hidden_residual,),
        trace=TraceRef(anchor="trace://test", kind="DECLARED_ENTRY"),
        source=readiness,
        fit_verdict="fitted",
        fit_rank=Rank.CANDIDATE,
    )

    bad_verdict = LicensingBoundaryVerdict(
        source=bad_fit,
        boundary_kind=LicenseBoundaryKind.LEXICAL,
        eligibility_verdict="boundary_eligible:LEXICAL",
        eligibility_rank=Rank.CANDIDATE,
        evidence_summary="LEXICAL:test",
    )

    # prove_dal should refuse due to hidden residual
    result_hidden = prove_dal(bad_verdict, "qatala", "phonetic://qatala")
    assert result_hidden.verdict_state is DalBoundaryState.REFUSED
    assert result_hidden.failure_code is FailureCode.HIDDEN_RESIDUAL

    # Test with blocking residual
    blocking_fit = WFC(
        value="qatala",
        type="weight_fit",
        origin="declared_fixture",
        identity="wf-blocking-test",
        domain="arabic_morphophonology",
        scope="test",
        rank=Rank.CANDIDATE,
        residuals=(blocking_residual,),
        trace=TraceRef(anchor="trace://test", kind="DECLARED_ENTRY"),
        source=readiness,
        fit_verdict="fitted",
        fit_rank=Rank.CANDIDATE,
    )

    blocking_verdict = LicensingBoundaryVerdict(
        source=blocking_fit,
        boundary_kind=LicenseBoundaryKind.LEXICAL,
        eligibility_verdict="boundary_eligible:LEXICAL",
        eligibility_rank=Rank.CANDIDATE,
        evidence_summary="LEXICAL:test",
    )

    result_blocking = prove_dal(blocking_verdict, "qatala", "phonetic://qatala")
    assert result_blocking.verdict_state is DalBoundaryState.REFUSED
    assert result_blocking.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


# ---------------------------------------------------------------------------
# 7. TraceRef remains reference, not ledger commit
# ---------------------------------------------------------------------------


def test_trace_ref_is_reference_not_ledger_commit() -> None:
    """docs/26 §7 — trace_ref is a reference, not an audit ledger commit.

    The trace_ref field on DalOnlyCandidate and DalBoundaryVerdict
    is a string path reference, not a ledger commit hash or ledger write.
    """
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    # trace_ref is a path-like string reference
    assert isinstance(candidate.trace_ref, str)
    assert candidate.trace_ref.startswith("prove_dal/")
    assert "ledger" not in candidate.trace_ref.lower()
    assert "commit" not in candidate.trace_ref.lower()

    # Same for the verdict
    assert isinstance(result.trace_ref, str)
    assert result.trace_ref.startswith("prove_dal/")


# ---------------------------------------------------------------------------
# 8. PR-15 does not import or define forbidden types
# ---------------------------------------------------------------------------


def test_pr15_module_does_not_import_forbidden_types() -> None:
    """docs/26 §9 — PR-15 must not import/define ContractableUnitGeometry,
    ExtraLetterLicense, C_Aug, RelationCandidate, or VerbalMadlulCandidate.

    Static AST check of the dal_only.py module.
    """
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    dal_only_path = repo_root / "src" / "taaqqul_slot_geometry" / "weight" / "dal_only.py"
    assert dal_only_path.is_file()

    source = dal_only_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_names = {
        "ContractableUnitGeometry",
        "ExtraLetterLicense",
        "AugmentationCategory",
        "RelationCandidate",
        "VerbalMadlulCandidate",
        "DalMadlulBindingCandidate",
        "IfadahCandidate",
        "HukmCandidate",
        "TanzilCandidate",
    }

    # Check all imported names
    imported_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name)

    found = imported_names & forbidden_names
    assert not found, f"PR-15 dal_only.py imports forbidden types: {found}"

    # Check all class definitions
    defined_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            defined_names.add(node.name)

    found_defined = defined_names & forbidden_names
    assert not found_defined, f"PR-15 dal_only.py defines forbidden types: {found_defined}"


# ---------------------------------------------------------------------------
# 9. Any refusal has named FailureCode
# ---------------------------------------------------------------------------


def test_every_refusal_has_named_failure_code() -> None:
    """docs/26 §8 — every refusal from prove_dal() carries a named FailureCode.

    No silent None refusal. Every REFUSED verdict has a member of FailureCode.
    """
    verdict = _licensing_verdict()

    # Refusal: missing signifier identity
    result = prove_dal(verdict, "", "phonetic://qatala")
    assert result.verdict_state is DalBoundaryState.REFUSED
    assert result.failure_code is not None
    assert isinstance(result.failure_code, FailureCode)
    assert result.failure_code is FailureCode.IDENTITY_BROKEN

    # Refusal: missing phonetic trace
    result = prove_dal(verdict, "qatala", "")
    assert result.verdict_state is DalBoundaryState.REFUSED
    assert result.failure_code is not None
    assert isinstance(result.failure_code, FailureCode)
    assert result.failure_code is FailureCode.TRACE_MISSING

    # Refusal: invalid prior verdict
    result = prove_dal(42, "qatala", "phonetic://qatala")  # type: ignore[arg-type]
    assert result.verdict_state is DalBoundaryState.REFUSED
    assert result.failure_code is not None
    assert isinstance(result.failure_code, FailureCode)
    assert result.failure_code is FailureCode.GATE_REQUIRED


# ---------------------------------------------------------------------------
# 10. Candidate declaration is not semantic verdict
# ---------------------------------------------------------------------------


def test_candidate_declaration_is_not_semantic_verdict() -> None:
    """docs/26 §10 — DalOnlyCandidate is a candidate declaration,
    not a semantic verdict.

    It does not decide what the signifier means. It only declares
    that the signifier surface exists as a proven boundary-eligible
    entity.
    """
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    # The candidate carries signifier identity but no semantic content
    assert candidate.signifier_identity == "qatala"
    assert candidate.phonetic_trace_ref == "phonetic://qatala"
    assert candidate.graphic_trace_ref == "graphic://qatala"

    # No semantic/meaning attributes
    assert not hasattr(candidate, "meaning")
    assert not hasattr(candidate, "semantic_verdict")
    assert not hasattr(candidate, "dalalah")
    assert not hasattr(candidate, "ifadah")
    assert not hasattr(candidate, "hukm")

    # The verdict state is PROVEN (signifier candidacy), not a semantic state
    assert result.verdict_state.value == "PROVEN"
    # It is not "MEANINGFUL" or "SEMANTICALLY_VALID" or similar
    all_states = [s.value for s in DalBoundaryState]
    assert "MEANINGFUL" not in all_states
    assert not any("SEMANTIC" in s.upper() for s in all_states)


# ---------------------------------------------------------------------------
# Additional: prove_dal() success path validates full chain
# ---------------------------------------------------------------------------


def test_prove_dal_success_path() -> None:
    """docs/26 §1 — prove_dal() produces a valid DalBoundaryVerdict on success."""
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")

    assert isinstance(result, DalBoundaryVerdict)
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.failure_code is None
    assert result.candidate is not None
    assert isinstance(result.candidate, DalOnlyCandidate)
    assert result.candidate.signifier_identity == "qatala"
    assert result.candidate.phonetic_trace_ref == "phonetic://qatala"
    assert result.candidate.graphic_trace_ref == "graphic://qatala"
    assert result.candidate.prior_licensing_verdict is verdict
    assert result.candidate.dal_rank <= DAL_BOUNDARY_RANK_CEILING
    assert result.verdict_rank <= DAL_BOUNDARY_RANK_CEILING


def test_prove_dal_graphic_trace_may_be_empty() -> None:
    """docs/26 §2.1 — graphic_trace_ref may be empty for oral-only forms."""
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "")

    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    assert result.candidate.graphic_trace_ref == ""


def test_prove_dal_graphic_trace_default_empty() -> None:
    """docs/26 §2.1 — graphic_trace_ref defaults to empty string."""
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala")

    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    assert result.candidate.graphic_trace_ref == ""
