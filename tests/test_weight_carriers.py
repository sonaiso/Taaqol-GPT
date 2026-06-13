"""Constitutional tests for the PR-10 weight + pre-weight carrier surface.

Coverage mirrors the docs/14 *PR-10* row and the two laws it binds:

1.  **The origin laws are present** (docs/13 — the PR-1C guard
    shape): ``docs/19_ARABIC_WEIGHT_BOUNDARY_LAW.md`` and
    ``docs/20_PRE_WEIGHT_LICENSING_LAW.md`` exist and are non-empty.
2.  **The nine-field carrier law** (docs/14 — PR-10): every carrier
    is a frozen dataclass carrying value, type, origin, identity,
    domain, scope, rank, residuals, trace — and refuses each missing
    axis at birth with a named :class:`FailureCode`.
3.  **The input boundary** (docs/20 §1): :class:`MawzunCandidate`
    exists only on a licensed :class:`WeightReadinessCandidate`;
    a raw word, a surface, a syllable, or a root is refused as
    ``UNLICENSED_OPENING``.
4.  **The output boundary** (docs/19 §2, §4): every imaging carrier
    lands in PatternSpace and nowhere else; a different landing
    space is the registered straight line *Weight → Meaning* and is
    refused as ``FORBIDDEN_STRAIGHT_LINE``.
5.  **The stage order** (docs/20 §3–§11): every chain carrier
    refuses a skipped or untyped predecessor (``GATE_REQUIRED``),
    and a root standing on a non-ROOT path is the registered
    straight line of docs/20 §8/§12.
6.  **Carriers only** (docs/14 — PR-10 Forbidden): static AST
    guards — in the shape the suite already uses for the audit and
    adapter layers — prove the weight package defines no callable
    but ``__post_init__`` birth guards, holds no meaning / agency /
    hukm / reality field, binds none of the reserved PR-11/12/13/14
    names, and never touches the adapter or audit layers in either
    direction.

Disciplines: PR-10 ships no ``Γ``, no ``Ω``, no gate, and produces
no :class:`ClosureState` verdict, so these are carrier birth-guard
tests in the PR-2 construction-test shape — ``pytest.raises`` plus
the named code asserted in the message (docs/12 §4). The
verdict-walking :class:`ConstitutionalChainTestCase` harness binds
the operations when they land (Ω and the ``μ`` chain in PR-12,
``weigh()`` in PR-13).
"""

from __future__ import annotations

import ast
import dataclasses
import importlib
import importlib.util
import pathlib

import pytest

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
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
    SlotAlignment,
    SyllableCandidate,
    SyllableSequenceCandidate,
    WeightCarrierBase,
    WeightCarrierSchemaError,
    WeightImage,
    WeightReadinessCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
)

_DOC_19 = "docs/19_ARABIC_WEIGHT_BOUNDARY_LAW.md"
_DOC_20 = "docs/20_PRE_WEIGHT_LICENSING_LAW.md"

#: The nine mandatory axes of the docs/14 PR-10 row, in field order.
_NINE_FIELDS = (
    "value",
    "type",
    "origin",
    "identity",
    "domain",
    "scope",
    "rank",
    "residuals",
    "trace",
)


# ---------------------------------------------------------------------------
# 0. The origin laws themselves must be present (the PR-1C guard shape).
# ---------------------------------------------------------------------------


def test_pr10_constitutional_documents_are_present() -> None:
    """docs/13 — a PR's origin law must exist in the repository.

    PR-10 branches from docs/19 (the output boundary) and docs/20
    (the input boundary); weight carriers in a repository where
    either law is absent or empty would be a ``FORBIDDEN_LEAP``
    regardless of CI status.
    """

    repo_root = pathlib.Path(__file__).resolve().parent.parent
    for doc in (_DOC_19, _DOC_20):
        path = repo_root / doc
        assert path.is_file(), f"missing PR-10 origin document: {doc}"
        assert path.read_text(encoding="utf-8").strip(), (
            f"PR-10 origin document is empty: {doc}"
        )


# ---------------------------------------------------------------------------
# Carrier factories — one licit instance per stage, the chain in order.
# ---------------------------------------------------------------------------


def _base(kind: str, ident: str, value: str) -> dict[str, object]:
    """The nine docs/14 axes, filled licitly for a test carrier."""

    return {
        "value": value,
        "type": kind,
        "origin": "declared_fixture",
        "identity": ident,
        "domain": "arabic_morphophonology",
        "scope": "pr10-carrier-test",
        "rank": Rank.CANDIDATE,
        "residuals": (),
        "trace": TraceRef(anchor="trace://pr10/qatala", kind="DECLARED_ENTRY"),
    }


def _syllable() -> SyllableCandidate:
    return SyllableCandidate(
        **_base("syllable", "syll-qa", "qa"), units=(("q", "a"),)
    )


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


def _image() -> WeightImage:
    return WeightImage(**_base("weight_image", "wi-faala", "faala"))


def _alignment() -> SlotAlignment:
    return SlotAlignment(
        **_base("slot_alignment", "al-qatala", "qatala~faala"),
        mawzun=_mawzun(),
        mizan=_mizan(),
        pairs=(("q", "f"), ("t", "ayn"), ("l", "lam")),
    )


_FACTORIES = (
    _syllable,
    _sequence,
    _boundary,
    _word_carrier,
    _path,
    _root_stem,
    _original_extra,
    _operations,
    _surface,
    _readiness,
    _mawzun,
    _mizan,
    _image,
    _alignment,
)

_ALL_CARRIERS = (
    SyllableCandidate,
    SyllableSequenceCandidate,
    WordBoundaryCandidate,
    WordCarrierCandidate,
    PathCandidate,
    RootStemCandidate,
    OriginalExtraMap,
    OperationTraceCandidate,
    PreWeightSurface,
    WeightReadinessCandidate,
    MawzunCandidate,
    Mizan,
    WeightImage,
    SlotAlignment,
)


def _refused(code: FailureCode, build: object) -> None:
    """A carrier birth must refuse with the named code in the message."""

    with pytest.raises(WeightCarrierSchemaError) as excinfo:
        build()  # type: ignore[operator]
    assert code.value in str(excinfo.value)


# ---------------------------------------------------------------------------
# 1. The nine-field law — every carrier, every axis (docs/14 — PR-10).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("carrier", _ALL_CARRIERS, ids=lambda c: c.__name__)
def test_every_carrier_leads_with_the_nine_mandatory_fields(carrier: type) -> None:
    """docs/14 — PR-10: "each carrying value, type, origin, identity,
    domain, scope, rank, residuals, trace"."""

    assert issubclass(carrier, WeightCarrierBase)
    field_names = tuple(field.name for field in dataclasses.fields(carrier))
    assert field_names[: len(_NINE_FIELDS)] == _NINE_FIELDS


@pytest.mark.parametrize("factory", _FACTORIES, ids=lambda f: f.__name__.strip("_"))
def test_every_carrier_is_frozen_and_hashable(factory: object) -> None:
    """docs/14 — PR-10: frozen carriers; docs/11 carrier discipline."""

    instance = factory()  # type: ignore[operator]
    with pytest.raises(dataclasses.FrozenInstanceError):
        instance.value = "tampered"  # type: ignore[misc]
    assert isinstance(hash(instance), int)


@pytest.mark.parametrize(
    ("overrides", "code"),
    [
        ({"value": ""}, FailureCode.REQUIRED_SLOT_EMPTY),
        ({"value": "   "}, FailureCode.REQUIRED_SLOT_EMPTY),
        ({"type": ""}, FailureCode.IDENTITY_BROKEN),
        ({"origin": ""}, FailureCode.UNLICENSED_OPENING),
        ({"identity": ""}, FailureCode.IDENTITY_BROKEN),
        ({"domain": ""}, FailureCode.DOMAIN_MISSING),
        ({"scope": ""}, FailureCode.SCOPE_MISSING),
        ({"rank": "CANDIDATE"}, FailureCode.RANK_PROMOTION_WITHOUT_GATE),
        ({"residuals": ["listed"]}, FailureCode.HIDDEN_RESIDUAL),
        ({"residuals": ("untyped",)}, FailureCode.HIDDEN_RESIDUAL),
        ({"trace": "trace://bare-string"}, FailureCode.TRACE_MISSING),
        ({"trace": None}, FailureCode.TRACE_MISSING),
    ],
    ids=lambda v: str(v) if isinstance(v, FailureCode) else next(iter(v)),
)
def test_each_missing_axis_is_refused_with_its_named_code(
    overrides: dict[str, object], code: FailureCode
) -> None:
    """Missing means refuse — never synthesise (docs/11; docs/12 §4).

    Every violated axis of the nine-field law is refused at birth
    with the :class:`FailureCode` of that axis named in the message.
    """

    _refused(code, lambda: dataclasses.replace(_syllable(), **overrides))


# ---------------------------------------------------------------------------
# 2. The birth rank ceiling — no rank promotion without a gate, and no
#    weight-branch gate exists before PR-11 (docs/11 §8; docs/20 §11).
# ---------------------------------------------------------------------------


def test_birth_rank_ceiling_is_candidate() -> None:
    assert BIRTH_RANK_CEILING is Rank.CANDIDATE


@pytest.mark.parametrize("factory", _FACTORIES, ids=lambda f: f.__name__.strip("_"))
def test_no_carrier_is_born_above_the_ceiling(factory: object) -> None:
    """docs/11 §8 — the gate is the only path that can promote a rank;
    a weight carrier born above CANDIDATE would be an ungated promotion.
    """

    _refused(
        FailureCode.RANK_PROMOTION_WITHOUT_GATE,
        lambda: dataclasses.replace(factory(), rank=Rank.LICENSED),  # type: ignore[operator]
    )


@pytest.mark.parametrize(
    "rank", [Rank.HYPOTHESIS, Rank.LICENSED, Rank.STRONG, Rank.CERTIFICATE]
)
def test_every_rank_above_candidate_is_refused_at_birth(rank: Rank) -> None:
    _refused(
        FailureCode.RANK_PROMOTION_WITHOUT_GATE,
        lambda: dataclasses.replace(_syllable(), rank=rank),
    )


@pytest.mark.parametrize("rank", [Rank.ZERO, Rank.TRACE, Rank.CANDIDATE])
def test_ranks_at_or_below_the_ceiling_are_licit_at_birth(rank: Rank) -> None:
    assert dataclasses.replace(_syllable(), rank=rank).rank is rank


# ---------------------------------------------------------------------------
# 3. The pre-weight stage order (docs/20 §3–§11) — no skipped stage.
# ---------------------------------------------------------------------------


def test_syllable_refuses_empty_or_broken_units() -> None:
    """docs/20 §4 — a syllable whose units lose their letters has no
    identity; a ḥaraka may be empty (sukūn), a letter may not."""

    _refused(
        FailureCode.IDENTITY_BROKEN,
        lambda: dataclasses.replace(_syllable(), units=()),
    )
    _refused(
        FailureCode.IDENTITY_BROKEN,
        lambda: dataclasses.replace(_syllable(), units=(("q",),)),
    )
    _refused(
        FailureCode.IDENTITY_BROKEN,
        lambda: dataclasses.replace(_syllable(), units=(("", "a"),)),
    )
    sukun = dataclasses.replace(_syllable(), units=(("q", ""),))
    assert sukun.units == (("q", ""),)


def test_sequence_refuses_raw_text_and_empty_chains() -> None:
    """docs/20 §4 — a sequence is built from licensed syllables only;
    a raw string entry is the straight line from raw text into the
    chain."""

    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_sequence(), syllables=()),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_sequence(), syllables=("qa",)),
    )


def test_boundary_refuses_anything_but_a_licensed_sequence() -> None:
    """docs/20 §5 — no word boundary before the syllable sequence."""

    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_boundary(), sequence="qatala"),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_boundary(), sequence=_syllable()),
    )


def test_word_carrier_refuses_an_unbounded_sequence() -> None:
    """docs/20 §6 — no word carrier before the word boundary."""

    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_word_carrier(), bounded_surface=_sequence()),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_word_carrier(), bounded_surface="qatala"),
    )


def test_path_refuses_unkinded_or_ungated_exits() -> None:
    """docs/20 §7 — every word carrier exits the path gate on exactly
    one named path; an unkinded path has not passed the gate."""

    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_path(), kind="ROOT"),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_path(), carrier=_boundary()),
    )


def test_path_kind_family_is_exactly_the_seven_licensed_exits() -> None:
    """docs/20 §7 — the path family is closed: the root path and the
    six non-root paths, nothing else."""

    assert {kind.value for kind in PathKind} == {
        "ROOT",
        "JAMID",
        "MABNI",
        "OPERATOR",
        "PROPER_NAME",
        "BORROWED",
        "RESIDUAL",
    }


@pytest.mark.parametrize(
    "kind", [kind for kind in PathKind if kind is not PathKind.ROOT]
)
def test_root_stem_refuses_every_non_root_path(kind: PathKind) -> None:
    """docs/20 §8, §12 — a root claim standing on a non-root path is
    the registered straight line from a non-root path to a root."""

    _refused(
        FailureCode.FORBIDDEN_STRAIGHT_LINE,
        lambda: dataclasses.replace(_root_stem(), path=_path(kind)),
    )


def test_root_stem_refuses_a_missing_path_entirely() -> None:
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_root_stem(), path=_word_carrier()),
    )


def test_original_extra_map_refuses_erased_or_untyped_splits() -> None:
    """docs/20 §9 — an erased underlying form loses its trace; an
    unassigned or untyped letter breaks the map's identity."""

    _refused(
        FailureCode.TRACE_MISSING,
        lambda: dataclasses.replace(_original_extra(), underlying_form="  "),
    )
    _refused(
        FailureCode.IDENTITY_BROKEN,
        lambda: dataclasses.replace(_original_extra(), assignments=()),
    )
    _refused(
        FailureCode.IDENTITY_BROKEN,
        lambda: dataclasses.replace(
            _original_extra(), assignments=(("q", "ORIGINAL"),)
        ),
    )


def test_operation_trace_refuses_empty_or_erased_steps() -> None:
    """docs/20 §10 — a trace with no steps, or an erased step, has
    lost the history it exists to carry."""

    _refused(
        FailureCode.TRACE_MISSING,
        lambda: dataclasses.replace(_operations(), steps=()),
    )
    _refused(
        FailureCode.TRACE_MISSING,
        lambda: dataclasses.replace(_operations(), steps=("declared_seq", " ")),
    )


def test_pre_weight_surface_refuses_any_skipped_stage() -> None:
    """docs/20 §11 — the surface is the bounded carrier with its path,
    its original/extra map, and its operation trace; no part may be
    skipped or stand in for another."""

    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_surface(), carrier="qatala"),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_surface(), path=_word_carrier()),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_surface(), original_extra=("q", "ORIGINAL")),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_surface(), operations=("declared_seq",)),
    )


def test_pre_weight_surface_refuses_a_path_of_a_different_carrier() -> None:
    """docs/20 §11 — a surface whose path wraps a different carrier
    has broken its own identity."""

    other = WordCarrierCandidate(
        **_base("word_carrier", "wc-other", "daraba"), bounded_surface=_boundary()
    )
    _refused(
        FailureCode.IDENTITY_BROKEN,
        lambda: dataclasses.replace(
            _surface(),
            path=PathCandidate(
                **_base("path", "path-other", "root_path"),
                kind=PathKind.ROOT,
                carrier=other,
            ),
        ),
    )


def test_weight_readiness_exists_only_on_a_full_surface() -> None:
    """docs/20 §11 — readiness without the surface skips the chain."""

    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_readiness(), surface=_word_carrier()),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_readiness(), surface="qatala"),
    )


# ---------------------------------------------------------------------------
# 4. The input boundary of the Mīzān (docs/20 §1) — nothing is weighed
#    before it is a licensed WeightReadinessCandidate.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "unlicensed",
    [
        "qatala",  # a raw word
        _syllable,  # a syllable
        _sequence,  # a bare sequence
        _root_stem,  # a root
        _word_carrier,  # a bounded surface without its chain
        _surface,  # even a full surface is not readiness (Ω is PR-12)
    ],
    ids=["raw-word", "syllable", "sequence", "root", "word-carrier", "surface"],
)
def test_mawzun_refuses_every_unlicensed_opening(unlicensed: object) -> None:
    """docs/20 §1 — ``weigh(raw_word)``, ``weigh(surface)``,
    ``weigh(syllable)``, ``weigh(root)`` are all unlicensed openings
    of the weighing space; at carrier birth the mawzūn refuses them
    before any ``weigh()`` could ever exist (PR-13)."""

    readiness = unlicensed() if callable(unlicensed) else unlicensed
    _refused(
        FailureCode.UNLICENSED_OPENING,
        lambda: dataclasses.replace(_mawzun(), readiness=readiness),
    )


# ---------------------------------------------------------------------------
# 5. The output boundary of the Mīzān (docs/19 §2, §4) — weight maps
#    into PatternSpace, not Meaning.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "factory", [_image, _mizan, _alignment], ids=["WeightImage", "Mizan", "SlotAlignment"]
)
@pytest.mark.parametrize(
    "landing_space", ["MeaningSpace", "Meaning", "", None], ids=str
)
def test_every_landing_space_but_pattern_space_is_refused(
    factory: object, landing_space: object
) -> None:
    """docs/19 §4 — a landing space other than PatternSpace is the
    registered straight line *Weight → Meaning*."""

    _refused(
        FailureCode.FORBIDDEN_STRAIGHT_LINE,
        lambda: dataclasses.replace(factory(), landing_space=landing_space),  # type: ignore[operator]
    )


def test_pattern_space_is_the_declared_default_landing_space() -> None:
    assert PATTERN_SPACE == "PatternSpace"
    assert _image().landing_space == PATTERN_SPACE
    assert _mizan().landing_space == PATTERN_SPACE
    assert _alignment().landing_space == PATTERN_SPACE


def test_mizan_carries_no_pattern_table() -> None:
    """docs/19 §6 — pattern inventories, lexica, samāʿ and qiyās
    material enter only through the PR-14 licensing boundary; the
    PR-10 Mīzān is the instrument's carrier shape and nothing more.
    """

    field_names = {field.name for field in dataclasses.fields(Mizan)}
    assert field_names == set(_NINE_FIELDS) | {"landing_space"}


def test_weight_image_carries_nothing_but_its_landing_space() -> None:
    """docs/19 §3 — an image is not a meaning, not a hukm, and not
    knowledge; structurally it is the nine axes plus the one landing
    space."""

    field_names = {field.name for field in dataclasses.fields(WeightImage)}
    assert field_names == set(_NINE_FIELDS) | {"landing_space"}


def test_alignment_is_depicted_pairs_never_a_computation() -> None:
    """docs/19 §9 — PR-10 depicts an alignment as declared pairs; an
    alignment with no pairs depicts nothing, and a pair that loses
    either side breaks the alignment's identity."""

    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_alignment(), mawzun=_readiness()),
    )
    _refused(
        FailureCode.GATE_REQUIRED,
        lambda: dataclasses.replace(_alignment(), mizan=_image()),
    )
    _refused(
        FailureCode.REQUIRED_SLOT_EMPTY,
        lambda: dataclasses.replace(_alignment(), pairs=()),
    )
    _refused(
        FailureCode.IDENTITY_BROKEN,
        lambda: dataclasses.replace(_alignment(), pairs=(("q",),)),
    )
    _refused(
        FailureCode.IDENTITY_BROKEN,
        lambda: dataclasses.replace(_alignment(), pairs=(("", "f"),)),
    )


# ---------------------------------------------------------------------------
# 6. The full licit chain — every stage present, nothing promoted,
#    nothing hidden, every trace anchored (docs/20 §3; docs/14 — PR-10).
# ---------------------------------------------------------------------------


def test_the_full_licit_chain_constructs_and_stays_below_the_ceiling() -> None:
    """The positive branch: syllable → sequence → boundary → word
    carrier → path → root/stem + original-extra + operations →
    surface → readiness → mawzūn → mīzān → image → alignment. Every
    carrier holds rank ≤ CANDIDATE, a visible (empty) residual
    surface, and a named trace anchor — and none carries a verdict,
    a fit, or a meaning."""

    chain: tuple[WeightCarrierBase, ...] = (
        _syllable(),
        _sequence(),
        _boundary(),
        _word_carrier(),
        _path(),
        _root_stem(),
        _original_extra(),
        _operations(),
        _surface(),
        _readiness(),
        _mawzun(),
        _mizan(),
        _image(),
        _alignment(),
    )
    for carrier in chain:
        assert isinstance(carrier, WeightCarrierBase)
        assert carrier.rank.value <= BIRTH_RANK_CEILING.value
        assert isinstance(carrier.residuals, tuple)
        assert isinstance(carrier.trace, TraceRef)
        assert carrier.trace.anchor


# ---------------------------------------------------------------------------
# 7. Static guards — carriers only, and the branch stays in its lane
#    (docs/14 — PR-10 Forbidden; docs/19 §6, §8; docs/20 §13, §15).
# ---------------------------------------------------------------------------

_WEIGHT_MODULES = (
    "taaqqul_slot_geometry.weight",
    "taaqqul_slot_geometry.weight.carrier_core",
    "taaqqul_slot_geometry.weight.pre_weight",
    "taaqqul_slot_geometry.weight.weight_image",
)

#: PR-11 adds the path gate module — it is a gate, not a carrier,
#: so it legitimately references RankLattice (for the bounded meet).
#: PR-12 adds the mu_chain module — operations and Ω governance,
#: not carriers; it legitimately defines functions and uses RankLattice.
#: PR-13 adds the weight_fit module — the minimal weigh() operation,
#: not carriers; it legitimately defines functions and uses RankLattice.
#: PR-14 adds the licensing_boundary module — boundary assessment,
#: not carriers; it legitimately defines functions and uses RankLattice.
#: PR-15 adds the dal_only module — signifier boundary proof,
#: not carriers; it legitimately defines functions and uses RankLattice.
#: PR-16 adds the verbal_madlul module — verbal signified boundary proof,
#: not carriers; it legitimately defines functions and uses RankLattice.
_WEIGHT_GATE_MODULES = (
    "taaqqul_slot_geometry.weight.path_gate",
    "taaqqul_slot_geometry.weight.mu_chain",
    "taaqqul_slot_geometry.weight.weight_fit",
    "taaqqul_slot_geometry.weight.licensing_boundary",
    "taaqqul_slot_geometry.weight.dal_only",
    "taaqqul_slot_geometry.weight.verbal_madlul",
)

_ADAPTER_AND_AUDIT_MODULES = (
    "taaqqul_slot_geometry.adapters",
    "taaqqul_slot_geometry.adapters.adapter_boundary",
    "taaqqul_slot_geometry.adapters.in_memory",
    "taaqqul_slot_geometry.audit",
    "taaqqul_slot_geometry.audit.answer_audit",
    "taaqqul_slot_geometry.audit.model_client",
    "taaqqul_slot_geometry.audit.successor",
)

#: The weight branch sees the carrier vocabulary of the kernel —
#: FailureCode, Rank, Residual, TraceRef — and its own modules.
#: Nothing else: no gamma, no gate, no ledger, no audit, no adapter.
_ALLOWED_WEIGHT_FIRST_PARTY = {
    "taaqqul_slot_geometry.core.failure_taxonomy",
    "taaqqul_slot_geometry.core.rank_lattice",
    "taaqqul_slot_geometry.core.residual_policy",
    "taaqqul_slot_geometry.core.slot_graph",
    "taaqqul_slot_geometry.weight.carrier_core",
    "taaqqul_slot_geometry.weight.chain_report",
    "taaqqul_slot_geometry.weight.contractable_unit_geometry",
    "taaqqul_slot_geometry.weight.dal_madlul_binding",
    "taaqqul_slot_geometry.weight.dal_only",
    "taaqqul_slot_geometry.weight.formal_shape",
    "taaqqul_slot_geometry.weight.licensing_boundary",
    "taaqqul_slot_geometry.weight.mu_chain",
    "taaqqul_slot_geometry.weight.path_gate",
    "taaqqul_slot_geometry.weight.pre_weight",
    "taaqqul_slot_geometry.weight.registry_closure",
    "taaqqul_slot_geometry.weight.registry_contract",
    "taaqqul_slot_geometry.weight.relation_candidate",
    "taaqqul_slot_geometry.weight.verbal_madlul",
    "taaqqul_slot_geometry.weight.weight_fit",
    "taaqqul_slot_geometry.weight.weight_image",
}

#: Kernel authority that must stay unreachable from the weight branch
#: (docs/19 §8; docs/20 §15 — the branch judges nothing, records
#: nothing, gates nothing, and emits nothing).
_KERNEL_AUTHORITY_NAMES = {
    "AnswerAudit",
    "AuditedAnswer",
    "ClosureState",
    "Gamma",
    "GammaResult",
    "RankLattice",
    "SlotGraph",
    "TraceEntryCandidate",
    "TraceLedger",
    "TransitionGate",
    "TransitionState",
    "TransitionVerdict",
    "emit_successor",
    "gamma",
}

#: Names reserved by docs/14 for later chain steps. Defining any of
#: them in PR-10 would be a FORBIDDEN_LEAP regardless of CI status.
_RESERVED_LATER_PR_NAMES = {
    # PR-13 names now defined — removed from reserved set
    # PR-14 — licensing-boundary material
    "PatternTable",
    "Lexicon",
}

#: Field names that may never exist on a weight carrier (docs/19 §2,
#: §3; docs/20 §13): PatternSpace contains no meaning, agency,
#: patienthood, hukm, reality, real event, or knowledge.
_FORBIDDEN_FIELD_NAMES = {
    "meaning",
    "agency",
    "patienthood",
    "hukm",
    "reality",
    "real_event",
    "knowledge",
    "semantics",
    "truth",
}


def _module_tree(module_name: str) -> ast.Module:
    spec = importlib.util.find_spec(module_name)
    assert spec is not None and spec.origin is not None
    source = pathlib.Path(spec.origin).read_text(encoding="utf-8")
    return ast.parse(source)


def _first_party_imports(module_name: str) -> set[str]:
    imported: set[str] = set()
    for node in ast.walk(_module_tree(module_name)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("taaqqul_slot_geometry"):
                    imported.add(alias.name)
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module
            and node.module.startswith("taaqqul_slot_geometry")
        ):
            imported.add(node.module)
    return imported


def test_weight_package_defines_only_birth_guards() -> None:
    """docs/14 — PR-10: no operation, no fit computation. The only
    callables licensed in the weight carrier modules are ``__post_init__``
    birth guards — no other function, no async def, no lambda.
    The path_gate module (PR-11) is excluded: it is a gate, not a
    carrier, and legitimately defines ``decide``."""

    for module_name in _WEIGHT_MODULES:
        # Skip __init__.py — it only re-exports, no definitions
        if module_name == "taaqqul_slot_geometry.weight":
            continue
        for node in ast.walk(_module_tree(module_name)):
            assert not isinstance(node, ast.AsyncFunctionDef), (
                f"{module_name} defines an async callable (docs/14 — PR-10)"
            )
            assert not isinstance(node, ast.Lambda), (
                f"{module_name} defines a lambda (docs/14 — PR-10)"
            )
            if isinstance(node, ast.FunctionDef):
                assert node.name == "__post_init__", (
                    f"{module_name} defines {node.name!r}: the only "
                    "callables licensed in PR-10 are carrier birth "
                    "guards (docs/14 — PR-10: carriers only)"
                )


def test_no_carrier_holds_a_meaning_field() -> None:
    """docs/19 §2 — PatternSpace contains no meaning; docs/20 §13 —
    no pre-weight carrier has, or may ever gain, a meaning, agency,
    hukm, or reality field."""

    for carrier in (WeightCarrierBase, *_ALL_CARRIERS):
        field_names = {field.name for field in dataclasses.fields(carrier)}
        leaked = field_names & _FORBIDDEN_FIELD_NAMES
        assert not leaked, (
            f"{carrier.__name__} carries forbidden semantic fields: "
            f"{sorted(leaked)} (docs/19 §2; docs/20 §13)"
        )


def test_weight_branch_imports_only_the_carrier_vocabulary() -> None:
    """docs/19 §8; docs/20 §15 — the weight branch never touches the
    adapter or audit layers, and sees only the kernel's carrier
    vocabulary (FailureCode, Rank, Residual, TraceRef)."""

    for module_name in _WEIGHT_MODULES:
        leaked = _first_party_imports(module_name) - _ALLOWED_WEIGHT_FIRST_PARTY
        assert not leaked, (
            f"{module_name} imports beyond the PR-10 licence: "
            f"{sorted(leaked)} (docs/19 §8; docs/20 §15)"
        )


def test_adapter_and_audit_layers_never_import_the_weight_branch() -> None:
    """docs/19 §8 — the boundary holds in both directions: no adapter
    or audit module may reach into the weight branch."""

    for module_name in _ADAPTER_AND_AUDIT_MODULES:
        leaked = {
            name
            for name in _first_party_imports(module_name)
            if name.startswith("taaqqul_slot_geometry.weight")
        }
        assert not leaked, (
            f"{module_name} imports the weight branch: {sorted(leaked)} "
            "(docs/19 §8)"
        )


def test_weight_branch_references_no_kernel_authority() -> None:
    """The PR-2 purity-guard pattern: no judge, ledger, gate, or
    successor authority is even *named* inside the weight carrier
    modules. The path_gate module (PR-11) legitimately uses
    RankLattice for the bounded meet — it is excluded from this
    carrier-only guard."""

    for module_name in _WEIGHT_MODULES:
        referenced: set[str] = set()
        for node in ast.walk(_module_tree(module_name)):
            if isinstance(node, ast.Name):
                referenced.add(node.id)
            elif isinstance(node, ast.Attribute):
                referenced.add(node.attr)
        leaked = referenced & _KERNEL_AUTHORITY_NAMES
        assert not leaked, (
            f"{module_name} references kernel authority: {sorted(leaked)} "
            "(docs/19 §8; docs/20 §15)"
        )


def test_reserved_later_pr_symbols_stay_unbound() -> None:
    """docs/14 — the μ operations are PR-12, the path gates PR-11,
    ``weigh()`` and the fit PR-13, and pattern tables PR-14. None of
    those names may be *bound* anywhere in the weight package."""

    for module_name in _WEIGHT_MODULES:
        bound: set[str] = set()
        for node in ast.walk(_module_tree(module_name)):
            if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
                bound.add(node.name)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                bound.add(node.id)
        leaked = bound & _RESERVED_LATER_PR_NAMES
        assert not leaked, (
            f"{module_name} binds names reserved for later PRs: "
            f"{sorted(leaked)} (docs/14 — FORBIDDEN_LEAP)"
        )


def test_weight_package_exports_exactly_the_reserved_carrier_surface() -> None:
    """docs/19 §9 + docs/20 §16 + docs/22 + docs/24 + docs/25 + docs/26
    + docs/27 + docs/28 + docs/29 + docs/30 + docs/31 + docs/32 + docs/33
    + docs/34 — the
    package surface is exactly the reserved carriers, the path/standing families,
    the schema error, the landing-space constant, the shared base, the ceilings,
    the PR-11 path gate structures, the PR-12 μ chain operations, the PR-13
    weight fit operation, the PR-14 licensing boundary assessment, the
    PR-15 DalOnlyCandidate boundary, the PR-16 VerbalMadlulCandidate
    boundary, the PR-16B unified pre-semantic chain report, the
    PR-16C pre-semantic registry contract, the PR-16C.1 registry
    closure discipline, the PR-17 Dal-Madlul binding candidate,
    the PR-18 ContractableUnitGeometry boundary, the
    PR-19 RelationCandidate boundary, and the
    PR-F2 Word-Class Formal Definitions."""

    module = importlib.import_module("taaqqul_slot_geometry.weight")
    assert set(module.__all__) == {
        "ADAH_FORM_DEFINITION",
        "ADAH_FORM_FAMILY",
        "ADJECTIVE_FORM_DEFINITION",
        "ADJECTIVE_FORM_FAMILY",
        "BINDING_RANK_CEILING",
        "BIRTH_RANK_CEILING",
        "BORROWED_NOUN_FORM_DEFINITION",
        "BORROWED_NOUN_FORM_FAMILY",
        "CHAIN_REPORT_RANK_CEILING",
        "COMMON_NOUN_FORM_DEFINITION",
        "COMMON_NOUN_FORM_FAMILY",
        "COMPOUND_NOUN_FORM_DEFINITION",
        "COMPOUND_NOUN_FORM_FAMILY",
        "CONNECTOR_FORM_DEFINITION",
        "CONNECTOR_FORM_FAMILY",
        "CONTRACTABLE_UNIT_RANK_CEILING",
        "DAL_BOUNDARY_RANK_CEILING",
        "FIL_DEFINITION",
        "FIL_FAMILY",
        "FORMAL_SHAPE_RANK_CEILING",
        "HARF_DEFINITION",
        "HARF_FAMILY",
        "ISM_DEFINITION",
        "ISM_FAMILY",
        "JAMID_NOUN_FORM_DEFINITION",
        "JAMID_NOUN_FORM_FAMILY",
        "LICENSE_BOUNDARY_RANK_CEILING",
        "MADLUL_BOUNDARY_RANK_CEILING",
        "MU_CHAIN_RANK_CEILING",
        "MUSHTAQ_NOUN_FORM_DEFINITION",
        "MUSHTAQ_NOUN_FORM_FAMILY",
        "PATH_GATE_RANK_CEILING",
        "PATTERN_SPACE",
        "PROPER_NAME_FORM_DEFINITION",
        "PROPER_NAME_FORM_FAMILY",
        "REGISTRY_CLOSURE_RANK_CEILING",
        "REGISTRY_RANK_CEILING",
        "RELATION_CANDIDATE_RANK_CEILING",
        "WEIGHT_FIT_RANK_CEILING",
        "WORD_CLASS_FAMILIES",
        "WORD_CLASS_FAMILIES_EXTENDED",
        "WORD_CLASS_SUBFAMILY_DEFINITIONS",
        "WORD_CLASS_SUBFAMILIES",
        "BindingState",
        "BoundaryEvidence",
        "ChainReportResult",
        "ChainReportState",
        "ContractabilityProfile",
        "ContractableUnitGeometry",
        "ContractableUnitState",
        "ContractableUnitVerdict",
        "DalBoundaryState",
        "DalBoundaryVerdict",
        "DalMadlulBindingCandidate",
        "DalMadlulBindingVerdict",
        "DalOnlyCandidate",
        "FormalShapeClosureState",
        "FormalShapeDefinition",
        "FormalShapeDomain",
        "FormalShapeFamily",
        "FormalShapeRegistry",
        "LetterStanding",
        "LicenseBoundaryKind",
        "LicensingBoundaryResult",
        "LicensingBoundaryState",
        "LicensingBoundaryVerdict",
        "MadlulBoundaryState",
        "MawzunCandidate",
        "Mizan",
        "MuStepResult",
        "MuStepState",
        "OmegaGovernanceState",
        "OperationTraceCandidate",
        "OriginalExtraMap",
        "PathCandidate",
        "PathGateProof",
        "PathGateState",
        "PathGateVerdict",
        "PathKind",
        "PreSemanticChainReport",
        "PreWeightPathGate",
        "PreWeightSurface",
        "RegistryClosureKind",
        "RegistryClosureState",
        "RegistryClosureVerdict",
        "RegistryDomain",
        "RegistryEntry",
        "RegistryLookupResult",
        "RegistryLookupState",
        "RegistryScope",
        "RelationCandidate",
        "RelationState",
        "RelationVerdict",
        "ResidualGovernanceVerdict",
        "RootStemCandidate",
        "SlotAlignment",
        "SyllableCandidate",
        "SyllableSequenceCandidate",
        "VerbalMadlulBoundaryVerdict",
        "VerbalMadlulCandidate",
        "WeightCarrierBase",
        "WeightCarrierSchemaError",
        "WeightFitCandidate",
        "WeightFitResult",
        "WeightFitState",
        "WeightImage",
        "WeightReadinessCandidate",
        "WordBoundaryCandidate",
        "WordCarrierCandidate",
        "WordClassDefinitionState",
        "WordClassDefinitionVerdict",
        "assemble_chain_report",
        "assess_license",
        "bind_dal_madlul",
        "build_word_class_registry",
        "define_word_class_shape",
        "lookup_registry_entry",
        "mu_boundary",
        "mu_ops",
        "mu_original_extra",
        "mu_root_stem",
        "mu_seq",
        "mu_weight_readiness",
        "mu_word_carrier",
        "omega_governance",
        "prove_contractable_unit",
        "prove_dal",
        "prove_relation_candidate",
        "prove_verbal_madlul",
        "weigh",
    }
