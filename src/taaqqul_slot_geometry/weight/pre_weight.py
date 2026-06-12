"""Pre-weight carriers — PR-10 binding of docs/20 (carriers only).

The Pre-Weight Licensing Law (``docs/20_PRE_WEIGHT_LICENSING_LAW.md``)
declares the input boundary of the Mīzān: nothing is weighed before
it becomes a licensed :class:`WeightReadinessCandidate`, and nothing
becomes weight-ready except through the ordered stage chain. PR-10
ships only the **carriers** each stage names — the depicted outputs,
never the stage operations themselves:

* §4  Stage 1 (``μ_seq``):               :class:`SyllableCandidate` →
  :class:`SyllableSequenceCandidate`
* §5  Stage 2 (``μ_boundary``):          → :class:`WordBoundaryCandidate`
* §6  Stage 3 (``μ_word_carrier``):      → :class:`WordCarrierCandidate`
* §7  Stage 4 (``μ_path_gate``):         → :class:`PathCandidate`
  (the seven-member :class:`PathKind` family)
* §8  Stage 5 (``μ_root_stem``):         → :class:`RootStemCandidate`
* §9  Stage 6 (``μ_original_extra``):    → :class:`OriginalExtraMap`
  (with :class:`LetterStanding`)
* §10 Stage 7 (``μ_ops``):               → :class:`OperationTraceCandidate`
* §11 Stage 8 (``μ_weight_readiness``):  :class:`PreWeightSurface` →
  :class:`WeightReadinessCandidate`

The ``μ`` operations themselves are PR-12 surface, the path gates
are PR-11 surface, and the Ω judgment over the
:class:`PreWeightSurface` is PR-12 surface (docs/20 §16, docs/14).
Nothing here computes, gates, judges, or weighs: every class is a
frozen carrier whose birth guard refuses a skipped stage with a
named :class:`FailureCode` — presenting a stage output without its
licensed predecessor is exactly the stage-order violation docs/20 §3
forbids, and at carrier birth the violated axis is the missing gate
(``GATE_REQUIRED``).

No carrier here has — or may ever gain — a meaning, agency, hukm, or
reality field (docs/20 §13, binds PR-10). No lexicon, no samāʿ, no
qiyās material enters before the PR-14 licensing boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.weight.carrier_core import (
    WeightCarrierBase,
    WeightCarrierSchemaError,
)


class PathKind(StrEnum):
    """The docs/20 §7 path family — the path gate precedes the root.

    Exactly the seven licensed exits of ``μ_path_gate`` (PR-11): the
    derivational root path (*mushtaqq*) and the six non-root paths.
    PR-10 only names the family; no gate logic exists here.
    """

    ROOT = "ROOT"
    JAMID = "JAMID"
    MABNI = "MABNI"
    OPERATOR = "OPERATOR"
    PROPER_NAME = "PROPER_NAME"
    BORROWED = "BORROWED"
    RESIDUAL = "RESIDUAL"


class LetterStanding(StrEnum):
    """The docs/20 §9 original/extra split of letters.

    Each letter of the underlying form stands as either an original
    (*aṣlī*) or an extra (*zāʼid*) letter. The split is depicted by
    :class:`OriginalExtraMap`; PR-10 never computes it.
    """

    ORIGINAL = "ORIGINAL"
    EXTRA = "EXTRA"


@dataclass(frozen=True, slots=True)
class SyllableCandidate(WeightCarrierBase):
    """A licensed syllable — the entry carrier of the chain (docs/20 §4).

    Born only from the docs/15–17 licensed textual entry (docs/20
    §2–§3); its structural content is the ordered ``(letter, ḥaraka)``
    units it depicts. A ḥaraka may be the empty string (an
    unvocalised letter / sukūn); a letter may not — a syllable whose
    units lose their letters has no identity (docs/20 §4 refusals).
    """

    units: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.units, tuple) or len(self.units) == 0:
            raise WeightCarrierSchemaError(
                "SyllableCandidate.units must be a non-empty tuple of "
                f"(letter, haraka) pairs ({FailureCode.IDENTITY_BROKEN.value})"
            )
        for unit in self.units:
            if (
                not isinstance(unit, tuple)
                or len(unit) != 2
                or not isinstance(unit[0], str)
                or not isinstance(unit[1], str)
            ):
                raise WeightCarrierSchemaError(
                    "SyllableCandidate.units entries must be (letter, haraka) "
                    f"string pairs ({FailureCode.IDENTITY_BROKEN.value})"
                )
            if not unit[0].strip():
                raise WeightCarrierSchemaError(
                    "SyllableCandidate.units letters must be non-empty "
                    f"({FailureCode.IDENTITY_BROKEN.value})"
                )


@dataclass(frozen=True, slots=True)
class SyllableSequenceCandidate(WeightCarrierBase):
    """The output carrier of stage 1, ``μ_seq`` (docs/20 §4).

    A sequence is built from licensed :class:`SyllableCandidate`
    carriers **only**. An empty sequence, or any entry that is not a
    licensed syllable, is the straight line from raw text into the
    chain that docs/20 §4 refuses — at birth the violated axis is
    the missing stage gate.
    """

    syllables: tuple[SyllableCandidate, ...]

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.syllables, tuple) or len(self.syllables) == 0:
            raise WeightCarrierSchemaError(
                "SyllableSequenceCandidate.syllables must be a non-empty tuple "
                f"of SyllableCandidate carriers ({FailureCode.GATE_REQUIRED.value})"
            )
        for syllable in self.syllables:
            if not isinstance(syllable, SyllableCandidate):
                raise WeightCarrierSchemaError(
                    "SyllableSequenceCandidate.syllables entries must be "
                    "licensed SyllableCandidate carriers "
                    f"({FailureCode.GATE_REQUIRED.value})"
                )


@dataclass(frozen=True, slots=True)
class WordBoundaryCandidate(WeightCarrierBase):
    """The output carrier of stage 2, ``μ_boundary`` (docs/20 §5).

    No word boundary before the syllable sequence: the boundary is
    drawn *around* a licensed :class:`SyllableSequenceCandidate`,
    never around raw text or a bare string.
    """

    sequence: SyllableSequenceCandidate

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.sequence, SyllableSequenceCandidate):
            raise WeightCarrierSchemaError(
                "WordBoundaryCandidate.sequence must be a "
                "SyllableSequenceCandidate — no boundary before the sequence "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


@dataclass(frozen=True, slots=True)
class WordCarrierCandidate(WeightCarrierBase):
    """The output carrier of stage 3, ``μ_word_carrier`` (docs/20 §6).

    No word carrier before the word boundary: the carrier holds a
    licensed bounded surface, never an unbounded sequence and never
    raw text.
    """

    bounded_surface: WordBoundaryCandidate

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.bounded_surface, WordBoundaryCandidate):
            raise WeightCarrierSchemaError(
                "WordCarrierCandidate.bounded_surface must be a "
                "WordBoundaryCandidate — no carrier before the boundary "
                f"({FailureCode.GATE_REQUIRED.value})"
            )


@dataclass(frozen=True, slots=True)
class PathCandidate(WeightCarrierBase):
    """The output carrier of stage 4, ``μ_path_gate`` (docs/20 §7).

    The path gate precedes the root: every word carrier exits the
    gate on exactly one of the seven :class:`PathKind` paths. PR-10
    depicts the exit; the gate itself is PR-11 surface. An unkinded
    path, or a path not built on a licensed word carrier, is ungated.
    """

    kind: PathKind
    carrier: WordCarrierCandidate

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.kind, PathKind):
            raise WeightCarrierSchemaError(
                "PathCandidate.kind must be a PathKind member — an unkinded "
                f"path has not passed the path gate ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.carrier, WordCarrierCandidate):
            raise WeightCarrierSchemaError(
                "PathCandidate.carrier must be a WordCarrierCandidate — no "
                f"path gate before the word carrier ({FailureCode.GATE_REQUIRED.value})"
            )


@dataclass(frozen=True, slots=True)
class RootStemCandidate(WeightCarrierBase):
    """The output carrier of stage 5, ``μ_root_stem`` (docs/20 §8).

    The root is reached only through its path: a root/stem claim
    standing on anything but a :attr:`PathKind.ROOT` path is the
    registered straight line from a non-root path to a root (docs/20
    §8, §12). The depicted root/stem string travels in ``value``.
    """

    path: PathCandidate

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.path, PathCandidate):
            raise WeightCarrierSchemaError(
                "RootStemCandidate.path must be a PathCandidate — the root is "
                f"reached only through its path ({FailureCode.GATE_REQUIRED.value})"
            )
        if self.path.kind is not PathKind.ROOT:
            raise WeightCarrierSchemaError(
                "RootStemCandidate.path must carry PathKind.ROOT — a root from "
                f"a {self.path.kind.value} path is a forbidden straight line "
                f"({FailureCode.FORBIDDEN_STRAIGHT_LINE.value})"
            )


@dataclass(frozen=True, slots=True)
class OriginalExtraMap(WeightCarrierBase):
    """The output carrier of stage 6, ``μ_original_extra`` (docs/20 §9).

    Depicts which letters of the underlying form are original and
    which are extra, without erasing the underlying form itself: an
    empty underlying form erases the trace back to the carrier, and
    an unassigned or untyped letter breaks the map's identity
    (docs/20 §9 refusals).
    """

    underlying_form: str
    assignments: tuple[tuple[str, LetterStanding], ...]

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.underlying_form, str) or not self.underlying_form.strip():
            raise WeightCarrierSchemaError(
                "OriginalExtraMap.underlying_form must be a non-empty string — "
                f"an erased underlying form loses its trace ({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.assignments, tuple) or len(self.assignments) == 0:
            raise WeightCarrierSchemaError(
                "OriginalExtraMap.assignments must be a non-empty tuple of "
                f"(letter, LetterStanding) pairs ({FailureCode.IDENTITY_BROKEN.value})"
            )
        for assignment in self.assignments:
            if (
                not isinstance(assignment, tuple)
                or len(assignment) != 2
                or not isinstance(assignment[0], str)
                or not assignment[0].strip()
                or not isinstance(assignment[1], LetterStanding)
            ):
                raise WeightCarrierSchemaError(
                    "OriginalExtraMap.assignments entries must be non-empty "
                    "(letter, LetterStanding) pairs "
                    f"({FailureCode.IDENTITY_BROKEN.value})"
                )


@dataclass(frozen=True, slots=True)
class OperationTraceCandidate(WeightCarrierBase):
    """The output carrier of stage 7, ``μ_ops`` (docs/20 §10).

    The ordered, named steps already applied to the carrier. A trace
    with no steps, or with an erased (empty) step, has lost the very
    history it exists to carry (docs/20 §10 refusals). PR-10 depicts
    the trace; it never records or replays one.
    """

    steps: tuple[str, ...]

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.steps, tuple) or len(self.steps) == 0:
            raise WeightCarrierSchemaError(
                "OperationTraceCandidate.steps must be a non-empty tuple of "
                f"step names ({FailureCode.TRACE_MISSING.value})"
            )
        for step in self.steps:
            if not isinstance(step, str) or not step.strip():
                raise WeightCarrierSchemaError(
                    "OperationTraceCandidate.steps entries must be non-empty "
                    f"strings — an erased step erases the trace "
                    f"({FailureCode.TRACE_MISSING.value})"
                )


@dataclass(frozen=True, slots=True)
class PreWeightSurface(WeightCarrierBase):
    """The assembled pre-weight surface (docs/20 §11).

    The bounded carrier **with its** path, its original/extra map,
    and its operation trace — no stage skipped, no part standing in
    for another. A surface whose path wraps a different carrier has
    broken its own identity. The Ω judgment over this surface
    (FunctionalClosure | WeightOpening | Residual) is PR-12 surface
    and does not exist here.
    """

    carrier: WordCarrierCandidate
    path: PathCandidate
    original_extra: OriginalExtraMap
    operations: OperationTraceCandidate

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.carrier, WordCarrierCandidate):
            raise WeightCarrierSchemaError(
                "PreWeightSurface.carrier must be a WordCarrierCandidate — no "
                f"stage may be skipped ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.path, PathCandidate):
            raise WeightCarrierSchemaError(
                "PreWeightSurface.path must be a PathCandidate — no stage may "
                f"be skipped ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.original_extra, OriginalExtraMap):
            raise WeightCarrierSchemaError(
                "PreWeightSurface.original_extra must be an OriginalExtraMap — "
                f"no stage may be skipped ({FailureCode.GATE_REQUIRED.value})"
            )
        if not isinstance(self.operations, OperationTraceCandidate):
            raise WeightCarrierSchemaError(
                "PreWeightSurface.operations must be an OperationTraceCandidate "
                f"— no stage may be skipped ({FailureCode.GATE_REQUIRED.value})"
            )
        if self.path.carrier != self.carrier:
            raise WeightCarrierSchemaError(
                "PreWeightSurface.path must be the path of this surface's own "
                f"carrier ({FailureCode.IDENTITY_BROKEN.value})"
            )


@dataclass(frozen=True, slots=True)
class WeightReadinessCandidate(WeightCarrierBase):
    """The output carrier of stage 8, ``μ_weight_readiness`` (docs/20 §11).

    The only object the Mīzān may ever receive (docs/20 §1 — the
    input boundary). It exists solely as the licensed completion of a
    full :class:`PreWeightSurface`; presenting readiness without the
    surface skips the entire chain.
    """

    surface: PreWeightSurface

    def __post_init__(self) -> None:
        WeightCarrierBase.__post_init__(self)
        if not isinstance(self.surface, PreWeightSurface):
            raise WeightCarrierSchemaError(
                "WeightReadinessCandidate.surface must be a PreWeightSurface — "
                f"readiness without the chain is ungated ({FailureCode.GATE_REQUIRED.value})"
            )


__all__ = [
    "LetterStanding",
    "OperationTraceCandidate",
    "OriginalExtraMap",
    "PathCandidate",
    "PathKind",
    "PreWeightSurface",
    "RootStemCandidate",
    "SyllableCandidate",
    "SyllableSequenceCandidate",
    "WeightReadinessCandidate",
    "WordBoundaryCandidate",
    "WordCarrierCandidate",
]
