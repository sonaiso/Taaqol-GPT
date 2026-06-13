"""Constitutional tests for PR-16: VerbalMadlulCandidate Boundary.

Origin: docs/26, docs/27_VERBAL_MADLUL_CANDIDATE_BOUNDARY_LAW.md, docs/04.

Coverage of the 15 required constitutional tests:

1.  VerbalMadlulCandidate requires DalOnlyCandidate.
2.  Raw surface cannot produce VerbalMadlulCandidate.
3.  VerbalMadlulCandidate is not Meaning.
4.  VerbalMadlulCandidate carries no reference certainty.
5.  VerbalMadlulCandidate carries no ifadah/hukm/reality fields.
6.  VerbalMadlulCandidate does not create DalMadlulBindingCandidate.
7.  VerbalMadlulCandidate does not create RelationCandidate.
8.  correspondence_candidate is not final denotation.
9.  inclusion_candidate is not final concept.
10. iltizam_condition is a condition, not a conclusion.
11. Rank is bounded.
12. Residual governance is respected.
13. trace_ref remains reference, not ledger commit.
14. Every refusal has named FailureCode.
15. PR-16 imports/defines no ContractableUnitGeometry, ExtraLetterLicense,
    C_Aug, Ifadah, Hukm, or Reality.
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
    BoundaryEvidence,
    DalBoundaryState,
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
from taaqqul_slot_geometry.weight.verbal_madlul import (
    MADLUL_BOUNDARY_RANK_CEILING,
    MadlulBoundaryState,
    VerbalMadlulBoundaryVerdict,
    VerbalMadlulCandidate,
    prove_verbal_madlul,
)

_DOC_27 = "docs/27_VERBAL_MADLUL_CANDIDATE_BOUNDARY_LAW.md"


# ---------------------------------------------------------------------------
# Test fixtures — build a DalOnlyCandidate through the lawful chain
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr16-verbal-madlul-boundary-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr16/qatala", kind="DECLARED_ENTRY"),
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


def _dal_only_candidate() -> DalOnlyCandidate:
    """Produce a valid DalOnlyCandidate through the lawful chain."""
    verdict = _licensing_verdict()
    result = prove_dal(verdict, "qatala", "phonetic://qatala", "graphic://qatala")
    assert result.verdict_state is DalBoundaryState.PROVEN
    assert result.candidate is not None
    return result.candidate


# ---------------------------------------------------------------------------
# 0. Origin law must be present
# ---------------------------------------------------------------------------


def test_pr16_constitutional_document_is_present() -> None:
    """docs/27 — PR-16 origin law must exist."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    path = repo_root / _DOC_27
    assert path.is_file(), f"missing PR-16 origin document: {_DOC_27}"
    assert path.read_text(encoding="utf-8").strip(), f"PR-16 origin document is empty: {_DOC_27}"


# ---------------------------------------------------------------------------
# 1. VerbalMadlulCandidate requires DalOnlyCandidate
# ---------------------------------------------------------------------------


def test_verbal_madlul_requires_dal_only_candidate() -> None:
    """docs/27 §3 — VerbalMadlulCandidate requires a DalOnlyCandidate.

    prove_verbal_madlul() refuses any input that is not a DalOnlyCandidate.
    """
    dal = _dal_only_candidate()

    # Valid — should succeed
    result = prove_verbal_madlul(dal, "wad:lexical_root_qatala")
    assert result.verdict_state is MadlulBoundaryState.PROVEN

    # Invalid: raw string
    result = prove_verbal_madlul("raw_surface", "wad:test")  # type: ignore[arg-type]
    assert result.verdict_state is MadlulBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: LicensingBoundaryVerdict (must pass through prove_dal first)
    result = prove_verbal_madlul(_licensing_verdict(), "wad:test")  # type: ignore[arg-type]
    assert result.verdict_state is MadlulBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: None
    result = prove_verbal_madlul(None, "wad:test")  # type: ignore[arg-type]
    assert result.verdict_state is MadlulBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: WeightFitCandidate (too early)
    result = prove_verbal_madlul(_weight_fit_candidate(), "wad:test")  # type: ignore[arg-type]
    assert result.verdict_state is MadlulBoundaryState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED


# ---------------------------------------------------------------------------
# 2. Raw surface cannot produce VerbalMadlulCandidate
# ---------------------------------------------------------------------------


def test_raw_surface_cannot_produce_verbal_madlul() -> None:
    """docs/27 §3 — A raw surface without a dal boundary verdict is ungated.

    Birth guard: VerbalMadlulCandidate refuses construction with non-DalOnlyCandidate.
    """
    with pytest.raises(WeightCarrierSchemaError, match="GATE_REQUIRED"):
        VerbalMadlulCandidate(
            dal_only="not_a_dal_only",  # type: ignore[arg-type]
            wad_usage_boundary="wad:test",
            correspondence_candidate="",
            inclusion_candidate="",
            iltizam_condition="",
            existence_carrier_candidate="",
            event_carrier_candidate="",
            relation_affordance_candidate="",
            madlul_rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="trace://test",
        )


# ---------------------------------------------------------------------------
# 3. VerbalMadlulCandidate is not Meaning
# ---------------------------------------------------------------------------


def test_verbal_madlul_candidate_is_not_meaning() -> None:
    """docs/27 §2.2 — VerbalMadlulCandidate does NOT carry meaning.

    No field named meaning, dalalah, conceptual_meaning, final_meaning,
    or semantic_content exists on VerbalMadlulCandidate.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(dal, "wad:lexical_root_qatala")
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    fields = set(candidate.__dataclass_fields__.keys())
    forbidden_meaning_fields = {
        "meaning", "dalalah", "conceptual_meaning", "final_meaning",
        "semantic_content", "lexical_meaning", "final_denotation",
    }
    found = fields & forbidden_meaning_fields
    assert not found, f"VerbalMadlulCandidate carries forbidden meaning fields: {found}"


# ---------------------------------------------------------------------------
# 4. VerbalMadlulCandidate carries no reference certainty
# ---------------------------------------------------------------------------


def test_verbal_madlul_carries_no_reference_certainty() -> None:
    """docs/27 §2.2 — VerbalMadlulCandidate does NOT carry reference certainty.

    No field named reference, reference_certainty, final_reference,
    or denotation exists on VerbalMadlulCandidate.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(dal, "wad:lexical_root_qatala")
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    fields = set(candidate.__dataclass_fields__.keys())
    forbidden_reference_fields = {
        "reference", "reference_certainty", "final_reference",
        "denotation", "final_denotation",
    }
    found = fields & forbidden_reference_fields
    assert not found, f"VerbalMadlulCandidate carries forbidden reference fields: {found}"


# ---------------------------------------------------------------------------
# 5. VerbalMadlulCandidate carries no ifadah/hukm/reality fields
# ---------------------------------------------------------------------------


def test_verbal_madlul_carries_no_ifadah_hukm_reality() -> None:
    """docs/27 §2.2 — VerbalMadlulCandidate does NOT carry ifadah/hukm/reality.

    No field named ifadah, hukm, reality, judgment, proposition,
    application, tanzil, or truth_value exists on VerbalMadlulCandidate.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(dal, "wad:lexical_root_qatala")
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    fields = set(candidate.__dataclass_fields__.keys())
    forbidden_fields = {
        "ifadah", "hukm", "reality", "judgment", "proposition",
        "application", "tanzil", "truth_value", "agency", "patienthood",
    }
    found = fields & forbidden_fields
    assert not found, f"VerbalMadlulCandidate carries forbidden fields: {found}"


# ---------------------------------------------------------------------------
# 6. VerbalMadlulCandidate does not create DalMadlulBindingCandidate
# ---------------------------------------------------------------------------


def test_verbal_madlul_does_not_create_binding() -> None:
    """docs/27 §9 — VerbalMadlulCandidate does not create DalMadlulBindingCandidate.

    The verbal signified candidate proves signified candidacy only.
    It does not produce a binding between signifier and signified.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(dal, "wad:lexical_root_qatala")
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    # No binding field on the candidate
    fields = set(candidate.__dataclass_fields__.keys())
    forbidden_binding_fields = {
        "binding", "dal_madlul_binding", "dal_madlul_binding_candidate",
        "binding_candidate",
    }
    found = fields & forbidden_binding_fields
    assert not found, f"VerbalMadlulCandidate carries forbidden binding fields: {found}"

    # The type is VerbalMadlulCandidate, not DalMadlulBindingCandidate
    assert type(candidate).__name__ == "VerbalMadlulCandidate"


# ---------------------------------------------------------------------------
# 7. VerbalMadlulCandidate does not create RelationCandidate
# ---------------------------------------------------------------------------


def test_verbal_madlul_does_not_create_relation_candidate() -> None:
    """docs/27 §9 — VerbalMadlulCandidate does not create RelationCandidate.

    relation_affordance_candidate is a string field describing an affordance,
    not a RelationCandidate type.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(
        dal, "wad:lexical_root_qatala",
        relation_affordance_candidate="action_affordance",
    )
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    # relation_affordance_candidate is a plain string
    assert isinstance(candidate.relation_affordance_candidate, str)
    assert candidate.relation_affordance_candidate == "action_affordance"

    # The type is specifically str, not a RelationCandidate type
    assert type(candidate.relation_affordance_candidate) is str

    # The candidate type itself is VerbalMadlulCandidate
    assert type(candidate).__name__ == "VerbalMadlulCandidate"


# ---------------------------------------------------------------------------
# 8. correspondence_candidate is not final denotation
# ---------------------------------------------------------------------------


def test_correspondence_candidate_is_not_final_denotation() -> None:
    """docs/27 §10 — correspondence_candidate is not final denotation.

    It is a string candidate field, not a final reference or denotation.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(
        dal, "wad:lexical_root_qatala",
        correspondence_candidate="action_type_candidate",
    )
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    # correspondence_candidate is a plain string
    assert isinstance(candidate.correspondence_candidate, str)
    assert candidate.correspondence_candidate == "action_type_candidate"

    # No 'denotation' or 'reference' field exists
    fields = set(candidate.__dataclass_fields__.keys())
    assert "denotation" not in fields
    assert "final_denotation" not in fields
    assert "reference" not in fields


# ---------------------------------------------------------------------------
# 9. inclusion_candidate is not final concept
# ---------------------------------------------------------------------------


def test_inclusion_candidate_is_not_final_concept() -> None:
    """docs/27 §10 — inclusion_candidate is not final concept.

    It is a string candidate field, not a final concept or meaning.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(
        dal, "wad:lexical_root_qatala",
        inclusion_candidate="transitive_action_inclusion",
    )
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    # inclusion_candidate is a plain string
    assert isinstance(candidate.inclusion_candidate, str)
    assert candidate.inclusion_candidate == "transitive_action_inclusion"

    # No 'concept' or 'final_concept' field exists
    fields = set(candidate.__dataclass_fields__.keys())
    assert "concept" not in fields
    assert "final_concept" not in fields
    assert "meaning" not in fields


# ---------------------------------------------------------------------------
# 10. iltizam_condition is a condition, not a conclusion
# ---------------------------------------------------------------------------


def test_iltizam_condition_is_condition_not_conclusion() -> None:
    """docs/27 §10 — iltizam_condition is a condition, not a conclusion.

    It is a string condition field, not a final necessary consequence.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(
        dal, "wad:lexical_root_qatala",
        iltizam_condition="requires_agent_condition",
    )
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    # iltizam_condition is a plain string
    assert isinstance(candidate.iltizam_condition, str)
    assert candidate.iltizam_condition == "requires_agent_condition"

    # No 'conclusion' or 'necessary_consequence' field exists
    fields = set(candidate.__dataclass_fields__.keys())
    assert "conclusion" not in fields
    assert "necessary_consequence" not in fields
    assert "iltizam_conclusion" not in fields


# ---------------------------------------------------------------------------
# 11. Rank is bounded
# ---------------------------------------------------------------------------


def test_madlul_rank_is_bounded() -> None:
    """docs/27 §5 — VerbalMadlulCandidate.madlul_rank <= MADLUL_BOUNDARY_RANK_CEILING.

    No rank promotion beyond the ceiling, mirroring PR-15.
    """
    assert MADLUL_BOUNDARY_RANK_CEILING == DAL_BOUNDARY_RANK_CEILING
    assert MADLUL_BOUNDARY_RANK_CEILING == Rank.HYPOTHESIS

    dal = _dal_only_candidate()
    result = prove_verbal_madlul(dal, "wad:lexical_root_qatala")
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    assert result.candidate is not None
    assert result.candidate.madlul_rank <= MADLUL_BOUNDARY_RANK_CEILING
    assert result.verdict_rank <= MADLUL_BOUNDARY_RANK_CEILING

    # Birth guard: constructing with rank above ceiling fails
    with pytest.raises(WeightCarrierSchemaError, match="RANK_EXCEEDS_CEILING"):
        VerbalMadlulCandidate(
            dal_only=dal,
            wad_usage_boundary="wad:test",
            correspondence_candidate="",
            inclusion_candidate="",
            iltizam_condition="",
            existence_carrier_candidate="",
            event_carrier_candidate="",
            relation_affordance_candidate="",
            madlul_rank=Rank.LICENSED,  # above HYPOTHESIS ceiling
            residuals=(),
            trace_ref="trace://test",
        )


# ---------------------------------------------------------------------------
# 12. Residual governance is respected
# ---------------------------------------------------------------------------


def test_residual_governance_is_respected() -> None:
    """docs/27 §6 — residual governance from PR-15 is inherited.

    HIDDEN_FORBIDDEN and BLOCKING residuals refuse the candidate.
    """
    hidden_residual = Residual(
        name="hidden_test", kind=ResidualKind.HIDDEN_FORBIDDEN, visible=False
    )
    blocking_residual = Residual(
        name="blocking_test", kind=ResidualKind.BLOCKING, visible=True
    )

    # Build a DalOnlyCandidate with hidden residuals for testing
    verdict = _licensing_verdict()

    # Construct a DalOnlyCandidate carrying the residuals directly
    dal_with_hidden = DalOnlyCandidate(
        signifier_identity="qatala",
        phonetic_trace_ref="phonetic://qatala",
        graphic_trace_ref="graphic://qatala",
        prior_licensing_verdict=verdict,
        dal_rank=Rank.CANDIDATE,
        residuals=(hidden_residual,),
        trace_ref="trace://test/hidden",
    )

    result_hidden = prove_verbal_madlul(dal_with_hidden, "wad:test")
    assert result_hidden.verdict_state is MadlulBoundaryState.REFUSED
    assert result_hidden.failure_code is FailureCode.HIDDEN_RESIDUAL

    # Test with blocking residual
    dal_with_blocking = DalOnlyCandidate(
        signifier_identity="qatala",
        phonetic_trace_ref="phonetic://qatala",
        graphic_trace_ref="graphic://qatala",
        prior_licensing_verdict=verdict,
        dal_rank=Rank.CANDIDATE,
        residuals=(blocking_residual,),
        trace_ref="trace://test/blocking",
    )

    result_blocking = prove_verbal_madlul(dal_with_blocking, "wad:test")
    assert result_blocking.verdict_state is MadlulBoundaryState.REFUSED
    assert result_blocking.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


# ---------------------------------------------------------------------------
# 13. trace_ref remains reference, not ledger commit
# ---------------------------------------------------------------------------


def test_trace_ref_is_reference_not_ledger_commit() -> None:
    """docs/27 §7 — trace_ref is a reference, not an audit ledger commit.

    The trace_ref field on VerbalMadlulCandidate and
    VerbalMadlulBoundaryVerdict is a string path reference, not a
    ledger commit hash or ledger write.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(dal, "wad:lexical_root_qatala")
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    candidate = result.candidate
    assert candidate is not None

    # trace_ref is a path-like string reference
    assert isinstance(candidate.trace_ref, str)
    assert candidate.trace_ref.startswith("prove_verbal_madlul/")
    assert "ledger" not in candidate.trace_ref.lower()
    assert "commit" not in candidate.trace_ref.lower()

    # Same for the verdict
    assert isinstance(result.trace_ref, str)
    assert result.trace_ref.startswith("prove_verbal_madlul/")


# ---------------------------------------------------------------------------
# 14. Every refusal has named FailureCode
# ---------------------------------------------------------------------------


def test_every_refusal_has_named_failure_code() -> None:
    """docs/27 §8 — every refusal from prove_verbal_madlul() carries a
    named FailureCode.

    No silent None refusal. Every REFUSED verdict has a member of FailureCode.
    """
    dal = _dal_only_candidate()

    # Refusal: missing wad_usage_boundary
    result = prove_verbal_madlul(dal, "")
    assert result.verdict_state is MadlulBoundaryState.REFUSED
    assert result.failure_code is not None
    assert isinstance(result.failure_code, FailureCode)
    assert result.failure_code is FailureCode.BOUNDARY_MISSING

    # Refusal: invalid prior (not a DalOnlyCandidate)
    result = prove_verbal_madlul(42, "wad:test")  # type: ignore[arg-type]
    assert result.verdict_state is MadlulBoundaryState.REFUSED
    assert result.failure_code is not None
    assert isinstance(result.failure_code, FailureCode)
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Refusal: whitespace-only boundary
    result = prove_verbal_madlul(dal, "   ")
    assert result.verdict_state is MadlulBoundaryState.REFUSED
    assert result.failure_code is FailureCode.BOUNDARY_MISSING


# ---------------------------------------------------------------------------
# 15. PR-16 does not import or define forbidden types
# ---------------------------------------------------------------------------


def test_pr16_module_does_not_import_forbidden_types() -> None:
    """docs/27 §9 — PR-16 must not import/define ContractableUnitGeometry,
    ExtraLetterLicense, C_Aug, RelationCandidate, Ifadah, Hukm, Reality.

    Static AST check of the verbal_madlul.py module.
    """
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    verbal_madlul_path = (
        repo_root / "src" / "taaqqul_slot_geometry" / "weight" / "verbal_madlul.py"
    )
    assert verbal_madlul_path.is_file()

    source = verbal_madlul_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_names = {
        "ContractableUnitGeometry",
        "ExtraLetterLicense",
        "AugmentationCategory",
        "RelationCandidate",
        "DalMadlulBindingCandidate",
        "IfadahCandidate",
        "HukmCandidate",
        "TanzilCandidate",
        "Meaning",
        "Reality",
    }

    # Check all imported names
    imported_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name)

    found = imported_names & forbidden_names
    assert not found, f"PR-16 verbal_madlul.py imports forbidden types: {found}"

    # Check all class definitions
    defined_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            defined_names.add(node.name)

    found_defined = defined_names & forbidden_names
    assert not found_defined, (
        f"PR-16 verbal_madlul.py defines forbidden types: {found_defined}"
    )


# ---------------------------------------------------------------------------
# Additional: prove_verbal_madlul() success path validates full chain
# ---------------------------------------------------------------------------


def test_prove_verbal_madlul_success_path() -> None:
    """docs/27 §1 — prove_verbal_madlul() produces a valid
    VerbalMadlulBoundaryVerdict on success.
    """
    dal = _dal_only_candidate()
    result = prove_verbal_madlul(
        dal,
        "wad:lexical_root_qatala",
        correspondence_candidate="action_type",
        inclusion_candidate="transitive_action",
        iltizam_condition="requires_agent",
        existence_carrier_candidate="event_existence",
        event_carrier_candidate="action_event",
        relation_affordance_candidate="agent_patient_affordance",
    )

    assert isinstance(result, VerbalMadlulBoundaryVerdict)
    assert result.verdict_state is MadlulBoundaryState.PROVEN
    assert result.failure_code is None
    assert result.candidate is not None
    assert isinstance(result.candidate, VerbalMadlulCandidate)
    assert result.candidate.dal_only is dal
    assert result.candidate.wad_usage_boundary == "wad:lexical_root_qatala"
    assert result.candidate.correspondence_candidate == "action_type"
    assert result.candidate.inclusion_candidate == "transitive_action"
    assert result.candidate.iltizam_condition == "requires_agent"
    assert result.candidate.existence_carrier_candidate == "event_existence"
    assert result.candidate.event_carrier_candidate == "action_event"
    assert result.candidate.relation_affordance_candidate == "agent_patient_affordance"
    assert result.candidate.madlul_rank <= MADLUL_BOUNDARY_RANK_CEILING
    assert result.verdict_rank <= MADLUL_BOUNDARY_RANK_CEILING
