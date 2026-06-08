"""SlotGraph — the geometric carrier of every entity entering the engine.

PR-1 freezes the minimal surface specified in
``docs/02_SLOT_GEOMETRY_CONSTITUTION.md`` under "PR-1 binding subset".

All dataclasses in this module are frozen and slotted. A transition
does not mutate a graph; it constructs a new one.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum

from taaqqul_slot_geometry.core.rank_lattice import Rank
from taaqqul_slot_geometry.core.residual_policy import Residual


class SlotState(StrEnum):
    """The three slot-level identity states recognised in PR-1."""

    EMPTY = "EMPTY"
    FILLED = "FILLED"
    BROKEN = "BROKEN"


class Layer(IntEnum):
    """Generic ordered layer carrier for PR-1.

    This is **not** the Forbidden Straight-Line Registry. It exists
    only so ``gamma`` has a total order to consult for the
    ``FORBIDDEN_LEAP`` rule. The typed registry with required-bridge
    mappings lands in PR-4.
    """

    L0_RAW = 0
    L1_FORM = 1
    L2_MEANING = 2
    L3_JUDGMENT = 3
    L4_APPLICATION = 4


@dataclass(frozen=True, slots=True)
class SlotBoundary:
    """Label-only boundary carrier.

    PR-1 attaches no semantics to the label. Later PRs may bind
    boundary policies without changing the ``Slot`` shape.
    """

    name: str


@dataclass(frozen=True, slots=True)
class Slot:
    """A single slot inside a ``SlotGraph``."""

    name: str
    required: bool
    state: SlotState
    boundary: SlotBoundary | None = None
    value_ref: str | None = None


@dataclass(frozen=True, slots=True)
class SlotGraph:
    """Geometric carrier of an entity entering the engine.

    Immutable: ``frozen=True, slots=True``. Validators in
    ``__post_init__`` enforce the two structural invariants required by
    PR-1: unique slot names and edges that reference known slots.
    """

    center: str
    slots: tuple[Slot, ...]
    edges: tuple[tuple[str, str], ...] = ()
    constraints: tuple[str, ...] = ()
    residuals: tuple[Residual, ...] = ()
    rank: Rank = Rank.ZERO
    declared_layer: Layer = Layer.L0_RAW
    output_boundary: Layer | None = None
    trace_ref: str | None = None

    def __post_init__(self) -> None:
        names: set[str] = set()
        for slot in self.slots:
            if slot.name in names:
                raise ValueError(f"duplicate slot name: {slot.name!r}")
            names.add(slot.name)
        for src, tgt in self.edges:
            if src not in names:
                raise ValueError(f"edge references unknown slot: {src!r}")
            if tgt not in names:
                raise ValueError(f"edge references unknown slot: {tgt!r}")


# Public surface for PR-1.
__all__ = [
    "Layer",
    "Slot",
    "SlotBoundary",
    "SlotGraph",
    "SlotState",
]
