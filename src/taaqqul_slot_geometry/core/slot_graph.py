"""Executable ``SlotGraph`` carriers — PR-2 minimal kernel, PR-2A hardened.

This module binds the structural part of
``docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`` §1–§5 and the
constructor obligations named in
``docs/17_SLOTGRAPH_GENERATION_LAW.md`` §2.

PR-2A tightens the construction surface so that every row of
``docs/17 §3`` that is structurally checkable at birth is refused at
birth rather than deferred to ``Γ``. Two shapes coexist:

* Direct dataclass construction (``SlotGraph(...)`` and the nested
  carriers) raises :class:`SlotGraphSchemaError` for any missing or
  empty mandatory field. Each message names the constitutional
  :class:`FailureCode` member it corresponds to, so a programmer
  reading the traceback can map straight back to ``docs/17 §3``.
* The named construction surface :meth:`SlotGraph.construct` returns
  a :class:`ConstructionResult` value carrying the named
  :class:`FailureCode` for presence-level refusals (``center is
  None``, ``boundary is None``, ``entry_boundary`` missing when the
  source is a declared textual entry, …). This is the *constitutional*
  refusal path: callers that want a value never get a bare
  ``TypeError``.

The two paths agree on the same failure taxonomy. Direct construction
raises because the caller did not even reach the construction surface;
:meth:`SlotGraph.construct` returns a value because that is what
``docs/17 §5 totality`` requires.

Constitutional shape of a ``SlotGraph``:

    G = ⟨Center, Slots, Boundary, Residuals, Rank,
         OutputBoundary, GenerationSource, EntryBoundary?⟩

``EntryBoundary`` is mandatory when ``generation_source`` is
:attr:`GenerationSource.DECLARED_ENTRY` (docs/15 §5); for the other
two licensed sources it is absent because the boundary lives in the
prior graph or in the gate verdict.

This module deliberately ships **no behaviour beyond construction
checks**: no rank promotion, no residual classification engine, no
gate emission. Those are reserved for PR-3 and PR-4. The
construction surface is pure (no I/O, no logging, no time reads, no
ledger writes) — see ``docs/17 §5``.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import IntEnum, StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual


class SlotGraphSchemaError(TypeError):
    """Raised when a constitutional carrier is constructed with a
    missing or empty mandatory field, or with the wrong *type* of
    value.

    Every message names the :class:`FailureCode` member that the
    constitution assigns to the violation (docs/17 §3). The exception
    subtype itself is a Python schema guard; callers that want a
    *value* refusal must go through :meth:`SlotGraph.construct`,
    which catches presence-level gaps and returns a
    :class:`ConstructionResult`.
    """


class SlotState(StrEnum):
    """Per-slot value state used by ``Γ`` step 4/§5/§8 of docs/11."""

    EMPTY = "EMPTY"
    FILLED = "FILLED"
    BROKEN = "BROKEN"


class Layer(IntEnum):
    """Ordered layers used for the output-boundary check.

    PR-2 ships the minimum order needed by ``Γ`` step 5
    (``output_boundary ⪯ declared_layer``). Names match the
    Declared Entry Boundary Law (docs/11 §13) and the licensing
    chain (docs/16): a textual entry is the lowest operational
    layer; a candidate emitted by a closed graph sits above the
    slot layer; a certificate is reserved for later PRs.
    """

    TEXT_ENTRY = 1
    SLOT = 2
    CANDIDATE = 3
    CERTIFICATE = 4


class GenerationSource(StrEnum):
    """The three licensed generation sources from docs/17 §1."""

    DECLARED_ENTRY = "DECLARED_ENTRY"
    CANDIDATE = "CANDIDATE"
    TRANSITION_VERDICT = "TRANSITION_VERDICT"


@dataclass(frozen=True, slots=True)
class TraceRef:
    """Opaque trace anchor inherited from the generation source.

    Core treats ``anchor`` as opaque (docs/11 §12 — *Trace is opaque
    to core*). An empty ``anchor`` is a constitutional refusal at
    construction time (docs/17 §3 row ``TRACE_MISSING``): a
    :class:`TraceRef` is the carrier of a *named* prior trace, never
    a placeholder for the absence of one.
    """

    anchor: str
    kind: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.anchor, str):
            raise SlotGraphSchemaError(
                f"TraceRef.anchor must be a string ({FailureCode.TRACE_MISSING.value})"
            )
        if not self.anchor.strip():
            raise SlotGraphSchemaError(
                "TraceRef.anchor must be a non-empty string "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.kind, str):
            raise SlotGraphSchemaError("TraceRef.kind must be a string")


@dataclass(frozen=True, slots=True)
class SlotBoundary:
    """The perimeter declaration named in docs/11 §3.

    A boundary is named by its refusals: ``refusal_codes`` lists the
    :class:`FailureCode` members that crossing this boundary would
    emit. PR-2A enforces that the tuple is non-empty: a boundary
    without declared refusals is constitutionally incomplete and is
    refused at construction time with a message naming
    :attr:`FailureCode.BOUNDARY_MISSING` (docs/11 §3, docs/17 §3).
    """

    domain: str
    scope: str
    refusal_codes: tuple[FailureCode, ...]
    licensed_operations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.domain, str):
            raise SlotGraphSchemaError("SlotBoundary.domain must be a string")
        if not isinstance(self.scope, str):
            raise SlotGraphSchemaError("SlotBoundary.scope must be a string")
        if not isinstance(self.refusal_codes, tuple):
            raise SlotGraphSchemaError(
                "SlotBoundary.refusal_codes must be a tuple of FailureCode"
            )
        if len(self.refusal_codes) == 0:
            raise SlotGraphSchemaError(
                "SlotBoundary.refusal_codes must be a non-empty tuple of "
                f"FailureCode ({FailureCode.BOUNDARY_MISSING.value})"
            )
        for code in self.refusal_codes:
            if not isinstance(code, FailureCode):
                raise SlotGraphSchemaError(
                    "every SlotBoundary.refusal_codes entry must be a FailureCode"
                )
        if not isinstance(self.licensed_operations, tuple):
            raise SlotGraphSchemaError(
                "SlotBoundary.licensed_operations must be a tuple of strings"
            )
        for op in self.licensed_operations:
            if not isinstance(op, str):
                raise SlotGraphSchemaError(
                    "every SlotBoundary.licensed_operations entry must be a string"
                )


@dataclass(frozen=True, slots=True)
class OpeningPolicy:
    """Per-slot opening control (docs/11 §4 / docs/17 §2).

    ``allowed_potentials`` is the licensed domain of admissible
    fillings for a slot. PR-2A enforces that the frozenset is
    non-empty and that every member is a non-empty string: a slot
    with no licensed opening cannot be filled at all, and the
    construction-time refusal carries
    :attr:`FailureCode.UNLICENSED_OPENING` in the message
    (consistent with the same code used by :class:`Slot` when a
    FILLED value is outside this set).
    """

    allowed_potentials: frozenset[str]

    def __post_init__(self) -> None:
        if not isinstance(self.allowed_potentials, frozenset):
            raise SlotGraphSchemaError(
                "OpeningPolicy.allowed_potentials must be a frozenset of strings"
            )
        if len(self.allowed_potentials) == 0:
            raise SlotGraphSchemaError(
                "OpeningPolicy.allowed_potentials must be a non-empty frozenset "
                f"({FailureCode.UNLICENSED_OPENING.value})"
            )
        for potential in self.allowed_potentials:
            if not isinstance(potential, str):
                raise SlotGraphSchemaError(
                    "every OpeningPolicy.allowed_potentials entry must be a string"
                )
            if not potential.strip():
                raise SlotGraphSchemaError(
                    "every OpeningPolicy.allowed_potentials entry must be a "
                    f"non-empty string ({FailureCode.UNLICENSED_OPENING.value})"
                )


@dataclass(frozen=True, slots=True)
class Slot:
    """A constitutional slot (docs/11 §1, §11 — *no Slot without Boundary*).

    A ``Slot`` always carries its boundary, its opening policy, and a
    value state. ``FILLED`` requires a ``value`` that is inside the
    opening policy; ``EMPTY`` and ``BROKEN`` carry no value.
    """

    name: str
    value_state: SlotState
    boundary: SlotBoundary
    opening: OpeningPolicy
    required: bool
    value: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise SlotGraphSchemaError("Slot.name must be a non-empty string")
        if not isinstance(self.value_state, SlotState):
            raise SlotGraphSchemaError("Slot.value_state must be a SlotState member")
        if not isinstance(self.boundary, SlotBoundary):
            raise SlotGraphSchemaError("Slot.boundary must be a SlotBoundary")
        if not isinstance(self.opening, OpeningPolicy):
            raise SlotGraphSchemaError("Slot.opening must be an OpeningPolicy")
        if not isinstance(self.required, bool):
            raise SlotGraphSchemaError("Slot.required must be a bool")

        if self.value_state is SlotState.FILLED:
            if not isinstance(self.value, str) or not self.value:
                raise SlotGraphSchemaError(
                    "a FILLED Slot must carry a non-empty string value"
                )
            if self.value not in self.opening.allowed_potentials:
                # docs/17 §3 row: "Opening outside slot boundary" →
                # UNLICENSED_OPENING. We refuse at construction time
                # because Γ cannot inspect a value that was silently
                # coerced; the refusal carrier name is preserved in
                # the exception message for traceability.
                raise SlotGraphSchemaError(
                    f"Slot.value {self.value!r} not in opening.allowed_potentials "
                    f"({FailureCode.UNLICENSED_OPENING.value})"
                )
        else:
            if self.value is not None:
                raise SlotGraphSchemaError(
                    "a non-FILLED Slot must not carry a value"
                )


@dataclass(frozen=True, slots=True)
class Center:
    """Identity-preserving anchor (docs/11 §2, docs/17 §3).

    PR-2A enforces the full ``docs/17 §3`` row set for the center at
    construction time:

    * ``identity_claim`` must be a non-empty string — empty raises
      :class:`SlotGraphSchemaError` naming
      :attr:`FailureCode.IDENTITY_BROKEN`.
    * ``trace_ref`` must be a real :class:`TraceRef` — ``None``
      raises :class:`SlotGraphSchemaError` naming
      :attr:`FailureCode.TRACE_MISSING`. Combined with
      :class:`TraceRef`'s own non-empty-anchor guard, this means a
      ``Center`` cannot be born with a hollow trace.

    ``Γ`` still emits the same codes at closure time for any graph
    that somehow reaches it without satisfying these invariants
    (docs/17 §6 — construction refusal is a strict subset of ``Γ``'s
    refusal set).
    """

    identity_claim: str
    domain: str
    scope: str
    trace_ref: TraceRef

    def __post_init__(self) -> None:
        if not isinstance(self.identity_claim, str):
            raise SlotGraphSchemaError("Center.identity_claim must be a string")
        if not self.identity_claim.strip():
            raise SlotGraphSchemaError(
                "Center.identity_claim must be a non-empty string "
                f"({FailureCode.IDENTITY_BROKEN.value})"
            )
        if not isinstance(self.domain, str):
            raise SlotGraphSchemaError("Center.domain must be a string")
        if not isinstance(self.scope, str):
            raise SlotGraphSchemaError("Center.scope must be a string")
        if self.trace_ref is None:
            raise SlotGraphSchemaError(
                "Center.trace_ref must be a TraceRef "
                f"({FailureCode.TRACE_MISSING.value})"
            )
        if not isinstance(self.trace_ref, TraceRef):
            raise SlotGraphSchemaError("Center.trace_ref must be a TraceRef")


@dataclass(frozen=True, slots=True)
class EntryBoundary:
    """Declared Entry Boundary carrier (docs/11 §13.2, docs/15 §5).

    PR-2A extends the carrier so that every field named in
    ``docs/15 §5`` is mandatory and non-empty at construction time.
    The carrier is purely declarative: the constructor enforces
    *presence* but never inspects or coerces the values themselves
    (the values' meaning is text-only in docs/15, and binding them
    into typed enumerations is reserved for PR-5 alongside the
    Forbidden Straight-Line Registry).

    By construction, an ``EntryBoundary`` instance proves:

    * the entry is representational (``representation_status``);
    * the entry is *not* an ontological origin
      (``ontological_status``);
    * the entry is *not* a sound (``sound_status``);
    * the entry is *not* a meaning (``meaning_status``);
    * the entry produces only a ``TextTraceCandidate``
      (``produces_only``);
    * the prior trace is preserved (``prior_trace_status``).
    """

    declared_entry_kind: str
    representation_status: str
    ontological_status: str
    sound_status: str
    meaning_status: str
    prior_trace_status: str
    produces_only: str

    def __post_init__(self) -> None:
        for name, value in (
            ("declared_entry_kind", self.declared_entry_kind),
            ("representation_status", self.representation_status),
            ("ontological_status", self.ontological_status),
            ("sound_status", self.sound_status),
            ("meaning_status", self.meaning_status),
            ("prior_trace_status", self.prior_trace_status),
            ("produces_only", self.produces_only),
        ):
            if not isinstance(value, str) or not value.strip():
                raise SlotGraphSchemaError(
                    f"EntryBoundary.{name} must be a non-empty string "
                    f"({FailureCode.BOUNDARY_MISSING.value})"
                )


@dataclass(frozen=True, slots=True)
class OutputBoundary:
    """Output-layer perimeter used by ``Γ`` step 5.

    ``output_layer`` is the layer the graph *claims* to produce into.
    ``declared_layer`` is the perimeter declared by the generation
    source. ``Γ`` emits ``FORBIDDEN_LEAP / OUTPUT_EXCEEDS_LAYER`` when
    ``output_layer > declared_layer``.
    """

    declared_layer: Layer
    output_layer: Layer

    def __post_init__(self) -> None:
        if not isinstance(self.declared_layer, Layer):
            raise SlotGraphSchemaError(
                "OutputBoundary.declared_layer must be a Layer member"
            )
        if not isinstance(self.output_layer, Layer):
            raise SlotGraphSchemaError(
                "OutputBoundary.output_layer must be a Layer member"
            )


@dataclass(frozen=True, slots=True)
class SlotGraph:
    """The nine-tuple of docs/11 §1 in carrier form.

    Operations (``Ω``) and the closure verdict function (``Γ``) are
    not stored on the graph: ``Ω`` is reserved for PR-4, ``Γ`` is
    bound externally by :func:`taaqqul_slot_geometry.core.gamma.gamma`
    and is constitutionally pure.

    All fields are mandatory. ``center`` is a real :class:`Center`
    (PR-2A — never ``None``); ``boundary`` is a real
    :class:`SlotBoundary`. ``entry_boundary`` is mandatory whenever
    :attr:`generation_source` is :attr:`GenerationSource.DECLARED_ENTRY`
    (docs/15 §5) and must be absent otherwise — the other two
    licensed sources carry their boundary in the prior graph or in
    the gate verdict.

    Direct construction (``SlotGraph(...)``) raises
    :class:`SlotGraphSchemaError` for any missing or empty mandatory
    field. This is the Python schema guard, not a constitutional
    refusal: callers that want a *value* refusal must go through
    :meth:`SlotGraph.construct`, which returns a
    :class:`ConstructionResult` carrying the named
    :class:`FailureCode` for every presence-level gap listed in
    ``docs/17 §3``.
    """

    center: Center
    slots: tuple[Slot, ...]
    boundary: SlotBoundary
    residuals: tuple[Residual, ...]
    rank: Rank
    output_boundary: OutputBoundary
    generation_source: GenerationSource
    entry_boundary: EntryBoundary | None = None

    def __post_init__(self) -> None:
        if self.center is None:
            raise SlotGraphSchemaError(
                "SlotGraph.center must be a Center "
                f"({FailureCode.CENTER_MISSING.value})"
            )
        if not isinstance(self.center, Center):
            raise SlotGraphSchemaError("SlotGraph.center must be a Center")

        if not isinstance(self.slots, tuple):
            raise SlotGraphSchemaError("SlotGraph.slots must be a tuple of Slot")
        for slot in self.slots:
            if not isinstance(slot, Slot):
                raise SlotGraphSchemaError(
                    "every SlotGraph.slots entry must be a Slot"
                )

        if not isinstance(self.boundary, SlotBoundary):
            raise SlotGraphSchemaError(
                "SlotGraph.boundary must be a SlotBoundary "
                f"({FailureCode.BOUNDARY_MISSING.value})"
            )

        if not isinstance(self.residuals, tuple):
            raise SlotGraphSchemaError(
                "SlotGraph.residuals must be a tuple of Residual (may be empty)"
            )
        for residual in self.residuals:
            if not isinstance(residual, Residual):
                raise SlotGraphSchemaError(
                    "every SlotGraph.residuals entry must be a Residual"
                )

        if not isinstance(self.rank, Rank):
            raise SlotGraphSchemaError("SlotGraph.rank must be a Rank member")

        if not isinstance(self.output_boundary, OutputBoundary):
            raise SlotGraphSchemaError(
                "SlotGraph.output_boundary must be an OutputBoundary"
            )

        if not isinstance(self.generation_source, GenerationSource):
            raise SlotGraphSchemaError(
                "SlotGraph.generation_source must be a GenerationSource member"
            )

        if self.generation_source is GenerationSource.DECLARED_ENTRY:
            if self.entry_boundary is None:
                raise SlotGraphSchemaError(
                    "SlotGraph(generation_source=DECLARED_ENTRY) requires an "
                    "entry_boundary (docs/15 §5; "
                    f"{FailureCode.BOUNDARY_MISSING.value})"
                )
            if not isinstance(self.entry_boundary, EntryBoundary):
                raise SlotGraphSchemaError(
                    "SlotGraph.entry_boundary must be an EntryBoundary"
                )
        else:
            if self.entry_boundary is not None:
                raise SlotGraphSchemaError(
                    "SlotGraph.entry_boundary must be None unless generation_source is "
                    "DECLARED_ENTRY (docs/15 §5; "
                    f"{FailureCode.BOUNDARY_MISSING.value})"
                )

    @classmethod
    def construct(
        cls,
        *,
        center: Center | None,
        slots: tuple[Slot, ...],
        boundary: SlotBoundary | None,
        residuals: tuple[Residual, ...],
        rank: Rank,
        output_boundary: OutputBoundary | None,
        generation_source: GenerationSource,
        entry_boundary: EntryBoundary | None = None,
    ) -> ConstructionResult:
        """Named construction surface — docs/17 §5 totality.

        Returns a :class:`ConstructionResult` value for every
        expected presence-level refusal (``center is None``,
        ``boundary is None``, ``entry_boundary`` missing when the
        source is a declared textual entry, …). The returned
        ``failure_code`` is the named :class:`FailureCode` from
        ``docs/17 §3`` that the refusal corresponds to.

        On success, the method instantiates the dataclass normally
        and returns a result carrying the new graph. The dataclass'
        own ``__post_init__`` schema guards still bind: a structural
        mistake the construction surface did not anticipate (e.g. a
        slot value outside its opening policy) will surface as
        :class:`SlotGraphSchemaError`, exactly as it does for direct
        construction.

        Purity (docs/17 §5): no I/O, no logging, no ledger writes,
        no rank promotion, no residual classification.
        """

        if center is None:
            return ConstructionResult(
                graph=None,
                failure_code=FailureCode.CENTER_MISSING,
                message="SlotGraph.construct: center is required (docs/17 §3).",
            )
        if boundary is None:
            return ConstructionResult(
                graph=None,
                failure_code=FailureCode.BOUNDARY_MISSING,
                message="SlotGraph.construct: boundary is required (docs/17 §3).",
            )
        if output_boundary is None:
            return ConstructionResult(
                graph=None,
                failure_code=FailureCode.BOUNDARY_MISSING,
                message=(
                    "SlotGraph.construct: output_boundary is required "
                    "(docs/17 §3)."
                ),
            )
        if (
            generation_source is GenerationSource.DECLARED_ENTRY
            and entry_boundary is None
        ):
            return ConstructionResult(
                graph=None,
                failure_code=FailureCode.BOUNDARY_MISSING,
                message=(
                    "SlotGraph.construct: a DECLARED_ENTRY source requires "
                    "an entry_boundary (docs/15 §5)."
                ),
            )

        graph = cls(
            center=center,
            slots=slots,
            boundary=boundary,
            residuals=residuals,
            rank=rank,
            output_boundary=output_boundary,
            generation_source=generation_source,
            entry_boundary=entry_boundary,
        )
        return ConstructionResult(graph=graph, failure_code=None, message="")


@dataclass(frozen=True, slots=True)
class ConstructionResult:
    """The value returned by :meth:`SlotGraph.construct` (docs/17 §5).

    Exactly one of :attr:`graph` and :attr:`failure_code` is set:

    * a successful construction carries the new
      :class:`SlotGraph` and ``failure_code is None``;
    * a refusal carries ``graph is None`` and a named
      :class:`FailureCode` from ``docs/17 §3``.

    The schema invariant is enforced at construction time so a
    refusal value can never be silently treated as a graph and a
    graph value can never carry a failure code.
    """

    graph: SlotGraph | None
    failure_code: FailureCode | None
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.message, str):
            raise SlotGraphSchemaError("ConstructionResult.message must be a string")
        if self.graph is None and self.failure_code is None:
            raise SlotGraphSchemaError(
                "ConstructionResult must carry either a graph or a failure_code"
            )
        if self.graph is not None and self.failure_code is not None:
            raise SlotGraphSchemaError(
                "ConstructionResult cannot carry both a graph and a failure_code"
            )
        if self.graph is not None and not isinstance(self.graph, SlotGraph):
            raise SlotGraphSchemaError(
                "ConstructionResult.graph must be a SlotGraph or None"
            )
        if self.failure_code is not None and not isinstance(
            self.failure_code, FailureCode
        ):
            raise SlotGraphSchemaError(
                "ConstructionResult.failure_code must be a FailureCode or None"
            )

    @property
    def is_refusal(self) -> bool:
        """``True`` iff this result carries a named refusal."""

        return self.failure_code is not None


def required_slots(slots: Iterable[Slot]) -> tuple[Slot, ...]:
    """Helper used by ``Γ`` to project the required-slot subset."""

    return tuple(s for s in slots if s.required)


__all__ = [
    "Center",
    "ConstructionResult",
    "EntryBoundary",
    "GenerationSource",
    "Layer",
    "OpeningPolicy",
    "OutputBoundary",
    "Slot",
    "SlotBoundary",
    "SlotGraph",
    "SlotGraphSchemaError",
    "SlotState",
    "TraceRef",
    "required_slots",
]
