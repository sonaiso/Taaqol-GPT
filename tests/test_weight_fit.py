"""Constitutional tests for PR-13: Minimal WeightFit operation.

Origin: docs/19, docs/20, docs/24_MINIMAL_WEIGHT_FIT_LAW.md.

Coverage of the 12 required constitutional tests:

1.  weigh() requires WeightReadinessCandidate.
2.  weigh() refuses PathKind.
3.  weigh() refuses PathGateVerdict.
4.  weigh() refuses raw carrier declarations.
5.  WeightFitCandidate is not LicensedWeight.
6.  WeightFitCandidate carries no meaning/hukm/reality fields.
7.  WeightFitCandidate does not license lexical/samāʿ/qiyās.
8.  WeightFitCandidate does not license extra letters.
9.  Residual governance from PR-12 is respected.
10. Rank cannot be promoted beyond PR-13 ceiling.
11. TraceRef remains reference only, not audit ledger commit.
12. No DiscoverWeightAlgorithm is introduced in PR-13.
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
    MU_CHAIN_RANK_CEILING,
    WEIGHT_FIT_RANK_CEILING,
    OmegaGovernanceState,
    PathCandidate,
    PathGateProof,
    PathKind,
    PreWeightPathGate,
    PreWeightSurface,
    ResidualGovernanceVerdict,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightFitCandidate,
    WeightFitResult,
    WeightFitState,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
    omega_governance,
    weigh,
)
from taaqqul_slot_geometry.weight.carrier_core import WeightCarrierSchemaError
from taaqqul_slot_geometry.weight.pre_weight import (
    LetterStanding,
    OperationTraceCandidate,
    OriginalExtraMap,
)

_DOC_24 = "docs/24_MINIMAL_WEIGHT_FIT_LAW.md"


# ---------------------------------------------------------------------------
# Test fixtures — reuse the same carrier factory pattern as test_mu_chain.py
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr13-weight-fit-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr13/qatala", kind="DECLARED_ENTRY"),
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


def _path(kind: PathKind = PathKind.ROOT) -> PathCandidate:
    return PathCandidate(
        **_base("path", "path-qatala", "root_path"), kind=kind, carrier=_word_carrier()
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


def _granted_governance() -> ResidualGovernanceVerdict:
    """A GRANTED Ω governance verdict with no residuals."""
    return omega_governance((), Rank.CANDIDATE)


# ---------------------------------------------------------------------------
# 0. The origin law must be present.
# ---------------------------------------------------------------------------


def test_pr13_constitutional_document_is_present() -> None:
    """docs/24 — PR-13 origin law must exist."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    path = repo_root / _DOC_24
    assert path.is_file(), f"missing PR-13 origin document: {_DOC_24}"
    assert path.read_text(encoding="utf-8").strip(), f"PR-13 origin document is empty: {_DOC_24}"


# ---------------------------------------------------------------------------
# 1. weigh() requires WeightReadinessCandidate.
# ---------------------------------------------------------------------------


def test_weigh_requires_weight_readiness_candidate() -> None:
    """docs/24 §2.2 — weigh() accepts ONLY a WeightReadinessCandidate."""
    governance = _granted_governance()
    candidate = _weight_readiness()

    # Valid input — should succeed
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED
    assert result.candidate is not None
    assert isinstance(result.candidate, WeightFitCandidate)

    # Invalid: plain string
    result = weigh("not_a_candidate", governance)  # type: ignore[arg-type]
    assert result.state is WeightFitState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED

    # Invalid: None
    result = weigh(None, governance)  # type: ignore[arg-type]
    assert result.state is WeightFitState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED


# ---------------------------------------------------------------------------
# 2. weigh() refuses PathKind.
# ---------------------------------------------------------------------------


def test_weigh_refuses_path_kind() -> None:
    """docs/24 §2.2 — weigh() refuses PathKind values."""
    governance = _granted_governance()
    result = weigh(PathKind.ROOT, governance)  # type: ignore[arg-type]
    assert result.state is WeightFitState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED


# ---------------------------------------------------------------------------
# 3. weigh() refuses PathGateVerdict.
# ---------------------------------------------------------------------------


def test_weigh_refuses_path_gate_verdict() -> None:
    """docs/24 §2.2 — weigh() refuses PathGateVerdict values."""
    governance = _granted_governance()
    gate = PreWeightPathGate(name="test_gate", gate_rank=Rank.HYPOTHESIS)
    proof = PathGateProof(
        claimed_kind=PathKind.ROOT,
        evidence_surface="trilateral derivation",
        evidence_rank=Rank.HYPOTHESIS,
        domain="arabic_morphophonology",
    )
    verdict = gate.decide(_word_carrier(), proof)
    result = weigh(verdict, governance)  # type: ignore[arg-type]
    assert result.state is WeightFitState.REFUSED
    assert result.failure_code is FailureCode.GATE_REQUIRED


# ---------------------------------------------------------------------------
# 4. weigh() refuses raw carrier declarations.
# ---------------------------------------------------------------------------


def test_weigh_refuses_raw_carriers() -> None:
    """docs/24 §2.2 — weigh() refuses raw pre-weight carriers."""
    governance = _granted_governance()

    # SyllableCandidate
    result = weigh(_syllable(), governance)  # type: ignore[arg-type]
    assert result.state is WeightFitState.REFUSED

    # WordCarrierCandidate
    result = weigh(_word_carrier(), governance)  # type: ignore[arg-type]
    assert result.state is WeightFitState.REFUSED

    # PreWeightSurface (not wrapped in readiness)
    result = weigh(_surface(), governance)  # type: ignore[arg-type]
    assert result.state is WeightFitState.REFUSED

    # PathCandidate
    result = weigh(_path(), governance)  # type: ignore[arg-type]
    assert result.state is WeightFitState.REFUSED


# ---------------------------------------------------------------------------
# 5. WeightFitCandidate is not LicensedWeight.
# ---------------------------------------------------------------------------


def test_weight_fit_candidate_is_not_licensed_weight() -> None:
    """docs/24 §1 — WeightFitCandidate ≠ LicensedWeight.

    The module must not define, export, or reference LicensedWeight.
    WeightFitCandidate is a bounded fit assessment, not a license.
    """
    # Static proof: module does not define LicensedWeight
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/weight_fit.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "LicensedWeight" not in class_names, (
        "PR-13 must not define LicensedWeight"
    )

    # Runtime proof: WeightFitCandidate has no 'licensed' or 'weight_license' field
    candidate = _weight_readiness()
    governance = _granted_governance()
    result = weigh(candidate, governance)
    assert result.candidate is not None
    fit = result.candidate
    assert not hasattr(fit, "license")
    assert not hasattr(fit, "weight_license")
    assert not hasattr(fit, "licensed_weight")


# ---------------------------------------------------------------------------
# 6. WeightFitCandidate carries no meaning/hukm/reality fields.
# ---------------------------------------------------------------------------


def test_weight_fit_candidate_no_meaning_hukm_reality() -> None:
    """docs/24 §3.1 — WeightFitCandidate has no meaning/hukm/reality."""
    candidate = _weight_readiness()
    governance = _granted_governance()
    result = weigh(candidate, governance)
    fit = result.candidate
    assert fit is not None

    forbidden_fields = [
        "meaning", "madlul", "dalalah", "dalālah",
        "agency", "patienthood", "fāʿil", "mafʿūl",
        "hukm", "iʿrāb", "reality", "real_events",
    ]
    for field in forbidden_fields:
        assert not hasattr(fit, field), (
            f"WeightFitCandidate must not carry '{field}' (docs/24 §3.1)"
        )


# ---------------------------------------------------------------------------
# 7. WeightFitCandidate does not license lexical/samāʿ/qiyās.
# ---------------------------------------------------------------------------


def test_weight_fit_candidate_no_lexical_samaa_qiyas() -> None:
    """docs/24 §3.1 — WeightFitCandidate does not license lexical/samāʿ/qiyās."""
    candidate = _weight_readiness()
    governance = _granted_governance()
    result = weigh(candidate, governance)
    fit = result.candidate
    assert fit is not None

    forbidden_fields = [
        "lexical_entry", "samaa", "samāʿ", "qiyas", "qiyās",
        "lexical_license", "samaa_attestation", "qiyas_derivation",
    ]
    for field in forbidden_fields:
        assert not hasattr(fit, field), (
            f"WeightFitCandidate must not carry '{field}' (docs/24 §3.1)"
        )


# ---------------------------------------------------------------------------
# 8. WeightFitCandidate does not license extra letters.
# ---------------------------------------------------------------------------


def test_weight_fit_candidate_no_extra_letter_license() -> None:
    """docs/24 §3.1 — WeightFitCandidate does not license extra letters."""
    candidate = _weight_readiness()
    governance = _granted_governance()
    result = weigh(candidate, governance)
    fit = result.candidate
    assert fit is not None

    forbidden_fields = [
        "extra_letter_license", "extra_letters", "augmentation",
        "augmentation_category", "c_aug",
    ]
    for field in forbidden_fields:
        assert not hasattr(fit, field), (
            f"WeightFitCandidate must not carry '{field}' (docs/24 §3.1)"
        )


# ---------------------------------------------------------------------------
# 9. Residual governance from PR-12 is respected.
# ---------------------------------------------------------------------------


def test_residual_governance_respected_hidden() -> None:
    """docs/24 §5 — HIDDEN_FORBIDDEN governance → REFUSED."""
    hidden = Residual(name="hidden_danger", kind=ResidualKind.HIDDEN_FORBIDDEN, visible=False)
    governance = omega_governance((hidden,), Rank.CANDIDATE)
    assert governance.state is OmegaGovernanceState.REJECTED

    candidate = _weight_readiness()
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.REFUSED
    assert result.failure_code is FailureCode.HIDDEN_RESIDUAL


def test_residual_governance_respected_blocking() -> None:
    """docs/24 §5 — BLOCKING governance → REFUSED."""
    blocking = Residual(name="blocker", kind=ResidualKind.BLOCKING, visible=True)
    governance = omega_governance((blocking,), Rank.CANDIDATE)
    assert governance.state is OmegaGovernanceState.BLOCKED

    candidate = _weight_readiness()
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.REFUSED
    assert result.failure_code is FailureCode.BLOCKING_RESIDUAL_PRESENT


def test_residual_governance_respected_deferrable() -> None:
    """docs/24 §5 — DEFERRABLE governance → DEFERRED."""
    deferrable = Residual(name="deferred_item", kind=ResidualKind.DEFERRABLE, visible=True)
    governance = omega_governance((deferrable,), Rank.CANDIDATE)
    assert governance.state is OmegaGovernanceState.DEFERRED

    candidate = _weight_readiness()
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.DEFERRED
    assert result.failure_code is FailureCode.GATE_REQUIRED


def test_residual_governance_non_blocking_passes() -> None:
    """docs/24 §5 — NON_BLOCKING governance → FITTED with residual visible."""
    non_blocking = Residual(name="visible_remainder", kind=ResidualKind.NON_BLOCKING, visible=True)
    governance = omega_governance((non_blocking,), Rank.CANDIDATE)
    assert governance.state is OmegaGovernanceState.GRANTED

    candidate = _weight_readiness()
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED
    assert result.candidate is not None
    # Residual is carried, not erased
    assert len(result.residuals) == 1
    assert result.residuals[0].visible is True


# ---------------------------------------------------------------------------
# 10. Rank cannot be promoted beyond PR-13 ceiling.
# ---------------------------------------------------------------------------


def test_rank_bounded_by_ceiling() -> None:
    """docs/24 §4 — rank never exceeds WEIGHT_FIT_RANK_CEILING."""
    # WEIGHT_FIT_RANK_CEILING equals MU_CHAIN_RANK_CEILING = Rank.HYPOTHESIS
    assert WEIGHT_FIT_RANK_CEILING == MU_CHAIN_RANK_CEILING

    candidate = _weight_readiness()
    governance = _granted_governance()
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED
    assert result.rank <= WEIGHT_FIT_RANK_CEILING
    assert result.candidate is not None
    assert result.candidate.fit_rank <= WEIGHT_FIT_RANK_CEILING


def test_weight_fit_candidate_refuses_rank_above_ceiling() -> None:
    """docs/24 §4 — WeightFitCandidate birth refuses rank above ceiling."""
    candidate = _weight_readiness()
    with pytest.raises(WeightCarrierSchemaError, match="RANK_EXCEEDS_CEILING"):
        WeightFitCandidate(
            **_base("weight_fit", "fit-test", "fit_assessed"),
            source=candidate,
            fit_verdict="pattern_fit_assessed",
            fit_rank=Rank.LICENSED,  # Above HYPOTHESIS ceiling
        )


# ---------------------------------------------------------------------------
# 11. TraceRef remains reference only, not audit ledger commit.
# ---------------------------------------------------------------------------


def test_trace_ref_is_reference_not_ledger_commit() -> None:
    """docs/24 §6 — trace_ref in WeightFitResult is a reference only.

    It documents the decision path, not a ledger write.
    It does not reference an audit ledger commit.
    """
    candidate = _weight_readiness()
    governance = _granted_governance()
    result = weigh(candidate, governance)
    assert result.state is WeightFitState.FITTED

    # trace_ref is a string reference
    assert isinstance(result.trace_ref, str)
    assert result.trace_ref.strip()

    # It does not claim to be a ledger commit
    assert "ledger_commit" not in result.trace_ref.lower()
    assert "audit_write" not in result.trace_ref.lower()

    # The candidate's trace is a TraceRef (opaque anchor), not a ledger entry
    assert isinstance(result.candidate.trace, TraceRef)


# ---------------------------------------------------------------------------
# 12. No DiscoverWeightAlgorithm is introduced in PR-13.
# ---------------------------------------------------------------------------


def test_no_discover_weight_algorithm() -> None:
    """docs/24 §7 — PR-13 does not introduce DiscoverWeightAlgorithm.

    Static proof: the weight_fit module does not define or reference
    DiscoverWeightAlgorithm as a class or function.
    """
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/weight_fit.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # No class named DiscoverWeightAlgorithm
    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "DiscoverWeightAlgorithm" not in class_names

    # No function named discover_weight or discover_algorithm
    func_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    }
    assert "discover_weight" not in func_names
    assert "discover_algorithm" not in func_names

    # No import of DiscoverWeightAlgorithm
    import_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                import_names.add(alias.name)
    assert "DiscoverWeightAlgorithm" not in import_names


# ---------------------------------------------------------------------------
# Additional negative tests — boundary proofs
# ---------------------------------------------------------------------------


def test_no_weight_family_candidate() -> None:
    """docs/24 §7 — PR-13 does not introduce WeightFamilyCandidate."""
    module_path = pathlib.Path(__file__).resolve().parent.parent / (
        "src/taaqqul_slot_geometry/weight/weight_fit.py"
    )
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    assert "WeightFamilyCandidate" not in class_names


def test_weigh_result_states_invariants() -> None:
    """docs/24 §2.4 — WeightFitResult state invariants are enforced."""
    # FITTED must have candidate
    with pytest.raises(WeightCarrierSchemaError):
        WeightFitResult(
            state=WeightFitState.FITTED,
            failure_code=None,
            candidate=None,
            rank=Rank.CANDIDATE,
            residuals=(),
            trace_ref="test/invariant",
        )

    # REFUSED must have failure_code
    with pytest.raises(WeightCarrierSchemaError):
        WeightFitResult(
            state=WeightFitState.REFUSED,
            failure_code=None,
            candidate=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/invariant",
        )

    # DEFERRED must have failure_code
    with pytest.raises(WeightCarrierSchemaError):
        WeightFitResult(
            state=WeightFitState.DEFERRED,
            failure_code=None,
            candidate=None,
            rank=Rank.ZERO,
            residuals=(),
            trace_ref="test/invariant",
        )
