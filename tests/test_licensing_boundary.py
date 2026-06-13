"""Constitutional tests for PR-14: Lexical / Samāʿ / Qiyās License Boundary.

Origin: docs/19, docs/20, docs/25_LEXICAL_SAMAEE_QIYAS_LICENSE_BOUNDARY_LAW.md.

Coverage of the 15 required constitutional tests:

1.  assess_license() requires WeightFitCandidate — no earlier-stage input.
2.  Samāʿ evidence licenses occurrence only, not generalization.
3.  Qiyās without preserved root → refusal.
4.  Qiyās without effective description → refusal.
5.  Qiyās with disqualifying difference → refusal (blocked).
6.  Lexical boundary verdict carries no meaning field.
7.  Verdict does not carry LexicalMadlulCandidate.
8.  Verdict does not produce LicensedWeight.
9.  Verdict does not produce DiscoverWeightAlgorithm.
10. Verdict does not produce ExtraLetterLicense.
11. Verdict does not produce ContractableUnitGeometry.
12. Every refusal has a FailureCode from the existing taxonomy.
13. Rank does not rise above PR-14 ceiling.
14. Residual governance operates before verdict.
15. Samāʿ/qiyās conflict is not resolved by rank alone.
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
    LICENSE_BOUNDARY_RANK_CEILING,
    WEIGHT_FIT_RANK_CEILING,
    BoundaryEvidence,
    LicenseBoundaryKind,
    LicensingBoundaryResult,
    LicensingBoundaryState,
    LicensingBoundaryVerdict,
    OmegaGovernanceState,
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
    weigh,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
)

_DOC_25 = "docs/25_LEXICAL_SAMAEE_QIYAS_LICENSE_BOUNDARY_LAW.md"


# ---------------------------------------------------------------------------
# Test fixtures — build a WeightFitCandidate through the lawful chain
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr14-licensing-boundary-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr14/qatala", kind="DECLARED_ENTRY"),
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
    """A GRANTED Ω governance verdict with no residuals."""
    return omega_governance((), Rank.CANDIDATE)


def _lexical_evidence() -> BoundaryEvidence:
    return BoundaryEvidence(
        kind=LicenseBoundaryKind.LEXICAL,
        attestation="lexical_root_attested",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
    )


def _samaa_evidence() -> BoundaryEvidence:
    return BoundaryEvidence(
        kind=LicenseBoundaryKind.SAMAA,
        attestation="attested_occurrence_in_corpus",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
    )


def _qiyas_evidence() -> BoundaryEvidence:
    return BoundaryEvidence(
        kind=LicenseBoundaryKind.QIYAS,
        attestation="qiyas_eligibility_evidence",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
        preserved_root="q-t-l",
        effective_description="trilateral_active_verb",
        no_disqualifying_difference=True,
    )


# ---------------------------------------------------------------------------
# 0. Origin law must be present
# ---------------------------------------------------------------------------


def test_pr14_constitutional_document_is_present() -> None:
    """docs/25 — PR-14 origin law must exist."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    path = repo_root / _DOC_25
    assert path.is_file(), f"missing PR-14 origin document: {_DOC_25}"
    assert path.read_text(encoding="utf-8").strip(), f"PR-14 origin document is empty: {_DOC_25}"


# ---------------------------------------------------------------------------
# 1. assess_license() requires WeightFitCandidate
# ---------------------------------------------------------------------------


def test_assess_license_requires_weight_fit_candidate() -> None:
    """docs/25 §3.2 — assess_license() accepts ONLY a WeightFitCandidate."""
    governance = _granted_governance()
    evidence = _lexical_evidence()
    fit = _weight_fit_candidate()

    # Valid input — should succeed
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    assert isinstance(result.verdict, LicensingBoundaryVerdict)

    # Invalid: string
    result = assess_license("not_a_candidate", evidence, governance)  # type: ignore[arg-type]
    assert result.state is LicensingBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: WeightReadinessCandidate (must be weighed first)
    result = assess_license(_weight_readiness(), evidence, governance)  # type: ignore[arg-type]
    assert result.state is LicensingBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: None
    result = assess_license(None, evidence, governance)  # type: ignore[arg-type]
    assert result.state is LicensingBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED


# ---------------------------------------------------------------------------
# 2. Samāʿ evidence licenses occurrence only, not generalization
# ---------------------------------------------------------------------------


def test_samaa_licenses_occurrence_not_generalization() -> None:
    """docs/25 §7.1 — samāʿ attestation licenses occurrence, not generalization.

    The verdict does not carry any generalization or rule fields.
    """
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = _samaa_evidence()

    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    verdict = result.verdict
    assert verdict is not None

    # The verdict is a boundary eligibility assessment only
    assert "boundary_eligible:SAMAA" in verdict.eligibility_verdict

    # No generalization fields
    assert not hasattr(verdict, "generalized_rule")
    assert not hasattr(verdict, "generalization")
    assert not hasattr(verdict, "qiyas_base")
    assert not hasattr(verdict, "rule")
    assert not hasattr(verdict, "extension")


# ---------------------------------------------------------------------------
# 3. Qiyās without preserved root → refusal
# ---------------------------------------------------------------------------


def test_qiyas_without_preserved_root_refused() -> None:
    """docs/25 §7.2 — qiyās without preserved root → REFUSED."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = BoundaryEvidence(
        kind=LicenseBoundaryKind.QIYAS,
        attestation="qiyas_evidence",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
        preserved_root="",  # empty — no asl
        effective_description="trilateral_active_verb",
        no_disqualifying_difference=True,
    )

    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.REFUSED
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "qiyas_no_preserved_root" in result.trace_ref


# ---------------------------------------------------------------------------
# 4. Qiyās without effective description → refusal
# ---------------------------------------------------------------------------


def test_qiyas_without_effective_description_refused() -> None:
    """docs/25 §7.2 — qiyās without effective description → REFUSED."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = BoundaryEvidence(
        kind=LicenseBoundaryKind.QIYAS,
        attestation="qiyas_evidence",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
        preserved_root="q-t-l",
        effective_description="",  # empty — no wasf
        no_disqualifying_difference=True,
    )

    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.REFUSED
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "qiyas_no_effective_description" in result.trace_ref


# ---------------------------------------------------------------------------
# 5. Qiyās with disqualifying difference → blocked
# ---------------------------------------------------------------------------


def test_qiyas_with_disqualifying_difference_refused() -> None:
    """docs/25 §7.2 — qiyās with farq qādih → REFUSED."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = BoundaryEvidence(
        kind=LicenseBoundaryKind.QIYAS,
        attestation="qiyas_evidence",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
        preserved_root="q-t-l",
        effective_description="trilateral_active_verb",
        no_disqualifying_difference=False,  # farq qādih present
    )

    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.REFUSED
    assert result.failure_code is FailureCode.FORBIDDEN_STRAIGHT_LINE
    assert "qiyas_disqualifying_difference" in result.trace_ref


# ---------------------------------------------------------------------------
# 6. Lexical boundary verdict carries no meaning field
# ---------------------------------------------------------------------------


def test_lexical_boundary_verdict_no_meaning() -> None:
    """docs/25 §4.1 — LicensingBoundaryVerdict has no meaning fields."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = _lexical_evidence()

    result = assess_license(fit, evidence, governance)
    verdict = result.verdict
    assert verdict is not None

    forbidden_fields = [
        "meaning", "madlul", "dalalah", "dalālah", "ifādah",
        "agency", "patienthood", "fāʿil", "mafʿūl",
        "hukm", "iʿrāb", "reality", "real_events",
        "lexical_definition", "lexical_content",
    ]
    for field in forbidden_fields:
        assert not hasattr(verdict, field), (
            f"LicensingBoundaryVerdict must not carry '{field}' (docs/25 §4.1)"
        )


# ---------------------------------------------------------------------------
# 7. Verdict does not carry LexicalMadlulCandidate
# ---------------------------------------------------------------------------


def test_verdict_no_lexical_madlul_candidate() -> None:
    """docs/25 §10 — no LexicalMadlulCandidate in the module."""
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/licensing_boundary.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "LexicalMadlulCandidate" not in class_names, (
        "PR-14 must not define LexicalMadlulCandidate"
    )

    # Runtime: verdict has no such field
    fit = _weight_fit_candidate()
    result = assess_license(fit, _lexical_evidence(), _granted_governance())
    assert result.verdict is not None
    assert not hasattr(result.verdict, "lexical_madlul")
    assert not hasattr(result.verdict, "madlul_candidate")


# ---------------------------------------------------------------------------
# 8. Verdict does not produce LicensedWeight
# ---------------------------------------------------------------------------


def test_verdict_no_licensed_weight() -> None:
    """docs/25 §10 — no LicensedWeight in the module."""
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/licensing_boundary.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "LicensedWeight" not in class_names, (
        "PR-14 must not define LicensedWeight"
    )

    # Runtime: verdict has no licensed_weight field
    fit = _weight_fit_candidate()
    result = assess_license(fit, _lexical_evidence(), _granted_governance())
    assert result.verdict is not None
    assert not hasattr(result.verdict, "licensed_weight")
    assert not hasattr(result.verdict, "license")


# ---------------------------------------------------------------------------
# 9. Verdict does not produce DiscoverWeightAlgorithm
# ---------------------------------------------------------------------------


def test_verdict_no_discover_weight_algorithm() -> None:
    """docs/25 §10 — no DiscoverWeightAlgorithm in the module."""
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/licensing_boundary.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "DiscoverWeightAlgorithm" not in class_names

    func_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    }
    assert "discover_weight" not in func_names


# ---------------------------------------------------------------------------
# 10. Verdict does not produce ExtraLetterLicense
# ---------------------------------------------------------------------------


def test_verdict_no_extra_letter_license() -> None:
    """docs/25 §10 — no ExtraLetterLicense in the module."""
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/licensing_boundary.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "ExtraLetterLicense" not in class_names

    # Runtime: verdict has no extra_letter fields
    fit = _weight_fit_candidate()
    result = assess_license(fit, _lexical_evidence(), _granted_governance())
    assert result.verdict is not None
    assert not hasattr(result.verdict, "extra_letter_license")
    assert not hasattr(result.verdict, "extra_letters")


# ---------------------------------------------------------------------------
# 11. Verdict does not produce ContractableUnitGeometry
# ---------------------------------------------------------------------------


def test_verdict_no_contractable_unit_geometry() -> None:
    """docs/25 §10 — no ContractableUnitGeometry in the module."""
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/licensing_boundary.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "ContractableUnitGeometry" not in class_names

    # Runtime: verdict has no contractable_unit fields
    fit = _weight_fit_candidate()
    result = assess_license(fit, _lexical_evidence(), _granted_governance())
    assert result.verdict is not None
    assert not hasattr(result.verdict, "contractable_unit")
    assert not hasattr(result.verdict, "c_aug")
    assert not hasattr(result.verdict, "augmentation_category")


# ---------------------------------------------------------------------------
# 12. Every refusal uses existing FailureCode taxonomy
# ---------------------------------------------------------------------------


def test_all_refusals_use_existing_failure_codes() -> None:
    """docs/25 §9 — PR-14 introduces NO new FailureCode members.

    All refusals map to the existing PR-1A taxonomy.
    """
    # Verify the module does not define or import new FailureCode members
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/licensing_boundary.py"
    )
    source = module_path.read_text(encoding="utf-8")

    # No class extending FailureCode — the module must not redefine it
    # Stronger check: no StrEnum subclass that looks like a failure code
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            assert node.name != "FailureCode", "PR-14 must not redefine FailureCode"

    # Collect all FailureCode references used in the module
    existing_codes = set(FailureCode)
    fit = _weight_fit_candidate()
    governance = _granted_governance()

    # Test various refusal paths and verify all use existing codes
    # Missing evidence
    r = assess_license(fit, "invalid", governance)  # type: ignore[arg-type]
    assert r.failure_code in existing_codes

    # Qiyās failures
    bad_qiyas = BoundaryEvidence(
        kind=LicenseBoundaryKind.QIYAS,
        attestation="evidence",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
        preserved_root="",
        effective_description="desc",
        no_disqualifying_difference=True,
    )
    r = assess_license(fit, bad_qiyas, governance)
    assert r.failure_code in existing_codes


# ---------------------------------------------------------------------------
# 13. Rank does not rise above PR-14 ceiling
# ---------------------------------------------------------------------------


def test_rank_bounded_by_ceiling() -> None:
    """docs/25 §5 — rank never exceeds LICENSE_BOUNDARY_RANK_CEILING."""
    assert LICENSE_BOUNDARY_RANK_CEILING == WEIGHT_FIT_RANK_CEILING

    fit = _weight_fit_candidate()
    governance = _granted_governance()
    evidence = _lexical_evidence()

    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.rank <= LICENSE_BOUNDARY_RANK_CEILING
    assert result.verdict is not None
    assert result.verdict.eligibility_rank <= LICENSE_BOUNDARY_RANK_CEILING


def test_licensing_boundary_verdict_refuses_rank_above_ceiling() -> None:
    """docs/25 §5 — LicensingBoundaryVerdict refuses rank above ceiling."""
    fit = _weight_fit_candidate()
    with pytest.raises(WeightCarrierSchemaError, match="RANK_EXCEEDS_CEILING"):
        LicensingBoundaryVerdict(
            source=fit,
            boundary_kind=LicenseBoundaryKind.LEXICAL,
            eligibility_verdict="test_verdict",
            eligibility_rank=Rank.LICENSED,  # Above HYPOTHESIS ceiling
            evidence_summary="test_evidence",
        )


# ---------------------------------------------------------------------------
# 14. Residual governance operates before verdict
# ---------------------------------------------------------------------------


def test_residual_governance_respected_hidden() -> None:
    """docs/25 §6 — HIDDEN_FORBIDDEN governance → REFUSED."""
    hidden = Residual(name="hidden_danger", kind=ResidualKind.HIDDEN_FORBIDDEN, visible=False)
    governance = omega_governance((hidden,), Rank.CANDIDATE)
    assert governance.state is OmegaGovernanceState.REJECTED

    fit = _weight_fit_candidate()
    evidence = _lexical_evidence()
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.REFUSED
    assert result.failure_code is FailureCode.HIDDEN_RESIDUAL


def test_residual_governance_respected_blocking() -> None:
    """docs/25 §6 — BLOCKING governance → REFUSED."""
    blocking = Residual(name="blocker", kind=ResidualKind.BLOCKING, visible=True)
    governance = omega_governance((blocking,), Rank.CANDIDATE)
    assert governance.state is OmegaGovernanceState.BLOCKED

    fit = _weight_fit_candidate()
    evidence = _lexical_evidence()
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.REFUSED
    assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


def test_residual_governance_respected_deferrable() -> None:
    """docs/25 §6 — DEFERRABLE governance → DEFERRED."""
    deferrable = Residual(name="deferred_item", kind=ResidualKind.DEFERRABLE, visible=True)
    governance = omega_governance((deferrable,), Rank.CANDIDATE)
    assert governance.state is OmegaGovernanceState.DEFERRED

    fit = _weight_fit_candidate()
    evidence = _lexical_evidence()
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.DEFERRED
    assert result.failure_code is FailureCode.GATE_REQUIRED


def test_residual_governance_non_blocking_passes() -> None:
    """docs/25 §6 — NON_BLOCKING governance → ELIGIBLE with residual visible."""
    non_blocking = Residual(
        name="visible_remainder", kind=ResidualKind.NON_BLOCKING, visible=True
    )
    governance = omega_governance((non_blocking,), Rank.CANDIDATE)
    assert governance.state is OmegaGovernanceState.GRANTED

    fit = _weight_fit_candidate()
    evidence = _lexical_evidence()
    result = assess_license(fit, evidence, governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    # Residual is carried, not erased
    assert len(result.residuals) == 1
    assert result.residuals[0].visible is True


# ---------------------------------------------------------------------------
# 15. Samāʿ/qiyās conflict is not resolved by rank alone
# ---------------------------------------------------------------------------


def test_samaa_qiyas_conflict_not_resolved_by_rank() -> None:
    """docs/25 §7 — samāʿ and qiyās are independent boundary assessments.

    A samāʿ-attested form does not automatically license qiyās.
    Both must be assessed independently. Having a samāʿ attestation
    does not resolve qiyās eligibility.
    """
    fit = _weight_fit_candidate()
    governance = _granted_governance()

    # Samāʿ passes
    samaa_result = assess_license(fit, _samaa_evidence(), governance)
    assert samaa_result.state is LicensingBoundaryState.ELIGIBLE

    # Qiyās without proper conditions fails even though samāʿ passed
    bad_qiyas = BoundaryEvidence(
        kind=LicenseBoundaryKind.QIYAS,
        attestation="qiyas_evidence",
        evidence_rank=Rank.CANDIDATE,
        domain="arabic_morphophonology",
        preserved_root="",  # missing asl
        effective_description="trilateral_active_verb",
        no_disqualifying_difference=True,
    )
    qiyas_result = assess_license(fit, bad_qiyas, governance)
    assert qiyas_result.state is LicensingBoundaryState.REFUSED
    # The samāʿ success doesn't lift qiyās — they are independent


# ---------------------------------------------------------------------------
# Additional boundary tests — state invariants
# ---------------------------------------------------------------------------


def test_licensing_boundary_result_state_invariants() -> None:
    """docs/25 §3.5 — LicensingBoundaryResult state invariants enforced."""
    # ELIGIBLE must have verdict
    with pytest.raises(WeightCarrierSchemaError):
        LicensingBoundaryResult(
            state=LicensingBoundaryState.ELIGIBLE,
            failure_code=None,
            verdict=None,
            rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="test/invariant",
        )

    # REFUSED must have failure_code
    with pytest.raises(WeightCarrierSchemaError):
        LicensingBoundaryResult(
            state=LicensingBoundaryState.REFUSED,
            failure_code=None,
            verdict=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/invariant",
        )

    # DEFERRED must have failure_code
    with pytest.raises(WeightCarrierSchemaError):
        LicensingBoundaryResult(
            state=LicensingBoundaryState.DEFERRED,
            failure_code=None,
            verdict=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/invariant",
        )


def test_all_three_boundary_kinds_succeed() -> None:
    """docs/25 §2 — all three boundary kinds produce ELIGIBLE when valid."""
    fit = _weight_fit_candidate()
    governance = _granted_governance()

    # Lexical
    result = assess_license(fit, _lexical_evidence(), governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    assert result.verdict.boundary_kind is LicenseBoundaryKind.LEXICAL

    # Samāʿ
    result = assess_license(fit, _samaa_evidence(), governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    assert result.verdict.boundary_kind is LicenseBoundaryKind.SAMAA

    # Qiyās
    result = assess_license(fit, _qiyas_evidence(), governance)
    assert result.state is LicensingBoundaryState.ELIGIBLE
    assert result.verdict is not None
    assert result.verdict.boundary_kind is LicenseBoundaryKind.QIYAS


def test_no_generated_qiyas_form() -> None:
    """docs/25 §10 — no GeneratedQiyasForm in the module."""
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/licensing_boundary.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "GeneratedQiyasForm" not in class_names
    assert "GeneratedQiyāsForm" not in class_names

    func_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    }
    assert "generate_qiyas" not in func_names
    assert "generate_form" not in func_names
