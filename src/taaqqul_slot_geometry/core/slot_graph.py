"""Executable ``SlotGraph`` carriers — PR-2 minimal kernel.

This module binds the structural part of
``docs/11_MATHEMATICAL_SLOT_GEOMETRY_LAWS.md`` §1–§5 and the
constructor obligations named in
``docs/17_SLOTGRAPH_GENERATION_LAW.md`` §2. It is intentionally a
minimum: only the carriers needed to express a ``SlotGraph`` whose
verdict ``Γ`` can be computed in PR-2 are defined here. The full
constructor refusal table (docs/17 §3) is honoured *through* ``Γ``:
every refusal that the table promises surfaces with the named
``FailureCode`` when ``gamma(graph)`` is consulted (docs/17 §6 —
``construction refusal ⇒ Γ would refuse with the same code``).

Constitutional shape of a ``SlotGraph``:

    G = ⟨Center, Slots, Boundary, Residuals, Rank,
         OutputBoundary, GenerationSource, EntryBoundary?⟩

Refusals at the *Python* schema level (wrong type, missing required
field) are raised as :class:`SlotGraphSchemaError` and represent
programmer mistakes, never expected constitutional verdicts. Every
*expected* refusal stays a value: it is emitted by ``Γ`` as a
``FailureCode`` member, never as an exception.

This module deliberately ships **no behaviour beyond construction
checks**: no rank promotion, no residual classification engine, no
gate emission. Those are reserved for PR-3 and PR-4.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum

from taaqqul_slot_geometry.core.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual


class SlotGraphSchemaError(TypeError):
    """Raised when a constitutional carrier is constructed with the
    wrong *type* of value (e.g. a list where a tuple is required, a
    non-:class:`Center` passed as the center).

    This is a Python-level schema guard, not a constitutional verdict.
    Expected verdicts are values (``FailureCode``); only programmer
    mistakes raise.
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
    """The three licensed generation sources from docs/17 §1.

    The PR-2 kernel carries the declared source as a value; it does
    not yet inspect or police the source-specific obligations beyond
    requiring that one of these three names is declared. Source-bound
    construction checks (rank≥CANDIDATE without a Candidate source,
    etc.) are reserved for PR-3+ when ``RankLattice`` lands.
    """

    DECLARED_ENTRY = "DECLARED_ENTRY"
    CANDIDATE = "CANDIDATE"
    TRANSITION_VERDICT = "TRANSITION_VERDICT"


@dataclass(frozen=True, slots=True)
class TraceRef:
    """Opaque trace anchor inherited from the generation source.

    Core treats ``anchor`` as opaque (docs/11 §12 — *Trace is opaque
    to core*). An empty ``anchor`` represents an absent trace and is
    refused by ``Γ`` step 2 with ``TRACE_MISSING``.
    """

    anchor: str
    kind: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.anchor, str):
            raise SlotGraphSchemaError("TraceRef.anchor must be a string")
        if not isinstance(self.kind, str):
            raise SlotGraphSchemaError("TraceRef.kind must be a string")


@dataclass(frozen=True, slots=True)
class SlotBoundary:
    """The perimeter declaration named in docs/11 §3.

    A boundary is named by its refusals: ``refusal_codes`` lists the
    ``FailureCode`` members that crossing this boundary would emit.
    An empty ``refusal_codes`` tuple is not refused at construction
    time (boundaries with no declared refusals are unusual but legal
    carriers); ``Γ`` is the binding authority on whether the surface
    is well-formed.
    """

    domain: str
    scope: str
    refusal_codes: tuple[FailureCode, ...] = ()
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
    fillings for a slot. A filling outside this set is an
    ``UNLICENSED_OPENING``; the PR-2 kernel enforces this at slot
    construction time (an *invalid* construction, not an expected
    verdict) since the same value cannot be inspected by ``Γ`` once
    it has been silently coerced.
    """

    allowed_potentials: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.allowed_potentials, frozenset):
            raise SlotGraphSchemaError(
                "OpeningPolicy.allowed_potentials must be a frozenset of strings"
            )
        for potential in self.allowed_potentials:
            if not isinstance(potential, str):
                raise SlotGraphSchemaError(
                    "every OpeningPolicy.allowed_potentials entry must be a string"
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
    """Identity-preserving anchor (docs/11 §2).

    Construction permits empty strings so that ``Γ`` may emit
    ``CENTER_MISSING`` / ``TRACE_MISSING`` as values rather than
    exceptions (docs/17 §6 — construction refusals are a *subset* of
    ``Γ``'s; the rest surface through ``Γ``). The schema only
    requires the types.
    """

    identity_claim: str
    domain: str
    scope: str
    trace_ref: TraceRef | None

    def __post_init__(self) -> None:
        if not isinstance(self.identity_claim, str):
            raise SlotGraphSchemaError("Center.identity_claim must be a string")
        if not isinstance(self.domain, str):
            raise SlotGraphSchemaError("Center.domain must be a string")
        if not isinstance(self.scope, str):
            raise SlotGraphSchemaError("Center.scope must be a string")
        if self.trace_ref is not None and not isinstance(self.trace_ref, TraceRef):
            raise SlotGraphSchemaError("Center.trace_ref must be a TraceRef or None")


@dataclass(frozen=True, slots=True)
class EntryBoundary:
    """Declared Entry Boundary carrier (docs/11 §13.2, docs/15 §5).

    PR-2 ships the carrier so a ``SlotGraph`` generated from
    :attr:`GenerationSource.DECLARED_ENTRY` may name its prior trace
    status without erasing it. The detailed obligations are
    text-only in docs/15; PR-2 does not yet police them.
    """

    declared_entry_kind: str
    prior_trace_status: str = "OUT_OF_CURRENT_EXECUTION"
    produces_only: str = "TEXT_TRACE_CANDIDATE"

    def __post_init__(self) -> None:
        for name, value in (
            ("declared_entry_kind", self.declared_entry_kind),
            ("prior_trace_status", self.prior_trace_status),
            ("produces_only", self.produces_only),
        ):
            if not isinstance(value, str) or not value.strip():
                raise SlotGraphSchemaError(
                    f"EntryBoundary.{name} must be a non-empty string"
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

    All fields are mandatory. Constructing a ``SlotGraph`` without a
    ``boundary`` (or any other required field) raises a Python
    ``TypeError`` — this is the constitutional refusal of doc 17 §4
    *forbidden: SlotGraph(slots={...})  — free container* at the
    type-system level.
    """

    center: Center | None
    slots: tuple[Slot, ...]
    boundary: SlotBoundary
    residuals: tuple[Residual, ...]
    rank: Rank
    output_boundary: OutputBoundary
    generation_source: GenerationSource
    entry_boundary: EntryBoundary | None = None

    def __post_init__(self) -> None:
        if self.center is not None and not isinstance(self.center, Center):
            raise SlotGraphSchemaError("SlotGraph.center must be a Center or None")

        if not isinstance(self.slots, tuple):
            raise SlotGraphSchemaError("SlotGraph.slots must be a tuple of Slot")
        for slot in self.slots:
            if not isinstance(slot, Slot):
                raise SlotGraphSchemaError(
                    "every SlotGraph.slots entry must be a Slot"
                )

        if not isinstance(self.boundary, SlotBoundary):
            raise SlotGraphSchemaError("SlotGraph.boundary must be a SlotBoundary")

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

        if self.entry_boundary is not None and not isinstance(
            self.entry_boundary, EntryBoundary
        ):
            raise SlotGraphSchemaError(
                "SlotGraph.entry_boundary must be an EntryBoundary or None"
            )


def required_slots(slots: Iterable[Slot]) -> tuple[Slot, ...]:
    """Helper used by ``Γ`` to project the required-slot subset."""

    return tuple(s for s in slots if s.required)


__all__ = [
    "Center",
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
