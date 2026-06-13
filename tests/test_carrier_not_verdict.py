"""Negative constitutional tests for the docs/21 Carrier Declaration Is Not Verdict Law.

PR-10B (corrective PR, no new layer) — these tests prove that the
PR-10 carrier surface cannot be misread as gate verdicts, licenses,
or judgments. Each test asserts a specific discriminating identity
from docs/21 §2–§4:

1. **PathKind is not PathGateProof** — a declared path kind does not
   license a path gate; constructing a RootStemCandidate from
   PathKind.ROOT alone (without a PathGateProof) cannot produce a
   gate verdict, and no carrier field references PathGateProof.

2. **OriginalExtraMap is not ExtraLetterLicense** — the depicted
   split of letters into original/extra does not grant augmentation
   permission; no carrier field references augmentation or license.

3. **Mizan is not weighing authority** — the imaging instrument
   carries no pattern table, no fit scorer, no weigh() authority;
   it is only a landing surface.

4. **WeightReadinessCandidate is not WeightFitCandidate** — chain
   completion does not imply weighing has occurred.

5. **Typed residuals are not residual clearance** — a declared empty
   residual tuple is not Ω governance clearing a carrier.

6. **TraceRef is not audit ledger commit** — a birth trace reference
   is not a TraceLedger append or an audit finalization.

7. **Candidate rank is not gate rank** — birth at CANDIDATE cannot be
   interpreted as a gate-level rank or promotion.

Disciplines: These are reserved-symbol / negative-shape tests under
the PR-2 construction-test discipline (``pytest.raises`` where a
construction would be needed, field-set assertions otherwise). They
produce no ``ClosureState`` verdict.
"""

from __future__ import annotations

import dataclasses
import pathlib

import pytest

from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.slot_graph import TraceRef
from taaqqul_slot_geometry.weight import (
    BIRTH_RANK_CEILING,
    PATTERN_SPACE,
    LetterStanding,
    MawzunCandidate,
    Mizan,
    OperationTraceCandidate,
    OriginalExtraMap,
    PathCandidate,
    PathKind,
    PreWeightSurface,
    RootStemCandidate,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
)

# ---------------------------------------------------------------------------
# Carrier factories (same shape as test_weight_carriers.py).
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr10b-negative-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr10b/qatala", kind="DECLARED_ENTRY"),
    }


def _syllable() -> SyllableCandidate:
    return SyllableCandidate(**_base("syllable", "syll-qa", "qa"), units=(("q", "a"),))


def _sequence() -> SyllableSequenceCandidate:
    return SyllableSequenceCandidate(
        **_base("syllable_sequence", "seq-qatala", "qa-ta-la"),
        syllables=(
            _syllable(),
            SyllableCandidate(**_base("syllable", "syll-ta", "ta"), units=(("t", "a"),)),
            SyllableCandidate(**_base("syllable", "syll-la", "la"), units=(("l", "a"),)),
        ),
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


def _root_stem() -> RootStemCandidate:
    return RootStemCandidate(**_base("root_stem", "root-qtl", "q-t-l"), path=_path())


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


def _readiness() -> WeightReadinessCandidate:
    return WeightReadinessCandidate(
        **_base("weight_readiness", "wr-qatala", "qatala"), surface=_surface()
    )


def _mawzun() -> MawzunCandidate:
    return MawzunCandidate(
        **_base("mawzun", "mz-qatala", "qatala"), readiness=_readiness()
    )


def _mizan() -> Mizan:
    return Mizan(**_base("mizan", "mizan-faala", "fa-a-la"))


# ---------------------------------------------------------------------------
# 1. PathKind is not PathGateProof (docs/21 §2, §3)
# ---------------------------------------------------------------------------


def test_path_kind_does_not_license_path_gate() -> None:
    """docs/21 §2 — PathCandidate.kind is a declared candidate kind,
    not a PathGateProof. Constructing a PathCandidate with
    PathKind.ROOT does not produce, imply, or reference a
    PathGateProof.

    Proven: no field named 'proof', 'verdict', 'gate_result', or
    'licensed' exists on PathCandidate.
    """
    path = _path(PathKind.ROOT)
    field_names = {field.name for field in dataclasses.fields(path)}

    # A PathCandidate carries: the 9 mandatory + kind + carrier
    # It does NOT carry any gate-verdict field
    gate_verdict_names = {"proof", "verdict", "gate_result", "licensed", "gate_proof"}
    leaked = field_names & gate_verdict_names
    assert not leaked, (
        f"PathCandidate carries gate-verdict fields: {sorted(leaked)} — "
        "PathKind is not PathGateProof (docs/21 §2)"
    )


def test_declared_path_kind_is_not_gate_verdict() -> None:
    """docs/21 §3 — PathCandidate(kind=ROOT) ⇏ RootPathGateProof.

    The declared kind is one of the seven path-family members, and
    its type is PathKind (an enum), never a proof, verdict, or gate
    result type. The carrier itself does not reference any gate
    authority.
    """
    path = _path(PathKind.ROOT)
    assert isinstance(path.kind, PathKind)
    assert path.kind is PathKind.ROOT

    # The kind is just an enum member — not callable, not a proof object
    assert not hasattr(path.kind, "evidence")
    assert not hasattr(path.kind, "verdict")
    assert not hasattr(path.kind, "residual_governance")


@pytest.mark.parametrize("kind", list(PathKind))
def test_no_path_kind_value_is_itself_a_gate_proof(kind: PathKind) -> None:
    """docs/21 §4 — no PathKind value, regardless of its label, may
    be treated as having gate authority."""
    # PathKind is a StrEnum: its value is a plain string
    assert isinstance(kind.value, str)
    # No PathKind member has proof-like attributes
    assert not hasattr(kind, "approve")
    assert not hasattr(kind, "promote")
    assert not hasattr(kind, "license")


# ---------------------------------------------------------------------------
# 2. OriginalExtraMap is not ExtraLetterLicense (docs/21 §2, §3)
# ---------------------------------------------------------------------------


def test_original_extra_map_does_not_license_extra_letters() -> None:
    """docs/21 §2 — OriginalExtraMap.assignments is a depicted split
    candidate, not an ExtraLetterLicense or AugmentationProof.

    Proven: no field named 'license', 'augmentation', 'permission',
    or 'proof' exists on OriginalExtraMap.
    """
    oem = _original_extra()
    field_names = {field.name for field in dataclasses.fields(oem)}

    license_names = {"license", "augmentation", "permission", "proof", "augmentation_proof"}
    leaked = field_names & license_names
    assert not leaked, (
        f"OriginalExtraMap carries license fields: {sorted(leaked)} — "
        "OriginalExtraMap is not ExtraLetterLicense (docs/21 §2)"
    )


def test_original_extra_map_depicts_standing_without_granting_permission() -> None:
    """docs/21 §3 — OriginalExtraMap(assignments=(...)) ⇏
    ExtraLetterLicense. The assignments are LetterStanding values
    (ORIGINAL/EXTRA), which are descriptive labels — not permissions.
    """
    oem = _original_extra()
    for _, standing in oem.assignments:
        assert isinstance(standing, LetterStanding)
        # LetterStanding is descriptive, not permissive
        assert not hasattr(standing, "license")
        assert not hasattr(standing, "permit")
        assert not hasattr(standing, "authorize")


# ---------------------------------------------------------------------------
# 3. Mizan is not weighing authority (docs/21 §2, §3)
# ---------------------------------------------------------------------------


def test_mizan_is_not_weighing_authority() -> None:
    """docs/21 §2 — Mizan is an image landing surface, not a weighing
    authority or fit scorer.

    Proven: Mizan has no pattern table, no weigh method, no fit
    computation, and no scoring field.
    """
    mizan = _mizan()
    field_names = {field.name for field in dataclasses.fields(mizan)}

    # Mizan carries only: the 9 mandatory + landing_space
    authority_names = {
        "pattern_table", "patterns", "weigh", "fit", "score",
        "authority", "compute", "evaluate",
    }
    leaked = field_names & authority_names
    assert not leaked, (
        f"Mizan carries authority fields: {sorted(leaked)} — "
        "Mizan is not weighing authority (docs/21 §2)"
    )

    # No callable on the Mizan (frozen dataclass, __post_init__ only)
    assert not callable(getattr(mizan, "weigh", None))
    assert not callable(getattr(mizan, "compute_fit", None))


def test_mizan_landing_space_is_not_weighing_result() -> None:
    """docs/21 §3 — Mizan(landing_space="PatternSpace") ⇏ weigh()
    authority. The landing space is a declared boundary, not a
    computation result.
    """
    mizan = _mizan()
    assert mizan.landing_space == PATTERN_SPACE
    # The landing space is a plain string constant, not a result object
    assert isinstance(mizan.landing_space, str)
    assert mizan.landing_space == "PatternSpace"


# ---------------------------------------------------------------------------
# 4. WeightReadinessCandidate is not WeightFitCandidate (docs/21 §2, §3)
# ---------------------------------------------------------------------------


def test_weight_readiness_is_not_weight_fit() -> None:
    """docs/21 §2 — WeightReadinessCandidate is a chain-completion
    declaration, not a WeightFitCandidate.

    Proven: no field named 'fit', 'weight_fit', 'result', or
    'scored' exists on WeightReadinessCandidate.
    """
    wr = _readiness()
    field_names = {field.name for field in dataclasses.fields(wr)}

    fit_names = {"fit", "weight_fit", "result", "scored", "alignment_score"}
    leaked = field_names & fit_names
    assert not leaked, (
        f"WeightReadinessCandidate carries fit fields: {sorted(leaked)} — "
        "WeightReadinessCandidate is not WeightFitCandidate (docs/21 §2)"
    )


def test_weight_readiness_does_not_imply_weight_opening() -> None:
    """docs/21 §3 — WeightReadinessCandidate(surface=...) ⇏
    WeightOpening. The Ω judgment (FunctionalClosure | WeightOpening
    | Residual) is PR-12 surface and does not exist on the carrier.
    """
    wr = _readiness()
    # No Omega-related attributes
    assert not hasattr(wr, "omega_judgment")
    assert not hasattr(wr, "weight_opening")
    assert not hasattr(wr, "functional_closure")


# ---------------------------------------------------------------------------
# 5. Typed residuals are not residual clearance (docs/21 §2, §3)
# ---------------------------------------------------------------------------


def test_typed_residual_is_not_residual_clearance() -> None:
    """docs/21 §2 — carrier.residuals is a typed residual tuple at
    birth, not ResidualGovernance or residual clearance.

    Proven: an empty residual tuple at birth does not mean "no
    residuals exist" — it means no residuals have been *declared* yet.
    The Ω governance that clears residuals is PR-12 surface.
    """
    carrier = _syllable()
    assert carrier.residuals == ()
    assert isinstance(carrier.residuals, tuple)

    # The residuals field is a plain tuple — not a governance object
    assert not hasattr(carrier.residuals, "cleared")
    assert not hasattr(carrier.residuals, "governance")
    assert not hasattr(carrier.residuals, "omega_judged")


@pytest.mark.parametrize(
    "factory",
    [_syllable, _sequence, _boundary, _word_carrier, _path,
     _root_stem, _original_extra, _operations, _surface, _readiness, _mawzun, _mizan],
    ids=["syllable", "sequence", "boundary", "word_carrier", "path",
         "root_stem", "original_extra", "operations", "surface", "readiness", "mawzun", "mizan"],
)
def test_no_carrier_residual_tuple_implies_clearance(factory: object) -> None:
    """docs/21 §3 — carrier.residuals == () ⇏ residual clearance.
    Every carrier is born with an empty residual tuple, but this
    declaration of emptiness is not a judgment of absence.
    """
    carrier = factory()  # type: ignore[operator]
    assert isinstance(carrier.residuals, tuple)
    # Residuals may yet be discovered by gates — empty at birth is
    # not equivalent to Ω clearing the carrier of all residuals


# ---------------------------------------------------------------------------
# 6. TraceRef is not audit ledger commit (docs/21 §2, §3)
# ---------------------------------------------------------------------------


def test_trace_ref_is_not_audit_ledger_commit() -> None:
    """docs/21 §2 — carrier.trace is a TraceRef at birth, not a
    TraceLedger append or audit commit.

    Proven: TraceRef is a frozen carrier with (anchor, kind); it has
    no append, commit, finalize, or ledger method.
    """
    carrier = _syllable()
    assert isinstance(carrier.trace, TraceRef)

    # TraceRef is not a ledger — it's just a reference
    assert not hasattr(carrier.trace, "append")
    assert not hasattr(carrier.trace, "commit")
    assert not hasattr(carrier.trace, "finalize")
    assert not hasattr(carrier.trace, "entries")


def test_trace_ref_anchor_is_not_ledger_entry_id() -> None:
    """docs/21 §3 — TraceRef.anchor is a declared reference string,
    not a TraceLedger entry ID or audit log position.
    """
    carrier = _syllable()
    assert isinstance(carrier.trace.anchor, str)
    assert carrier.trace.anchor.startswith("trace://")
    # The anchor is a reference string — no ledger lookup capability
    assert not hasattr(carrier.trace, "lookup")
    assert not hasattr(carrier.trace, "resolve")


# ---------------------------------------------------------------------------
# 7. Candidate rank is not gate rank (docs/21 §2, §3)
# ---------------------------------------------------------------------------


def test_candidate_birth_rank_cannot_be_interpreted_as_gate_rank() -> None:
    """docs/21 §2 — carrier.rank == Rank.CANDIDATE is a birth rank
    ceiling, not a gate-level rank or promotion.

    Proven: CANDIDATE is the lowest named rank that a carrier may
    hold at birth, and it grants nothing — no license, no approval,
    no authority.
    """
    carrier = _syllable()
    assert carrier.rank is Rank.CANDIDATE
    assert carrier.rank is BIRTH_RANK_CEILING

    # CANDIDATE is strictly below every gate-level rank
    gate_ranks = [Rank.HYPOTHESIS, Rank.LICENSED, Rank.STRONG, Rank.CERTIFICATE]
    for gate_rank in gate_ranks:
        assert carrier.rank.value < gate_rank.value, (
            f"CANDIDATE must be below {gate_rank.name} — "
            "candidate rank is not gate rank (docs/21 §2)"
        )


def test_candidate_rank_does_not_grant_any_authority() -> None:
    """docs/21 §3 — Rank.CANDIDATE ⇏ approval / license / certainty.
    The CANDIDATE rank is the entry point; it is not a destination.
    """
    assert Rank.CANDIDATE is not Rank.LICENSED
    assert Rank.CANDIDATE is not Rank.STRONG
    assert Rank.CANDIDATE is not Rank.CERTIFICATE
    # CANDIDATE has no approval semantics
    assert not hasattr(Rank.CANDIDATE, "approved")
    assert not hasattr(Rank.CANDIDATE, "licensed")


# ---------------------------------------------------------------------------
# 8. Static guard: docs/21 origin document exists (PR-1C guard shape)
# ---------------------------------------------------------------------------


def test_pr10b_constitutional_document_is_present() -> None:
    """docs/13 — a PR's origin law must exist in the repository."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    doc = "docs/21_CARRIER_DECLARATION_IS_NOT_VERDICT_LAW.md"
    path = repo_root / doc
    assert path.is_file(), f"missing PR-10B origin document: {doc}"
    assert path.read_text(encoding="utf-8").strip(), (
        f"PR-10B origin document is empty: {doc}"
    )
